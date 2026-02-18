# main.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import time
import datetime
from common.bot_agent import BotAgent
from common.config_manager import cfg
from common.logger import log_manager
from common.x_config import XConfig
from tasks.task_login import run_login_task
from tasks.task_soft_reset import run_soft_reset_task
from tasks.task_clone_profile import run_clone_profile_task
from tasks.task_follow_followers import run_follow_followers_task
from tasks.task_reply_dm import run_reply_dm_task
from tasks.task_nurture import run_nurture_task
from tasks.task_home_interaction import run_home_interaction_task
from tasks.task_quote_intercept import run_quote_intercept_task
from tasks.task_reboot_device import reboot_device_via_api

# --- 🎨 暗黑风格配置 ---
THEME = {
    "bg_root": "#2B2B2B", "bg_panel": "#313335", "bg_card": "#3C3F41",
    "fg_text": "#A9B7C6", "fg_title": "#CC7832", "fg_info": "#6A8759",
    "btn_start_bg": "#499C54", "btn_start_fg": "#FFFFFF",
    "btn_stop_bg": "#9E2927", "btn_stop_fg": "#FFFFFF",
    "entry_bg": "#45494A", "entry_fg": "#FFFFFF",
    "chk_bg": "#3C3F41", "chk_fg": "#A9B7C6", "chk_select": "#CC7832",
    "log_bg": "#1E1E1E", "log_fg": "#BBBBBB"
}

TOTAL_DEVICES = 10

class DeviceCard(tk.Frame):
    def __init__(self, parent, index):
        super().__init__(parent, bg=THEME["bg_card"], bd=1, relief="solid")
        self.index = index
        self.stop_event = threading.Event()
        self.is_running = False
        self.rpa_port, self.api_port = BotAgent.calculate_ports(index)

        self.var_reset = tk.BooleanVar(value=False)
        self.var_login = tk.BooleanVar(value=False)
        self.var_clone = tk.BooleanVar(value=False)
        self.var_follow = tk.BooleanVar(value=True)
        self.var_dm = tk.BooleanVar(value=True)
        self.var_nurture = tk.BooleanVar(value=True)
        self.var_home = tk.BooleanVar(value=True)
        self.var_quote = tk.BooleanVar(value=True)

        self._init_ui()

    def _init_ui(self):
        header = tk.Frame(self, bg=THEME["bg_card"])
        header.pack(fill="x", padx=5, pady=5)
        tk.Label(header, text=f"DEVICE #{self.index:02d}", bg=THEME["bg_card"], fg=THEME["fg_title"], font=("Consolas", 12, "bold")).pack(side="left")
        tk.Label(header, text=f"R:{self.rpa_port}", bg=THEME["bg_card"], fg="#808080", font=("Arial", 9)).pack(side="right")

        self.status_frame = tk.Frame(self, bg=THEME["bg_card"], height=28)
        self.status_frame.pack(fill="x", padx=5)
        self.status_frame.pack_propagate(False)
        self.lbl_status = tk.Label(self.status_frame, text="[ IDLE ]", bg=THEME["bg_card"], fg=THEME["fg_text"], font=("Arial", 10))
        self.lbl_status.pack(expand=True)

        opt_frame = tk.Frame(self, bg=THEME["bg_card"])
        opt_frame.pack(fill="x", padx=5, pady=5)
        chk_style = {"bg": THEME["bg_card"], "fg": THEME["chk_fg"], "selectcolor": THEME["bg_card"], "activebackground": THEME["bg_card"], "activeforeground": THEME["chk_select"], "font": ("Arial", 10)}

        tk.Checkbutton(opt_frame, text="一键新机", variable=self.var_reset, **chk_style).grid(row=0, column=0, sticky="w")
        tk.Checkbutton(opt_frame, text="自动登录", variable=self.var_login, **chk_style).grid(row=0, column=1, sticky="w")
        tk.Checkbutton(opt_frame, text="仿冒博主", variable=self.var_clone, **chk_style).grid(row=1, column=0, sticky="w")
        tk.Checkbutton(opt_frame, text="关注截流", variable=self.var_follow, **chk_style).grid(row=1, column=1, sticky="w")
        tk.Checkbutton(opt_frame, text="私信回复", variable=self.var_dm, **chk_style).grid(row=2, column=0, sticky="w")
        self.chk_nurture = tk.Checkbutton(opt_frame, text="智能养号", variable=self.var_nurture, **chk_style)
        self.chk_nurture.grid(row=2, column=1, sticky="w")
        tk.Checkbutton(opt_frame, text="主页互动", variable=self.var_home, **chk_style).grid(row=3, column=0, sticky="w")
        tk.Checkbutton(opt_frame, text="引用截流", variable=self.var_quote, **chk_style).grid(row=3, column=1, sticky="w")

        btn_frame = tk.Frame(self, bg=THEME["bg_card"])
        btn_frame.pack(fill="x", padx=5, pady=10, side="bottom")
        self.btn_start = tk.Button(btn_frame, text="启动", bg=THEME["btn_start_bg"], fg=THEME["btn_start_fg"], activebackground="#5EA96A", activeforeground="white", relief="flat", width=6, font=("Arial", 10, "bold"), command=self.start_task)
        self.btn_start.pack(side="left", padx=5, expand=True, fill="x")
        self.btn_stop = tk.Button(btn_frame, text="停止", bg=THEME["btn_stop_bg"], fg=THEME["btn_stop_fg"], activebackground="#B53B39", activeforeground="white", relief="flat", width=6, font=("Arial", 10, "bold"), command=self.stop_task, state="disabled")
        self.btn_stop.pack(side="right", padx=5, expand=True, fill="x")
        
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="🔄 强制重启云机", command=self.force_reboot)
        self.bind("<Button-3>", lambda e: self.context_menu.post(e.x_root, e.y_root))

    def force_reboot(self):
        if messagebox.askyesno("确认", f"确定要强制重启设备 #{self.index} 吗？"):
            threading.Thread(target=reboot_device_via_api, args=(cfg.runtime_config["ip"], self.index, self.log)).start()

    def update_status(self, text, color=None):
        if not color: color = THEME["fg_text"]
        self.lbl_status.config(text=text, fg=color)

    def log(self, msg, level="info"):
        log_manager.log(self.index, msg, level)

    def start_task(self, override_opts=None):
        if self.is_running: return
        
        if override_opts:
            self.var_reset.set(override_opts.get("reset", False))
            self.var_login.set(override_opts.get("login", False))
            self.var_clone.set(override_opts.get("clone", False))
            self.var_follow.set(override_opts.get("follow", False))
            self.var_dm.set(override_opts.get("dm", False))
            self.var_nurture.set(override_opts.get("nurture", False))
            self.var_home.set(override_opts.get("home", False))
            self.var_quote.set(override_opts.get("quote", False))

        opts = {
            "reset": self.var_reset.get(), "login": self.var_login.get(),
            "clone": self.var_clone.get(), "follow": self.var_follow.get(),
            "dm": self.var_dm.get(), "nurture": self.var_nurture.get(),
            "home": self.var_home.get(), "quote": self.var_quote.get()
        }
        
        if not any(opts.values()):
            self.update_status("未选任务", "#FFFF00")
            return

        self.stop_event.clear()
        self.is_running = True
        self.btn_start.config(state="disabled", bg="#555555")
        self.btn_stop.config(state="normal", bg=THEME["btn_stop_bg"])
        self.update_status("准备启动...", THEME["fg_info"])

        device_info = {
            "ip": cfg.runtime_config["ip"],
            "index": self.index,
            "rpa_port": self.rpa_port,
            "api_port": self.api_port,
            "delay": cfg.runtime_config["delay"],
            "ai_type": cfg.ai_type
        }

        thread = threading.Thread(target=self._run_wrapper, args=(device_info, opts))
        thread.daemon = True
        thread.start()

    def _run_wrapper(self, device_info, opts):
        self.log(f"任务线程启动 (模式: {device_info['ai_type']})")
        delay = device_info.get("delay", 0)
        if delay > 0:
            for i in range(delay, 0, -1):
                if self.stop_event.is_set(): return
                self.update_status(f"延迟: {i}s", "#FFFF00")
                time.sleep(1)
        
        try:
            # 初始化阶段
            if opts["reset"]:
                if self.stop_event.is_set(): return
                self.update_status("一键新机...", "#00FFFF")
                run_soft_reset_task(device_info, None, self.stop_event)
                time.sleep(2)

            if opts["login"]:
                if self.stop_event.is_set(): return
                self.update_status("自动登录...", "#00FF00")
                if not run_login_task(device_info, None, self.stop_event):
                    self.log("❌ 自动登录失败，终止后续任务", "error")
                    self.update_status("登录失败", "#FF0000")
                    return
                time.sleep(2)

            if opts["clone"]:
                if self.stop_event.is_set(): return
                self.update_status("仿冒博主...", "#FF00FF")
                run_clone_profile_task(device_info, None, self.stop_event)
                time.sleep(2)

            # 循环阶段
            if not any([opts["follow"], opts["dm"], opts["nurture"], opts["home"], opts["quote"]]):
                self.log("无循环任务，流程结束")
                return

            while not self.stop_event.is_set():
                bot = BotAgent(self.index, device_info['ip'])
                if not bot.connect():
                    self.log("⚠️ 连接失败，停止任务", "error")
                    self.update_status("连接失败", "#FF0000")
                    break # 直接退出循环，不再重试

                # 封禁检测
                if not bot.is_on_home_page():
                    login_keywords = [XConfig.UI_TEXT.get("LOGIN_BTN_1", "ログイン"), "Log in", "Sign up"]
                    if bot.is_on_page(login_keywords):
                        self.log("🚫 检测到账号掉线/封禁，触发重置流程...", "warning")
                        self.update_status("账号异常重置...", "#FF0000")
                        run_soft_reset_task(device_info, None, self.stop_event)
                        if self.stop_event.is_set(): break
                        
                        if not run_login_task(device_info, None, self.stop_event):
                            self.log("❌ 重置后登录失败，停止循环", "error")
                            break
                            
                        run_clone_profile_task(device_info, None, self.stop_event)
                        if self.stop_event.is_set(): break
                        self.log("✅ 重置流程完成，恢复循环任务")
                        continue

                if opts["follow"]:
                    if self.stop_event.is_set(): break
                    self.update_status("关注截流...", "#FFA500")
                    run_follow_followers_task(device_info, None, self.stop_event)
                    time.sleep(2)

                if opts["dm"]:
                    if self.stop_event.is_set(): break
                    self.update_status("私信回复...", "#FF69B4")
                    run_reply_dm_task(device_info, None, self.stop_event)
                    time.sleep(2)
                    
                if opts["nurture"]:
                    if self.stop_event.is_set(): break
                    self.update_status("智能养号...", "#FFD700")
                    run_nurture_task(device_info, None, self.stop_event)
                    time.sleep(2)
                    
                if opts["home"]:
                    if self.stop_event.is_set(): break
                    self.update_status("主页互动...", "#00CED1")
                    run_home_interaction_task(device_info, None, self.stop_event)
                    time.sleep(2)
                    
                if opts["quote"]:
                    if self.stop_event.is_set(): break
                    self.update_status("引用截流...", "#FF4500")
                    run_quote_intercept_task(device_info, None, self.stop_event)

                self.update_status("本轮完成", THEME["fg_text"])
                self.log("本轮任务结束，等待 15s 后继续...")
                
                for i in range(15, 0, -1):
                    if self.stop_event.is_set(): break
                    self.update_status(f"冷却: {i}s", "#808080")
                    time.sleep(1)

        except Exception as e:
            self.log(f"异常: {e}", "error")
            self.update_status("异常", "#FF0000")
        finally:
            self.is_running = False
            try:
                self.btn_start.config(state="normal", bg=THEME["btn_start_bg"])
                self.btn_stop.config(state="disabled", bg="#555555")
                if not self.stop_event.is_set():
                    # 如果是因为连接失败退出的，状态可能已经是"连接失败"了，这里不覆盖
                    if "失败" not in self.lbl_status.cget("text"):
                        self.update_status("[ IDLE ]", THEME["fg_text"])
                else:
                    self.update_status("已停止", "#FF5555")
            except (tk.TclError, RuntimeError):
                pass

    def stop_task(self):
        self.stop_event.set()
        self.update_status("停止中...", "#FF5555")
        self.log("收到停止指令")

class MytControllerApp:
    def __init__(self, master):
        self.root = master
        self.root.title("Myt X 自动化总控台 [Dark Edition]")
        self.root.geometry("1280x850")
        self.root.configure(bg=THEME["bg_root"])
        
        self.devices = []
        self.g_vars = {
            "reset": tk.BooleanVar(value=False),
            "login": tk.BooleanVar(value=False),
            "clone": tk.BooleanVar(value=False),
            "follow": tk.BooleanVar(value=True),
            "dm": tk.BooleanVar(value=True),
            "nurture": tk.BooleanVar(value=True),
            "home": tk.BooleanVar(value=True),
            "quote": tk.BooleanVar(value=True),
            "schedule": tk.BooleanVar(value=False)
        }
        
        self._init_master_control()
        self._init_device_grid()
        self._init_log_area()
        
        log_manager.set_gui_callback(self.append_log)
        self.root.after(60000, self._schedule_monitor)

    def _init_master_control(self):
        panel = tk.Frame(self.root, bg=THEME["bg_panel"], bd=1, relief="raised")
        panel.pack(fill="x", side="top")

        tk.Label(panel, text="Myt X Master", bg=THEME["bg_panel"], fg=THEME["fg_title"], 
                 font=("Impact", 18)).pack(side="left", padx=20, pady=15)

        conf_frame = tk.Frame(panel, bg=THEME["bg_panel"])
        conf_frame.pack(side="left", padx=20)

        tk.Label(conf_frame, text="IP:", bg=THEME["bg_panel"], fg=THEME["fg_text"], font=("Arial", 10)).pack(side="left", padx=2)
        self.entry_ip = tk.Entry(conf_frame, bg=THEME["entry_bg"], fg=THEME["entry_fg"], 
                                 insertbackground="white", width=14, font=("Arial", 10))
        self.entry_ip.insert(0, "192.168.1.215")
        self.entry_ip.pack(side="left", padx=5)

        tk.Label(conf_frame, text="Delay:", bg=THEME["bg_panel"], fg=THEME["fg_text"], font=("Arial", 10)).pack(side="left", padx=2)
        self.entry_delay = tk.Entry(conf_frame, bg=THEME["entry_bg"], fg=THEME["entry_fg"], 
                                    insertbackground="white", width=4, font=("Arial", 10))
        self.entry_delay.insert(0, "5")
        self.entry_delay.pack(side="left", padx=5)
        
        tk.Label(conf_frame, text="AI:", bg=THEME["bg_panel"], fg=THEME["fg_text"], font=("Arial", 10)).pack(side="left", padx=2)
        self.combo_ai = ttk.Combobox(conf_frame, values=["交友接口", "兼职接口"], state="readonly", width=8, font=("Arial", 10))
        self.combo_ai.current(0)
        self.combo_ai.pack(side="left", padx=5)
        
        self.combo_ai.bind("<<ComboboxSelected>>", self.on_ai_change)

        # 全局任务
        opt_frame = tk.Frame(panel, bg=THEME["bg_panel"])
        opt_frame.pack(side="left", padx=20)
        
        chk_style = {"bg": THEME["bg_panel"], "fg": THEME["fg_text"], 
                     "selectcolor": THEME["bg_panel"], "activebackground": THEME["bg_panel"], 
                     "activeforeground": THEME["chk_select"], "font": ("Arial", 10)}
        
        tk.Checkbutton(opt_frame, text="一键新机", variable=self.g_vars["reset"], **chk_style).grid(row=0, column=0)
        tk.Checkbutton(opt_frame, text="自动登录", variable=self.g_vars["login"], **chk_style).grid(row=0, column=1)
        tk.Checkbutton(opt_frame, text="仿冒博主", variable=self.g_vars["clone"], **chk_style).grid(row=0, column=2)
        tk.Checkbutton(opt_frame, text="关注截流", variable=self.g_vars["follow"], **chk_style).grid(row=1, column=0)
        tk.Checkbutton(opt_frame, text="私信回复", variable=self.g_vars["dm"], **chk_style).grid(row=1, column=1)
        
        self.chk_nurture_g = tk.Checkbutton(opt_frame, text="智能养号", variable=self.g_vars["nurture"], **chk_style)
        self.chk_nurture_g.grid(row=1, column=2)
        
        # 补全缺失的任务
        tk.Checkbutton(opt_frame, text="主页互动", variable=self.g_vars["home"], **chk_style).grid(row=0, column=3)
        tk.Checkbutton(opt_frame, text="引用截流", variable=self.g_vars["quote"], **chk_style).grid(row=1, column=3)
        
        # 定时执行开关
        tk.Checkbutton(opt_frame, text="定时托管 (10:00-19:00)", variable=self.g_vars["schedule"], **chk_style).grid(row=2, column=0, columnspan=4)
        
        self.on_ai_change(None)

        # 按钮
        btn_frame = tk.Frame(panel, bg=THEME["bg_panel"])
        btn_frame.pack(side="right", padx=20)

        tk.Button(btn_frame, text="🚀 启动", bg=THEME["btn_start_bg"], fg="white",
                  font=("Arial", 11, "bold"), relief="flat", padx=10,
                  command=self.start_all).pack(side="left", padx=5)

        tk.Button(btn_frame, text="🛑 停止", bg=THEME["btn_stop_bg"], fg="white",
                  font=("Arial", 11, "bold"), relief="flat", padx=10,
                  command=self.stop_all).pack(side="left", padx=5)

    def on_ai_change(self, _):
        selected = self.combo_ai.get()
        is_part_time = (selected == "兼职接口")
        ai_type = "part_time" if is_part_time else "volc"
        cfg.update_runtime("ai_type", ai_type)
        
        if is_part_time:
            self.chk_nurture_g.config(state="normal")
            self.g_vars["nurture"].set(True)
        else:
            self.chk_nurture_g.config(state="normal")
            
        for dev in self.devices:
            dev.chk_nurture.config(state="normal")

    def _init_device_grid(self):
        self.main_split = tk.PanedWindow(self.root, orient="vertical", bg=THEME["bg_root"], sashwidth=4)
        self.main_split.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.grid_container = tk.Frame(self.main_split, bg=THEME["bg_root"])
        self.main_split.add(self.grid_container, height=450)

        columns = 5
        for i in range(1, TOTAL_DEVICES + 1):
            card = DeviceCard(self.grid_container, i)
            row = (i - 1) // columns
            col = (i - 1) % columns
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.grid_container.grid_columnconfigure(col, weight=1)
            self.devices.append(card)

    def _init_log_area(self):
        log_frame = tk.Frame(self.main_split, bg=THEME["bg_root"])
        self.main_split.add(log_frame)
        
        lbl_log = tk.Label(log_frame, text="运行日志", bg=THEME["bg_root"], fg=THEME["fg_info"], anchor="w", font=("Arial", 10))
        lbl_log.pack(fill="x")
        
        self.log_text = ScrolledText(log_frame, bg=THEME["log_bg"], fg=THEME["log_fg"], 
                                     font=("Consolas", 10), state="disabled", height=20)
        self.log_text.pack(fill="both", expand=True)

    def append_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _schedule_monitor(self):
        if self.g_vars["schedule"].get():
            now = datetime.datetime.now()
            hour = now.hour
            any_running = any(dev.is_running for dev in self.devices)
            
            if hour >= 19 or hour < 10:
                if any_running:
                    log_manager.log(0, f"⏰ 定时任务: 当前时间 {now.strftime('%H:%M')}，停止所有任务")
                    self.stop_all()
            elif 10 <= hour < 19:
                if not any_running:
                    log_manager.log(0, f"⏰ 定时任务: 当前时间 {now.strftime('%H:%M')}，启动所有任务")
                    self.start_all()
        self.root.after(60000, self._schedule_monitor)

    def start_all(self):
        cfg.update_runtime("ip", self.entry_ip.get().strip())
        cfg.update_runtime("delay", int(self.entry_delay.get().strip() or 0))
        
        opts = {k: v.get() for k, v in self.g_vars.items() if k != "schedule"}
        
        if not any(opts.values()):
            log_manager.log(0, "⚠️ 启动失败: 未勾选任何任务", "warning")
            return

        def _batch_start():
            for device in self.devices:
                if not device.is_running:
                    device.start_task(override_opts=opts)
                    time.sleep(0.5)
        
        threading.Thread(target=_batch_start, daemon=True).start()

    def stop_all(self):
        for device in self.devices:
            if device.is_running:
                device.stop_task()

if __name__ == "__main__":
    root = tk.Tk()
    app = MytControllerApp(root)
    root.mainloop()