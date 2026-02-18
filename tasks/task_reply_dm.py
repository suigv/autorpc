# tasks/task_reply_dm.py
import time
import requests
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme
from common.ai_providers import get_ai_provider

# 尝试导入 urllib3 禁用警告
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass

def extract_last_message(bot):
    """
    提取最后一条对方发送的消息
    逻辑：查找所有 View 节点，筛选包含中文冒号的，取最底部的
    """
    selector = bot.rpa.create_selector()
    if not selector: return None
    
    try:
        with selector:
            selector.addQuery_ClzEqual("android.view.View")
            nodes = selector.execQuery(100, 3000)
            
            if not nodes: return None
            
            valid_msgs = []
            for n in nodes:
                desc = n.get_node_desc()
                bounds = n.get_node_nound()
                # 筛选：包含冒号，且在左侧 (对方消息)
                # 注意：冒号可能是中文或英文，视 App 语言而定
                if ("：" in desc or ": " in desc) and bounds['left'] < 540:
                    valid_msgs.append(n)
            
            if not valid_msgs: return None
            
            # 按 Y 坐标排序，取最底部
            valid_msgs.sort(key=lambda x: x.get_node_nound_center()['y'], reverse=True)
            target = valid_msgs[0]
            
            clean_desc = target.get_node_desc().replace('\u200e', '').strip()
            
            # 提取正文
            # 假设格式 "昵称：正文。时间"
            if "：" in clean_desc:
                parts = clean_desc.split("：", 1)
                if len(parts) > 1:
                    content = parts[1]
                    # 去掉末尾的时间 (如果有句号分隔)
                    if "。" in content:
                        content = "。".join(content.split("。")[:-1])
                    return content.strip()
            
            return clean_desc # 兜底返回全部
    except:
        return None

def input_pin_code(bot, password="1234"):
    """输入 PIN 码"""
    bot.log("🔑 输入 PIN 码...")
    # 1. 激活输入框 (点击屏幕中部)
    bot.rpa.touchClick(0, 540, 600)
    time.sleep(1.5)
    
    # 2. 模拟按键
    key_map = {
        '0': 7, '1': 8, '2': 9, '3': 10, '4': 11,
        '5': 12, '6': 13, '7': 14, '8': 15, '9': 16
    }
    
    for char in password:
        if char in key_map:
            code = key_map[char]
            bot.shell_cmd(f"input keyevent {code}")
            time.sleep(0.5)
    
    bot.log("✅ PIN 码输入完成")

def run_reply_dm_task(device_info, _unused, stop_event):
    """
    私信回复任务
    """
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc') # 获取 AI 类型
    
    bot = BotAgent(idx, ip)
    
    # 获取 AI 实例
    ai_bot = get_ai_provider(ai_type, bot.log)
    bot.log(f"🤖 使用 AI 接口: {ai_type}")
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log("🚀 开始私信处理任务...")

        # 1. 跳转私信列表 (UI 导航 - 优化版)
        # (1) 检查是否已经在主页 (使用精准判断)
        if bot.is_on_home_page():
            bot.log("✅ 已在主页，跳过跳转")
            time.sleep(1) # 稍微缓冲
        else:
            bot.log("正在跳转主页...")
            bot.shell_cmd(XScheme.wrap_command(XScheme.HOME))
            # 循环检测是否加载完成，最多等 5 秒
            for _ in range(5):
                if bot.is_on_home_page():
                    break
                time.sleep(1)
            time.sleep(2) # 跳转后额外缓冲

        if stop_event.is_set(): return

        # (2) 点击底部私信图标 (快速查找版)
        dm_keywords = ["チャット", "メッセージ", "Messages", "Chat"]
        found_dm = False
        
        selector = bot.rpa.create_selector()
        if selector:
            with selector:
                selector.addQuery_Clickable(True)
                nodes = selector.execQuery(50, 2000)
                
                if nodes:
                    for n in nodes:
                        desc = n.get_node_desc()
                        if not desc: continue
                        for kw in dm_keywords:
                            if kw in desc:
                                bounds = n.get_node_nound()
                                if bounds['top'] > 1700:
                                    bot.log(f"✅ 快速找到私信图标: {kw}")
                                    n.click_events()
                                    found_dm = True
                                    break
                        if found_dm: break
        
        if not found_dm:
            bot.log("⚠️ 未找到私信图标，尝试坐标点击")
            bot.rpa.touchClick(0, 972, 1846)
            found_dm = True

        time.sleep(4) # 等待私信列表加载

        if stop_event.is_set(): return

        # 2. 处理密码/蒙层 (快速检测版)
        # 一次性获取页面所有文本节点，避免多次 RPC 调用
        for _ in range(3):
            if stop_event.is_set(): return
            
            # 获取所有 TextView
            all_texts = []
            selector = bot.rpa.create_selector()
            if selector:
                with selector:
                    selector.addQuery_ClzEqual("android.widget.TextView")
                    nodes = selector.execQuery(50, 1000) # 1秒超时
                    if nodes:
                        for n in nodes:
                            t = n.get_node_text()
                            if t: all_texts.append(t)
            
            # 检查关键词
            create_keywords = ["パスコードを作成", "暗証番号を作成", "Create passcode", "Create PIN"]
            enter_keywords = ["パスコードを入力", "暗証番号を入力", "Enter passcode", "Enter PIN"]
            
            found_create = False
            for t in all_texts:
                if any(kw in t for kw in create_keywords):
                    bot.log(f"🔐 检测到创建密码: {t}")
                    # 既然找到了文本，我们需要点击它
                    # 这里为了简单，直接调用 click_text (虽然它会重试，但既然确定存在，应该很快)
                    # 或者更优：在刚才遍历 nodes 时就记录下 node 并点击
                    # 为了代码结构简单，这里重新 click_text，但因为确定存在，应该不会超时
                    bot.click_text(t)
                    time.sleep(2)
                    input_pin_code(bot)
                    time.sleep(2)
                    input_pin_code(bot)
                    time.sleep(4)
                    found_create = True
                    break
            if found_create: continue
            
            found_enter = False
            for t in all_texts:
                if any(kw in t for kw in enter_keywords):
                    bot.log(f"🔐 检测到输入密码: {t}")
                    input_pin_code(bot)
                    time.sleep(4)
                    found_enter = True
                    break
            if found_enter: continue
            
            # 如果没发现密码相关文本，说明可能在列表页，消除蒙层
            bot.rpa.touchClick(0, 540, 200)
            break

        # 3. 检测未读消息
        bot.log("🔍 扫描未读消息...")
        has_unread = False
        
        selector = bot.rpa.create_selector()
        if selector:
            with selector:
                selector.addQuery_DescContainWith("未読")
                node = selector.execQueryOne(2000)
                
                if not node:
                    selector.clear_Query()
                    selector.addQuery_DescContainWith("Unread")
                    node = selector.execQueryOne(2000)
                
                if node:
                    bot.log("🔵 发现未读消息，进入...")
                    node.click_events()
                    has_unread = True
                    time.sleep(3)
        
        if not has_unread:
            bot.log("😴 无未读消息")
            # 即使无消息，也尝试回到主页
            bot.log("🏠 任务结束，返回主页")
            bot.rpa.touchClick(0, 108, 1846) # 点击左下角主页图标 (坐标估算)
            time.sleep(1)
            return

        if stop_event.is_set(): return

        # 4. AI 回复流程
        bot.log("🤖 开始 AI 回复流程...")
        
        ask_text = extract_last_message(bot)
        if not ask_text:
            bot.log("⚠️ 无法提取提问内容")
            bot.rpa.pressBack()
            return
            
        bot.log(f"📩 收到提问: {ask_text}")
        
        reply_text = ai_bot.get_reply(ask_text)
        if not reply_text:
            bot.log("⚠️ AI 无回复")
            bot.rpa.pressBack()
            return
            
        # 发送回复
        input_id = "com.twitter.android:id/tweet_text"
        if not bot.click_id(input_id):
             selector = bot.rpa.create_selector()
             with selector:
                 selector.addQuery_ClzEqual("android.widget.EditText")
                 node = selector.execQueryOne(2000)
                 if node:
                     node.click_events()
                 else:
                     bot.rpa.touchClick(0, 500, 1800)
        
        time.sleep(1)
        bot.input_text(reply_text)
        time.sleep(1)
        
        bot.log("📤 点击发送...")
        bot.rpa.touchClick(0, 970, 1800)
        time.sleep(2)
        
        bot.rpa.pressBack()
        bot.log("✅ 回复完成")
        
        # 5. 任务结束，回到主页
        bot.log("🏠 返回主页...")
        # 尝试点击左下角主页图标 (坐标估算: x=108, y=1846)
        # 也可以使用 XScheme.HOME，但点击更自然
        bot.rpa.touchClick(0, 108, 1846)
        time.sleep(2)

    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
