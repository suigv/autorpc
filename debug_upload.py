import requests
import os

def test_upload(ip, api_port, file_path):
    url = f"http://{ip}:{api_port}/upload"
    print(f"正在上传 {file_path} 到 {url} ...")
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=30)
            
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 上传请求成功，请在设备上查找文件位置。")
            print("建议检查路径: /sdcard/, /sdcard/Download/, /data/local/tmp/")
        else:
            print("❌ 上传失败")
            
    except Exception as e:
        print(f"❌ 异常: {e}")

if __name__ == "__main__":
    # 配置
    DEVICE_IP = "192.168.1.215"  # 请确认 IP
    DEVICE_INDEX = 2
    
    # 计算端口 (30000 + (index-1)*100 + 1)
    API_PORT = 30000 + (DEVICE_INDEX - 1) * 100 + 1
    
    # 根目录下的 22.png
    FILE_PATH = "22.png" 
    
    if not os.path.exists(FILE_PATH):
        # 如果当前目录下没有，尝试创建一个假的用于测试
        print(f"文件 {FILE_PATH} 不存在，创建一个临时文件...")
        with open(FILE_PATH, "w") as f:
            f.write("test image content")
            
    test_upload(DEVICE_IP, API_PORT, FILE_PATH)
