"""
工作流引擎
"""
import time
import threading

from common.bot_agent import BotAgent
from tasks.task_login import run_login_task
from tasks.task_soft_reset import run_soft_reset_task
from tasks.task_clone_profile import run_clone_profile_task
from tasks.task_follow_followers import run_follow_followers_task
from tasks.task_reply_dm import run_reply_dm_task
from tasks.task_nurture import run_nurture_task
from tasks.task_scrape_blogger import ensure_blogger_ready

from .port_calc import calculate_ports
from .config_loader import get_host_ip, get_stop_hour, get_cycle_interval
from .device_manager import check_stop_condition

class WorkflowEngine:
    def __init__(self):
        self.host_ip = get_host_ip()
        self.stop_hour = get_stop_hour()
        self.cycle_interval = get_cycle_interval()
        self.stop_event = threading.Event()
        
    def log(self, device_index, msg):
        prefix = f"[Dev {device_index}]" if device_index else "[Workflow]"
        print(f"{prefix} {msg}")
        
    def create_device_info(self, device_index, ai_type):
        rpa_port, api_port = calculate_ports(device_index)
        return {
            "ip": self.host_ip,
            "index": device_index,
            "rpa_port": rpa_port,
            "api_port": api_port,
            "delay": 0,
            "ai_type": ai_type
        }
        
    def check_device_online(self, device_index):
        try:
            bot = BotAgent(device_index, self.host_ip)
            if bot.connect():
                bot.quit()
                return True
        except:
            pass
        return False
        
    def run_device_full_flow(self, device_index, ai_type):
        self.log(device_index, f"开始完整流程 (AI: {ai_type})")
        
        device_info = self.create_device_info(device_index, ai_type)
        stop_event = threading.Event()
        
        try:
            if not self.check_device_online(device_index):
                self.log(device_index, f"设备离线，跳过")
                return False
                
            self.log(device_index, "Step 1: 一键新机")
            run_soft_reset_task(device_info, None, stop_event)
            time.sleep(2)
            
            self.log(device_index, "Step 2: 自动登录")
            if not run_login_task(device_info, None, stop_event):
                self.log(device_index, "登录失败，终止")
                return False
            time.sleep(2)
            
            self.log(device_index, "Step 3: 抓取博主")
            ensure_blogger_ready(device_info, ai_type)
            time.sleep(2)
            
            self.log(device_index, "Step 4: 仿冒博主")
            run_clone_profile_task(device_info, None, stop_event)
            time.sleep(2)
            
            self.log(device_index, "Step 5: 关注粉丝")
            run_follow_followers_task(device_info, None, stop_event)
            
            self.log(device_index, "进入循环任务阶段")
            
            while not stop_event.is_set() and not check_stop_condition(self.stop_hour):
                if self.stop_event.is_set():
                    break
                    
                self.log(device_index, "养号互动")
                run_nurture_task(device_info, None, stop_event)
                time.sleep(2)
                
                self.log(device_index, "私信回复")
                run_reply_dm_task(device_info, None, stop_event)
                time.sleep(2)
                
                self.log(device_index, f"本轮完成，等待 {self.cycle_interval}s")
                for i in range(self.cycle_interval, 0, -1):
                    if stop_event.is_set() or self.stop_event.is_set() or check_stop_condition(self.stop_hour):
                        break
                    time.sleep(1)
                    
            self.log(device_index, "任务结束")
            return True
            
        except Exception as e:
            self.log(device_index, f"异常: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def run_device_nurture_flow(self, device_index, ai_type):
        self.log(device_index, f"开始养号流程 (AI: {ai_type})")
        
        device_info = self.create_device_info(device_index, ai_type)
        stop_event = threading.Event()
        
        try:
            if not self.check_device_online(device_index):
                self.log(device_index, f"设备离线，跳过")
                return False
                
            self.log(device_index, "Step 1: 抓取博主")
            ensure_blogger_ready(device_info, ai_type)
            time.sleep(2)
            
            self.log(device_index, "进入养号循环")
            
            while not stop_event.is_set() and not check_stop_condition(self.stop_hour):
                if self.stop_event.is_set():
                    break
                    
                self.log(device_index, "养号互动")
                run_nurture_task(device_info, None, stop_event)
                time.sleep(2)
                
                self.log(device_index, "私信回复")
                run_reply_dm_task(device_info, None, stop_event)
                time.sleep(2)
                
                self.log(device_index, f"本轮完成，等待 {self.cycle_interval}s")
                for i in range(self.cycle_interval, 0, -1):
                    if stop_event.is_set() or self.stop_event.is_set() or check_stop_condition(self.stop_hour):
                        break
                    time.sleep(1)
                    
            self.log(device_index, "任务结束")
            return True
            
        except Exception as e:
            self.log(device_index, f"异常: {e}")
            return False
            
    def run_device_reset_login(self, device_index, ai_type):
        self.log(device_index, f"开始重置登录 (AI: {ai_type})")
        
        device_info = self.create_device_info(device_index, ai_type)
        stop_event = threading.Event()
        
        try:
            if not self.check_device_online(device_index):
                self.log(device_index, f"设备离线，跳过")
                return False
                
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
            
    def run_full_flow(self, devices, ai_type):
        self.log(0, f"启动完整流程: 设备 {devices}, AI: {ai_type}")
        self.stop_event.clear()
        
        threads = []
        for dev in devices:
            t = threading.Thread(target=self.run_device_full_flow, args=(dev, ai_type))
            t.start()
            threads.append(t)
            time.sleep(0.5)
            
        for t in threads:
            t.join()
            
        self.log(0, "所有设备任务完成")
        
    def run_nurture_flow(self, devices, ai_type):
        self.log(0, f"启动养号流程: 设备 {devices}, AI: {ai_type}")
        self.stop_event.clear()
        
        threads = []
        for dev in devices:
            t = threading.Thread(target=self.run_device_nurture_flow, args=(dev, ai_type))
            t.start()
            threads.append(t)
            time.sleep(0.5)
            
        for t in threads:
            t.join()
            
        self.log(0, "所有设备任务完成")
        
    def run_reset_login(self, devices, ai_type):
        self.log(0, f"启动重置登录: 设备 {devices}, AI: {ai_type}")
        self.stop_event.clear()
        
        threads = []
        for dev in devices:
            t = threading.Thread(target=self.run_device_reset_login, args=(dev, ai_type))
            t.start()
            threads.append(t)
            time.sleep(0.5)
            
        for t in threads:
            t.join()
            
        self.log(0, "所有设备任务完成")
        
    def stop_all(self):
        self.log(0, "停止所有任务")
        self.stop_event.set()
