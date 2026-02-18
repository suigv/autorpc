# tasks/debug_sqlite.py
from common.bot_agent import BotAgent

HOST_IP = "192.168.1.215"
INDEX = 1

def check_sqlite():
    bot = BotAgent(INDEX, HOST_IP)
    if bot.connect():
        print("检查 sqlite3...")
        ret, out = bot.shell_cmd("sqlite3 --version")
        print(f"Result: {out}")
        
        if "not found" not in out:
            print("✅ sqlite3 可用！")
            # 尝试查询账号类型
            cmd = "sqlite3 /data/system/users/0/accounts.db \"SELECT type FROM accounts;\""
            ret, out = bot.shell_cmd(cmd)
            print(f"当前账号类型:\n{out}")
        else:
            print("❌ sqlite3 不可用")
    bot.quit()

if __name__ == "__main__":
    check_sqlite()