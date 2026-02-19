# tasks/task_scrape_blogger.py
import time
import re
from common.bot_agent import BotAgent
from common.x_scheme import XScheme
from common.blogger_manager import BloggerManager

def scrape_bloggers(bot, keyword):
    """
    执行采集动作 (滑动循环 + 智能排除)
    :return: list of bloggers
    """
    bot.log(f"🔍 开始采集博主，关键词: {keyword}")
    
    # 1. 搜索
    search_uri = XScheme.get_url(XScheme.SEARCH, query=keyword, latest=True)
    bot.shell_cmd(XScheme.wrap_command(search_uri))
    time.sleep(8) # 等待加载
    
    # 2. 强制切换到 "最新" (Live)
    if bot.exists_desc("最新"):
        bot.log("👉 切换到 [最新] 标签")
        bot.click_desc("最新")
        time.sleep(4)
    
    collected = []
    max_swipes = 5
    swipe_cnt = 0
    
    # 标签关键词 (去除 #)
    tag_key = keyword.replace("#", "")
    
    while len(collected) < 10 and swipe_cnt < max_swipes:
        selector = bot.rpa.create_selector()
        if selector:
            with selector:
                selector.addQuery_IdEqual("com.twitter.android:id/row")
                nodes = selector.execQuery(20, 3000)
                
                if nodes:
                    for n in nodes:
                        desc = n.get_node_desc()
                        if not desc: continue
                        
                        # 提取所有 @username
                        matches = re.findall(r"@([a-zA-Z0-9_]+)", desc)
                        
                        if not matches: continue
                        
                        # 智能排除逻辑
                        sender = matches[0]
                        candidates = [m for m in matches[1:] if m != sender]
                        
                        if tag_key in desc:
                            parts = desc.split(tag_key)
                            if len(parts) > 1:
                                after_tag = parts[1]
                                tag_matches = re.findall(r"@([a-zA-Z0-9_]+)", after_tag)
                                tag_candidates = [m for m in tag_matches if m != sender]
                                if tag_candidates:
                                    candidates = tag_candidates
                        
                        for t in candidates:
                            if t not in collected:
                                collected.append(t)
                                bot.log(f"➕ 捕获博主: {t}")
        
        if len(collected) >= 10:
            break
            
        bot.swipe_screen("up", distance=0.6)
        swipe_cnt += 1
        time.sleep(3)
    
    return collected

def ensure_blogger_ready(device_info, ai_type):
    """
    确保有可用博主 (供其他任务调用)
    :return: (blogger, is_new_binding)
    """
    idx = device_info['index']
    ip = device_info['ip']
    
    # 1. 尝试获取
    blogger, need_scrape, is_new = BloggerManager.get_blogger(idx, ai_type)
    
    if blogger:
        return blogger, is_new
        
    if need_scrape:
        # 2. 执行采集
        bot = BotAgent(idx, ip)
        if bot.connect():
            keyword = "#mytxx" if ai_type == "volc" else "#mytjz"
            new_bloggers = scrape_bloggers(bot, keyword)
            count = BloggerManager.add_bloggers(ai_type, new_bloggers)
            bot.log(f"✅ 采集完成，入库 {count} 个")

            # 仅在实际采集到博主时记录采集时间。
            # 若 count == 0，不写入冷却状态，保证后续仍优先触发采集。
            if count > 0:
                BloggerManager.update_scrape_time(idx, ai_type)
            else:
                bot.log("⚠️ 本次采集为0，未写入冷却状态，后续将继续优先采集")

            bot.quit()
            
            # 3. 再次尝试获取
            blogger, _, is_new = BloggerManager.get_blogger(idx, ai_type)
            return blogger, is_new
            
    return None, False
