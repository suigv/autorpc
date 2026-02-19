# app/core/log_manager.py
import asyncio
from typing import Dict, List
from fastapi import WebSocket

class LogManager:
    """WebSocket日志管理器"""
    _instance = None
    _clients: List[WebSocket] = []
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self._clients.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self._clients:
            self._clients.remove(websocket)
    
    async def broadcast(self, message: str):
        """广播消息到所有客户端"""
        disconnected = []
        for client in self._clients:
            try:
                await client.send_text(message)
            except Exception:
                disconnected.append(client)
        
        for client in disconnected:
            self.disconnect(client)
    
    async def send_to_device(self, device_id: int, message: str):
        """发送消息到指定设备"""
        await self.broadcast(f"[Dev {device_id}] {message}")

# 全局单例
log_manager = LogManager.get_instance()
