# tasks/task_quote_intercept.py
import time
import random
import re
import os
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme
from common.config_manager import cfg
from tasks.task_scrape_blogger import ensure_blogger_ready

def get_random_quote_text(ai_type):
    """生成随机引用文案"""
    templates = XConfig.QUOTE_TEXTS.get(ai_type, XConfig.QUOTE_TEXTS["volc"])
    template = random.choice(templates)
    
    def spin(match):
        choices = match.group(1).split('|')
        return random.choice(choices)
    
    return re.sub(r'\{([^}]+)\}', spin, template)

def load_quoted_users(ai_type):
    """加载已引用的用户列表"""
    path = cfg.get_file_path("quoted_users.txt", ai_type)
    if not os.path.exists(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except:
        return set()

def save_quoted_user(ai_type, username):
    """保存已引用的用户"""
    path = cfg.get_file_path("quoted_users.txt", ai_type)
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"{username}\n")
    except:
        pass

def extract_username_from_desc(desc):
    """从 content-desc 中提取用户名 (@username)"""
    if not desc: return None
    # 假设格式: "Name @username. Content..."
    match = re.search(r"@([a-zA-Z0-9_]+)", desc)
    if match:
        return match.group(1)
    return None

def run_quote_intercept_task(device_info, _unused, stop_event):
    """
    引用截流任务 (重构版)：搜索 to:博主 -> 最新 -> 列表页直接引用
    """
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc')
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log("🚀 开始引用截流任务 (搜索模式)...")

        # 1. 智能启动
        if bot.is_on_home_page():
            bot.log("✅ 已在主页")
        else:
            bot.log("启动 X 应用...")
            bot.launch_app()

        if stop_event.is_set(): return

        # 2. 获取博主
        target_user, _ = ensure_blogger_ready(device_info, ai_type)
        if not target_user:
            bot.log("❌ 未获取到博主账号，任务终止")
            return
        
        target_user_clean = target_user.replace("@", "").strip()
        bot.log(f"🎯 目标博主: {target_user}")

        # 加载已引用列表
        quoted_users = load_quoted_users(ai_type)
        bot.log(f"📚 已加载 {len(quoted_users)} 个已引用用户")

        # 3. 执行搜索 (to:博主)
        query = f"to:{target_user_clean}"
        search_uri = XScheme.get_url(XScheme.SEARCH, query=query, latest=True)
        
        bot.log(f"🔍 搜索回复: {query}")
        bot.shell_cmd(XScheme.wrap_command(search_uri))
        time.sleep(8) 

        if bot.exists_desc("最新"):
            bot.log("👉 确保切换到 [最新] 标签")
            bot.click_desc("最新")
            time.sleep(3)

        if stop_event.is_set(): return

        # 4. 遍历评论列表 (列表页直接操作)
        processed_count = 0
        max_process = 5 
        already_processed_desc = []
        
        while processed_count < max_process:
            if stop_event.is_set(): break
            
            selector = bot.rpa.create_selector()
            if selector:
                with selector:
                    selector.addQuery_IdEqual("com.twitter.android:id/row")
                    nodes = selector.execQuery(10, 2000)
                    
                    if nodes:
                        valid_nodes = []
                        for n in nodes:
                            desc = n.get_node_desc()
                            if not desc: continue
                            
                            bounds = n.get_node_nound()
                            if bounds['top'] < 300: continue
                            
                            if desc in already_processed_desc: continue
                            
                            # 提取用户名并检查去重
                            username = extract_username_from_desc(desc)
                            if not username: continue
                            
                            # 排除博主自己
                            if username.lower() == target_user_clean.lower():
                                continue
                                
                            # 检查是否已引用过
                            if username in quoted_users:
                                # bot.log(f"⏭️ 用户 {username} 已引用过，跳过")
                                continue
                                
                            valid_nodes.append((n, username))
                        
                        if not valid_nodes:
                            bot.log("⏩ 当前页无有效评论(或已全部处理)，下滑...")
                        else:
                            for n, username in valid_nodes:
                                if processed_count >= max_process: break
                                if stop_event.is_set(): break
                                
                                desc = n.get_node_desc()
                                bot.log(f"🔄 处理评论 ({processed_count + 1}) - 用户: {username}")
                                
                                # 尝试直接点击转载按钮 (坐标推算)
                                bounds = n.get_node_nound()
                                # 转载按钮通常在 row 宽度的 30% 处，底部向上 50px
                                target_x = int(1080 * 0.30)
                                target_y = bounds['bottom'] - 50
                                
                                # 边界检查
                                if target_y > 1900: continue # 超出屏幕
                                
                                bot.log(f"👆 点击转载坐标 ({target_x}, {target_y})")
                                bot.rpa.touchClick(0, target_x, target_y)
                                time.sleep(1.5)
                                
                                # 检查是否弹出菜单
                                quote_keywords = ["引用", "Quote", "引用リポスト"]
                                clicked_quote = False
                                for kw in quote_keywords:
                                    if bot.click_text(kw):
                                        clicked_quote = True
                                        break
                                
                                if clicked_quote:
                                    time.sleep(2)
                                    text = get_random_quote_text(ai_type)
                                    bot.input_text(text)
                                    time.sleep(1)
                                    
                                    if bot.click_id("com.twitter.android:id/button_tweet"):
                                        bot.log(f"✅ 引用发布成功: {username}")
                                        processed_count += 1
                                        already_processed_desc.append(desc)
                                        
                                        # 记录到文件
                                        save_quoted_user(ai_type, username)
                                        quoted_users.add(username)

                                        time.sleep(3)
                                    else:
                                        bot.log("⚠️ 未找到发布按钮")
                                        bot.rpa.pressBack()
                                else:
                                    bot.log("⚠️ 未弹出引用菜单 (可能点歪了)")
                                    # 如果点歪了进了详情页，退回来
                                    if not bot.exists_id("com.twitter.android:id/row"):
                                        bot.rpa.pressBack()
                                        time.sleep(1)
                                
                                time.sleep(1)
            
            bot.swipe_screen("up", distance=0.7)
            time.sleep(3)

        bot.log(f"🎉 引用截流完成，共处理 {processed_count} 条")

    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
