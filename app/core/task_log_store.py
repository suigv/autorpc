"""In-memory task log store for frontend polling."""

from collections import deque
from datetime import datetime
import threading
from typing import Any, Dict, List, Optional

_MAX_LOGS = 5000

_lock = threading.Lock()
_logs: deque = deque(maxlen=_MAX_LOGS)
_next_id = 1
_device_task_map: Dict[int, str] = {}


def bind_device_task(device_index: int, task_id: str) -> None:
    with _lock:
        _device_task_map[device_index] = task_id


def unbind_device_task(device_index: int, task_id: Optional[str] = None) -> None:
    with _lock:
        current = _device_task_map.get(device_index)
        if current is None:
            return
        if task_id is None or task_id == current:
            _device_task_map.pop(device_index, None)


def get_device_task(device_index: int) -> Optional[str]:
    with _lock:
        return _device_task_map.get(device_index)


def append_task_log(
    message: str,
    device_index: Optional[int] = None,
    level: str = "info",
    task_id: Optional[str] = None,
    source: str = "task",
) -> Dict[str, Any]:
    global _next_id

    with _lock:
        resolved_task_id = task_id
        if resolved_task_id is None and device_index is not None:
            resolved_task_id = _device_task_map.get(device_index)

        entry = {
            "id": _next_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "device_index": device_index,
            "task_id": resolved_task_id,
            "level": level,
            "source": source,
            "message": message,
        }
        _next_id += 1
        _logs.append(entry)
        return entry


def get_task_logs(
    device_index: Optional[int] = None,
    task_id: Optional[str] = None,
    since_id: int = 0,
    limit: int = 200,
) -> Dict[str, Any]:
    limit = max(1, min(limit, 500))

    with _lock:
        items: List[Dict[str, Any]] = []
        for entry in _logs:
            if entry["id"] <= since_id:
                continue
            if device_index is not None and entry["device_index"] != device_index:
                continue
            if task_id is not None and entry["task_id"] != task_id:
                continue
            items.append(entry)

        if len(items) > limit:
            items = items[-limit:]

        next_since_id = since_id
        if items:
            next_since_id = items[-1]["id"]

        return {"logs": items, "next_since_id": next_since_id}
