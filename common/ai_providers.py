# common/ai_providers.py
"""
AI 服务提供者模块

请在环境变量或 config.json 中配置你的 API 密钥:
- VOLC_API_KEY: 火山引擎 API Key
- PART_TIME_API_KEY: 兼职接口 API Key
"""
import os
import requests
import random

# 从环境变量获取 API 密钥
VOLC_API_KEY = os.environ.get("VOLC_API_KEY", "")
PART_TIME_API_KEY = os.environ.get("PART_TIME_API_KEY", "")

# 尝试导入 urllib3 禁用警告
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    urllib3 = None


class BaseAIProvider:
    """AI 服务提供者的基类"""
    def __init__(self, log_func=print):
        self.log = log_func

    def get_reply(self, text):
        """
        获取 AI 回复
        :param text: 输入的文本
        :return: 回复的字符串，或 None
        """
        raise NotImplementedError("子类必须实现 get_reply 方法")


class VolcEngineAI(BaseAIProvider):
    """火山引擎豆包大模型 (交友接口)"""
    def __init__(self, log_func=print):
        super().__init__(log_func)
        self.api_key = VOLC_API_KEY or os.environ.get("VOLC_API_KEY", "")
        self.url = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
        self.model = "bot-20251130222029-mxr2b"  # TODO: 替换为你的 model ID

    def get_reply(self, text):
        if not self.api_key:
            self.log("❌ [交友AI] 未配置 API_KEY")
            return None

        headers = {
            "Content-Type": "application/json",
            f"Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [{"role": "user", "content": text}]
        }

        try:
            self.log(f"📡 [交友AI] 请求: {text[:15]}...")
            response = requests.post(self.url, headers=headers, json=payload, timeout=30, verify=False)

            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                self.log(f"💡 [交友AI] 回复: {reply[:15]}...")
                return reply.strip()
            else:
                self.log(f"❌ [交友AI] 请求失败: {response.status_code}")
                return None
        except Exception as e:
            self.log(f"💥 [交友AI] 异常: {e}")
            return None


class PartTimeAI(BaseAIProvider):
    """火山引擎 (兼职接口)"""
    def __init__(self, log_func=print):
        super().__init__(log_func)
        self.api_key = PART_TIME_API_KEY or os.environ.get("PART_TIME_API_KEY", "")
        self.url = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
        self.model = "bot-20260205014728-mphq8"  # TODO: 替换为你的 model ID

    def get_reply(self, text):
        if not self.api_key:
            self.log("❌ [兼职AI] 未配置 API_KEY")
            return None

        character = random.choice(["hunter", "master"])
        self.log(f"🎭 [兼职AI] 使用角色: {character}")

        headers = {
            "Content-Type": "application/json",
            f"Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [{"role": "user", "content": text}],
            "metadata": {
                "target_character_name": character
            }
        }

        try:
            self.log(f"📡 [兼职AI] 请求: {text[:15]}...")
            response = requests.post(self.url, headers=headers, json=payload, timeout=30, verify=False)

            if response.status_code == 200:
                result = response.json()
                reply = result['choices'][0]['message']['content']
                self.log(f"💡 [兼职AI] 回复: {reply[:15]}...")
                return reply.strip()
            else:
                self.log(f"❌ [兼职AI] 请求失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.log(f"💥 [兼职AI] 异常: {e}")
            return None


def get_ai_provider(provider_name, log_func=print):
    """
    AI 提供者工厂函数
    :param provider_name: "volc" (交友) 或 "part_time" (兼职)
    :param log_func: 日志回调函数
    :return: 对应的 AI Provider 实例
    """
    if provider_name.lower() == "volc":
        return VolcEngineAI(log_func)
    elif provider_name.lower() == "part_time":
        return PartTimeAI(log_func)
    else:
        log_func(f"⚠️ 未知的 AI Provider: {provider_name}, 默认使用 VolcEngineAI")
        return VolcEngineAI(log_func)
