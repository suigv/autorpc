# common/blogger_manager.py
import os
import json
import time
import threading
from common.config_manager import cfg

class BloggerManager:
    _lock = threading.Lock()
    
    @staticmethod
    def _load_json(path, default=None):
        if not os.path.exists(path):
            return default if default is not None else {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default if default is not None else {}

    @staticmethod
    def _save_json(path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def _append_history(ai_type, bloggers):
        path = cfg.get_file_path("history.txt", ai_type)
        with open(path, "a", encoding="utf-8") as f:
            for b in bloggers:
                f.write(f"{b}\n")

    @staticmethod
    def _load_history(ai_type):
        path = cfg.get_file_path("history.txt", ai_type)
        if not os.path.exists(path): return set()
        with open(path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
            
    @staticmethod
    def _remove_from_history(ai_type, blogger):
        path = cfg.get_file_path("history.txt", ai_type)
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if blogger in lines:
                lines.remove(blogger)
                with open(path, "w", encoding="utf-8") as f:
                    for line in lines:
                        f.write(f"{line}\n")
        except Exception:
            pass

    @staticmethod
    def _recycle_all_history(ai_type):
        hist_path = cfg.get_file_path("history.txt", ai_type)
        pool_path = cfg.get_file_path("bloggers_pool.json", ai_type)
        
        if not os.path.exists(hist_path): return False
        try:
            with open(hist_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines: return False
            
            pool = BloggerManager._load_json(pool_path, {"data": []})
            existing = set(pool.get("data", []))
            for b in lines:
                if b not in existing:
                    pool.setdefault("data", []).append(b)
            
            BloggerManager._save_json(pool_path, pool)
            with open(hist_path, "w", encoding="utf-8") as f:
                f.write("")
            return True
        except Exception:
            return False

    # --- 核心接口 ---

    @staticmethod
    def set_current_user(device_index, username, ai_type="volc"):
        path = cfg.get_file_path("current_users.json", ai_type)
        with BloggerManager._lock:
            users = BloggerManager._load_json(path)
            users[str(device_index)] = username.replace("@", "").strip()
            BloggerManager._save_json(path, users)

    @staticmethod
    def get_current_user(device_index, ai_type="volc"):
        path = cfg.get_file_path("current_users.json", ai_type)
        users = BloggerManager._load_json(path)
        return users.get(str(device_index))

    @staticmethod
    def get_blogger(device_index, ai_type):
        dev_key = str(device_index)
        pool_path = cfg.get_file_path("bloggers_pool.json", ai_type)
        bind_path = cfg.get_file_path("device_binding.json", ai_type)
        stat_path = cfg.get_file_path("scrape_status.json", ai_type)
        
        with BloggerManager._lock:
            # 1. 检查绑定
            bindings = BloggerManager._load_json(bind_path)
            if dev_key in bindings:
                return bindings[dev_key]["blogger"], False, False
            
            # 辅助函数：检查博主是否已被其他设备占用
            def is_blogger_occupied(blogger_name):
                for d_key, d_val in bindings.items():
                    if d_key != dev_key and d_val.get("blogger") == blogger_name:
                        return True
                return False

            # 2. 检查库存
            pool = BloggerManager._load_json(pool_path, {"data": []})
            target_pool = pool.get("data", [])
            
            blogger = None
            
            # 尝试从库存中取出一个未被占用的博主
            # 虽然理论上库存里的应该都是未分配的，但为了绝对安全，我们遍历检查
            while target_pool:
                candidate = target_pool.pop(0)
                if not is_blogger_occupied(candidate):
                    blogger = candidate
                    break
                else:
                    print(f"[Dev {device_index}] ⚠️ 博主 {candidate} 已被其他设备占用，跳过")
            
            if not blogger:
                # 3. 库存不足 -> 优先检查冷却
                status = BloggerManager._load_json(stat_path)
                last_scrape = status.get(dev_key, {}).get("last_scrape_time", 0)
                
                if time.time() - last_scrape > 3600: 
                    # 保存可能被修改的 pool (因为 pop 了被占用的)
                    pool["data"] = target_pool
                    BloggerManager._save_json(pool_path, pool)
                    return None, True, False 
                
                # 4. 冷却中 -> 尝试从备用文件获取
                # 也要检查备用博主是否被占用
                backup_candidates = BloggerManager._get_unused_backup_bloggers(ai_type)
                for candidate in backup_candidates:
                    if not is_blogger_occupied(candidate):
                        blogger = candidate
                        print(f"[Dev {device_index}] 冷却中，从备用获取: {blogger}")
                        break
                
                if not blogger:
                    # 5. 备用也没了 -> 尝试回收历史
                    print(f"[Dev {device_index}] ⚠️ 资源耗尽，尝试回收历史...")
                    if BloggerManager._recycle_all_history(ai_type):
                        # 重新加载 pool
                        pool = BloggerManager._load_json(pool_path)
                        target_pool = pool.get("data", [])
                        while target_pool:
                            candidate = target_pool.pop(0)
                            if not is_blogger_occupied(candidate):
                                blogger = candidate
                                print(f"[Dev {device_index}] ♻️ 回收成功: {blogger}")
                                break
                        
                        if not blogger:
                            pool["data"] = target_pool
                            BloggerManager._save_json(pool_path, pool)
                            return None, False, False
                    else:
                        pool["data"] = target_pool
                        BloggerManager._save_json(pool_path, pool)
                        return None, False, False

            # 保存
            pool["data"] = target_pool
            BloggerManager._save_json(pool_path, pool)
            
            bindings[dev_key] = {
                "blogger": blogger,
                "time": time.time()
            }
            BloggerManager._save_json(bind_path, bindings)
            
            BloggerManager._append_history(ai_type, [blogger])
            
            return blogger, False, True

    @staticmethod
    def add_bloggers(ai_type, new_bloggers, device_index=None):
        pool_path = cfg.get_file_path("bloggers_pool.json", ai_type)
        bind_path = cfg.get_file_path("device_binding.json", ai_type)
        
        with BloggerManager._lock:
            history = BloggerManager._load_history(ai_type)
            pool = BloggerManager._load_json(pool_path, {"data": []})
            bindings = BloggerManager._load_json(bind_path)
            
            current_user = None
            if device_index:
                current_user = BloggerManager.get_current_user(device_index, ai_type)

            # 获取所有正在使用的博主集合
            active_bloggers = set()
            for val in bindings.values():
                if val.get("blogger"):
                    active_bloggers.add(val["blogger"])

            valid_bloggers = []
            for b in new_bloggers:
                b = b.replace("@", "").strip()
                if current_user and b.lower() == current_user.lower():
                    continue
                
                # 增加检查：不在历史、不在库存、不在当前活跃绑定中
                if b and b not in history and b not in pool.get("data", []) and b not in active_bloggers:
                    valid_bloggers.append(b)
            
            if valid_bloggers:
                pool.setdefault("data", []).extend(valid_bloggers)
                BloggerManager._save_json(pool_path, pool)
                return len(valid_bloggers)
            return 0

    @staticmethod
    def update_scrape_time(device_index, ai_type):
        path = cfg.get_file_path("scrape_status.json", ai_type)
        with BloggerManager._lock:
            status = BloggerManager._load_json(path)
            status[str(device_index)] = {"last_scrape_time": time.time()}
            BloggerManager._save_json(path, status)

    @staticmethod
    def reset_binding_and_cooling(device_index):
        dev_key = str(device_index)
        for ai_type in ["volc", "part_time"]:
            bind_path = cfg.get_file_path("device_binding.json", ai_type)
            stat_path = cfg.get_file_path("scrape_status.json", ai_type)
            pool_path = cfg.get_file_path("bloggers_pool.json", ai_type)
            
            with BloggerManager._lock:
                # 回收
                bindings = BloggerManager._load_json(bind_path)
                if dev_key in bindings:
                    binding = bindings[dev_key]
                    blogger = binding.get("blogger")
                    if blogger:
                        BloggerManager._remove_from_history(ai_type, blogger)
                        pool = BloggerManager._load_json(pool_path, {"data": []})
                        pool.setdefault("data", []).insert(0, blogger)
                        BloggerManager._save_json(pool_path, pool)
                        print(f"[Dev {device_index}] ♻️ [{ai_type}] 博主 {blogger} 已回收")

                    del bindings[dev_key]
                    BloggerManager._save_json(bind_path, bindings)
                
                # 清除冷却
                status = BloggerManager._load_json(stat_path)
                if dev_key in status:
                    del status[dev_key]
                    BloggerManager._save_json(stat_path, status)

    @staticmethod
    def _get_unused_backup_bloggers(ai_type):
        """
        获取所有未使用的备用博主列表
        """
        path = cfg.get_backup_file(ai_type)
        if not os.path.exists(path): return []
        
        history = BloggerManager._load_history(ai_type)
        candidates = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip().replace("@", "") for line in f if line.strip()]
            for b in lines:
                if b not in history:
                    candidates.append(b)
        except Exception:
            pass
        return candidates
