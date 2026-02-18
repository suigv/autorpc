# tasks/task_follow_followers.py
import time
import random
import os
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme
from common.ToolsKit import ToolsKit
from tasks.task_scrape_blogger import ensure_blogger_ready
from tasks.task_clone_profile import run_clone_profile_task

def run_follow_followers_task(device_info, _unused, stop_event):
    """
    关注截流任务：跳转博主粉丝页 -> 随机关注
    """
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc')
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log("🚀 开始关注截流任务...")

        # 1. 智能启动
        if bot.is_on_home_page():
            bot.log("✅ 已在主页")
        else:
            bot.log("启动 X 应用...")
            bot.launch_app()

        if stop_event.is_set(): return

        # 2. 获取博主
        target_user, is_new_binding = ensure_blogger_ready(device_info, ai_type)
        
        if not target_user:
            bot.log("❌ 未获取到博主账号，任务终止")
            return
        
        # 如果是新绑定的博主，强制执行一次仿冒
        if is_new_binding:
            bot.log(f"🆕 检测到新绑定博主 {target_user}，强制执行仿冒...")
            bot.quit()
            run_clone_profile_task(device_info, None, stop_event)
            if not bot.connect(): return
        
        target_user_clean = target_user.replace("@", "").strip()
        bot.log(f"🎯 目标博主: {target_user}")

        # 3. 跳转粉丝列表页
        followers_uri = XScheme.get_url(XScheme.FOLLOWERS, screen_name=target_user_clean)
        bot.log(f"正在跳转 -> {followers_uri}")
        bot.shell_cmd(XScheme.wrap_command(followers_uri))
        time.sleep(6)

        if stop_event.is_set(): return

        # 4. 执行关注
        target_follow_count = random.randint(5, 10)
        followed_count = 0
        max_swipes = 10
        swipe_cnt = 0
        no_new_button_swipes = 0 # 连续未找到新按钮的滑动次数
        
        bot.log(f"🎯 计划关注 {target_follow_count} 人...")
        
        while followed_count < target_follow_count and swipe_cnt < max_swipes:
            if stop_event.is_set(): break
            
            # 查找所有 "关注" 按钮
            # 优先点击上方 -> 按 Y 坐标排序
            valid_buttons = []
            
            selector = bot.rpa.create_selector()
            if selector:
                with selector:
                    # 尝试查找任意语言的关注按钮
                    selector.addQuery_TextEqual("フォローする")
                    nodes = selector.execQuery(10, 2000)
                    
                    if not nodes:
                        selector.clear_Query()
                        selector.addQuery_TextEqual("Follow")
                        nodes = selector.execQuery(10, 2000)

                    if nodes:
                        for n in nodes:
                            bounds = n.get_node_nound()
                            # 过滤顶部导航栏
                            if bounds['top'] < 350: continue
                            valid_buttons.append(n)

            if valid_buttons:
                # 按 Y 坐标从小到大排序 (优先点击上方)
                valid_buttons.sort(key=lambda x: x.get_node_nound()['top'])
                
                clicked_in_this_page = False
                for n in valid_buttons:
                    if followed_count >= target_follow_count: break
                    if stop_event.is_set(): break
                    
                    bot.log(f"👆 点击关注 ({followed_count + 1}/{target_follow_count})")
                    n.click_events()
                    followed_count += 1
                    clicked_in_this_page = True
                    
                    # 随机延迟
                    sleep_time = random.uniform(1, 3)
                    time.sleep(sleep_time)
                
                if clicked_in_this_page:
                    no_new_button_swipes = 0 # 重置计数器
                else:
                    no_new_button_swipes += 1
            else:
                bot.log("当前屏幕未找到可关注用户")
                no_new_button_swipes += 1
            
            # 检查退出条件
            if no_new_button_swipes >= 2:
                bot.log("⚠️ 连续 2 次滑动未找到新关注，提前结束任务")
                break
            
            # 下滑加载更多
            bot.swipe_screen("up", distance=0.6)
            swipe_cnt += 1
            time.sleep(random.uniform(2, 3))

        bot.log(f"🎉 关注截流任务完成，共关注 {followed_count} 人")
        
    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
