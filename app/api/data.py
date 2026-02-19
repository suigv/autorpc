# app/api/data.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

# 数据文件路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataUpdate(BaseModel):
    content: str

@router.get("/accounts")
def get_accounts():
    """获取账号列表"""
    file_path = os.path.join(BASE_DIR, "账号.txt")
    if not os.path.exists(file_path):
        return {"data": ""}
    with open(file_path, "r", encoding="utf-8") as f:
        return {"data": f.read()}

@router.put("/accounts")
def update_accounts(data: DataUpdate):
    """更新账号列表"""
    file_path = os.path.join(BASE_DIR, "账号.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data.content)
    return {"status": "ok"}

@router.get("/location")
def get_location():
    """获取位置列表"""
    file_path = os.path.join(BASE_DIR, "位置.txt")
    if not os.path.exists(file_path):
        return {"data": ""}
    with open(file_path, "r", encoding="utf-8") as f:
        return {"data": f.read()}

@router.put("/location")
def update_location(data: DataUpdate):
    """更新位置列表"""
    file_path = os.path.join(BASE_DIR, "位置.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data.content)
    return {"status": "ok"}

@router.get("/website")
def get_website():
    """获取网站列表"""
    file_path = os.path.join(BASE_DIR, "网页.txt")
    if not os.path.exists(file_path):
        return {"data": ""}
    with open(file_path, "r", encoding="utf-8") as f:
        return {"data": f.read()}

@router.put("/website")
def update_website(data: DataUpdate):
    """更新网站列表"""
    file_path = os.path.join(BASE_DIR, "网页.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data.content)
    return {"status": "ok"}
