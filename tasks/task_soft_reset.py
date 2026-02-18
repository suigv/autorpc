# tasks/task_soft_reset.py
import time
import random
import requests
from common.bot_agent import BotAgent
from common.box_api import BoxApi
from common.x_config import XConfig
from common.blogger_manager import BloggerManager

def remove_account_via_ui(bot):
    """通过系统设置 UI 移除 X 账号"""
    bot.log("⚙️ 打开系统账号设置...")
    bot.shell_cmd("am start -a android.settings.SYNC_SETTINGS")
    time.sleep(2)
    
    target_account = None
    selector = bot.rpa.create_selector()
    
    with selector:
        selector.addQuery_TextEqual("X")
        selector.addQuery_IdEqual("android:id/summary")
        node = selector.execQueryOne(1500)
        if node:
            target_account = node
        else:
            selector.clear_Query()
            selector.addQuery_TextEqual("Twitter")
            selector.addQuery_IdEqual("android:id/summary")
            node = selector.execQueryOne(1500)
            if node: target_account = node

    if target_account:
        bot.log("✅ 找到 X 账号，点击进入...")
        target_account.click_events()
        time.sleep(1.5)
        
        remove_keywords = ["アカウントを削除", "削除", "Remove account", "Remove"]
        clicked_remove = False
        
        for kw in remove_keywords:
            if bot.click_text(kw):
                bot.log(f"点击移除: {kw}")
                clicked_remove = True
                time.sleep(1)
                break
        
        if clicked_remove:
            for kw in remove_keywords:
                if bot.click_text(kw):
                    bot.log(f"点击确认移除: {kw}")
                    time.sleep(1.5)
                    return True
            bot.log("⚠️ 未找到确认移除按钮")
        else:
            bot.log("⚠️ 未找到移除按钮")
    else:
        bot.log("ℹ️ 未在设置中发现 X 账号 (可能已清除)")
        return True

    return False

def run_soft_reset_task(device_info, account_data, stop_event):
    """
    软重置任务
    """
    host_ip = device_info['ip']
    idx = device_info['index']
    _, api_port = BotAgent.calculate_ports(idx)
    api_base_url = f"http://{host_ip}:{api_port}"
    
    box = BoxApi(host_ip)
    bot = BotAgent(idx, host_ip)

    print(f"[设备{idx}] 开始软重置流程...")

    try:
        # 0. 清除博主绑定
        BloggerManager.reset_binding_and_cooling(idx)
        print(f"[设备{idx}] 已清除博主绑定和采集冷却")

        # 1. 获取当前云机信息
        devs = box.get_android_list(idx)
        if not devs:
            print(f"[设备{idx}] ❌ 无法获取云机信息")
            return
        
        current_dev = devs[0]
        dev_name = current_dev['name']
        print(f"[设备{idx}] 目标云机: {dev_name}")

        # 2. 清除数据
        if bot.connect():
            print(f"[设备{idx}] 正在执行深度清除...")
            remove_account_via_ui(bot)
            
            # 清除应用数据
            bot.shell_cmd(f"am force-stop {XConfig.PACKAGE_NAME}")
            
            # [修正] shell_cmd 返回 (output_str, status_bool)
            output, ret = bot.shell_cmd(f"pm clear {XConfig.PACKAGE_NAME}")
            if "Success" in str(output):
                print(f"[设备{idx}] ✅ pm clear 成功")
            
            # 清除残留文件
            bot.shell_cmd(f"rm -rf /sdcard/Android/data/{XConfig.PACKAGE_NAME}")
            bot.shell_cmd("rm -rf /sdcard/Twitter")
            bot.shell_cmd("rm -rf /sdcard/.Twitter")
            
            # 清除系统相册 (媒体文件)
            print(f"[设备{idx}] 🧹 清除系统相册...")
            bot.shell_cmd("rm -rf /sdcard/DCIM/*")
            bot.shell_cmd("rm -rf /sdcard/Pictures/*")
            bot.shell_cmd("rm -rf /sdcard/Download/*")
            bot.shell_cmd("rm -rf /sdcard/Movies/*")
            
            # 尝试清除媒体数据库 (需要 root 权限，视情况而定)
            # bot.shell_cmd("pm clear com.android.providers.media")
            
            bot.quit()
        else:
            print(f"[设备{idx}] ⚠️ ADB连接失败，跳过清除数据步骤")

        # 3. 切换机型
        models = box.get_phone_models()
        if models:
            target_model = random.choice(models)
            model_id = target_model['id']
            model_name = target_model['name']
            
            print(f"[设备{idx}] 正在切换机型为: {model_name} (ID:{model_id})...")
            if box.switch_model(dev_name, model_id):
                print(f"[设备{idx}] 机型切换指令发送成功，等待重启 (强制等待 20s)...")
                time.sleep(20) 
                
                # 智能等待上线
                print(f"[设备{idx}] 开始检测设备上线...")
                for i in range(40):
                    if stop_event.is_set(): return
                    
                    d = box.get_android_list(idx)
                    if d and d[0]['status'] == 'running':
                        if bot.connect():
                            print(f"[设备{idx}] ✅ 设备已重新上线且 ADB 可连接")
                            bot.quit()
                            break
                    
                    time.sleep(2)
                    if i % 5 == 0:
                        print(f"[设备{idx}] 等待中... ({i*2}s)")
            else:
                print(f"[设备{idx}] ❌ 切换机型失败")
                return
        else:
            print(f"[设备{idx}] ❌ 获取机型列表失败")
            return

        # 4. 设置新环境
        time.sleep(5)
        
        # (1) 设置 S5 代理
        proxy_info = None 
        if account_data and 'proxy' in account_data:
            proxy_info = account_data['proxy']
        
        if proxy_info:
            print(f"[设备{idx}] 正在设置 S5 代理...")
            try:
                parts = proxy_info.split(':')
                if len(parts) >= 4:
                    p_ip, p_port, p_user, p_pass = parts[0], parts[1], parts[2], parts[3]
                    proxy_url = f"{api_base_url}/proxy"
                    params = {
                        "cmd": 2,
                        "type": 2,
                        "ip": p_ip,
                        "port": p_port,
                        "usr": p_user,
                        "pwd": p_pass
                    }
                    requests.get(proxy_url, params=params, timeout=5)
                    print(f"[设备{idx}] ✅ S5 代理已设置")
            except Exception as e:
                print(f"[设备{idx}] ⚠️ 设置代理失败: {e}")
        else:
            print(f"[设备{idx}] (预留) 未配置 S5 代理，跳过")

        # (2) 重置谷歌 ID
        print(f"[设备{idx}] 重置 Google ID...")
        try:
            requests.get(f"{api_base_url}/adid?cmd=2", timeout=5)
        except:
            pass

        # (3) 刷新 IP 定位
        print(f"[设备{idx}] 刷新 IP 定位...")
        try:
            requests.get(f"{api_base_url}/modifydev?cmd=11&launage=ja", timeout=5)
            print(f"[设备{idx}] IP 刷新指令已发送，等待设备重新上线 (强制等待 60s)...")
            
            # [修正] 强制等待 60s
            for i in range(60):
                if stop_event.is_set(): return
                time.sleep(1)
                if i % 10 == 0:
                    print(f"[设备{idx}] IP 刷新等待中... ({i}s)")
            
            # 再次确认连接
            for i in range(20):
                if stop_event.is_set(): return
                d = box.get_android_list(idx)
                if d and d[0]['status'] == 'running':
                    if bot.connect():
                        print(f"[设备{idx}] ✅ 设备已重新上线且 ADB 可连接")
                        bot.quit()
                        break
                time.sleep(2)
                    
        except Exception as e:
            print(f"[设备{idx}] ⚠️ 刷新 IP 异常: {e}")
            
        print(f"[设备{idx}] ✅ 软重置完成！")

    except Exception as e:
        print(f"[设备{idx}] ❌ 异常: {e}")
        import traceback
        traceback.print_exc()
