# common/account_handler.py
import os
import threading
from common.ToolsKit import ToolsKit

class AccountHandler:
    _lock = threading.Lock()
    
    @staticmethod
    def get_account(device_index):
        """
        获取账号：优先获取旧号，无旧号则取新号
        格式: X账号----X密码----邮箱----邮箱密码----Auth_Token----2FA
        """
        tools = ToolsKit()
        root_path = tools.GetRootPath()
        
        # 修改 Finish 文件路径到 log 文件夹
        log_dir = os.path.join(root_path, "log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        finish_file = os.path.join(log_dir, f"Finish{device_index}.txt")
        account_file = os.path.join(root_path, "账号.txt")
        
        def parse_account_line(line):
            parts = line.split("----")
            # 确保至少有足够的部分来获取 2FA (index 5)
            # 如果格式严格固定为6部分，可以直接取 parts[5]
            if len(parts) >= 6:
                return parts[0], parts[1], parts[5]
            # 兼容旧格式或不完整格式：如果只有3部分，假设是 User----Pwd----2FA
            elif len(parts) >= 3:
                return parts[0], parts[1], parts[2]
            return None

        with AccountHandler._lock:
            # 1. 尝试读取旧号
            if os.path.exists(finish_file):
                try:
                    with open(finish_file, "r", encoding="utf-8") as f:
                        line = f.readline().strip()
                        if line:
                            return parse_account_line(line)
                except Exception:
                    pass
            
            # 2. 获取新号 (严格互斥)
            if os.path.exists(account_file):
                try:
                    lines = []
                    with open(account_file, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    valid_lines = [l for l in lines if l.strip()]
                    
                    if valid_lines:
                        # 取第一行
                        new_line = valid_lines[0].strip()
                        result = parse_account_line(new_line)
                        
                        if result:
                            # 写入 Finish
                            with open(finish_file, "w", encoding="utf-8") as f:
                                f.write(new_line)
                            
                            # 回写账号文件 (删除第一行)
                            with open(account_file, "w", encoding="utf-8") as f:
                                f.writelines(valid_lines[1:])
                                
                            return result
                except Exception as e:
                    print(f"账号获取异常: {e}")
                    
        return None
