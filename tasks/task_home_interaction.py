# tasks/task_home_interaction.py
import time
import random
import re
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme

def parse_tweet_stats(desc):
    """解析推文数据"""
    if not desc: return 0, 0, 0, 0
    
    def extract_num(pattern, text):
        match = re.search(pattern, text)
        if match:
            num_str = match.group(1).replace(",", "")
            if "万" in num_str or "K" in num_str:
                return 10000
            return int(num_str)
        return 0

    reply = extract_num(r"(\d+)[件\s]*(?:の返信|replies)", desc)
    repost = extract_num(r"(\d+)[件\s]*(?:のリポスト|reposts)", desc)
    like = extract_num(r"(\d+)[件\s]*(?:のいいね|likes)", desc)
    view = extract_num(r"表示[:\s]*(\d+)[件\s]*", desc)
    if view == 0:
        view = extract_num(r"(\d+)[件\s]*(?:views)", desc)
        
    return reply, repost, like, view

def has_media(node):
    """检查是否包含图片 (通过高度判断)"""
    bounds = node.get_node_nound()
    height = bounds['bottom'] - bounds['top']
    return height > 600

def run_home_interaction_task(device_info, _unused, stop_event):
    """
    主页互动任务：重启X -> 差异化浏览
    """
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc')
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log("🚀 开始主页互动任务...")

        # 1. 强制重启 X (确保回到主页顶部)
        bot.log("🔄 重启 X 应用...")
        bot.shell_cmd(f"am force-stop {XConfig.PACKAGE_NAME}")
        time.sleep(1)
        bot.launch_app()
        time.sleep(5)
        
        # 刷新一下
        bot.swipe_screen("down", distance=0.6)
        time.sleep(4)

        # 2. 浏览循环
        max_swipes = 15
        swipe_cnt = 0
        interacted_count = 0
        
        while swipe_cnt < max_swipes:
            if stop_event.is_set(): break
            
            selector = bot.rpa.create_selector()
            if selector:
                with selector:
                    selector.addQuery_IdEqual("com.twitter.android:id/row")
                    nodes = selector.execQuery(10, 2000)
                    
                    if nodes:
                        # 检查当前屏幕是否有目标
                        screen_has_target = False
                        for n in nodes:
                            desc = n.get_node_desc()
                            if not desc: continue
                            
                            if ai_type == "part_time": # 兼职策略
                                if "円" in desc:
                                    screen_has_target = True
                                    break
                            else: # 交友策略
                                if has_media(n):
                                    screen_has_target = True
                                    break
                        
                        # 无目标 -> 快速下滑
                        if not screen_has_target:
                            bot.log("⏩ 当前页无目标，快速下滑...")
                            bot.swipe_screen("up", distance=0.8)
                            time.sleep(1.5)
                            continue
                        
                        # 有目标 -> 互动
                        random.shuffle(nodes)
                        for n in nodes:
                            desc = n.get_node_desc()
                            if not desc: continue
                            
                            bounds = n.get_node_nound()
                            if bounds['top'] < 300 or bounds['bottom'] > 1800: continue
                            
                            is_target = False
                            if ai_type == "part_time":
                                if "円" in desc: is_target = True
                            else:
                                if has_media(n): is_target = True
                                
                            if is_target:
                                bot.log(f"🎯 发现目标: {desc[:20]}...")
                                
                                if ai_type == "part_time":
                                    # 兼职: 必点详情 + 点赞
                                    bot.log("📄 查看详情...")
                                    n.click_events()
                                    time.sleep(random.uniform(5, 8))
                                    
                                    # 详情页点赞 (尝试找点赞按钮，或者盲点)
                                    # 详情页点赞按钮通常在底部，或者用 desc 查找
                                    # 简单起见，这里不强求详情页点赞，或者返回列表页点赞
                                    # 既然要求"查看停留点赞后返回"，我们在详情页点赞比较好
                                    # 尝试查找 "いいね"
                                    like_sel = bot.rpa.create_selector()
                                    with like_sel:
                                        like_sel.addQuery_DescContainWith("いいね")
                                        like_node = like_sel.execQueryOne(1000)
                                        if like_node:
                                            bot.log("❤️ 详情页点赞")
                                            like_node.click_events()
                                            time.sleep(1)
                                    
                                    bot.rpa.pressBack()
                                    time.sleep(2)
                                    interacted_count += 1
                                    
                                else:
                                    # 交友: 随机互动
                                    reply, repost, like, view = parse_tweet_stats(desc)
                                    # 筛选优质贴
                                    if reply > 0 and like > 0:
                                        action_roll = random.random()
                                        if action_roll < 0.6:
                                            # 列表页点赞
                                            target_x = int(1080 * 0.62)
                                            target_y = bounds['bottom'] - 60
                                            bot.log("❤️ 列表页点赞")
                                            bot.rpa.touchClick(0, target_x, target_y)
                                            time.sleep(1)
                                            interacted_count += 1
                                        
                                        if view > 2000:
                                            bot.log("📄 浏览量高，进入详情...")
                                            n.click_events()
                                            time.sleep(random.uniform(5, 10))
                                            bot.rpa.pressBack()
                                            time.sleep(2)
                                
                                break # 处理一个就够了
            
            # 正常下滑
            bot.swipe_screen("up", distance=0.7)
            swipe_cnt += 1
            time.sleep(random.uniform(3, 6))
            
        bot.log(f"🎉 主页互动完成，互动 {interacted_count} 次")

    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
