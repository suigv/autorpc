# -*- coding: utf-8 -*-
import requests

class BoxApi:
    """
    封装宿主机 8000 端口的管理 API (sdkapi.md)
    """
    def __init__(self, host_ip, port=8000):
        self.base_url = f"http://{host_ip}:{port}"
        self.session = requests.Session()

    def _get(self, endpoint, params=None, timeout=10):
        try:
            url = f"{self.base_url}{endpoint}"
            resp = self.session.get(url, params=params, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"[BoxApi] GET {endpoint} Error: {e}")
        return None

    def _post(self, endpoint, json_data=None, timeout=10):
        try:
            url = f"{self.base_url}{endpoint}"
            resp = self.session.post(url, json=json_data, timeout=timeout)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            print(f"[BoxApi] POST {endpoint} Error: {e}")
        return None

    # --- 1. 获取云机列表 ---
    def get_android_list(self, index_num=None):
        params = {}
        if index_num is not None:
            params['indexNum'] = index_num
        res = self._get("/android", params)
        if res and res.get('code') == 0:
            return res.get('data', {}).get('list', [])
        return []

    # --- 2. 获取线上机型列表 ---
    def get_phone_models(self):
        res = self._get("/android/phoneModel")
        if res and res.get('code') == 0:
            return res.get('data', {}).get('list', [])
        return []

    # --- 3. 切换机型 ---
    def switch_model(self, name, model_id):
        """
        切换机型
        :param name: 云机名称 (如 android-01)
        :param model_id: 机型 ID
        """
        data = {
            "name": name,
            "modelId": str(model_id)
        }
        res = self._post("/android/switchModel", data)
        return res and res.get('code') == 0

    # --- 4. 重启云机 ---
    def restart_android(self, name):
        data = {"name": name}
        res = self._post("/android/restart", data)
        return res and res.get('code') == 0
