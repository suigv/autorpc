# MYTOS API 接口文档 _ 魔云腾

*来源: MYTOS API 接口文档 _ 魔云腾.pdf*

---

## 第 1 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
MYTOS API 接口文档
MYTOS API 接口文档
文档版本: v3 | 更新日期: 2026-01-30
目标用户: Android 开发者、集成商、自动化测试人员
文档类型: 开发者参考手册
📚
快速导航
基础信息 #
安卓 APP 端口基础映射
基础概念
通用说明
常见问题
接口目录
1. 下载文件
2. 获取剪贴板内容
3. 设置剪贴板内容
4. 查询 S5 代理状态
5. 设置 S5 代理
6. 停止 S5 代理
7. 设置 S5 域名过滤
8. 接收短信
9. 上传 Google 证书
10. ADB 切换权限
11. 导出 app 信息
12. 导入 app 信息
13. 虚拟摄像头热启动
14. 后台保活
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 1/66

## 第 2 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
15. 屏蔽按键
16. 批量安装 apks/xapk 分包
17. 版本查询
18. 截图功能
19. 自动点击
20. 文件上传
21. 容器信息
22. 通话记录
23. 刷新定位
24. 谷歌 id
25. 安装面具
26. 添加联系人
27. webrtc 播放器
28. 获取后台允许 root 授权的 app 列表
29. 指定包名是否允许 root
30. 设置虚拟摄像头源和类型
31. 获取 APP 开机启动列表
32. 设置指定 APP 开机启动
33. IP定位
34. 设置语言和国家
安卓 APP 端口基础映射
Android 客户端自定义填写端口参数
桥接模式：
配置项 填写值 功能说明
输入 IP 192.168.x.x 公网可以被访问的 ip
固定值： 投屏画面推流端口 用于将手机屏幕画面实时推送到客户端
TCP Port
10000 （如 PC 或 Web 播放器）
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 2/66

## 第 3 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
配置项 填写值 功能说明
固定值：
UDP Port 远程控制指令端口 接收鼠标点击、滑动、按键等操作指令
10001
Image Port 固定值：9082 安卓 adk_api 端口
Camera 固定值： 虚拟摄像头视频流（TCP） 将手机摄像头画面推送到云手
Port1 10006 机或远程客户端
Camera 固定值： 虚拟摄像头控制/辅助流（UDP） 用于低延迟交互或信令同
Port2 10007 步
非桥接模式：
配置项 填写值 功能说明
输入 IP 192.168.x.x 公网可以被访问的 ip
30000 + (index - 1) × 100 + 3 投屏画面推流端口 用于将手机屏幕
TCP Port （index 是实例位，例如 index=1，端 画面实时推送到客户端（如 PC 或
口为 30003） Web 播放器）
30000 + (index - 1) × 100 + 4
远程控制指令端口 接收鼠标点击、
UDP Port （index 是实例位，例如 index=1，端
滑动、按键等操作指令
口为 30004）
30000 + (index - 1) × 100 + 1
Image
（index 是实例位，例如 index=1，端 安卓 adk_api 端口
Port
口为 30001）
30000 + (index - 1) × 100 + 5 虚拟摄像头视频流（TCP） 将手机
Camera
（index 是实例位，例如 index=1，端 摄像头画面推送到云手机或远程客
Port1
口为 30005） 户端
30000 + (index - 1) × 100 + 6 index
Camera 虚拟摄像头控制/辅助流（UDP） 用
是实例位，例如 index=1，端口为
Port2 于低延迟交互或信令同步
30006）
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 3/66

## 第 4 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
🔧
基础概念
IP 和 Port 说明
📌
什么是 IP 和 Port？
IP 地址（如 192.168.30.2）：用来定位具体的设备或宿主机
Port 端口（如 9082、10008）：用来区分同一 IP 下的不同设备或服务
完整地址：IP:Port（如 192.168.30.2:10008）
📌
Q1 和 P1 是什么？
Q1：一种虚拟安卓设备型号，可创建 1-12 个（index 范围 1-12）
P1：另一种虚拟安卓设备型号，可创建 1-24 个（index 范围 1-24）
index：设备的编号，用于计算端口号
📌
IP 地址的区别
桥接模式：每个设备有独立的 IP
桥接模式网络拓扑：
┌───────────────┐
│ 宿主机 │
│ 192.168.30.1 │
└──────┬────────┘
│
├─────────┬─────────┬─────────┬─────────────┬
│ │ │ │ │
┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│ Q1 设备 1 │ │ Q1 设备 2 │ │ Q1 设备 3 │ │ ... Q1 设备 12 │
│ 192.168.30.2 │ │ 192.168.30.3 │ │ 192.168.30.4 │ │ 192.168.30.12 │
└─────────────┘ └─────────────┘ └─────────────┘ └──────────────┘
非桥接模式：所有设备共享宿主机 IP
非桥接模式网络拓扑：
┌───────────────┐
│ 宿主机 │
│ 192.168.30.2 │
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 4/66

## 第 5 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
└──────┬────────┘
│
├─────────┬─────────┬─────────┬─────────────┬
│ │ │ │ │
┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
│ Q1 设备 1 │ │ Q1 设备 2 │ │ Q1 设备 3 │ │ ... Q1 设备 12 │
│ 192.168.30.2 │ │ 192.168.30.2 │ │ 192.168.30.2 │ │ 192.168.30.2 │
└─────────────┘ └─────────────┘ └─────────────┘ └──────────────┘
📌
Port 端口详解
桥接模式的端口（所有设备固定值相同）：
功能 端口号 用途说明
ADB 端口 5555 用于 ADB 命令连接
安卓 API 端口 9082 用于调用本文档中的所有 HTTP API 接口
安卓 RPA 端口 9083 用于自动化操作和脚本控制
投屏端口 10000 用于设备屏幕投屏
控制端口 10001 用于设备远程控制
安卓摄像头 TCP 10006 用于摄像头视频流传输（TCP 协议）
安卓摄像头 UDP 10007 用于摄像头视频流传输（UDP 协议）
webrtc 端口（TCP） 10008 用于浏览器控制
webrtc 端口（UDP） 10008 用于浏览器控制（UDP 协议）
非桥接模式的端口（需要根据 index 计算,index 为安卓实例位）：
功能 计算公式 用途说明
ADB 端口 30000 + (index - 1) × 100 用于 ADB 命令连接
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 5/66

## 第 6 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
功能 计算公式 用途说明
30000 + (index - 1) × 100 用于调用本文档中的所有 HTTP
安卓 API 端口
+ 1 API 接口
30000 + (index - 1) × 100
安卓 RPA 端口 用于自动化操作和脚本控制
+ 2
30000 + (index - 1) × 100
投屏端口 用于设备屏幕投屏
+ 3
30000 + (index - 1) × 100
控制端口 用于设备远程控制
+ 4
30000 + (index - 1) × 100 用于摄像头视频流传输（TCP 协
安卓摄像头 TCP
+ 5 议）
30000+ (index - 1) × 100 用于摄像头视频流传输（UDP 协
安卓摄像头 UDP
+ 6 议）
webRTC 端口 30000 + (index - 1) × 100 用于 webRTC 视频流传输（TCP 协
（TCP） + 7 议）
webRTC 端口 30000 + (index - 1) × 100 用于 webRTC 视频流传输（UDP
（UDP） + 8 协议）
📌
非桥接模式端口列表
Q1 设备端口列表（index 1-12）：
实 摄像 摄像 webRTC web
ADB API RPA 投屏 控制
例 头 头 端口 端
端口 端口 端口 端口 端口
位 TCP UDP （TCP） （U
Q1-
30000 30001 30002 30003 30004 30005 30006 30007 300
1
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 6/66

## 第 7 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
实 摄像 摄像 webRTC web
ADB API RPA 投屏 控制
例 头 头 端口 端
端口 端口 端口 端口 端口
位 TCP UDP （TCP） （U
Q1-
30100 30101 30102 30103 30104 30105 30106 30107 301
2
Q1-
30200 30201 30202 30203 30204 30205 30206 30207 302
3
Q1-
30300 30301 30302 30303 30304 30305 30306 30307 303
4
Q1-
30400 30401 30402 30403 30404 30405 30406 30407 304
5
Q1-
30500 30501 30502 30503 30504 30505 30506 30507 305
6
Q1-
30600 30601 30602 30603 30604 30605 30606 30607 306
7
Q1-
30700 30701 30702 30703 30704 30705 30706 30707 307
8
Q1-
30800 30801 30802 30803 30804 30805 30806 30807 308
9
Q1-
30900 30901 30902 30903 30904 30905 30906 30907 309
10
Q1-
31000 31001 31002 31003 31004 31005 31006 31007 310
11
Q1-
31100 31101 31102 31103 31104 31105 31106 31107 311
12
P1 设备端口列表（index 1-24）：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 7/66

## 第 8 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
实 摄像 摄像 webRTC web
ADB API RPA 投屏 控制
例 头 头 端口 端
端口 端口 端口 端口 端口
位 TCP UDP （TCP） （UD
P1-
30000 30001 30002 30003 30004 30005 30006 30007 3000
1
P1-
30100 30101 30102 30103 30104 30105 30106 30107 3010
2
P1-
30200 30201 30202 30203 30204 30205 30206 30207 3020
3
P1-
30300 30301 30302 30303 30304 30305 30306 30307 3030
4
P1-
30400 30401 30402 30403 30404 30405 30406 30407 3040
5
P1-
30500 30501 30502 30503 30504 30505 30506 30507 3050
6
P1-
30600 30601 30602 30603 30604 30605 30606 30607 3060
7
P1-
30700 30701 30702 30703 30704 30705 30706 30707 3070
8
P1-
30800 30801 30802 30803 30804 30805 30806 30807 3080
9
P1-
30900 30901 30902 30903 30904 30905 30906 30907 3090
10
P1-
31000 31001 31002 31003 31004 31005 31006 31007 3100
11
P1-
31100 31101 31102 31103 31104 31105 31106 31107 3110
12
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 8/66

## 第 9 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
实 摄像 摄像 webRTC web
ADB API RPA 投屏 控制
例 头 头 端口 端
端口 端口 端口 端口 端口
位 TCP UDP （TCP） （UD
P1-
31200 31201 31202 31203 31204 31205 31206 31207 3120
13
P1-
31300 31301 31302 31303 31304 31305 31306 31307 3130
14
P1-
31400 31401 31402 31403 31404 31405 31406 31407 3140
15
P1-
31500 31501 31502 31503 31504 31505 31506 31507 3150
16
P1-
31600 31601 31602 31603 31604 31605 31606 31607 3160
17
P1-
31700 31701 31702 31703 31704 31705 31706 31707 3170
18
P1-
31800 31801 31802 31803 31804 31805 31806 31807 3180
19
P1-
31900 31901 31902 31903 31904 31905 31906 31907 3190
20
P1-
32000 32001 32002 32003 32004 32005 32006 32007 3200
21
P1-
32100 32101 32102 32103 32104 32105 32106 32107 3210
22
P1-
32200 32201 32202 32203 32204 32205 32206 32207 3220
23
P1-
32300 32301 32302 32303 32304 32305 32306 32307 3230
24
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 9/66

## 第 10 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
桥接模式 vs 非桥接模式
维度 桥接模式 非桥接模式（NAT）
设备直接接入物理网络，拥有独立 设备通过宿主转发网络，共享宿主
网络身份
IP IP
外部可访问
同一网络内的设备可直接访问 外部设备默认无法直接访问
性
配置复杂度 需和物理网络参数一致 自动适配宿主网络
使用场景 需要被外部设备访问 仅需要设备自己上网
工作原理详解：
桥接模式：设备直接连接到物理交换机/路由器，获取和宿主同网段的独立 IP（由物理网络的
DHCP 分配），网络数据直接在物理网络中传输。相当于在物理网络中"新增一个设备"。
非桥接模式：设备处于宿主创建的私有网络中，宿主作为"网关"转发数据。设备用私有 IP（如
192.168.122.xx），对外通信时由宿主把设备的请求"伪装"成自己的请求（NAT 地址转换），再
把响应转发给设备。
📋
通用说明
请求方式
所有 API 均使用 HTTP 协议，支持以下请求方式：
GET：用于查询和修改操作（大多数接口）
POST：用于文件上传和大数据传输
返回格式
所有 API 返回 JSON、file 格式数据，基本结构如下：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 10/66

## 第 11 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
成功响应：
{
"code": 200,
"msg": "ok",
"data": {} // 可选，根据接口而定
}
失败响应：
{
"code": 201,
"error": "错误原因"
}
或
{
"code": 202,
"reason": "失败原因"
}
状态码说明
状态码 含义 说明
200 成功 操作成功完成
201 通用错误 操作失败，查看 error 字段获取详细信息
202 操作失败 特定操作失败，查看 reason 字段获取详细信息
其他 未知错误 联系技术支持
编码说明
某些参数需要特殊编码处理：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 11/66

## 第 12 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
Base64 编码（用于应用列表等）：
import base64
import json
# 示例：隐藏应用列表
data = ["com.example.app1", "com.example.app2"]
json_str = json.dumps(data)
encoded = base64.urlsafe_b64encode(json_str.encode("utf-8")).decode("utf-8")
print(encoded) # 输出:
WyJjb20uZXhhbXBsZS5hcHAxIiwgImNvbS5leGFtcGxlLmFwcDIiXQ==
URL 编码（用于包含特殊字符的参数）：
from urllib.parse import quote
data = '{"device_id":"abc123"}'
encoded = quote(data)
print(encoded) # 输出: %7B%22device_id%22%3A%22abc123%22%7D
🔌
接口详解
1. 下载文件
功能说明：从设备下载指定文件到本地计算机
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/download?path={filepath}
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 12/66

## 第 13 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数名 必选 类型 说明
path 是 string 要下载的文件完整路径
参数详解：
path: 必须是文件的完整绝对路径
获取方式：
a. 使用"获取文件列表"接口查询文件路径
b. 或直接使用已知的文件路径
常见文件路径：
/sdcard/Download/file.apk（下载的 APK 文件）
/sdcard/DCIM/Camera/photo.jpg（相机照片）
/data/app/com.example/base.apk（已安装应用）
请求示例：
curl "http://192.168.99.108:10038/download?path=/sdcard/Download/1.jpg" -o
1.jpg
返回示例：
成功：返回文件的二进制数据，浏览器会自动下载
失败：
{
"code": 201,
"error": "文件不存在或无权限访问"
}
错误码：
错误码 说明
200 成功
其他 下载失败
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 13/66

## 第 14 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
注意事项：
文件下载采用流式传输，支持大文件
下载时会显示下载进度信息
下载完成后会自动保存到指定位置
如果本地文件已存在，需要先删除或重命名
某些系统文件可能需要特殊权限才能下载
建议使用绝对路径访问文件，以避免路径解析错误
2. 获取剪贴板内容
功能说明：获取设备剪贴板中的文本内容
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/clipboard
请求参数：
参数名 必选 类型 说明
ip 是 string ip
port 是 int port
请求示例：
curl "http://192.168.30.2:10008/clipboard"
返回示例：
成功：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 14/66

## 第 15 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
{
"code": 200,
"msg": "query success",
"data": {
"text": "123"
}
}
失败：
{
"code": 201,
"error": "异常原因"
}
{
"code":202,
"reason":"失败原因"
}
注意事项：
只能获取文本内容，不支持图片或其他格式
需要设备授予剪贴板访问权限
3. 设置剪贴板内容
功能说明：将文本内容设置到设备的剪贴板
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/clipboard
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 15/66

## 第 16 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数名 必选 类型 说明
cmd 是 int 固定值：2
text 是 string 要设置的文本内容
参数详解：
text: 可以是任意文本内容
如果包含特殊字符，需要进行 URL 编码
请求示例：
curl "http://192.168.30.2:10008/clipboard?cmd=2&text=123"
返回示例：
成功：
{
"code": 200,
"msg": "ok"
}
失败：
{
"code": 201,
"error": "异常原因"
}
{
"code": 202,
"error": "失败原因"
}
注意事项：
特殊字符需要进行 URL 编码
设置后立即生效，用户可以粘贴该内容
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 16/66

## 第 17 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
4. 查询 S5 代理状态
功能说明：查询设备的 S5 代理服务状态
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/proxy
请求示例：
curl "http://192.168.30.2:10008/proxy"
请求参数 无
返回参数：
参数名 类型 说明
code int 状态码
data object 返回数据对象
data.status string 查询结果
data.status Text string 提示信息
data.addr string 代理地址
data.type int 代理类型
返回示例：
成功：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 17/66

## 第 18 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
启动
{
"code": 200,
"msg": "query success",
"data": {
"status": 1,
"statusText": "已启动",
"addr": "socks5://test:123456@192.168.1.100:8080",
"type": 2
}
}
未启动
{
"code":200,
"msg":"query success",
"data":{"status":0,"statusText":"未启动"}
}
失败：
{
"code": 201,
"error": "查询失败"
}
返回参数说明：
code: 状态码（200 表示成功）
注意事项：
S5 代理是 SOCKS5 代理协议的实现
5. 设置 S5 代理
功能说明：启动或配置设备的 S5 代理服务
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 18/66

## 第 19 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求 URL：
http://{ip}:{port}/proxy?cmd=2
请求参数：
参数名 必选 类型 说明
cmd 是 int 固定值：2
port 是 int s5 服务器端口
usr 是 string s5 用户名
pwd 是 string s5 密码
type 否 int s5 域名模式 1:本地域名解析 2:服务端域名解析
参数详解：
port: s5 服务器端口
usr: s5 用户名
pwd: s5 密码
type: s5 域名模式(1:本地域名解析 2:服务端域名解析)
请求示例：
curl "http://192.168.30.2:10008/proxy?
cmd=2&type=2&ip=192.168.1.100&port=8080&usr=test&pwd=123456"
返回示例：
成功：
{
"code": 200,
"msg": "start success"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 19/66

## 第 20 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
注意事项：
代理配置必须正确，否则无法连接
设置后需要重启代理服务才能生效
6. 停止 S5 代理
功能说明：停止设备的 S5 代理服务
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/proxy?cmd=3
请求参数：
参数名 必选 类型 说明
cmd 是 int 固定值：3
请求示例：
curl "http://192.168.30.2:10008/proxy?cmd=3"
返回示例：
成功：
{
"code": 200,
"msg": "stop success"
}
注意事项：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 20/66

## 第 21 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
停止后代理服务将不可用
7. 设置 S5 域名过滤
功能说明：为 S5 代理设置域名过滤规则
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：POST
请求 URL：
http://{ip}:{port}/proxy?cmd=4
请求参数：
参数名 必选 类型 说明
cmd 是 int 固定值：4
参数详解：
domains: 可以使用逗号分隔的域名列表，或 JSON 数组格式
请求示例：
POST "http://192.168.30.2:10008/proxy?cmd=4"
body
[
"qq.com",
"baidu.com"
]
返回示例：
成功：
{
"code": 200,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 21/66

## 第 22 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"msg": "set success"
}
失败：
{
"code": 201,
"error": "设置失败"
}
注意事项：
在使用 S5 代理时，建议先检查代理服务器的可用性
域名过滤规则的变更会立即生效
如果需要临时禁用 S5 代理，可以使用停止 S5 代理接口
S5 代理的设置会影响所有网络请求的路由
8. 接收短信
功能说明：模拟接收短信消息
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：POST
请求 URL：
http://{ip}:{port}/sms
请求参数：
参数名 必选 类型 说明
cmd 是 int 固定值：4
address 是 string 发送者电话号码
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 22/66

## 第 23 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数名 必选 类型 说明
mbody 是 string 短信内容
scaddress 否 string 短信中心号码
参数详解：
address: 发送短信的电话号码
mbody: 短信的文本内容
scaddress: 短信中心号码
请求示例：
POST "http://192.168.30.2:10008/sms?cmd=4"
headers = {"Content-Type": "application/json"}
请求体
body = {
"address": "13800138000",
"body": "Hello, this is a test message.",
"scaddress": "+8613900000000"
}
返回示例：
成功：
{
"code": 200,
"msg": "add inbox success",
"data": { "status": 0 }
}
失败：
{
"code": 201,
"error": "接收失败"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 23/66

## 第 24 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
注意事项：
电话号码必须是有效的格式
短信内容支持特殊字符，但需要 URL 编码
9. 上传 Google 证书
功能说明：上传或更新 Google 服务的证书
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：POST
请求 URL：
http://{ip}:{port}/uploadkeybox
请求参数：
参数名 必选 类型 说明
file 是 file 证书文件（如.pem）
参数详解：
file: 上传 Google 证书文件（PEM 格式）
请求示例：
POST
"http://192.168.30.2:10008/uploadkeybox"
请求体
form_data 上传文件
{'fileToUpload': 文件}
返回示例：
成功：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 24/66

## 第 25 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
导入完成permissionabc
selinux123
失败：
导入失败，错误信息：
注意事项：
证书文件必须是有效的 PEM 格式
上传后需要重启设备才能生效
某些 Google 服务可能需要特定的证书
10. ADB 切换权限
功能说明：查询、开启、关闭当前 ADB 权限状态
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/adb
请求参数：
参数 必
类型 说明
名 选
操作命令：1: 查询权限状态；2: 开启 ADB root 权限；3: 关闭
cmd 是 string
ADB root 权限
接口说明:
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 25/66

## 第 26 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
操作 功能 说明
cmd=1 查询状态 返回当前 ADB 是否启用 ROOT 权限
cmd=2 开启 root 设置 persist.adbd.shell=0 并重启 adbd，允许 root 权限
cmd=2 关闭 root persist.adbd.shell=1 并重启 adbd，仅保留 shell 权限
请求示例：
查询权限状态
curl "http://192.168.30.2:10008/adb?"
开启ADB root权限
curl "http://192.168.99.108:10008/adb?cmd=2"
关闭ADB root权限
curl "http://192.168.99.108:10008/adb?cmd=3"
返回示例：
成功：
查询
{
"code": 200,
"msg": "query success",
"data": { "status": 0, "statusText": "open" }
}
开启权限
{
"code":200,
"msg":"open adb root success"
}
关闭权限
{
"code":200,
"msg":"close adb root success"
}
失败：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 26/66

## 第 27 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
{
"code": 202
"reason":"错误原因"
}
注意事项:
此功能依赖设备已 root 且系统支持 persist.adbd.shell 属性
修改后需重新连接 ADB 才能生效
11. 导出 app 信息
功能说明：导出已安装应用的信息
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/backrestore
请求参数：
参数名 必选 类型 说明
cmd 是 str backup
pkg 是 str 包名
saveto 是 str 导出文件路径
请求示例：
# 导出导出app信息
curl "http://192.168.30.2:10020/backrestore?
cmd=backup&pkg=com.ss.android.ugc.aweme&saveto=/sdcard/test.tar.gz"
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 27/66

## 第 28 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
返回示例：
成功：
{
"status": "success",
"message": "Backup completed successfully"
}
失败：
{
"status": "failed",
"message": "失败原因"
}
返回参数说明：
status: 状态码（success 表示成功）
message: 状态信息
注意事项：
返回所有已安装应用的基本信息
返回的信息包括包名、应用名称、版本等
可用于获取设备上所有应用的列表
12. 导入 app 信息
功能说明：导入应用信息到设备，导入 APP 信息不需要 pkg（应用包名）参数。
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/backrestore
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 28/66

## 第 29 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求参数：
参数名 必选 类型 说明
cmd 是 str recovery
backuppath 是 str 导入文件路径
导入 APP 信息不需要 pkg（应用包名）。
请求示例：
# 导入导出app信息
GET http://192.168.30.2:10020/backrestore?
cmd=recovery&backuppath=/sdcard/test.tar.gz
返回示例：
成功：
{
"status": "success",
"message": "Recovery completed successfully"
}
失败：
{
"status": "failed",
"message": "失败原因"
}
注意事项：
应用信息文件必须是有效的 JSON 格式
导入后需要重启安卓才能生效
13. 虚拟摄像头热启动
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 29/66

## 第 30 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
功能说明：热启动虚拟摄像头功能，无需重启设备
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/camera?cmd=start
请求参数：
参数 必 类
说明
名 选 型
cmd 是 str start,stop
rtmp 地址或者本地地址，首次使用需要传参，后续如果不传 path 参
path 否 str
数则使用上次的 path 参数
请求示例：
curl "http://192.168.30.2:10008/camera?cmd=start&path=/sdcard/Download/1.jpg"
返回示例：
成功：
{
"code": 200,
"msg": "ok"
}
失败：
{
"code": 202,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 30/66

## 第 31 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"reason": "错误原因"
}
注意事项：
热启动不需要重启设备
启动后虚拟摄像头立即可用
14. 后台保活
功能说明：为指定应用启用后台保活功能，防止应用被系统杀死
支持模式：仅 Android 14 支持
版本要求：镜像日期大于 20251217
请求方式：GET
请求 URL：
http://{ip}:{port}/background
请求参数：
必 类
参数名 说明
选 型
操作类型 ：查询=1 增加=2 删除=3 更新=4 更新接口说明：被保
cmd 是 str
活应用卸载和重新安装后需要调用
package 否 str 应用包名 ；cmd=2 和 3 需要
参数详解：
cmd: 操作类型
1：查询（查询所有保活应用）
2：增加（添加应用到保活列表）
3：删除（从保活列表删除应用）
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 31/66

## 第 32 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
4：更新（更新保活应用列表）
package: 当 cmd=2 或 3 时需要提供
被保活应用卸载和重新安装后需要调用更新接口
请求示例：
查询保活应用：
curl "http://192.168.99.149:10026/background?cmd=1"
添加应用到保活列表：
curl "http://192.168.99.149:10026/background?
cmd=2&package=com.ss.android.ugc.aweme"
删除应用：
curl "http://192.168.99.149:10026/background?
cmd=3&package=com.ss.android.ugc.aweme"
返回示例：
cmd=1 (查询)：
{
"code": 200,
"msg": "获取成功",
"data": {
"apps": ["com.ss.android.ugc.aweme"]
}
}
cmd=2 (添加)：
{
"code": 200,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 32/66

## 第 33 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"msg": "添加成功"
}
cmd=3 (删除)：
{
"code": 200,
"msg": "移除成功"
}
cmd=4 (更新)：
{
"code": 200,
"msg": "更新成功",
"data": {
"apps": ["com.ss.android.ugc.aweme"]
}
}
失败：
{
"code": 202,
"reason": "应用已在保护列表中"
}
错误返回xxx为java层报错信息，不固定：
{
"code":201,
"error":"xxxxx"
}
注意事项：
目前只支持安卓 14 版本
版本要求：镜像日期大于 20251217
被保活应用卸载和重新安装后需要调用更新接口
某些系统应用可能无法保活
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 33/66

## 第 34 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
15. 屏蔽按键
功能说明：屏蔽或启用设备的物理按键
支持模式：仅 Android14 支持
请求方式：GET
请求 URL：
http://{ip}:{port}/disablekey?value=1
请求参数：
参数名 必选 类型 说明
value 否 str 1 为开启 0 为关闭
参数详解：
value: 屏蔽状态
1：开启屏蔽
0：关闭屏蔽
请求示例：
开启屏蔽：
curl "http://192.168.99.108:10017/disablekey?value=1"
关闭屏蔽：
curl "http://192.168.99.108:10017/disablekey?value=0"
返回示例：
成功：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 34/66

## 第 35 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
{
"code": 200,
"msg": "ok"
}
失败：
错误返回xxx为java层报错信息，不固定
{
"code": 201,
"error": "Java层报错信息"
}
注意事项：
屏蔽后物理按键将不可用
16. 批量安装 apks/xapk 分包
功能说明：用于批量安装 Android apks/xapk 文件的接口，支持通过 ZIP 压缩包上传多个
apks/xapk 文件并自动安装
支持模式：安卓 10、12（从 v22.9.2 开始）、14 都支持
请求方式：POST
请求 URL：
http://{ip}:{port}/installapks
请求参数：
参数名 必选 类型 说明
file 是 file 包含多个 apks/xapk 文件的 ZIP 压缩包
参数详解：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 35/66

## 第 36 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
file: 上传包含多个 apks/xapk 文件的 ZIP 压缩包
步骤：
a. 将多个 apks/xapk 文件放入一个文件夹
b. 将文件夹压缩为 ZIP 文件
c. 上传 ZIP 文件
请求示例：
使用 curl 命令：
curl -X POST \
"http://192.168.99.108:10017/installapks" \
-H "Content-Type: multipart/form-data" \
-F "file=@/path/to/your/apks.zip"
文件上传示例:
HTML 代码:
<!DOCTYPE html>
<html>
<head>
<title>文件上传示例</title>
</head>
<body>
<!--请将"http://ip:9082"替换为实际IP和端口,桥接安卓的端口是9082，非桥接请查
看本文档最上面”非桥接模式的端口”表格里对应实例位的安卓
API 端口-->
<h1>文件上传示例</h1>
<form
action="http://ip:9082/installapks"
method="post"
enctype="multipart/form-data"
>
<label for="installer">Installer 参数:</label>
<input
type="text"
id="installer"
name="installer"
value="com.android.vending"
/>
<br /><br />
<input type="file" name="fileToUpload" id="fileToUpload" />
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 36/66

## 第 37 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
<input type="submit" value="上传" name="submit" />
</form>
</body>
</html>
apks/xapk 压缩包示例如下：
返回示例：
成功 (HTTP 200)：
全部安装完成
失败：
错误返回xxx为java层报错信息，不固定
{
"code": 202,
"error": "Java层报错信息"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 37/66

## 第 38 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
注意事项：
支持安卓 10、12（从 v22.9.2 开始）、14
ZIP 文件必须包含有效的 APK 文件
安装过程可能需要几分钟，请耐心等待
如果某个 APK 安装失败，其他 APK 仍会继续安装
17. 版本查询
功能说明：查询设备或服务的版本信息
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/queryversion
请求参数：无
请求示例：
curl "http://192.168.30.2:10008/queryversion"
返回示例：
成功：
{
"code": 200,
"msg": "3"
}
失败：
{
"code": 202,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 38/66

## 第 39 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"reason": "失败原因"
}
注意事项：
版本信息可能包含多个字段
不同设备或服务可能返回不同的版本信息
18. 截图功能
功能说明：获取设备屏幕截图
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/snapshot
请求参数：
参数名 必选 类型 说明
type 否 string 截图类型
quality 否 int 截图质量（1-100）
请求示例：
curl "http://192.168.30.2:10008/snapshot"
curl "http://192.168.30.2:10008/snapshot?quality=80"
返回示例：
成功：返回图片二进制数据
失败：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 39/66

## 第 40 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
{
"code": 201,
"error": "截图失败"
}
注意事项：
截图需要设备屏幕处于唤醒状态
高分辨率截图可能需要较长时间
截图大小可能有限制
19. 自动点击
功能说明：自动点击
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/autoclick
请求参数：
必选 类型 说明
点击动作，可选值：touchdown 按 touchup 放 touchmove 移动 tap 点
action string
击 keypress 根据按键键码点击对应按键
id int 点击事件编号 1-10 多指触控
x int x 坐标
y int y 坐标
code int 按键键码，action 为 keypress 时必填, 点击按键键码对应的按键
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 40/66

## 第 41 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求示例：
按下
curl "http://192.168.99.108:10038/autoclick?action=touchdown&id=1&x=100&y=100"
放开
curl "http://192.168.99.108:10038/autoclick?action=touchup&id=1&x=100&y=100"
移动
curl "http://192.168.99.108:10038/autoclick?action=touchmove&id=1&x=100&y=100"
点击
curl "http://192.168.99.108:10038/autoclick?action=tap&id=1&x=100&y=100"
根据按键键码点击对应按键
curl "http://192.168.99.108:10038/autoclick?action=keypress&id=1&code=4"
返回示例：
成功：
{
"code": 200,
"msg": "ok"
}
错误原因：
{
"code": 201,
"error": "错误原因"
}
按键键码查询 code 参数部分键码参考 3 主菜单键 4 返回键 5 联系人
20. 文件上传
功能说明：文件上传
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：POST
请求 URL：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 41/66

## 第 42 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
http://{ip}:{port}/upload
请求参数：
参数名 必选 类型 说明
file 是 file 需要上传的文件（如.txt）
请求示例：
curl -X POST "http://192.168.99.108:10038/upload" -H "Content-Type:
multipart/form-data" -F "file=@./1.txt"
html 实例
<!DOCTYPE html>
<html>
<head>
<title>文件上传示例</title>
</head>
<body>
<h1>文件上传示例</h1>
<form
action="http://10.10.0.117:10008/upload"
method="post"
enctype="multipart/form-data"
>
<input type="file" name="fileToUpload" id="fileToUpload" />
<input type="submit" value="上传" name="submit" />
</form>
</body>
</html>
返回示例：
成功：
文件上传完成！
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 42/66

## 第 43 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
失败：
{
"code": 202,
"reason": "失败原因"
}
另一种文件上传方式：
请求方式：GET
请求 URL：
http://{ip}:{port}/?task=upload&file={}
请求参数：
参数名 必选 类型 说明
file 是 file 要上传的文件
task 是 string 任务类型，固定为 upload
请求示例：
curl "http://192.168.99.108:10026/?
task=upload&file=http://192.168.99.136:7878/%E6%8A%96%E9%9F%B3.apk"
返回示例：
成功：
{
"code": 200,
"msg": "ok"
}
失败：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 43/66

## 第 44 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
{
"code": 202,
"reason": "失败原因"
}
两种接口请求区别:
维度 接口 1（POST 方式） 接口 2（GET 方式）
请求方式 POST GET
参数传递方 file 是文件 URL（通过 URL 参数传
file 是本地文件 （通过请求体上传）
式 递）
多一个 task 参数（固定值
必选参数 仅需 file 参数
upload）
成功返回文本“文件上传完成!”，失败返 JSON 格式（code：
返回格式
回 JSON 200+msg：“ok”
注意事项：
接口一是标准文件上传：通过 multipart/form-data 格式直接将本地文件（如本地 APK）上
传到接口；适用场景：上传本地存储的文件，是常规的文件上传方式。
接口二是文件 URL 上传：通过 URL 参数传递文件 URL，接口会自动下载文件并上传；适用
场景：上传远程存储的文件，如文件服务器上的文件，或需要先下载再上传。
21. 容器信息
功能说明：获取容器信息
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/info
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 44/66

## 第 45 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求参数： 无
请求示例：
curl "http://192.168.99.108:10026/info"
返回示例：
成功：
{
"code": 200,
"msg": "ok",
"data": {
"hostIp": "-",
"instance": "8",
"name": "p738c384c1581ad24c3fcf199684f5f5_8",
"buildTime": "1766829184"
}
}
失败：
{
"code": 202,
"reason": "失败原因"
}
22. 通话记录
功能说明：获取容器通话记录
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/callog
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 45/66

## 第 46 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求参数：
参数名 类型 是否必选 说明
number string 是 要模拟的电话号码（如 "13800138000"）
type int 否 通话类型：1 呼出 2 接收 3 错过（默认）
date string 否 时间戳（毫秒），默认当前时间
duration int 否 通话时长（秒），默认 0
presentation int 否 显示方式，默认 1
subscription_id int 否 SIM 卡 ID，默认 0
is_read int 否 是否已读，默认 1
new int 否 是否新消息，默认 1
features int 否 特性标志，默认 0
请求示例：
curl "http://192.168.30.2:10008/callog?number=10086&type=2"
返回示例：
成功：
{
"code": 200,
"msg": "query success"
}
失败：
{
"code": 202,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 46/66

## 第 47 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"reason": "失败原因"
}
23. 刷新定位
功能说明：根据 ip 刷新定位
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/task
请求参数： 无
请求示例：
curl "http://192.168.99.108:10026/task"
返回示例：
成功：
{
"code": 200
}
失败：
{
"code": 202,
"reason": "失败原因"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 47/66

## 第 48 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
24. 谷歌 id
功能说明：获取容器谷歌 id
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
接口路径：/googleid（需与 Handler 注册路径一致）
请求方式：GET
请求 URL：
http://{ip}:{port}/adid
请求参数：
参数 是否必
类型 说明
名 选
操作指令：1 - 自定义设置谷歌 ID（需传 adid 参数）2 - 生成
cmd string 是
随机谷歌 ID 默认值：1
adid string 是 仅 cmd=1 时必选，需设置的谷歌 ID 值
请求示例：
curl "http://192.168.99.108:10026/adid?cmd=1&adid=my_adid"
返回示例：
成功：
{
"succ": true,
"msg": "generate random adid success",
"data": {
"adid": "my_adid"
}
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 48/66

## 第 49 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
失败：
{
"succ": false,
"msg": "cmd err"
}
25. 安装面具
功能说明：安装面具（安装面具之后需要重启）
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/modulemgr?cmd=install&moduler={}
请求参数：
参数 是否必
类型 说明
名 选
操作指令：check - 检查模块状态；install - 安装模块 ；
cmd string 是
uninstall - 卸载模块
adid string 是 面具名称
请求参数：
module 参数值 对应模块 说明
magisk Magisk 模块 安卓系统的 root 权限管理工具
gms GMS 模块 谷歌移动服务（Google Mobile Services）
响应规则：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 49/66

## 第 50 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
若模块已安装：响应体 succ 字段返回"1"；
若模块未安装：响应体 succ 字段返回"0"；
若传非支持的模块类型：响应体返回"不支持的模块类型"，succ 为 false。
请求示例：
#以gms为例，检查面具状态
curl "http://192.168.99.108:10026/modulemgr?cmd=check&module=gms"
#安装面具
curl "http://192.168.99.108:10026/modulemgr?cmd=install&module=gms"
#卸载面具
curl "http://192.168.99.108:10026/modulemgr?cmd=uninstall&module=gms"
返回示例：
成功：
检查面具是否安装，如果安装了返回结果：
{
"code":200,
"msg":"1"
}
检查面具是否安装，如果没有安装返回结果：
{
"code":200,
"msg":"0"
}
安装成功：
{
"code":200,
"msg":"OK"
}
失败：
安装面具失败：
{
"code": 201,
"msg": "Error"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 50/66

## 第 51 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
注意事项:
安装面具后需要重启
26. 添加联系人
功能说明：添加联系人
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
接口路径：/addcontact（需与 Handler 注册路径一致）
请求方式：GET
请求 URL：
http://{ip}:{port}/addcontact？data=[]
请求参数：
参数 是否必
类型 说明
名 选
JSON 字符 联系人列表，数组内每个对象需包含：- user：联系人姓
data 是
串 名- tel：联系电话
请求示例：
GET
"http://192.168.99.108:10035/addcontact?data=[{"user":"张
三","tel":"13800138000"},{"user":"李四","tel":"13900139000"}]"
返回示例：
成功：
{
"code": 200,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 51/66

## 第 52 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"msg": "OK"
}
失败：
{
"code": 201,
"error": "org.json.JSONException: Unterminated string at character 59 of
[{\"user\":\"张三\",\"tel\":\"13800138000\"},{\"user\":\"李四
\",\"tel\":\"1390"
}
27. webrtc 播放器
功能说明：调用 webrtc 的播放器
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
调用方法:
下载播放器,将压缩包解压到本地目录，下载地址：webplayer.zip
打开浏览器，拼接完整 URL
确保文件本地目录地址正确
检查参数是否正确
成功后即可观看 WebRTC 视频流
请求 URL：
webplayer/play.html?shost={ip}&sport={webrtc_port}&q=1&v=h264&rtc_i=
{ip}&rtc_p={webrtc_port}
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 52/66

## 第 53 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数名 是否必选 类型 说明
shost 是 string WebRTC 流媒体服务器主机地址（如 192.168.99.108）
sport 是 string WebRTC 流媒体服务器端口（TCP）（如 31207）
q 是 string 视频质量参数 (0=低 1=高)
v 是 string 视频编码格式（如 h264）
rtc_j 是 string RTC 服务端 IP（与 shost 一致，用于建立点对点连接）
rtc_p 是 string WebRTC 端口（UDP）（如 31208）
请求示例：
GET
"./webplayer/play.html?
shost=192.168.99.108&sport=31207&q=1&v=h264&rtc_i=192.168.99.108&rtc_p=31208"
返回示例：
成功：
成功响应（页面加载完成）
失败：
失败响应（页面加载失败）
28. 获取后台允许 root 授权的 app 列表
功能说明：获取当前后台配置中允许授予 Root 权限的应用包名列表。
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 53/66

## 第 54 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求 URL：
http://{ip}:{port}/modifydev?cmd=10&action=list
请求参数：
参数名 是否必选 类型 说明
cmd 是 string 固定值：10
action 是 string 固定值：list
请求示例：
GET
"http://192.168.99.108:31401/modifydev?cmd=10&action=list"
返回示例：
成功：
{
"code": 200,
"msg": "获取成功",
"data": { "apps": ["com.ss.android.ugc.aweme"] }
}
查询列表：老版本未支持的时候提示
{
"code":202,
"reason":"not find package:null"
}
29. 指定包名是否允许 root
功能说明：为指定包名的应用开启 ROOT 权限，安卓里面先要安装对应的 apk。
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 54/66

## 第 55 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
请求方式：GET
请求 URL：
http://{ip}:{port}/modifydev?cmd=10&pkg={package}&root=true
请求参数：
参数名 是否必选 类型 说明
cmd 是 string 固定值：10
pkg 是 string 应用包名（如抖音：com.ss.android.ugc.aweme）
action 是 string 固定值 true，表示允许 root
请求示例：
GET
"http://192.168.99.108:31401/modifydev?
cmd=10&pkg=com.ss.android.ugc.aweme&root=true"
返回示例：
成功：
{
"code": 200,
"msg": "OK"
}
失败：
找不到包名
{
"code":202,
"reason":"not find package:com.ss.android.ugc.awemenull"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 55/66

## 第 56 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
30. 设置虚拟摄像头源和类型
功能说明：配置虚拟摄像头的视频源类型及地址（支持图像、视频文件、RTMP 流、WebRTC、
物理摄像头等）。
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
http://{ip}:{port}/modifydev?cmd=4&type={type}&path={path}&resolution=
{resolution}
请求参数：
是
否
参数名 类型 说明
必
选
cmd 是 string 固定值：4
视频源类型，可选值：image、video、webrtc、rtmp、
type 是 string
camera
对应资源路径或 URL:1.image/video：本地文件路径（如
/sdcard/test.jpg） 2.rtmp/webrtc：流地址（如
path 是 string
rtmp://server/live） 3.camera：固定值null（实际由魔云互
联接管设备物理摄像头）
分辨率预设：1 = 自动（默认）;2 = 1920x1080@30;3 =
resolution 否 int
1280x720@30
请求示例：
GET
设置物理摄像头：
"http://192.168.99.108:31401/modifydev?cmd=4&type=camera&path=null "
设置视频video：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 56/66

## 第 57 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"http://192.168.99.108:31401/modifydev?
cmd=4&type=video&path=/Dowload/11111.mp4&resolution=1 "
仅修改分辨率为 720P（不换源）:
"http://192.168.99.108:31401/modifydev?cmd=4&resolution=3 "
返回示例：
成功：
{
"code": 200,
"msg": "OK"
}
失败：
{
"code":202,
"reason":"错误原因"
}
已知错误原因列表：type is not find:"+type
path is empty
image not exist（image类型）
注意事项:
如果只传 resolution 而不传 type 和 path，系统将仅修改当前视频流的分辨率，不会切换源
当 type=camera（物理摄像头）时，需要配合「魔云互联」使用。
31. 获取 APP 开机启动列表
功能说明：获取当前已配置为开机启动的应用列表.
🌉 🔗
支持模式： 桥接模式 | 非桥接模式
请求方式：GET
请求 URL：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 57/66

## 第 58 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
http://{ip}:{port}/appbootstart?cmd=1
请求参数：
参数名 是否必选 类型 说明
cmd 是 int cmd=1：获取当前已配置为开机启动的应用列表
请求示例：
GET：
"http://192.168.99.182:30301/appbootstart?cmd=1"
返回示例：
成功：
{
"code": 200,
"msg": "query success",
"data": { "pkg": ["cn.test", "android.ttt"] }
}
32. 设置指定 APP 开机启动
功能说明：设置指定应用是否允许在系统启动时自动运行。
请求方式：GET
请求 URL：
http://{ip}:{port}/appbootstart?cmd=2
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 58/66

## 第 59 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数 是否必 类
说明
名 选 型
cmd=2：设置一组应用为开机启动（需通过 POST 提交 JSON
cmd 是 int
数组）
body 是 list APP数组
请求示例：
POST
curl "http://127.0.0.1:9082/appbootstart?cmd=2" -X POST -H "Content-Type:
application/json" -d '["cn.test", "android.ttt"]'
返回示例：
成功：
{
"code": 200,
"msg": "set success"
}
失败：
{
"code": 201,
"error": "失败原因"
}
33. IP定位
功能说明：设置设备语言或IP，同时会自动更新相关的区域设置和系统环境。
请求方式：GET
请求 URL：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 59/66

## 第 60 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
http://{ip}:{port}/modifydev?cmd=11
请求参数：
是否必
参数名 类型 说明
选
cmd 是 string 固定值：11
语言代码(zh 中文/en 英语/fr 法语/th 泰国/vi 越南/ja 日
launage 否 string
本/ko 韩国/lo 老挝/in 印尼)
ip 否 string 用户IP，用于确定地理位置相关的设置
请求示例：
# 设置语言为英语（美国）
GET
"http://192.168.99.182:30301/modifydev?cmd=11&launage=en"
# 设置IP为23.247.138.215
GET
"http://192.168.99.182:30301/modifydev?cmd=11&ip=23.247.138.215"
返回示例：
成功：
{
"code": 200,
"msg": "OK"
}
失败：
{
"code": 201,
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 60/66

## 第 61 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
"error": "异常原因"
}
错误码：
错误码 说明
200 成功
注意事项：
1.语言设置会影响系统的显示语言、键盘输入法、时间格式等
2.设置语言后需要等待几秒钟才能完全生效
3.某些应用可能需要重启才能应用新的语言设置
4.建议在设置语言后检查系统语言是否已正确更新
5.支持的语言代码遵循ISO 639-1标准和ISO 3166-1标准的组合
6.如果设置了user_ip，系统会根据IP自动调整相关的区域设置
34. 设置语言和国家
功能说明：设置设备语言和国家。
请求方式：GET
请求 URL：
http://{ip}:{port}/modifydev?cmd=13
请求参数：
参数名 是否必选 类型 说明
cmd 是 string 固定值：13
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 61/66

## 第 62 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
参数名 是否必选 类型 说明
language 是 string 语言代码
country 是 string 国家代码
请求示例：
GET
"http://192.168.99.182:30301/modifydev?cmd=13&language=zh&country=US"
常见的国家和语言 字典表 国家=>语言
'GR'=>'el','NL'=>'nl','BE'=>'de','FR'=>'fr','MC'=>'fr','AD'=>'ca','ES'=>'eu','HU
'CZ'=>'cs','SK'=>'sk','AT'=>'en','GB'=>'cy','DK'=>'en','SE'=>'se','NO'=>'nn','FI
'GI'=>'en','PT'=>'pt','LU'=>'lb','IE'=>'en','IS'=>'is','AL'=>'sq','MT'=>'en','CY
'MQ'=>'fr','BB'=>'en','AG'=>'en','KY'=>'en','VG'=>'en','BM'=>'en','GD'=>'en','MS
'AE'=>'ar','PS'=>'ar','BH'=>'ar','QA'=>'ar','MN'=>'mn','NP'=>'ne','AE'=>'ar','AE
'CN'=>'zh','CN'=>'zh','TW'=>'zh','KP'=>'ko','BD'=>'bn','MY'=>'en','AU'=>'en','ID
 
返回示例：
成功：
{
"code": 200,
"msg": "OK"
}
失败：
{
"code": 202,
"reason": "失败原因"
}
{
"code": 201,
"reason": "异常原因"
}
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 62/66

## 第 63 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
📚
常见问题解答
Q1: 如何获取应用包名？
A: 有以下几种方式：
1. 在安卓设备上，进入"设置" > "应用" > 选择要查看的应用，查看"应用详情"
2. 使用 ADB 命令：adb shell pm list packages
3. 使用本 API 的"导出 app 信息"接口获取
4. 常见应用包名：
com.android.chrome（Chrome 浏览器）
com.tencent.mm（微信）
com.sina.weibo（新浪微博）
Q2: 如何获取 IP 和 Port？
A: 在 MYTOS 管理界面或设备信息页面查看。通常：
IP 是 192.168.x.x 格式
Port 是 10008 或 10009
不同设备实例的端口可能不同
Q3: 如何进行 Base64 编码？
A: Python 示例：
import base64
import json
data = ["com.example.app1", "com.example.app2"]
json_str = json.dumps(data)
encoded = base64.urlsafe_b64encode(json_str.encode("utf-8")).decode("utf-8")
print(encoded)
Q4: 如何进行 URL 编码？
A: Python 示例：
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 63/66

## 第 64 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
from urllib.parse import quote
data = '{"device_id":"abc123"}'
encoded = quote(data)
print(encoded)
Q5: 常见文件路径有哪些？
A: 安卓常见目录路径：
/sdcard：SD 卡根目录（存储用户文件）
/data：系统数据目录
/system：系统文件目录
/data/app：已安装应用目录
/sdcard/Download：下载文件目录
/sdcard/DCIM：相机照片目录
Q6: 桥接模式和非桥接模式有什么区别？
A:
桥接模式：设备直接接入物理网络，拥有独立 IP，可被同一网络内的其他设备直接访问
非桥接模式（NAT）：设备通过宿主转发网络，共享宿主 IP，外部设备默认无法直接访问
Q7: 如何处理 API 返回的错误？
A:
1. 检查返回的 code 字段
2. 查看 error 或 reason 字段获取详细错误信息
3. 常见错误：
应用包名不存在 → 检查包名是否正确
权限被拒绝 → 检查设备是否支持该操作
网络超时 → 检查网络连接是否正常
Q8: 某个接口返回"不支持"或"未实现"，怎么办？
A:
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 64/66

## 第 65 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
1. 检查设备的固件版本是否满足要求
2. 某些接口只支持特定的安卓版本（如 Q14、P14 等）
3. 查看接口的"版本要求"部分
4. 如果确实不支持，可以联系技术支持
📝
文档更新历史
日期 更新内容
2026-01-
新增接口：IP定位、设置语言和国家
30
2026-01-
修改批量安装 apks/xapk 分包接口
26
2026-01-
新增接口：获取获取 APP 开机启动列表、设置指定 APP 开机启动
22
2026-01- 新增接口：获取后台允许 root 授权的 app 列表、指定包名是否允许 root、设
21 置虚拟摄像头源和类型
2026-01-
更新端口计算公式，新增投屏、控制等端口
14
2026-01-
新增接口：批量安装 apks/xapk 分包
08
2026-01-
新增接口：屏蔽按键
07
2026-01-
新增接口：后台保活
06
📞
技术支持
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 65/66

## 第 66 页
2026/2/2 15:21 MYTOS API 接⼝⽂档 | 魔云腾
如有问题或建议，请联系：
官方文档
公司网站
技术支持：support@moyunteng.com
文档版本: v3 | 最后更新: 2026-01-30 | 作者: 武汉魔云腾科技有限公司
Last updated on Jan 30, 2026
https://dev.moyunteng.com/docs/NewMYTOS/MYT_ANDROID_API 66/66

