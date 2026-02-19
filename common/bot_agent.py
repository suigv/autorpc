# common/bot_agent.py
import time
import random
import functools
import requests
from common.mytRpc import MytRpc
from common.logger import logger
from common.ToolsKit import ToolsKit
from common.x_config import XConfig

def safe_action(retries=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            last_err = None
            for i in range(retries):
                try:
                    if not self._is_connected:
                        self.log(f"检测到连接断开，尝试重连 ({i + 1})...")
                        if not self.connect():
                            time.sleep(2)
                            continue
                    return func(self, *args, **kwargs)
                except Exception as e:
                    last_err = e
                    self.log(f"⚠️ 操作 {func.__name__} 失败 (第 {i + 1} 次): {e}")
                    time.sleep(delay)
            self.log(f"❌ 操作 {func.__name__} 彻底失败: {last_err}")
            return False
        return wrapper
    return decorator

class BotAgent:
    @staticmethod
    def calculate_ports(index):
        base_port = 30000 + (index - 1) * 100
        rpa_port = base_port + 2
        api_port = base_port + 1
        return rpa_port, api_port

    def __init__(self, index, host_ip, log_func=None):
        self.index = index
        self.host_ip = host_ip
        self.log_callback = log_func
        self.cfg = XConfig
        self.rpa_port, self.api_port = self.calculate_ports(index)
        self.rpa = MytRpc()
        self.tools = ToolsKit()
        self._is_connected = False

    def __enter__(self):
        if self.connect(): return self
        raise ConnectionError(f"[Device {self.index}] RPA连接失败")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def connect(self):
        try:
            if self.rpa.init(self.host_ip, self.rpa_port, 10):
                self._is_connected = True
                # [新增] 获取并打印设备 ID，用于排查串号问题
                android_id = self.shell_cmd("settings get secure android_id")
                self.log(f"✅ 连接成功 (Port: {self.rpa_port}, ID: {android_id})")
                return True
        except Exception as e:
            logger.error(f"连接异常: {e}")
        return False

    def quit(self):
        self._is_connected = False

    def log(self, message):
        full_msg = f"[Dev {self.index}] {message}"
        if self.log_callback: self.log_callback(full_msg)
        logger.info(full_msg)

    @safe_action(retries=2)
    def shell_cmd(self, cmd):
        return self.rpa.exec_cmd(cmd)

    def upload_file(self, local_path):
        """通过 HTTP API 上传文件"""
        url = f"http://{self.host_ip}:{self.api_port}/upload"
        try:
            with open(local_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files, timeout=30)
                
            if response.status_code == 200:
                return True
            else:
                self.log(f"❌ API 上传失败: {response.text}")
                return False
        except Exception as e:
            self.log(f"❌ API 上传异常: {e}")
            return False

    def download_file(self, remote_path, local_path):
        """通过 HTTP API 下载文件"""
        url = f"http://{self.host_ip}:{self.api_port}/download"
        params = {"path": remote_path}
        try:
            response = requests.get(url, params=params, stream=True, timeout=30)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                self.log(f"❌ API 下载失败: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ API 下载异常: {e}")
            return False

    @safe_action(retries=3)
    def exists_text(self, text, timeout=500):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_TextContainWith(text)
            node = selector.execQueryOne(timeout)
            return node is not None

    @safe_action(retries=3)
    def exists_desc(self, text, timeout=500):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_DescContainWith(text)
            node = selector.execQueryOne(timeout)
            return node is not None
            
    @safe_action(retries=3)
    def exists_id(self, res_id, timeout=500):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_IdEqual(res_id)
            node = selector.execQueryOne(timeout)
            return node is not None

    @safe_action(retries=3)
    def is_tab_selected(self, keyword, timeout=1000):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_DescContainWith(keyword)
            selector.addQuery_Selectedable(True)
            node = selector.execQueryOne(timeout)
            return node is not None

    @safe_action(retries=3)
    def click_text(self, text, timeout=2000):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_TextContainWith(text)
            selector.addQuery_Clickable(True)
            node = selector.execQueryOne(timeout)
            
            if not node:
                selector.clear_Query()
                selector.addQuery_TextContainWith(text)
                node = selector.execQueryOne(timeout)

            if node:
                node.click_events()
                self.log(f"🖱️ 点击 -> [{text}]")
                return True
        return False

    @safe_action(retries=3)
    def click_id(self, res_id, timeout=2000):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_IdEqual(res_id)
            selector.addQuery_Clickable(True)
            node = selector.execQueryOne(timeout)
            
            if not node:
                selector.clear_Query()
                selector.addQuery_IdEqual(res_id)
                node = selector.execQueryOne(timeout)

            if node:
                node.click_events()
                self.log(f"🖱️ 点击ID -> [{res_id}]")
                return True
        return False
    
    @safe_action(retries=3)
    def click_desc(self, desc, timeout=2000):
        selector = self.rpa.create_selector()
        if not selector: return False
        with selector:
            selector.addQuery_DescContainWith(desc)
            selector.addQuery_Clickable(True)
            node = selector.execQueryOne(timeout)
            
            if not node:
                selector.clear_Query()
                selector.addQuery_DescContainWith(desc)
                node = selector.execQueryOne(timeout)

            if node:
                node.click_events()
                self.log(f"🖱️ 点击Desc -> [{desc}]")
                return True
        return False

    @safe_action(retries=2)
    def input_text(self, text, hint_text=None):
        if hint_text:
            if not self.click_text(hint_text): return False
            time.sleep(0.5)
        self.rpa.sendText(text)
        self.log(f"⌨️ 输入 -> {text[:5]}...")
        return True
    
    @safe_action(retries=2)
    def keyPress(self, key_code):
        return self.rpa.keyPress(key_code)

    @safe_action(retries=2)
    def swipe_screen(self, direction="up", distance=0.5):
        w, h = 1080, 1920
        center_x, center_y = w // 2, h // 2
        offset = int(h * distance / 2)
        sx, sy, ex, ey = center_x, center_y, center_x, center_y
        if direction == "up": sy, ey = center_y + offset, center_y - offset
        elif direction == "down": sy, ey = center_y - offset, center_y + offset
        jitter = random.randint(-20, 20)
        sx += jitter
        ex -= jitter
        cmd = f"input swipe {sx} {sy} {ex} {ey} {random.randint(180, 250)}"
        self.shell_cmd(cmd)
        return True

    @safe_action(retries=1)
    def jump_to(self, uri):
        self.log(f"🔗 跳转: {uri[:40]}...")
        cmd = f"am start -a android.intent.action.VIEW -d \"{uri}\" &"
        self.shell_cmd(cmd)
        time.sleep(3)
        return True

    def launch_app(self):
        pkg = self.cfg.PACKAGE_NAME
        try:
            if hasattr(self.rpa, 'openApp') and self.rpa.openApp(pkg):
                self.log("[SDK] 启动指令发送")
        except:
            pass
        time.sleep(1)
        self.shell_cmd(f"am start -n {pkg}/{self.cfg.ACTIVITY_NAME}")
        return self._wait_for_launch_complete()

    def _wait_for_launch_complete(self, timeout=30):
        start = time.time()
        home_keywords = [self.cfg.UI_TEXT.get("HOME_TAB", "ホーム"), "Home"]
        login_keywords = [self.cfg.UI_TEXT.get("LOGIN_BTN_1", "ログイン"), "Log in", "Sign up", "アカウントを作成"]
        
        while time.time() - start < timeout:
            self.dismiss_popups()
            if self.is_on_home_page(home_keywords, timeout=500):
                self.log("✅ App 就绪 (主页)")
                return True
            if self.is_on_page(login_keywords, timeout=500):
                self.log("✅ App 就绪 (登录页)")
                return True
            time.sleep(1)
        return False

    def is_on_page(self, keywords, timeout=500):
        if isinstance(keywords, str): keywords = [keywords]
        for kw in keywords:
            if not kw: continue
            if self.exists_text(kw, timeout=timeout): return True
            if self.exists_desc(kw, timeout=timeout): return True
        return False

    def is_on_home_page(self, keywords=None, timeout=1000):
        if not keywords:
            keywords = [self.cfg.UI_TEXT.get("HOME_TAB", "ホーム"), "Home"]
        if isinstance(keywords, str): keywords = [keywords]
        for kw in keywords:
            if self.is_tab_selected(kw, timeout): return True
        return False
        
    def check_ban_status(self):
        ban_keywords = ["suspended", "冻结", "ロック", "永久", "Account locked", "アカウントは凍結", "ご利用のアカウントは一時的に機能が制限"]
        for kw in ban_keywords:
            if self.exists_text(kw, timeout=1000):
                self.log(f"🚫 检测到封禁关键词: {kw}")
                return True
        return False

    def ensure_app_running(self):
        """确保X App正在运行"""
        import time
        pkg = self.cfg.PACKAGE_NAME
        
        # 方法1：检查进程是否存在
        result = self.shell_cmd(f"ps -A | grep {pkg}")
        app_running = pkg in result
        
        if not app_running:
            # App确实没有运行（崩溃/被杀死）
            self.log("⚠️ 检测到App未运行，尝试启动...")
            self.launch_app()
            time.sleep(3)
            
            # 检查是否成功启动
            if self.is_on_home_page():
                self.log("✅ App已启动")
                return True
            else:
                self.log("❌ App启动失败，尝试强制重启")
                self.force_stop_app()
                time.sleep(2)
                self.launch_app()
                time.sleep(3)
                return self.is_on_home_page()
        else:
            # App正在运行，检查是否在主页
            if self.is_on_home_page():
                return True
            else:
                # App在后台但未响应，尝试恢复
                self.log("⚠️ App在后台，尝试恢复...")
                self.launch_app()
                time.sleep(3)
                return self.is_on_home_page()

    def force_stop_app(self):
        """强制停止App"""
        pkg = self.cfg.PACKAGE_NAME
        self.shell_cmd(f"am force-stop {pkg}")
        
    def grant_all_permissions(self):
        pkg = self.cfg.PACKAGE_NAME
        self.log("🛡️ 正在预授权应用权限...")
        perms = [
            "android.permission.POST_NOTIFICATIONS",
            "android.permission.READ_MEDIA_IMAGES",
            "android.permission.READ_MEDIA_VIDEO",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.CAMERA"
        ]
        for p in perms: self.shell_cmd(f"pm grant {pkg} {p}")
        self.log("✅ 权限授予指令已发送")
        return True

    def check_env(self):
        tz = self.shell_cmd("getprop persist.sys.timezone")
        if "Tokyo" not in str(tz) and "Japan" not in str(tz):
            self.log(f"⚠️ 时区异常: {tz}")
            return False
        return True

    def dismiss_popups(self):
        popups = [
            self.cfg.UI_TEXT.get("POPUP_NOT_NOW"), 
            self.cfg.UI_TEXT.get("POPUP_DENY"),
            self.cfg.UI_TEXT.get("POPUP_ALLOW")
        ]
        for p in popups:
            if p and self.click_text(p, timeout=300):
                self.log(f"🛡️ 关闭弹窗: {p}")
                return True
        return False

    def get_screen_text(self):
        return ""