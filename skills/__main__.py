#!/usr/bin/env python3
"""
MYT Skills CLI 入口

用法:
    python -m skills run full 1-5 volc      # 完整流程
    python -m skills run nurture 1-5 volc    # 养号流程
    python -m skills run reset 1-5 volc      # 重置登录
    python -m skills scrape 1 volc           # 单独抓取
    python -m skills config show              # 显示配置
    python -m skills config ip 192.168.1.xxx # 修改IP
"""
import argparse
import sys

from skills.core import (
    WorkflowEngine,
    parse_device_range,
    parse_ai_type,
    get_host_ip,
    get_total_devices,
    update_host_ip
)

def cmd_run(args):
    engine = WorkflowEngine()
    devices = parse_device_range(args.devices)
    ai_type = parse_ai_type(args.ai)
    
    if args.flow == "full":
        engine.run_full_flow(devices, ai_type)
    elif args.flow == "nurture":
        engine.run_nurture_flow(devices, ai_type)
    elif args.flow == "reset":
        engine.run_reset_login(devices, ai_type)
    else:
        print(f"未知流程: {args.flow}")

def cmd_scrape(args):
    from tasks.task_scrape_blogger import ensure_blogger_ready
    from common.bot_agent import BotAgent
    from skills.core import calculate_ports
    
    device = int(args.device)
    ai_type = parse_ai_type(args.ai)
    host_ip = get_host_ip()
    rpa_port, api_port = calculate_ports(device)
    
    device_info = {
        "ip": host_ip,
        "index": device,
        "rpa_port": rpa_port,
        "api_port": api_port,
        "ai_type": ai_type
    }
    
    bot = BotAgent(device, host_ip)
    if not bot.connect():
        print(f"[Dev {device}] 连接失败")
        return
    
    print(f"[Dev {device}] 开始抓取博主任务")
    blogger, is_new = ensure_blogger_ready(device_info, ai_type)
    print(f"[Dev {device}] 抓取完成: {blogger}, is_new={is_new}")
    bot.quit()

def cmd_config(args):
    if args.action == "show":
        from skills.core import load_config
        import json
        print(json.dumps(load_config(), indent=2, ensure_ascii=False))
    elif args.action == "ip":
        update_host_ip(args.value)
        print(f"已更新 IP: {args.value}")
    else:
        print(f"未知操作: {args.action}")

def main():
    parser = argparse.ArgumentParser(description="MYT Skills CLI")
    subparsers = parser.add_subparsers()
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="运行工作流")
    run_parser.add_argument("flow", choices=["full", "nurture", "reset"], help="流程类型")
    run_parser.add_argument("devices", help="设备范围，如 1-5 或 1,3,5")
    run_parser.add_argument("ai", nargs="?", default="volc", help="AI类型: volc 或 part_time")
    run_parser.set_defaults(func=cmd_run)
    
    # scrape 命令
    scrape_parser = subparsers.add_parser("scrape", help="单独抓取博主")
    scrape_parser.add_argument("device", help="设备索引")
    scrape_parser.add_argument("ai", nargs="?", default="volc", help="AI类型")
    scrape_parser.set_defaults(func=cmd_scrape)
    
    # config 命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument("action", choices=["show", "ip"], help="操作")
    config_parser.add_argument("value", nargs="?", help="值")
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
