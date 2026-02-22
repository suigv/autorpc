# -*- coding: utf-8 -*-
import os
import sys
import platform


class ToolsKit(object):
    def __init__(self):
        pass

    def load_accounts(self, file_path="账号.txt"):
        """
        读取账号文件
        格式兼容：user----pass----email----email_pass----token----2fa
        """
        accounts = []
        # 处理相对路径问题，优先查找当前运行目录
        if not os.path.exists(file_path):
            root = self.GetRootPath()
            file_path = os.path.join(root, file_path)

        if not os.path.exists(file_path):
            print(f"[ToolsKit] 警告: 找不到账号文件 {file_path}")
            return accounts

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue

                    parts = line.split("----")
                    # 至少包含账号和密码
                    if len(parts) >= 2:
                        acc = {
                            "user": parts[0],
                            "pass": parts[1],
                            # 如果有更多字段，按顺序读取，防止越界
                            "email": parts[2] if len(parts) > 2 else "",
                            "email_pass": parts[3] if len(parts) > 3 else "",
                            "token": parts[4] if len(parts) > 4 else "",
                            "2fa": parts[5] if len(parts) > 5 else ""
                        }
                        accounts.append(acc)
            print(f"[ToolsKit] 成功加载 {len(accounts)} 个账号")
        except Exception as e:
            print(f"[ToolsKit] 读取账号文件异常: {e}")

        return accounts

    def GetRootPath(self):
        """获取当前程序的可执行文件路径"""
        # 首先检查环境变量
        if 'MYT_ROOT_PATH' in os.environ:
            return os.environ['MYT_ROOT_PATH']
        
        # 检查当前工作目录是否有config目录
        cwd = os.getcwd()
        if os.path.exists(os.path.join(cwd, 'config', 'devices.json')):
            return cwd
        
        # in bundle
        args = sys.argv[0]
        # 判断是否 是相对路径 还是绝对路径
        if not os.path.exists(args):
            pwd = os.getcwd()
            bundle_dir = os.path.join(pwd, args)
        else:
            bundle_dir = os.path.dirname(args)
            if bundle_dir == '':
                bundle_dir = os.getcwd()
        return bundle_dir

    def check_process(self, pid):
        """检查进程是否存在"""
        try:
            import psutil
            pid = int(pid)
            if psutil.pid_exists(pid):
                return True
        except:
            pass
        return False

    def check_multi_run(self):
        """
        判断是否多次运行
        return: True 存在相同进程实例, False 不存在
        """
        if platform.machine() == 'aarch64':  # arm板是容器部署不进行判断
            return False

        ret = False
        root_path = self.GetRootPath()
        config_dir = os.path.join(root_path, "conf")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        pid_file = os.path.join(config_dir, "myt.pid")

        if os.path.isfile(pid_file):
            try:
                with open(pid_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        pid = int(content)
                        if self.check_process(pid):
                            ret = True
            except Exception:
                ret = False

        if not ret:
            # 写入当前进程PID
            try:
                with open(pid_file, 'w') as f:
                    f.write(str(os.getpid()))
            except Exception as e:
                print(f"[ToolsKit] 无法写入PID文件: {e}")

        return ret
