# tasks/task_login.py
import time
from common.bot_agent import BotAgent
from common.account_handler import AccountHandler
from common.x_config import XConfig
from common.x_scheme import XScheme

def run_login_task(device_info, _unused, stop_event):
    """
    自动登录任务
    """
    ip = device_info['ip']
    idx = device_info['index']
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        # 获取账号
        account = AccountHandler.get_account(idx)
        if not account:
            bot.log("❌ 未分配到账号")
            return
            
        user, pwd, fa2 = account
        bot.log(f"准备登录: {user}")

        # 1. 启动 App 并预授权
        bot.log("启动 App...")
        bot.launch_app()
        
        # [新增] 执行预授权
        bot.grant_all_permissions()
        
        time.sleep(5)

        # 2. 检查是否已登录
        if bot.is_on_home_page():
            bot.log("✅ 检测到已在主页，跳过登录")
            return

        # 3. 使用 Scheme 跳转登录页 (加速)
        login_uri = XConfig.SCHEMES["login_flow"]
        bot.shell_cmd(XScheme.wrap_command(login_uri))
        time.sleep(5)

        # 4. 输入账号
        # 查找输入框 (id: ocf_text_input_edit)
        if bot.click_id("com.twitter.android:id/ocf_text_input_edit"):
            bot.input_text(user)
            time.sleep(1)
            # 点击下一步 (id: cta_button, text: 次へ)
            if bot.click_text("次へ") or bot.click_text("Next"):
                time.sleep(3)
            else:
                # 尝试点击右下角按钮 (通常是下一步)
                bot.click_id("com.twitter.android:id/cta_button")
                time.sleep(3)
        else:
            bot.log("⚠️ 未找到账号输入框")
            # 尝试点击 "登录" 按钮 (如果 Scheme 跳转失败停留在首页)
            if bot.click_text("ログイン") or bot.click_text("Log in"):
                time.sleep(3)
                # 重试输入... (简化逻辑，假设 Scheme 有效)

        # 5. 输入密码
        # 查找密码框 (id: password_edit_text)
        if bot.click_id("com.twitter.android:id/password_edit_text"):
            bot.input_text(pwd)
            time.sleep(1)
            # 点击登录 (id: cta_button, text: ログイン)
            if bot.click_text("ログイン") or bot.click_text("Log in"):
                time.sleep(5)
            else:
                bot.click_id("com.twitter.android:id/cta_button")
                time.sleep(5)
        
        # 6. 处理 2FA (如果有)
        # 检查是否出现 2FA 输入框 (通常 id 也是 ocf_text_input_edit，或者 hint 包含 code)
        if bot.exists_text("コード") or bot.exists_text("code"):
            bot.log("🔐 检测到 2FA 请求...")
            if bot.click_id("com.twitter.android:id/ocf_text_input_edit"):
                bot.input_text(fa2)
                time.sleep(1)
                if bot.click_text("次へ") or bot.click_text("Next"):
                    time.sleep(5)
                else:
                    bot.click_id("com.twitter.android:id/cta_button")
                    time.sleep(5)

        # 7. 最终检查
        if bot.is_on_home_page():
            bot.log("✅ 登录成功")
        else:
            bot.log("⚠️ 登录可能未完成，请检查")
            
    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
