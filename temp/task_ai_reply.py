import time
import re
try:
    import requests
except ImportError:
    requests = None
import json
try:
    import urllib3
except ImportError:
    urllib3 = None

# 禁用安全请求警告
if urllib3:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def execute_ai_reply_process(mytapi, index, log_func=print):
    """
    独立任务：AI 回复流程 (集成火山 AI 请求版)
    """
    log_func(f"🤖 设备 {index}: 启动 AI 自动回复子任务...")

    # 1. 提取内容 (直接尝试提取，不做界面预检查)
    ask = _extract_ask_content(mytapi, index, log_func)
    if not ask:
        log_func(f"⚠️ 设备 {index}: 未提取到有效提问内容，任务终止。")
        # 即使提取失败，也尝试按一下返回，防止卡在某个界面
        mytapi.pressBack()
        return False

    # 2. 调用火山 AI 接口
    reply = _get_ai_response(ask, log_func)
    if not reply:
        log_func(f"⚠️ 设备 {index}: AI 接口未返回有效内容，任务终止。")
        mytapi.pressBack()
        return False

    # 3. 执行发送
    success = _send_reply_text(mytapi, reply, index, log_func)
    if success:
        log_func(f"✅ 设备 {index}: AI 回复流程执行成功。")
    else:
        log_func(f"❌ 设备 {index}: AI 回复流程执行失败。")
        
    return success


def _get_ai_response(ask_text, log_func):
    """
    对接火山引擎 API
    """
    if requests is None:
        log_func(f"❌ 错误: requests 模块未安装，无法调用 AI 接口")
        return None

    url = "https://ark.cn-beijing.volces.com/api/v3/bots/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 6dfbadd6-a61f-4a35-801f-b67a76ff3d2b"
    }
    payload = {
        "model": "bot-20251130222029-mxr2b",
        "stream": False,
        "messages": [{"role": "user", "content": ask_text}]
    }

    try:
        log_func(f"📡 正在请求 AI 接口...")
        response = requests.post(url, headers=headers, json=payload, timeout=30, verify=False)

        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            log_func(f"💡 AI 回复获取成功，长度: {len(reply)}")
            return reply.strip()
        else:
            log_func(f"❌ 接口请求失败，状态码: {response.status_code}, 内容: {response.text}")
            return None
    except Exception as e:
        log_func(f"💥 AI 接口调用异常: {e}")
        return None


def _extract_ask_content(mytapi, index, log_func):
    """
    提取逻辑：锁定最底部消息并从 content-desc 切分
    """
    s = mytapi.create_selector()
    try:
        s.addQuery_ClzEqual("android.view.View")
        nodes = s.execQuery(maxNode=100, timeout=3000)

        if not nodes:
            log_func(f"⚠️ 提取内容失败：未找到任何 'android.view.View' 节点。")
            return None

        valid_messages = []
        for n in nodes:
            desc = n.getNodeDesc() or ""
            bounds = n.getNodeNound()
            # 筛选条件：包含中文冒号，且在屏幕左侧
            if "：" in desc and bounds['left'] < 540: 
                valid_messages.append(n)

        if not valid_messages:
            log_func(f"⚠️ 未找到符合格式的消息节点。")
            return None

        # 按 Y 坐标排序，取最底部最新消息
        valid_messages.sort(key=lambda x: x.getNodeNoundCenter()['y'], reverse=True)
        
        target_node = valid_messages[0]
        clean_desc = target_node.getNodeDesc().replace('\u200e', '').strip()

        try:
            # 格式 "昵称：正文。时间。"
            after_nick = clean_desc.split("：", 1)[1]
            # 尽可能提取到最后一个句号前的内容
            if "。" in after_nick:
                ask = "。".join(after_nick.split("。")[:-1]).strip()
            else:
                ask = after_nick

            if ask:
                log_func(f"📖 提取成功 ask: 「{ask}」")
                return ask
            else:
                log_func(f"⚠️ 解析提取正文为空，原始 desc: 「{clean_desc}」")
                return None
        except Exception as e:
            log_func(f"⚠️ 解析提取正文失败: {e}，原始 desc: 「{clean_desc}」")
            return None
    finally:
        mytapi.release_selector(s)


def _send_reply_text(mytapi, reply_content, index, log_func):
    """
    将 AI 的 reply 内容输入私信输入框并发送
    """
    # 尝试查找输入框节点 (基于 XML 特征)
    found_input = False
    s = mytapi.create_selector()
    try:
        s.addQuery_ClzEqual("android.widget.EditText")
        nodes = s.execQuery(maxNode=10, timeout=2000)
        
        if nodes:
            for n in nodes:
                # getNodeText() 不接受任何参数
                if "私信" in n.getNodeText():
                    log_func("✅ 找到私信输入框节点，点击输入...")
                    n.Click_events()
                    found_input = True
                    break
    finally:
        mytapi.release_selector(s)

    if not found_input:
        log_func("⚠️ 未找到输入框节点，执行坐标点击 (500, 1800)...")
        mytapi.touchClick(0, 500, 1800)
    
    time.sleep(1)
    mytapi.sendText(reply_content)
    
    time.sleep(1)
    # 点击发送按钮 (使用坐标)
    mytapi.touchClick(0, 970, 1800)
    log_func(f"📤 设备 {index}: 回复已发出 (坐标点击)")
    
    time.sleep(2)
    # 点击返回按钮，回到上一个界面
    mytapi.pressBack()
    log_func(f"🔙 设备 {index}: 已点击返回")
    return True
