"""
设备管理 API
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.device import DeviceStatusResponse, DeviceInfo, DeviceCreate, DeviceStatus, AIType
from app.core.device_manager import DeviceManager, parse_device_range, parse_ai_type
from app.core.workflow_engine import WorkflowEngine

router = APIRouter()
device_manager = DeviceManager()
workflow_engine = WorkflowEngine()


@router.get("/", response_model=List[DeviceInfo])
def list_devices():
    devices = device_manager.get_all_devices()
    result = []
    for idx, dev in devices.items():
        info = device_manager.get_device_info(idx)
        result.append(DeviceInfo(
            index=info["index"],
            ip=info["ip"],
            rpa_port=info["rpa_port"],
            api_port=info["api_port"],
            ai_type=AIType(dev.ai_type),
            status=DeviceStatus(dev.status)
        ))
    return result


@router.post("/batch/start")
def batch_start_devices(devices: str, task_type: str = "full_flow", ai_type: str = "volc"):
    device_list = parse_device_range(devices)
    ai_type = parse_ai_type(ai_type)
    
    if task_type == "full_flow":
        result = workflow_engine.run_full_flow(device_list, ai_type)
    elif task_type == "nurture_flow":
        result = workflow_engine.run_nurture_flow(device_list, ai_type)
    elif task_type == "reset_login":
        result = workflow_engine.run_reset_login(device_list, ai_type)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {task_type}")
    
    return {"devices": device_list, "status": "started", "result": result}


@router.post("/batch/stop")
def batch_stop_devices():
    workflow_engine.stop_all()
    return {"status": "all_stopped"}


@router.get("/{device_id}", response_model=DeviceInfo)
def get_device(device_id: int):
    info = device_manager.get_device_info(device_id)
    dev = device_manager.get_device(device_id)
    return DeviceInfo(
        index=info["index"],
        ip=info["ip"],
        rpa_port=info["rpa_port"],
        api_port=info["api_port"],
        ai_type=AIType(dev.ai_type),
        status=DeviceStatus(dev.status)
    )


@router.get("/{device_id}/status", response_model=DeviceStatusResponse)
def get_device_status(device_id: int):
    dev = device_manager.get_device(device_id)
    return DeviceStatusResponse(
        index=device_id,
        status=DeviceStatus(dev.status),
        current_task=dev.current_task,
        message=dev.message
    )


@router.post("/{device_id}/start")
def start_device(device_id: int, task_type: str = "full_flow", ai_type: str = "volc"):
    ai_type = parse_ai_type(ai_type)
    
    if task_type == "full_flow":
        result = workflow_engine.run_full_flow([device_id], ai_type)
    elif task_type == "nurture_flow":
        result = workflow_engine.run_nurture_flow([device_id], ai_type)
    elif task_type == "reset_login":
        result = workflow_engine.run_reset_login([device_id], ai_type)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown task type: {task_type}")
    
    return {"device_id": device_id, "status": "started", "result": result}


@router.post("/{device_id}/stop")
def stop_device(device_id: int):
    success = workflow_engine.stop_device(device_id)
    if success:
        return {"device_id": device_id, "status": "stopped"}
    raise HTTPException(status_code=400, detail="No running task to stop")
