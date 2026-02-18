# 文件路径: common/x_scheme.py
import urllib.parse


class XScheme:
    """
    X (Twitter) 兼容版 Scheme 字典
    已优化跳转指令，增加后台执行标识防止设备死机。
    """

    # --- 🏠 基础导航 ---
    HOME = "twitter://timeline"
    NOTIFICATIONS = "twitter://mentions"
    TRENDS = "twitter://trends"

    # --- 📬 私信 ---
    DM_COMPOSE = "twitter://messages/compose?recipient_id={recipient_id}&text={text}"

    # --- 🖊️ 内容创作 ---
    POST = "twitter://post?message={text}"

    # --- 🔍 搜索与发现 ---
    SEARCH = "https://twitter.com/search?q={query}"
    SEARCH_TEMPLATE = "{query}"
    SEARCH_FROM_USER = "(from:{user}) {text}"
    SEARCH_DATE = "{query} since:{since} until:{until}"
    SEARCH_NO_RETWEETS = "{query} -filter:retweets"

    # --- 👤 用户主页 ---
    PROFILE = "twitter://user?screen_name={screen_name}"
    PROFILE_MEDIA = "https://twitter.com/{screen_name}/media"
    PROFILE_LIKES = "https://twitter.com/{screen_name}/likes"
    FOLLOWERS = "https://twitter.com/{screen_name}/followers"
    FOLLOWING = "https://twitter.com/{screen_name}/following"
    USER_LISTS = "https://twitter.com/{screen_name}/lists"

    # --- 🛠️ 账号管理 ---
    EDIT_PROFILE = "https://twitter.com/settings/profile"
    SETTINGS_ACCOUNT = "twitter://settings/account"
    SETTINGS_BLOCKS = "https://twitter.com/settings/blocked/all"

    @classmethod
    def get_url(cls, template, latest=True, **kwargs):
        """
        统一生成编码后的 URL，并处理最新(Live)参数
        """
        safe_kwargs = {k: urllib.parse.quote(str(v)) for k, v in kwargs.items()}

        try:
            if isinstance(template, str):
                url = template.format(**safe_kwargs)
            else:
                url = str(template)
        except (KeyError, IndexError):
            url = template

        if "search" in url and latest and "f=live" not in url:
            connector = "&" if "?" in url else "?"
            url += f"{connector}f=live"

        return url

    @staticmethod
    def wrap_command(url):
        """
        【重要修改】生成 Android 标准跳转指令。
        在末尾添加了 " &"，确保指令发送给系统后 RPA 立即返回，不等待 App 启动结果。
        这能有效防止因 App 卡顿、弹窗导致 RPA 进程堆积引发的死机。
        """
        return f"am start -a android.intent.action.VIEW -d \"{url}\" &"
