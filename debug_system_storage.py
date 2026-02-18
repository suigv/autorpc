# tasks/debug_system_storage.py
import time
from common.bot_agent import BotAgent

# === 配置 ===
DEVICE_INDEX = 1
HOST_IP = "192.168.1.215"
PACKAGE_NAME = "com.twitter.android"
# ============

def debug_storage():
    print(f"--- 开始调试系统级存储 (设备 #{DEVICE_INDEX}) ---")
    bot = BotAgent(DEVICE_INDEX, HOST_IP)
    if not bot.connect():
        print("❌ 连接失败")
        return

    print("✅ 连接成功")
    
    # 1. 检查 AccountManager (系统账号)
    print("\n🔍 [1/4] 检查系统账号 (dumpsys account)...")
    ret, output = bot.shell_cmd("dumpsys account")
    if ret:
        if "twitter" in output.lower() or "com.twitter" in output.lower():
            print("⚠️ 发现 Twitter 账号残留!")
            # 提取相关行
            for line in output.split('\n'):
                if "twitter" in line.lower():
                    print(f"  -> {line.strip()}")
        else:
            print("✅ 未发现 Twitter 系统账号")
    else:
        print("❌ dumpsys account 执行失败")

    # 2. 检查 SD 卡残留
    print("\n🔍 [2/4] 检查 SD 卡残留...")
    paths_to_check = [
        f"/sdcard/Android/data/{PACKAGE_NAME}",
        "/sdcard/Twitter",
        "/sdcard/.Twitter",
        "/sdcard/Android/media/{PACKAGE_NAME}"
    ]
    
    for path in paths_to_check:
        ret, output = bot.shell_cmd(f"ls -d {path}")
        if ret and "No such file" not in output:
            print(f"⚠️ 发现残留目录: {path}")
        else:
            print(f"✅ 目录不存在: {path}")

    # 3. 检查 Data 分区 (需要 Root 或 Debug 权限)
    print("\n🔍 [3/4] 检查 Data 分区 (/data/data)...")
    ret, output = bot.shell_cmd(f"ls -la /data/data/{PACKAGE_NAME}")
    if ret and "No such file" not in output and "Permission denied" not in output:
        print(f"⚠️ Data 目录依然存在 (包含 {len(output.splitlines())} 个文件/目录)")
        # 检查 shared_prefs
        ret, sp_out = bot.shell_cmd(f"ls /data/data/{PACKAGE_NAME}/shared_prefs")
        if ret and "No such file" not in sp_out:
             print(f"  -> shared_prefs: {sp_out.strip()}")
    elif "Permission denied" in output:
        print("❌ 无权限访问 /data/data (需要 Root)")
    else:
        print("✅ Data 目录不存在 (已清除)")

    # 4. 尝试清除系统账号 (实验性)
    # 如果发现了系统账号，尝试用 pm clear com.android.providers.contacts (慎用，会清空通讯录)
    # 这里只打印建议
    print("\n💡 [建议]")
    print("如果发现系统账号残留，且 pm clear 无效，可能需要手动进入 '设置 -> 账号' 删除。")
    print("或者尝试硬重置 (销毁容器)。")

    bot.quit()
    print("\n--- 调试结束 ---")

if __name__ == "__main__":
    debug_storage()