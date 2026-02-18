import os
import random
import time
from PIL import Image, ImageEnhance
from common.bot_agent import BotAgent

class ImageProcessor:
    @staticmethod
    def process_latest_image(bot, local_temp_dir="temp"):
        """
        拉取设备上最新的图片，进行去重处理（微调），然后推回设备
        策略：找到最新下载的图 -> API下载 -> 处理 -> 删除原图 -> API上传新图 -> 移动到 DCIM -> 广播
        """
        try:
            if not os.path.exists(local_temp_dir):
                os.makedirs(local_temp_dir)

            # 1. 找到设备上最新的图片
            # 扩大搜索范围
            search_dirs = [
                "/sdcard/Pictures/Twitter/",
                "/sdcard/Download/",
                "/sdcard/Pictures/"
            ]
            
            target_file = None
            
            def is_valid_filename(name):
                if not name: return False
                name = name.strip()
                # 放宽检查，只要不是布尔值字符串且长度合理
                return name and name.lower() not in ["true", "false", "null", "none"] and len(name) > 3

            # 重试机制：最多尝试 3 次，每次间隔 2 秒
            for attempt in range(3):
                for d in search_dirs:
                    # ls -t: 按时间排序, -1: 每行一个
                    cmd = f"ls -t -1 {d} | head -n 1"
                    
                    # [修正] 根据日志，shell_cmd 返回的是 (output_string, status_bool)
                    output_val, status_val = bot.shell_cmd(cmd)
                    
                    # 确保 output_val 是字符串
                    output_str = str(output_val) if output_val is not None else ""
                    
                    # bot.log(f"🔍 [DEBUG] 搜索目录: {d}, 结果: {res}, 输出: '{output_str}'")
                    
                    if status_val and is_valid_filename(output_str) and "No such file" not in output_str:
                        target_file = f"{d}{output_str.strip()}"
                        break
                
                if target_file:
                    break
                
                if attempt < 2:
                    bot.log(f"⏳ 等待图片保存... ({attempt+1}/3)")
                    time.sleep(2)

            if not target_file:
                bot.log("⚠️ 未找到刚才下载的图片 (ls输出无效)")
                return False

            bot.log(f"🖼️ 锁定原图: {target_file}")
            
            # 2. Pull 到本地 (使用 BotAgent 的 download_file)
            local_filename = f"raw_{bot.index}_{int(time.time())}.jpg"
            local_path = os.path.join(local_temp_dir, local_filename)
            
            if not bot.download_file(target_file, local_path):
                bot.log("❌ 图片拉取失败")
                return False
            
            time.sleep(1)
            
            if not os.path.exists(local_path):
                bot.log("❌ 本地文件未生成")
                return False

            # 3. 处理图片
            img = Image.open(local_path)
            img = img.convert("RGB")
            
            scale = random.uniform(0.99, 1.01)
            w, h = img.size
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(random.uniform(0.98, 1.02))
            
            processed_filename = f"new_{int(time.time())}_{random.randint(100,999)}.jpg"
            processed_path = os.path.join(local_temp_dir, processed_filename)
            img.save(processed_path, quality=95)
            
            # 4. 删除原图
            bot.shell_cmd(f"rm -f {target_file}")
            bot.shell_cmd(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{target_file}")
            
            # 5. 使用 API 上传新图 (使用 BotAgent 的 upload_file)
            if bot.upload_file(processed_path):
                # 上传后文件在 /sdcard/upload/processed_filename
                uploaded_path = f"/sdcard/upload/{processed_filename}"
                
                # 确定目标路径 (DCIM/Camera)
                remote_dir = "/sdcard/DCIM/Camera/"
                # [修正] 同样修正这里的返回值解包
                ls_out, _ = bot.shell_cmd(f"ls -d {remote_dir}")
                
                # 检查 ls_out 是否包含 "No such file" 或为空
                if not ls_out or "No such file" in str(ls_out):
                     remote_dir = "/sdcard/Pictures/"
                
                final_path = f"{remote_dir}{processed_filename}"
                
                # 移动文件
                bot.shell_cmd(f"mv {uploaded_path} {final_path}")
                
                bot.log(f"✅ 图片已处理并替换: {final_path}")
                
                # 6. 广播新图
                bot.shell_cmd(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{final_path}")
                
                # 清理本地
                try:
                    os.remove(local_path)
                    os.remove(processed_path)
                except:
                    pass
                return True
            else:
                return False

        except Exception as e:
            bot.log(f"❌ 图片处理异常: {e}")
            return False
