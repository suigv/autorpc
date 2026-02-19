"""
工作流引擎 - 任务编排
"""
import time
import logging
import threading
from typing import Dict, Callable

from app.core.device_manager import DeviceManager, check_stop_condition
from app.core.config_loader import get_host_ip, get_stop_hour, get_cycle_interval
from app.core.port_calc import calculate_ports

logger = logging.getLogger(__name__)

# 全局停止事件存储 - 所有实例共享
_global_stop_events: Dict[int, threading.Event] = {}


def get_stop_event(device_index: int) -> threading.Event:
    """获取设备的全局停止事件"""
    if device_index not in _global_stop_events:
        _global_stop_events[device_index] = threading.Event()
    return _global_stop_events[device_index]


def clear_stop_event(device_index: int):
    """清除设备的停止事件"""
    if device_index in _global_stop_events:
        _global_stop_events[device_index].clear()


class WorkflowEngine:
    def __init__(self):
        self.device_manager = DeviceManager()
        self.host_ip = get_host_ip()
        self.stop_hour = get_stop_hour()
        self.cycle_interval = get_cycle_interval()
        self._running_tasks: Dict[int, str] = {}

    @property
    def _stop_events(self):
        """使用全局stop_events"""
        return _global_stop_events

    def get_device_info(self, device_index: int, ai_type: str) -> dict:
        rpa_port, api_port = calculate_ports(device_index)
        return {
            "ip": self.host_ip,
            "index": device_index,
            "rpa_port": rpa_port,
            "api_port": api_port,
            "ai_type": ai_type
        }

    def log(self, device_index: int, msg: str):
        prefix = f"[Dev {device_index}]" if device_index else "[Workflow]"
        logger.info(f"{prefix} {msg}")

    def check_device_online(self, device_index: int) -> bool:
        try:
            from common.bot_agent import BotAgent
            print(f"DEBUG check_device_online: device={device_index}, host_ip={self.host_ip}")
            bot = BotAgent(device_index, self.host_ip)
            result = bot.connect()
            print(f"DEBUG check_device_online: connect result={result}")
            if result:
                bot.quit()
                return True
        except Exception as e:
            logger.warning(f"Device {device_index} online check failed: {e}")
            print(f"DEBUG check_device_online error: {e}")
        return False

    def run_full_flow(self, devices: list, ai_type: str) -> dict:
        results = {}
        threads = []

        def run_device(idx):
            result = self._run_device_full_flow(idx, ai_type)
            results[idx] = result

        for dev in devices:
            t = threading.Thread(target=run_device, args=(dev,))
            t.start()
            threads.append(t)
            time.sleep(0.5)

        for t in threads:
            t.join()

        return {"total": len(devices), "results": results}

    def _run_device_full_flow(self, device_index: int, ai_type: str) -> bool:
        stop_event = get_stop_event(device_index)
        clear_stop_event(device_index)
        device_info = self.get_device_info(device_index, ai_type)

        try:
            self.log(device_index, f"开始完整流程 (AI: {ai_type})")
            self.device_manager.set_device_status(device_index, "running", "full_flow")

            if not self.check_device_online(device_index):
                self.log(device_index, "设备离线，跳过")
                return False

            from tasks.task_soft_reset import run_soft_reset_task
            from tasks.task_login import run_login_task
            from tasks.task_clone_profile import run_clone_profile_task
            from tasks.task_quote_intercept import run_quote_intercept_task
            from tasks.task_follow_followers import run_follow_followers_task
            from tasks.task_nurture import run_nurture_task
            from tasks.task_reply_dm import run_reply_dm_task
            from tasks.task_home_interaction import run_home_interaction_task
            from tasks.task_scrape_blogger import ensure_blogger_ready

            self.log(device_index, "Step 1: 一键新机")
            run_soft_reset_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 2: 自动登录")
            if not run_login_task(device_info, None, stop_event):
                self.log(device_index, "登录失败")
                return False
            time.sleep(2)

            self.log(device_index, "Step 3: 抓取博主")
            ensure_blogger_ready(device_info, ai_type)
            time.sleep(2)

            self.log(device_index, "Step 4: 仿冒博主")
            run_clone_profile_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 5: 关注截流")
            run_follow_followers_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 6: 智能养号")
            run_nurture_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 7: 主页互动")
            run_home_interaction_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 8: 引用截流")
            run_quote_intercept_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 9: 私信回复")
            run_reply_dm_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "进入循环任务阶段")

            while not stop_event.is_set() and not check_stop_condition(self.stop_hour):
                self.log(device_index, "关注截流")
                run_follow_followers_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "智能养号")
                run_nurture_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "主页互动")
                run_home_interaction_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "引用截流")
                run_quote_intercept_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "私信回复")
                run_reply_dm_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, f"等待 {self.cycle_interval}s")
                for i in range(self.cycle_interval, 0, -1):
                    if stop_event.is_set() or check_stop_condition(self.stop_hour):
                        break
                    time.sleep(1)

            self.log(device_index, "任务结束")
            return True

        except Exception as e:
            self.log(device_index, f"异常: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.device_manager.set_device_status(device_index, "idle")
            self._stop_events.pop(device_index, None)

    def run_nurture_flow(self, devices: list, ai_type: str) -> dict:
        results = {}
        threads = []

        def run_device(idx):
            result = self._run_device_nurture_flow(idx, ai_type)
            results[idx] = result

        for dev in devices:
            t = threading.Thread(target=run_device, args=(dev,))
            t.start()
            threads.append(t)
            time.sleep(0.5)

        for t in threads:
            t.join()

        return {"total": len(devices), "results": results}

    def _run_device_nurture_flow(self, device_index: int, ai_type: str) -> bool:
        stop_event = get_stop_event(device_index)
        clear_stop_event(device_index)
        device_info = self.get_device_info(device_index, ai_type)

        try:
            self.log(device_index, f"开始养号流程 (AI: {ai_type})")
            self.device_manager.set_device_status(device_index, "running", "nurture_flow")

            if not self.check_device_online(device_index):
                self.log(device_index, "设备离线，跳过")
                return False

            from tasks.task_nurture import run_nurture_task
            from tasks.task_reply_dm import run_reply_dm_task
            from tasks.task_follow_followers import run_follow_followers_task
            from tasks.task_home_interaction import run_home_interaction_task
            from tasks.task_quote_intercept import run_quote_intercept_task
            from tasks.task_scrape_blogger import ensure_blogger_ready

            self.log(device_index, "Step 1: 抓取博主")
            ensure_blogger_ready(device_info, ai_type)
            time.sleep(2)

            self.log(device_index, "进入养号循环")

            while not stop_event.is_set() and not check_stop_condition(self.stop_hour):
                self.log(device_index, "关注截流")
                run_follow_followers_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "智能养号")
                run_nurture_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "主页互动")
                run_home_interaction_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "引用截流")
                run_quote_intercept_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, "私信回复")
                run_reply_dm_task(device_info, None, stop_event)
                time.sleep(2)

                self.log(device_index, f"等待 {self.cycle_interval}s")
                for i in range(self.cycle_interval, 0, -1):
                    if stop_event.is_set() or check_stop_condition(self.stop_hour):
                        break
                    time.sleep(1)

            self.log(device_index, "任务结束")
            return True

        except Exception as e:
            self.log(device_index, f"异常: {e}")
            return False
        finally:
            self.device_manager.set_device_status(device_index, "idle")
            self._stop_events.pop(device_index, None)

    def run_reset_login(self, devices: list, ai_type: str) -> dict:
        results = {}
        threads = []

        def run_device(idx):
            result = self._run_device_reset_login(idx, ai_type)
            results[idx] = result

        for dev in devices:
            t = threading.Thread(target=run_device, args=(dev,))
            t.start()
            threads.append(t)
            time.sleep(0.5)

        for t in threads:
            t.join()

        return {"total": len(devices), "results": results}

    def _run_device_reset_login(self, device_index: int, ai_type: str) -> bool:
        stop_event = get_stop_event(device_index)
        clear_stop_event(device_index)
        device_info = self.get_device_info(device_index, ai_type)

        try:
            self.log(device_index, f"开始重置登录 (AI: {ai_type})")
            self.device_manager.set_device_status(device_index, "running", "reset_login")

            if not self.check_device_online(device_index):
                self.log(device_index, "设备离线，跳过")
                return False

            from tasks.task_soft_reset import run_soft_reset_task
            from tasks.task_login import run_login_task

            self.log(device_index, "Step 1: 一键新机")
            run_soft_reset_task(device_info, None, stop_event)
            time.sleep(2)

            self.log(device_index, "Step 2: 自动登录")
            result = run_login_task(device_info, None, stop_event)

            if result:
                self.log(device_index, "重置登录完成")
            else:
                self.log(device_index, "登录失败")

            return result

        except Exception as e:
            self.log(device_index, f"异常: {e}")
            return False
        finally:
            self.device_manager.set_device_status(device_index, "idle")
            self._stop_events.pop(device_index, None)

    def stop_device(self, device_index: int):
        """停止指定设备的任务"""
        stop_event = get_stop_event(device_index)
        stop_event.set()
        
        # 额外：尝试强制停止设备上的X App
        try:
            from common.bot_agent import BotAgent
            bot = BotAgent(device_index, self.host_ip)
            if bot.connect():
                bot.force_stop_app()
                bot.quit()
        except:
            pass
        
        return True

    def stop_all(self):
        for stop_event in self._stop_events.values():
            stop_event.set()
