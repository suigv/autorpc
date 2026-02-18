import time
import task_ai_reply


def execute_dm_task(mytapi, index, log_func=print):
    """
    私信处理任务：进入私信、处理密码/蒙层、检测未读小蓝点
    """
    log_func(f"✉️ 设备 {index}: 启动私信处理任务...")
    my_password = "1234"

    # 1. 点击底栏私信图标
    found_dm_entry = False
    s = mytapi.create_selector()
    try:
        s.addQuery_IdEqual("com.twitter.android:id/x_chat")
        node = s.execQueryOne(timeout=3000)
        if node:
            node.Click_events()
            found_dm_entry = True
    finally:
        mytapi.release_selector(s)

    if not found_dm_entry:
        mytapi.touchClick(0, 980, 1850)  # 坐标保底

    time.sleep(4)

    # 2. 状态循环判定 (处理密码页或直接进入)
    for attempt in range(4):
        s = mytapi.create_selector()
        try:
            # 判定 A: 是否成功进入聊天列表 (XML特征: 存在"搜索"或"聊天"标题)
            s.addQuery_TextEqual("All")
            if s.execQueryOne(timeout=1500):
                log_func(f"✅ 设备 {index}: 已进入聊天界面")
                # 尝试点击空白处消除可能存在的灰色蒙层 (坐标取屏幕中心靠上位置)
                mytapi.touchClick(0, 540, 200)
                time.sleep(1)
                break  # 跳出密码处理循环

            # 判定 B: 是否是【创建密码】
            s.clear_Query()
            s.addQuery_TextEqual("创建密码")
            if s.execQueryOne(timeout=1000):
                log_func(f"🔐 设备 {index}: 处理【创建密码】...")
                mytapi.clickText("创建密码")
                time.sleep(2)
                _input_pin_sequence(mytapi, my_password)  # 第一次
                time.sleep(2)
                _input_pin_sequence(mytapi, my_password)  # 确认
                time.sleep(4)
                continue

            # 判定 C: 是否是【输入你的密码】
            s.clear_Query()
            s.addQuery_TextEqual("输入你的密码")
            if s.execQueryOne(timeout=1000):
                log_func(f"🔑 设备 {index}: 处理【输入密码】...")
                _input_pin_sequence(mytapi, my_password)
                time.sleep(4)
                continue
        finally:
            mytapi.release_selector(s)

    # 3. 未读消息检测 (根据 image_99441f.png 特征)
    # 逻辑：检查是否存在蓝色小圆点图标
    log_func(f"🔍 设备 {index}: 正在扫描未读消息(小蓝点)...")
    has_unread = False
    s = mytapi.create_selector()
    try:
        # 在 Twitter XML 中，小蓝点通常是一个没有 Text 但有关联描述的 View
        # 根据 image_99441f.png，我们可以查找 content-desc 包含 "未读" 的节点
        s.addQuery_DescContainWith("未读")
        unread_node = s.execQueryOne(timeout=3000)

        if unread_node:
            log_func(f"🔵 设备 {index}: 发现未读消息，准备进入...")
            unread_node.Click_events()
            has_unread = True
            time.sleep(3)
        else:
            # 方案 B: 坐标保底检测。小蓝点通常在屏幕右侧 [1000, 650] 附近
            # 此处优先使用节点识别，若识别不到则认为没有未读
            log_func(f"😴 设备 {index}: 未发现小蓝点，无需操作。")
    finally:
        mytapi.release_selector(s)

    if has_unread:
        log_func(f"📩 进入未读对话，触发 AI 自动回复...")
        task_ai_reply.execute_ai_reply_process(mytapi, index, log_func)
        time.sleep(3)

    return True


def _input_pin_sequence(mytapi, password_str):
    """
    修复版：先激活输入框，再通过 ADB 物理指令输入密码
    """
    # 1. 激活输入框 (点击那四个圆点的位置)
    # 根据截图，圆点大概在屏幕垂直方向的 35%-40% 处
    # 假设是 1080x1920 分辨率，X=540, Y=600 左右
    print(f"👉 正在激活密码输入框...")
    mytapi.touchClick(0, 540, 600)
    time.sleep(1.5) # 等待键盘弹出（即使弹不出来，下面的指令也有效）

    # 2. 定义数字到 ADB KeyCode 的映射
    # ADB KeyCode: 0->7, 1->8 ... 9->16
    key_map = {
        '0': 7, '1': 8, '2': 9, '3': 10, '4': 11,
        '5': 12, '6': 13, '7': 14, '8': 15, '9': 16
    }

    # 3. 循环发送物理按键指令
    for char in password_str:
        if char in key_map:
            code = key_map[char]
            print(f"⌨️ 输入密码字符: {char} (KeyCode: {code})")
            # 使用 input keyevent 直接模拟硬件按键，无视 UI 布局
            mytapi.exec_cmd(f"input keyevent {code}")
            time.sleep(0.5) # 稍微慢一点，防止输入过快丢失

    print("✅ 密码输入指令发送完毕")
