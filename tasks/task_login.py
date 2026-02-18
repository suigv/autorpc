# tasks/task_login.py
import time
import random
import pyotp
import re
from common.bot_agent import BotAgent
from common.account_handler import AccountHandler
from common.blogger_manager import BloggerManager

def run_login_task(device_info, _unused, stop_event):
    """
    自动登录任务 (直接使用密钥版)
    Returns: True (成功), False (失败)
    """
    ip = device_info['ip']
    idx = device_info['index']
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return False

        account = AccountHandler.get_account(idx)
        if not account:
            bot.log("❌ 未分配到账号")
            return False
            
        user, pwd, fa2_secret = account
        bot.log(f"准备登录: {user}")

        # 1. 启动 App 并预授权
        bot.log("启动 App...")
        if bot.launch_app():
            bot.grant_all_permissions()
        else:
            bot.log("⚠️ App 启动超时")

        # 2. 检查是否已登录
        if bot.is_on_home_page():
            bot.log("✅ 检测到已在主页，跳过登录")
            BloggerManager.set_current_user(idx, user)
            return True

        # 3. 进入登录页 (强制坐标点击)
        bot.log("🖱️ 尝试进入登录页...")
        
        if not bot.exists_id("com.twitter.android:id/ocf_text_input_edit"):
            target_x, target_y = 690, 1820
            bot.log(f"🖱️ 强制坐标点击底部: ({target_x}, {target_y})")
            
            # 1. API 点击
            bot.rpa.touchClick(0, target_x, target_y)
            time.sleep(0.5)
            
            # 2. ADB 点击 (备选)
            bot.shell_cmd(f"input tap {target_x} {target_y}")
            
            time.sleep(5)

        # 4. 输入账号
        if bot.click_id("com.twitter.android:id/ocf_text_input_edit"):
            bot.input_text(user)
            time.sleep(1)
            if bot.click_text("次へ") or bot.click_text("Next"):
                time.sleep(3)
            else:
                bot.click_id("com.twitter.android:id/cta_button")
                time.sleep(3)
        else:
            bot.log("❌ 无法找到账号输入框，登录失败")
            return False

        # 5. 输入密码
        if bot.click_id("com.twitter.android:id/password_edit_text"):
            bot.input_text(pwd)
            time.sleep(1)
            if bot.click_text("ログイン") or bot.click_text("Log in"):
                time.sleep(5)
            else:
                bot.click_id("com.twitter.android:id/cta_button")
                time.sleep(5)
        
        # 6. 处理 2FA
        if bot.exists_text("コード") or bot.exists_text("code"):
            bot.log("🔐 检测到 2FA 请求...")
            
            try:
                # 仅去除空格，不做其他复杂处理，直接使用 pyotp
                clean_secret = fa2_secret.replace(" ", "").strip()
                
                totp = pyotp.TOTP(clean_secret)
                totp_code = totp.now()
                bot.log(f"🔢 生成验证码: {totp_code}")
                
                # 循环尝试寻找输入框，防止页面加载延迟
                input_found = False
                for _ in range(3):
                    if bot.click_id("com.twitter.android:id/ocf_text_input_edit"):
                        input_found = True
                        break
                    time.sleep(1)
                
                if input_found:
                    time.sleep(1)
                    # 改为一次性输入文本，提高速度
                    bot.shell_cmd(f"input text {totp_code}")
                    time.sleep(1)
                    
                    if bot.click_text("次へ") or bot.click_text("Next"):
                        time.sleep(5)
                    else:
                        bot.click_id("com.twitter.android:id/cta_button")
                        time.sleep(5)
                else:
                    bot.log("❌ 未找到 2FA 输入框")
                    return False

            except Exception as e:
                bot.log(f"❌ 2FA 处理失败: {e}")
                return False

        # 7. 最终检查
        if bot.is_on_home_page():
            bot.log("✅ 登录成功")
            BloggerManager.set_current_user(idx, user)
            return True
        else:
            bot.log("⚠️ 登录可能未完成，请检查")
            return False
            
    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        bot.quit()
