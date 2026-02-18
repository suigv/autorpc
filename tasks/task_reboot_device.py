# tasks/task_reboot_device.py
import time
import requests
from common.bot_agent import BotAgent
from common.box_api import BoxApi

def reboot_device_via_api(host_ip, index, log_func=print):
    """
    通过 SDK API 重启指定设备 (容器或宿主机)
    注意：SDK API 文档中 /server/device/reboot 是重启宿主机(盒子)！
    如果是重启云机容器，应该用 /android/restart
    """
    # 根据需求，如果是"设备死机"（指云机卡死），应该重启云机
    # 如果是"端口连接失败"（指 adb 连不上），通常重启云机容器即可恢复
    # 只有当整个盒子都连不上时，才需要重启盒子（但那时候 API 也连不上了...）
    
    # 所以我们优先尝试重启云机容器
    
    log_func(f"🚑 [设备{index}] 检测到异常，准备执行恢复流程...")
    
    box = BoxApi(host_ip)
    
    # 1. 获取云机名
    devs = box.get_android_list(index)
    if not devs:
        log_func(f"❌ [设备{index}] 无法获取云机信息，无法重启容器")
        return False
        
    dev_name = devs[0]['name']
    
    # 2. 重启容器
    log_func(f"🔄 [设备{index}] 正在重启容器: {dev_name}...")
    if box.restart_android(dev_name):
        log_func(f"✅ [设备{index}] 重启指令已发送，等待恢复 (约60s)...")
        
        # 3. 等待恢复
        time.sleep(10)
        for i in range(30): # 60s
            # 检查状态
            d = box.get_android_list(index)
            if d and d[0]['status'] == 'running':
                # 尝试连接 ADB
                bot = BotAgent(index, host_ip)
                if bot.connect():
                    log_func(f"✅ [设备{index}] 恢复成功！ADB 已连接")
                    bot.quit()
                    return True
            
            time.sleep(2)
            if i % 5 == 0:
                log_func(f"⏳ [设备{index}] 等待中... ({i*2}s)")
                
        log_func(f"❌ [设备{index}] 重启后仍无法连接")
        return False
    else:
        log_func(f"❌ [设备{index}] 重启指令发送失败")
        return False

def run_reboot_task(device_info, _unused, stop_event):
    """
    手动触发的重启任务
    """
    ip = device_info['ip']
    idx = device_info['index']
    
    # 包装 log 函数以适配 main.py 的调用
    def log_wrapper(msg):
        print(msg)
        # 如果有 gui_log 也可以调用
        
    reboot_device_via_api(ip, idx, log_wrapper)
