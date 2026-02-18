# tasks/task_clone_profile.py
import time
import random
import os
import re
from common.bot_agent import BotAgent
from common.x_config import XConfig
from common.x_scheme import XScheme
from common.ToolsKit import ToolsKit
from tasks.task_scrape_blogger import ensure_blogger_ready
from common.image_processor import ImageProcessor

def get_node_text_by_id(bot, res_id):
    selector = bot.rpa.create_selector()
    if not selector: return None
    with selector:
        selector.addQuery_IdEqual(res_id)
        node = selector.execQueryOne(2000)
        if node:
            return node.get_node_text() or node.get_node_desc()
    return None

def clean_bio(bio_text):
    if not bio_text: return bio_text
    pattern = re.compile(r"@[a-zA-Z0-9_]+")
    cleaned = pattern.sub("", bio_text)
    return " ".join(cleaned.split())

def download_image_from_viewer(bot):
    menu_keywords = ["その他のオプション", "More options"]
    menu_clicked = False
    
    for kw in menu_keywords:
        if bot.exists_desc(kw):
            bot.log(f"🔍 发现菜单按钮: {kw}")
            selector = bot.rpa.create_selector()
            with selector:
                selector.addQuery_DescContainWith(kw)
                node = selector.execQueryOne(2000)
                if node:
                    node.click_events()
                    menu_clicked = True
                    break
    
    if not menu_clicked:
        bot.log("⚠️ 未找到右上角菜单按钮，尝试盲点右上角")
        bot.rpa.touchClick(0, 1000, 100)
        time.sleep(1)

    time.sleep(1.5)

    save_keywords = ["保存", "Save"]
    for kw in save_keywords:
        selector = bot.rpa.create_selector()
        with selector:
            selector.addQuery_TextEqual(kw)
            node = selector.execQueryOne(2000)
            if node:
                bot.log(f"✅ 点击保存: {kw}")
                node.click_events()
                time.sleep(2)
                
                # [新增] 图片处理逻辑
                bot.log("🖼️ 处理下载的图片...")
                ImageProcessor.process_latest_image(bot)
                
                bot.rpa.pressBack()
                return True

    bot.log("⚠️ 菜单中未找到保存按钮")
    bot.rpa.pressBack()
    time.sleep(0.5)
    bot.rpa.pressBack()
    return False

def select_photo_from_gallery(bot, photo_index=0):
    bot.log(f"🖼️ 正在选择照片 (索引: {photo_index})...")
    time.sleep(2)
    
    # 处理弹出框：选择从相册/文件夹选择
    gallery_keywords = ["フォルダから画像を選択", "Choose existing photo", "Existing photo"]
    
    clicked_option = False
    for kw in gallery_keywords:
        if bot.exists_text(kw):
            bot.log(f"🔍 发现相册选项: {kw}")
            if bot.click_text(kw):
                bot.log(f"✅ 点击相册选项: {kw}")
                clicked_option = True
                time.sleep(3) # 等待相册加载
                break
    
    if not clicked_option:
        if bot.exists_id("com.twitter.android:id/select_dialog_listview"):
            bot.log("⚠️ 未找到文本，尝试点击列表第二项")
            bot.rpa.touchClick(0, 540, 1054)
            time.sleep(3)

    # 进入系统相册后的操作 (基于 dump_20260208_022627.xml)
    # 图片区域在 y=1136 之后
    # 第一张图中心约 (177, 1460)
    # 第二张图中心约 (539, 1460)
    
    target_x = 177 if photo_index == 0 else 539
    target_y = 1460  # 修正后的 Y 坐标
    
    bot.log(f"👆 点击图片坐标: ({target_x}, {target_y})")
    bot.rpa.touchClick(0, target_x, target_y)
    time.sleep(2)
    
    # 选中图片后，通常会进入 Twitter 的裁剪/预览页面，需要点击右上角的 Use/Apply/保存
    done_id = "com.twitter.android:id/done"
    if bot.click_id(done_id):
        bot.log(f"✅ 点击确认按钮 (ID: {done_id})")
        time.sleep(2)
        return True

    confirm_keywords = ["USE", "APPLY", "保存", "Save", "Done", "使う", "適用"]
    for kw in confirm_keywords:
        if bot.click_text(kw):
            bot.log(f"✅ 点击确认按钮 (Text: {kw})")
            time.sleep(2)
            return True
            
    bot.log("⚠️ 未找到图片确认按钮，尝试坐标点击右上角")
    bot.rpa.touchClick(0, 990, 120)
    time.sleep(2)
    return True

def clear_and_input(bot, text, element_id, device_info):
    if not text: return
    
    current_text = get_node_text_by_id(bot, element_id)
    if current_text == text:
        bot.log(f"✅ 内容一致，跳过输入: {text[:10]}...")
        return

    bot.log(f"✏️ 准备输入: {text[:10]}... -> {element_id}")
    
    if bot.click_id(element_id):
        time.sleep(1.5)
        bot.rpa.ClearText(60) 
        time.sleep(0.5)
        bot.rpa.ClearText(20)
        time.sleep(0.5)
        
        if set_clipboard(device_info['ip'], device_info['api_port'], text):
             bot.rpa.keyPress(279)
        else:
             bot.input_text(text)
        time.sleep(1)
    else:
        bot.log(f"⚠️ 未找到输入框: {element_id}")

def set_clipboard(ip, api_port, text):
    import requests
    try:
        url = f"http://{ip}:{api_port}/clipboard"
        resp = requests.get(url, params={"cmd": 2, "text": text}, timeout=3)
        return resp.status_code == 200
    except:
        return False

def get_assigned_line(file_path, ai_type):
    tools = ToolsKit()
    root_path = tools.GetRootPath()
    if not os.path.exists(file_path):
        file_path = os.path.join(root_path, file_path)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines: return None
        
        target_index = 0 if ai_type == "volc" else 1
        
        if target_index < len(lines):
            return lines[target_index]
        else:
            return lines[-1]
    except:
        return None

def run_clone_profile_task(device_info, _unused, stop_event):
    ip = device_info['ip']
    idx = device_info['index']
    ai_type = device_info.get('ai_type', 'volc')
    
    bot = BotAgent(idx, ip)
    
    try:
        if not bot.connect():
            bot.log("❌ 连接失败")
            return

        bot.log("🚀 开始仿冒博主任务...")

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

        # 3. 跳转主页
        profile_uri = XScheme.get_url(XScheme.PROFILE, screen_name=target_user_clean)
        bot.shell_cmd(XScheme.wrap_command(profile_uri))
        time.sleep(5)

        if stop_event.is_set(): return

        bot.log("📥 正在抓取信息...")
        nick = get_node_text_by_id(bot, XConfig.PROFILE_LOCATORS["nick_name"]["id"])
        introd = get_node_text_by_id(bot, XConfig.PROFILE_LOCATORS["user_bio"]["id"])
        username = get_node_text_by_id(bot, XConfig.PROFILE_LOCATORS["user_name"]["id"]) or target_user
        
        if introd: introd = clean_bio(introd)
        bot.log(f"✅ 抓取结果: Nick={nick}, Introd={introd}")

        # 5. 下载头像
        if bot.click_id("com.twitter.android:id/profile_image"):
            bot.log("📥 下载头像...")
            time.sleep(3)
            download_image_from_viewer(bot)
        else:
            bot.log("⚠️ 未找到头像节点")

        if stop_event.is_set(): return

        # 6. 下载 Banner
        nobanner = 0
        if bot.click_id("com.twitter.android:id/profile_header"):
            bot.log("📥 下载 Banner...")
            time.sleep(3)
            if not download_image_from_viewer(bot):
                nobanner = 1
                bot.log("⚠️ Banner下载失败，标记 nobanner=1")
        else:
            bot.log("⚠️ 无 Banner 节点，标记 nobanner=1")
            nobanner = 1

        if stop_event.is_set(): return

        # 7. 下滑转载
        target_repost_count = random.randint(5, 8)
        reposted_count = 0
        already_clicked_y = []
        
        bot.log(f"🔄 准备转载 {target_repost_count} 条...")
        
        # 动态滑动距离
        next_swipe_distance = 0.6
        
        for _ in range(10):
            if reposted_count >= target_repost_count: break
            if stop_event.is_set(): break
            
            # 每次循环重置为默认值，除非检测到大帖子
            next_swipe_distance = 0.6
            
            selector = bot.rpa.create_selector()
            if selector:
                with selector:
                    selector.addQuery_IdEqual("com.twitter.android:id/row")
                    nodes = selector.execQuery(10, 2000)
                    if nodes:
                        for n in nodes:
                            if reposted_count >= target_repost_count: break
                            
                            # 1. 检查内容是否包含 @
                            desc = n.get_node_desc()
                            if desc and "@" in desc:
                                bot.log("⚠️ 帖子内容包含 @，跳过")
                                continue

                            bounds = n.get_node_nound()
                            if bounds['bottom'] <= bounds['top']: continue
                            if bounds['top'] < 350 or bounds['bottom'] > 1800: continue
                            
                            # 检查是否为大帖子 (高度 > 800)
                            post_height = bounds['bottom'] - bounds['top']
                            if post_height > 800:
                                bot.log(f"📸 检测到大帖子 (H={post_height})，减小下次滑动幅度")
                                next_swipe_distance = 0.4
                            
                            center_y = (bounds['top'] + bounds['bottom']) // 2
                            if any(abs(center_y - old_y) < 100 for old_y in already_clicked_y): continue

                            target_x = int(1080 * 0.37)
                            # 调整点击坐标：向上偏移 55 像素，确保点中图标中心 (之前是80可能太高点到图片)
                            target_y = bounds['bottom'] - 55
                            
                            bot.log(f"👆 点击转载 (y={target_y})")
                            bot.rpa.touchClick(0, target_x, target_y)
                            already_clicked_y.append(center_y)
                            time.sleep(1.5)
                            
                            # 查找确认按钮 (分多次查找以避免 AND 逻辑问题)
                            found_confirm = False
                            
                            # 优先检查是否是“撤销转载” (Undo Retweet / リポストを取り消す)
                            # 如果弹出了撤销菜单，说明已经转载过，必须关闭菜单并跳过
                            # [修正] 必须分开查询，否则是 AND 关系
                            is_undo = False
                            
                            undo_sel1 = bot.rpa.create_selector()
                            with undo_sel1:
                                undo_sel1.addQuery_TextContainWith("取り消す")
                                if undo_sel1.execQueryOne(500):
                                    is_undo = True
                            
                            if not is_undo:
                                undo_sel2 = bot.rpa.create_selector()
                                with undo_sel2:
                                    undo_sel2.addQuery_TextContainWith("Undo")
                                    if undo_sel2.execQueryOne(500):
                                        is_undo = True

                            if is_undo:
                                bot.log("⚠️ 已经转载过，关闭菜单并跳过")
                                bot.rpa.pressBack() # 必须关闭菜单
                                continue # 跳过当前帖子

                            # 1. 查找 "リポスト"
                            sel1 = bot.rpa.create_selector()
                            with sel1:
                                sel1.addQuery_TextEqual("リポスト")
                                sel1.addQuery_IdEqual("com.twitter.android:id/action_sheet_item_title")
                                node = sel1.execQueryOne(1000)
                                if node:
                                    node.click_events()
                                    found_confirm = True
                            
                            # 2. 如果没找到，查找 "Retweet"
                            if not found_confirm:
                                sel2 = bot.rpa.create_selector()
                                with sel2:
                                    sel2.addQuery_TextEqual("Retweet")
                                    sel2.addQuery_IdEqual("com.twitter.android:id/action_sheet_item_title")
                                    node = sel2.execQueryOne(1000)
                                    if node:
                                        node.click_events()
                                        found_confirm = True
                            
                            # 3. 如果还没找到，尝试微调坐标重试 (针对大图片帖子可能点击偏差)
                            if not found_confirm:
                                bot.log("⚠️ 未弹出确认，尝试微调坐标重试...")
                                bot.rpa.touchClick(0, target_x, target_y - 20) # 再向上一点
                                time.sleep(1.5)
                                # 再次检查确认框 (简化检查)
                                sel3 = bot.rpa.create_selector()
                                with sel3:
                                    sel3.addQuery_IdEqual("com.twitter.android:id/action_sheet_item_title")
                                    nodes_confirm = sel3.execQuery(5, 1000)
                                    if nodes_confirm:
                                        for nc in nodes_confirm:
                                            txt = nc.get_node_text()
                                            if txt in ["リポスト", "Retweet"]:
                                                nc.click_events()
                                                found_confirm = True
                                                break
                                            # 再次检查撤销
                                            if "取り消す" in txt or "Undo" in txt:
                                                bot.log("⚠️ 已经转载过(重试检测)，关闭菜单并跳过")
                                                bot.rpa.pressBack()
                                                found_confirm = False # 标记为未成功转载
                                                break # 跳出内层循环，外层循环会继续

                            if found_confirm:
                                reposted_count += 1
                                bot.log(f"✅ 转载成功 ({reposted_count})")
                            else:
                                bot.log("⚠️ 最终未成功转载，继续下一个")
                                # 这里不需要 pressBack，因为如果没弹出菜单，按返回会退出主页
                                # 如果弹出了菜单但没匹配到（极少见），可能会卡住，但通常点击空白处或下次滑动会解决

                            time.sleep(1)
            
            bot.swipe_screen("up", distance=next_swipe_distance)
            time.sleep(random.uniform(2, 3))
            already_clicked_y.clear()

        # 8. 编辑资料
        bot.log("📝 开始编辑资料...")
        edit_uri = XScheme.get_url(XScheme.EDIT_PROFILE)
        bot.shell_cmd(XScheme.wrap_command(edit_uri))
        time.sleep(6)
        
        if bot.exists_text("プロフィールを編集") or bot.exists_text("保存"):
            bot.log("✅ 进入编辑页")
            time.sleep(2)
            
            if bot.click_id("com.twitter.android:id/avatar_image"):
                idx = 1 if nobanner == 0 else 0
                select_photo_from_gallery(bot, photo_index=idx)
            
            if nobanner == 0:
                if bot.click_id("com.twitter.android:id/header_image"):
                    select_photo_from_gallery(bot, photo_index=0)
            
            location = get_assigned_line("位置.txt", ai_type)
            website = get_assigned_line("网页.txt", ai_type)
            
            clear_and_input(bot, location, "com.twitter.android:id/edit_location", device_info)
            clear_and_input(bot, nick, "com.twitter.android:id/edit_name", device_info)
            clear_and_input(bot, introd, "com.twitter.android:id/edit_bio", device_info)
            clear_and_input(bot, website, "com.twitter.android:id/edit_web_url", device_info)
            
            if bot.click_id("com.twitter.android:id/save"):
                bot.log("✅ 点击保存")
            else:
                bot.log("⚠️ 未找到保存按钮 (可能未修改或已保存)")
        else:
            bot.log("❌ 未能进入编辑页")

        bot.log("🎉 任务全部完成")
        
    except Exception as e:
        bot.log(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        bot.quit()
