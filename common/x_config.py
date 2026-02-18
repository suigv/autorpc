# -*- coding: utf-8 -*-
"""
X (Twitter) Android 客户端 UI 配置文件 - 日文环境专用版 (v1.0 Fix)
基于 2026-02 提供的 XML 节点分析生成
"""


class XConfig:
    # === 基础配置 ===
    PACKAGE_NAME = "com.twitter.android"
    ACTIVITY_NAME = "com.twitter.android.StartActivity"  # 添加 Activity 名称
    APP_LAUNCH_TIMEOUT = 15
    
    # UI 文本常量 (用于 BotAgent 检测)
    UI_TEXT = {
        "HOME_TAB": "ホーム",
        "SEARCH_TAB": "検索",
        "LOGIN_BTN_1": "ログイン",
        "POPUP_NOT_NOW": "今はしない",
        "POPUP_DENY": "許可しない",
        "POPUP_ALLOW": "許可" # 添加允许
    }

    # ==============================
    # 1. 协议导航 (Schemes) - 核心加速
    # ==============================
    # 直接调用 BotAgent.goto_page(key) 使用，跳过 UI 层级查找
    SCHEMES = {
        # 直接进入登录流程（跳过首页点击）
        "login_flow": "twitter://onboarding/task?flow_token=login",
        # 强制回到主页时间线
        "home": "twitter://home",
        # 搜索页
        "search": "twitter://search",
        # 发推页面
        "compose": "twitter://post",
        # 个人主页 (需配合 format 使用)
        "profile": "twitter://user?screen_name={}",
        # 粉丝列表 (需配合 format 使用)
        "followers": "https://twitter.com/{}/followers",
        # 设置页
        "settings": "twitter://settings"
    }
    
    # ==============================
    # 7. 养号/引流配置 (通用版)
    # ==============================
    
    # --- A. 兼职/PayPay 关键词 (已更新 v2) ---
    PAYPAY_CORE = [
        "PayPay (全員 OR 全プレ) -filter:links min_faves:20",
        "PayPay (突発 OR 抽選) -filter:links min_faves:20",
        "現金 (配布 OR プレゼント) -filter:links min_faves:20",
        "paypay 配布", "paypay あげます"
    ]
    PAYPAY_ACTION = [
        "PayPay (リプ OR コメント) -filter:links min_faves:20",
        "PayPay (早い者勝ち OR 即渡し) -filter:links min_faves:10",
        "PayPay 通知オン -filter:links min_faves:20",
        "paypay フォロー RT"
    ]
    PAYPAY_DERIVATIVE = [
        "PayPay (ハズレなし OR 確定) -filter:links min_faves:20",
        "PayPay (生活費 OR 救済) -filter:links min_faves:20",
        "PayPay (在庫 OR 残高) filter:images min_faves:20",
        "PayPay 実績 filter:images min_faves:20",
        "PayPay (1000円 OR 3000円 OR 5000円) -filter:links min_faves:10",
        "アマギフ (全員 OR 配布) -filter:links min_faves:20"
    ]
    PAYPAY_TARGET = [
        "paypay 欲しい", "paypay 恵んで", "金欠", "助けて"
    ]
    PAYPAY_BLACKLIST = [
        "業者", "アダルト", "裏垢", "代行", "副業", "案件"
    ]
    
    # --- B. 交友/Dating 关键词 (深度优化版 v3 - 擦边特化) ---
    DATING_CORE = [
        "#裏垢女子 filter:images min_faves:50",
        "#ナースコス filter:images min_faves:20",
        "#彼シャツ filter:images"
    ]
    DATING_ACTION = [
        "#バニーガール filter:images min_faves:10"
    ]
    DATING_DERIVATIVE = [
        "#黒スト filter:images min_faves:10",
        "#お風呂上がり filter:images"
    ]
    DATING_TARGET = [
        "#太もも filter:images min_faves:10"
    ]
    DATING_BLACKLIST = [
        "業者", "ママ活", "パパ活", "ビジネス", "スカウト", "募集"
    ]

    # ==============================
    # 8. 引用截流文案 (Quote Texts)
    # ==============================
    QUOTE_TEXTS = {
        "volc": [
            "最高です",
            "可愛すぎます",
            "エロすぎ💕 ",
            "保存しました",
            "フォローしました！",
            "DMしてもいい？",
            "仲良くしてください",
            "返信待ってます🥺",
            "に追加💕",
            "もっと見たい"
        ],
        "part_time": [
            "参加します！🙇‍♂️",
            "応募します！",
            "参加させてください！✨",
            "当たりますように🙏️",
            "ご縁がありますように✨",
            "当選しますように🔥",
            "頼みます！🔥",
            "お願いします！🍀"
        ]
    }


    # ==============================
    # 2. 登录流程选择器 (Login Flow)
    # ==============================
    LOGIN_LOCATORS = {
        # [场景: 启动页]
        # 策略: 寻找底部的 "ログイン" 小字
        # 来源: 登录页面节点.xml (无 ID, 靠文本定位)
        "entry_login_btn": {
            "text": "ログイン",
            "class": "android.widget.TextView",
            "desc": "启动页-底部登录入口"
        },

        # [场景: 输入账号]
        # 策略: 页面唯一的 EditText
        # 来源: username.xml
        "input_user": {
            "id": "com.twitter.android:id/ocf_text_input_edit", # 更新为准确的 ID
            "class": "android.widget.EditText",
            "desc": "账号输入框"
        },

        # [场景: 点击下一步]
        # 策略: 寻找文本为 "次へ" 的按钮
        # 来源: username.xml
        "btn_next": {
            "text": "次へ",
            "id": "com.twitter.android:id/cta_button", # 添加 ID，这是真正可点击的父容器
            "class": "android.widget.TextView",
            "desc": "下一步按钮"
        },

        # [场景: 输入密码]
        # 策略: 寻找 Hint 为 "パスワード" 的输入框
        # 来源: password.xml
        "input_password": {
            "id": "com.twitter.android:id/password_edit_text", # 更新为准确的 ID
            "text_hint": "パスワード",
            "class": "android.widget.EditText",
            "desc": "密码输入框"
        },

        # [场景: 提交登录]
        # 策略: 右下角实心按钮，文本为 "ログイン"
        # 来源: password.xml
        "btn_submit_login": {
            "text": "ログイン",
            "id": "com.twitter.android:id/cta_button", # 与下一步按钮 ID 相同
            "class": "android.widget.TextView",
            "desc": "提交登录按钮"
        },

        # [场景: 2FA 验证]
        # 来源: profile_page_dump.xml (2FA页面)
        "input_2fa": {
            "id": "com.twitter.android:id/ocf_text_input_edit", # 与账号输入框 ID 相同
            "text_hint": "コードを入力",
            "class": "android.widget.EditText",
            "desc": "验证码输入框"
        },
        
        # 2FA 页面的下一步按钮
        "btn_submit_2fa": {
            "text": "次へ",
            "id": "com.twitter.android:id/cta_button", # 通用按钮 ID
            "class": "android.widget.TextView",
            "desc": "2FA提交按钮"
        }
    }

    # ==============================
    # 3. 业务功能 UI (Traffic/Home)
    # ==============================
    HOME_LOCATORS = {
        # 底部导航栏 - 强烈建议使用 content-desc (无障碍描述)
        # ID 在不同版本中极不稳定
        "nav_home": {
            "desc_exact": "ホーム",  # Home
            "class": "android.widget.FrameLayout"  # 通常是 FrameLayout
        },
        "nav_search": {
            "desc_exact": "検索",  # Search
        },
        "nav_notif": {
            "desc_exact": "通知",  # Notifications
        },
        "nav_msg": {
            "desc_exact": "メッセージ",  # Messages
        },

        # 侧边栏菜单 (左上角头像)
        "drawer_icon": {
            "desc_contain": "アカウント情報表示",  # 包含匹配
            "class": "android.widget.ImageButton"
        },

        # 发帖悬浮按钮 (+)
        "fab_compose": {
            "desc_exact": "ツイートを作成",  # 或 "ポストする" 取决于版本，建议用 ID 辅助
            "id": "com.twitter.android:id/composer_write"
        }
    }
    
    # ==============================
    # 5. 博主主页 (Profile)
    # ==============================
    PROFILE_LOCATORS = {
        "nick_name": {
            "id": "com.twitter.android:id/name",
            "desc": "博主昵称"
        },
        "user_bio": {
            "id": "com.twitter.android:id/user_bio",
            "desc": "个人简介"
        },
        "user_name": {
            "id": "com.twitter.android:id/user_name",
            "desc": "ScreenName (@xxx)"
        }
    }
    
    # ==============================
    # 6. 私信 (DM)
    # ==============================
    DM_LOCATORS = {
        # 底部导航栏的私信图标
        "nav_dm": {
            "desc_contain": "メッセージ", # 日文: メッセージ, 英文: Messages
            "id": "com.twitter.android:id/x_chat" # 假设 ID
        },
        # 密码输入相关
        "create_pin": {
            "text": "暗証番号を作成", # 日文: 暗証番号を作成, 英文: Create PIN
        },
        "enter_pin": {
            "text": "暗証番号を入力", # 日文: 暗証番号を入力, 英文: Enter PIN
        },
        # 未读消息 (小蓝点)
        "unread_dot": {
            "desc_contain": "未読", # 日文: 未読, 英文: Unread
        },
        # 聊天界面
        "chat_input": {
            "text_hint": "メッセージを作成", # 日文: メッセージを作成, 英文: Start a message
            "class": "android.widget.EditText"
        },
        "send_btn": {
            "desc": "送信", # 日文: 送信, 英文: Send
            # 坐标点击兜底
        }
    }

    # ==============================
    # 4. 弹窗与异常处理 (Popups)
    # ==============================
    POPUP_LOCATORS = {
        # 安卓系统权限弹窗 (位置/通讯录等)
        "sys_perm_allow": {
            "text": "許可",  # 日文：允许
            "id": "com.android.permissioncontroller:id/permission_allow_button"
        },
        "sys_perm_deny": {
            "text": "許可しない",  # 日文：不允许
            "id": "com.android.permissioncontroller:id/permission_deny_button"
        },

        # X 内部引导 (如: 开启通知)
        "app_dialog_negative": {
            "text": "今はしない",  # Not now
            "id": "android:id/button2"  # 通用负向按钮 ID
        },
        
        # X 内部引导 (开启通知 - 允许)
        "app_notif_allow": {
            "text": "許可", # 或者 "通知をオンにする"
            "id": "com.android.permissioncontroller:id/permission_allow_button" # 通常最终还是调起系统弹窗
        }
    }

    @staticmethod
    def get_xpath(key, category="login"):
        """
        工厂方法：将配置字典转换为 XPath 字符串
        兼容 BotAgent 的 find_element 逻辑
        """
        data = {}
        if category == "login":
            data = XConfig.LOGIN_LOCATORS.get(key)
        elif category == "home":
            data = XConfig.HOME_LOCATORS.get(key)
        elif category == "popup":
            data = XConfig.POPUP_LOCATORS.get(key)
        elif category == "scheme":
            return XConfig.SCHEMES.get(key)  # 特殊处理
        elif category == "profile":
            data = XConfig.PROFILE_LOCATORS.get(key)
        elif category == "dm":
            data = XConfig.DM_LOCATORS.get(key)

        if not data: return ""

        # 1. 显式 XPath 优先
        if "xpath" in data: return data["xpath"]

        # 2. 构建 XPath
        # 基础部分
        class_name = data.get("class", "*")
        xpath = f"//{class_name}"

        conditions = []

        # 属性拼接
        if "id" in data:
            conditions.append(f"@resource-id='{data['id']}'")

        if "text" in data:
            conditions.append(f"@text='{data['text']}'")

        if "desc_exact" in data:
            conditions.append(f"@content-desc='{data['desc_exact']}'")

        if "desc_contain" in data:
            conditions.append(f"contains(@content-desc, '{data['desc_contain']}')")

        # 组合
        if conditions:
            xpath += "[" + " and ".join(conditions) + "]"

        # 索引 (XPath 索引从 1 开始，如果 config 写 0 需要注意转换，这里假设 config 存的是 XPath 逻辑的索引)
        # 如果是 RPA 框架通常用 find_elements()[index]，这里仅生成 string
        if "index" in data:
            # 注意：这通常用于 find_elements 后的 Python 切片，
            # 如果必须写在 XPath 里，则是 (xpath)[n]
            pass

        return xpath

    @staticmethod
    def get_selector_dict(key, category="login"):
        """
        推荐：直接返回字典供 mytSelector 使用，比 XPath 更灵活
        """
        if category == "login": return XConfig.LOGIN_LOCATORS.get(key)
        if category == "home": return XConfig.HOME_LOCATORS.get(key)
        if category == "popup": return XConfig.POPUP_LOCATORS.get(key)
        if category == "profile": return XConfig.PROFILE_LOCATORS.get(key)
        if category == "dm": return XConfig.DM_LOCATORS.get(key)
        return None