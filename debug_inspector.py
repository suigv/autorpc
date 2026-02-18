# debug_inspector.py
import time
import os
import datetime
from xml.dom import minidom
from common.mytRpc import MytRpc

# === 配置 ===
HOST_IP = "192.168.1.215"
DEVICE_INDEX = 3  # 设备序号
# ============

def get_rpc_port(index):
    return 30000 + (index - 1) * 100 + 2

def save_xml(xml_str, prefix="dump"):
    """保存格式化后的 XML"""
    if not xml_str:
        print("❌ XML 内容为空")
        return None
    
    try:
        # 尝试格式化 XML
        parsed = minidom.parseString(xml_str)
        pretty_xml = parsed.toprettyxml(indent="  ")
    except:
        pretty_xml = xml_str # 格式化失败则保存原始内容

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.xml"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    
    print(f"📝 XML 已保存至: {os.path.abspath(filename)}")
    return filename

def inspect_nodes(rpc):
    """扫描并分析节点"""
    print("\n🔍 开始扫描当前页面节点...")
    
    selector = rpc.create_selector()
    if not selector:
        print("❌ 创建 Selector 失败")
        return

    # 获取所有节点 (限制数量防止卡死)
    # 注意：execQuery 如果不加条件，可能返回空或者所有节点，取决于 SDK 实现
    # 这里尝试查找所有 View，以获取尽可能多的节点
    with selector:
        selector.addQuery_ClzEqual("android.view.View") # 基础类，通常能匹配大多数
        # 或者尝试不加条件，如果 SDK 支持
        nodes = selector.execQuery(200, 5000)

    if not nodes:
        print("⚠️ 未找到节点，尝试无条件查询...")
        selector = rpc.create_selector()
        with selector:
            nodes = selector.execQuery(200, 5000)

    if not nodes:
        print("❌ 无法获取节点信息")
        return

    print(f"📊 共获取到 {len(nodes)} 个节点 (展示前 50 个关键节点)")
    print("-" * 80)
    print(f"{'ID / Text / Desc':<50} | {'Class':<20} | {'Bounds':<20} | {'Clickable'}")
    print("-" * 80)

    for i, n in enumerate(nodes[:50]):
        # 获取属性
        nid = n.getNodeId() or ""
        text = n.getNodeText() or ""
        desc = n.getNodeDesc() or ""
        clz = n.getNodeClass() or ""
        bounds = n.getNodeNound()
        
        # 尝试获取 clickable 状态 (如果 SDK 支持)
        # mytRpc 似乎没有直接获取 clickable 属性的方法，只能通过 selector 筛选
        # 这里我们只打印基本信息
        
        # 组合显示内容
        content = nid
        if text: content += f" | T:{text}"
        if desc: content += f" | D:{desc}"
        if not content: content = "<无标识>"
        
        # 简化 Bounds 显示
        b_str = f"[{bounds['left']},{bounds['top']}][{bounds['right']},{bounds['bottom']}]"
        
        print(f"{content[:48]:<50} | {clz.split('.')[-1]:<20} | {b_str:<20} | ?")

    print("-" * 80)

def run_inspector():
    port = get_rpc_port(DEVICE_INDEX)
    print(f"📡 连接设备 #{DEVICE_INDEX} ({HOST_IP}:{port})...")

    rpc = MytRpc()
    if not rpc.init(HOST_IP, port, 10):
        print("❌ 连接失败")
        return

    print("✅ 连接成功")

    while True:
        print("\n👇 请选择操作:")
        print("1. 📸 导出当前页面 XML (Dump)")
        print("2. 🔍 扫描并打印节点列表")
        print("3. 🖱️ 测试点击 (输入 ID 或 Text)")
        print("q. 退出")
        
        choice = input("> ").strip()
        
        if choice == '1':
            xml_data = rpc.dumpNodeXml(True)
            save_xml(xml_data)
        elif choice == '2':
            inspect_nodes(rpc)
        elif choice == '3':
            target = input("请输入要点击的 ID 或 文本: ").strip()
            if target:
                # 尝试点击
                selector = rpc.create_selector()
                with selector:
                    # 尝试 ID
                    selector.addQuery_IdEqual(target)
                    node = selector.execQueryOne(1000)
                    if not node:
                        # 尝试 Text
                        selector.clear_Query()
                        selector.addQuery_TextContainWith(target)
                        node = selector.execQueryOne(1000)
                    if not node:
                        # 尝试 Desc
                        selector.clear_Query()
                        selector.addQuery_DescContainWith(target)
                        node = selector.execQueryOne(1000)
                    
                    if node:
                        print(f"✅ 找到节点，执行点击...")
                        node.Click_events()
                    else:
                        print("❌ 未找到匹配节点")
        elif choice.lower() == 'q':
            break
        else:
            print("无效输入")

if __name__ == "__main__":
    run_inspector()