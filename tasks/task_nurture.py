# tasks/task_nurture.py
import time
import random
import os
import json
import datetime
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme
from common.ToolsKit import ToolsKit
from common.config_manager import cfg

# 养号计数文件
NURTURE_COUNT_FILE = "log/nurture_count.json"

def get_nurture_count(device_index):
    """获取今日养号次数"""
    tools = ToolsKit()
    root = tools.GetRootPath()
    path = os.path.join(root, NURTURE_COUNT_FILE)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    default_data = {"date": today, "counts": {}}
    
    if not os.path.exists(path):
        return 0, default_data, path
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if data.get("date") != today:
            return 0, default_data, path
            
        return data.get("counts", {}).get(str(device_index), 0), data, path
    except:
        return 0, default_data, path

def increment_nurture_count(device_index):
    """增加养号次数"""
    count, data, path = get_nurture_count(device_index)
    data["counts"][str(device_index)] = count + 1
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return count + 1

def get_assigned_blogger(device_index, file_path="博主.txt"):
    tools = ToolsKit()
    root_path = tools.GetRootPath()
    if not os.path.exists(file_path):
        file_path = os.path.join(root_path, file_path)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        target_index = device_index - 1
        if target_index < len(lines):
            return lines[target_index].replace("@", "").strip()
    except:
        pass
    return "kamakiri_pay"

def get_weighted_keywords(ai_type, count=2):
    pool = []
    if ai_type == "volc": # 交友
        pool.extend(XConfig.DATING_CORE * 5)
        pool.extend(XConfig.DATING_ACTION * 3)
        pool.extend(XConfig.DATING_DERIVATIVE * 2)
        pool.extend(XConfig.DATING_TARGET * 1)
    else: # 兼职
        pool.extend(XConfig.PAYPAY_CORE * 5)
        pool.extend(XConfig.PAYPAY_ACTION * 3)
        pool.extend(XConfig.PAYPAY_DERIVATIVE * 2)
        pool.extend(XConfig.PAYPAY_TARGET * 1)
    
    if not pool: return []
    return random.sample(pool, min(count, len(pool)))

def is_blacklisted(text, ai_type):
    if not text: return False
    blacklist = XConfig.DATING_BLACKLIST if ai_type == "volc" else XConfig.PAYPAY_BLACKLIST
    for bad_word in blacklist:
        if bad_word in text:
            return True
    return False

def has_media(node):
    """检查是否包含图片 (通过高度判断)"""
    bounds = node.get_node_nound()
    height = bounds['bottom'] - bounds['top']
    return height > 600

def run_nurture_task(device_info, _unused, stop_event):
    """
    通用养号任务：根据接口类型执行不同策略
    """
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc')
    
    bot = BotAgent(idx, ip)
    task_name = "交友养号" if ai_type == "volc" else "PayPay养号"
    
    current_count, _, _ = get_nurture_count(idx)
    if current_count >= 5:
        bot.log(f"🛑 今日{task_name}次数已达上限 ({current_count}/5)，跳过")
        return

    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log(f"🚀 开始 {task_name} 任务 (今日第 {current_count + 1} 次)...")

        if bot.is_on_home_page():
            bot.log("✅ 已在主页")
        else:
            bot.log("启动 X 应用...")
            bot.launch_app()

        if stop_event.is_set(): return

        target_keywords = get_weighted_keywords(ai_type, count=random.randint(2, 3))
        blogger = get_assigned_blogger(idx) 
        
        if not target_keywords:
            bot.log("⚠️ 关键词库为空，跳过养号")
            return

        for kw in target_keywords:
            if stop_event.is_set(): break
            
            final_kw = kw.replace("{blogger}", blogger)
            is_live = random.random() < 0.7
            mode_str = "最新(Live)" if is_live else "热门(Top)"
            
            bot.log(f"🔍 搜索: {final_kw} [{mode_str}]")
            
            search_uri = XScheme.get_url(XScheme.SEARCH, query=final_kw, latest=is_live)
            bot.shell_cmd(XScheme.wrap_command(search_uri))
            time.sleep(8)
            
            if is_live:
                if bot.exists_desc("最新"):
                    bot.log("👉 确保切换到 [最新] 标签")
                    bot.click_desc("最新")
                    time.sleep(3)
            
            # --- 深度养成循环 (差异化策略) ---
            swipe_count = random.randint(8, 15)
            bot.log(f"👀 浏览 {swipe_count} 次...")
            
            already_clicked_y = []
            
            for i in range(swipe_count):
                if stop_event.is_set(): break
                
                found_target = False
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
                            
                            # 如果全屏无目标，直接下滑
                            if not screen_has_target:
                                bot.log("⏩ 当前页无目标，快速下滑...")
                                bot.swipe_screen("up", distance=0.8)
                                time.sleep(1.5) # 缩短等待
                                continue # 跳过本次循环的后续操作
                            
                            # 有目标，开始互动
                            # 随机选一个符合条件的
                            random.shuffle(nodes) # 打乱顺序
                            for n in nodes:
                                desc = n.get_node_desc()
                                if not desc: continue
                                
                                # 黑名单过滤
                                if is_blacklisted(desc, ai_type):
                                    continue
                                
                                # 坐标过滤
                                bounds = n.get_node_nound()
                                if bounds['top'] < 300 or bounds['bottom'] > 1800: continue
                                
                                is_target = False
                                if ai_type == "part_time":
                                    if "円" in desc: is_target = True
                                else:
                                    if has_media(n): is_target = True
                                    
                                if is_target:
                                    found_target = True
                                    bot.log(f"🎯 发现目标帖子: {desc[:20]}...")
                                    
                                    # 兼职: 必点详情
                                    # 交友: 随机互动
                                    action_roll = random.random()
                                    
                                    if ai_type == "part_time" or action_roll < 0.5:
                                        bot.log("📄 查看详情...")
                                        n.click_events()
                                        time.sleep(random.uniform(5, 10))
                                        if random.random() < 0.5:
                                            bot.swipe_screen("up", distance=0.5)
                                            time.sleep(2)
                                        bot.rpa.pressBack()
                                        time.sleep(2)
                                    elif action_roll < 0.8: # 交友点赞
                                        target_x = int(1080 * 0.62)
                                        target_y = bounds['bottom'] - 60
                                        center_y = (bounds['top'] + bounds['bottom']) // 2
                                        if not any(abs(center_y - old_y) < 100 for old_y in already_clicked_y):
                                            bot.log(f"❤️ 随机点赞")
                                            bot.rpa.touchClick(0, target_x, target_y)
                                            already_clicked_y.append(center_y)
                                            time.sleep(1.5)
                                    
                                    break # 处理一个就够了，或者继续处理下一个？通常处理一个就下滑
                
                # 正常下滑
                bot.swipe_screen("up", distance=random.uniform(0.5, 0.8))
                time.sleep(random.uniform(3, 6))
            
            bot.log(f"✅ 关键词 {final_kw} 浏览完成")
            time.sleep(3)

        bot.log("🏠 回到主页并刷新...")
        bot.shell_cmd(XScheme.wrap_command(XScheme.HOME))
        time.sleep(3)
        bot.swipe_screen("down", distance=0.6)
        time.sleep(3)
        
        new_count = increment_nurture_count(idx)
        bot.log(f"🎉 养号任务完成 (今日已执行 {new_count} 次)")

    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
