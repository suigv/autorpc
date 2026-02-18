# 盒子内SDK API 开发文档 _ 魔云腾

*来源: 盒子内SDK API 开发文档 _ 魔云腾.pdf*

---

## 第 1 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
盒子内SDK API 开发文档
盒子内SDK API 开发文档
MYT-SDK API 接口文档
更新日期 2026-1-29
📌
接口说明 #
访问地址: http://{主机IP}:8000/swagger
主机IP：设备的网络IP地址（例如：192.168.99.108）
端口：固定为 8000
协议：HTTP
响应格式：所有接口统一返回JSON格式
{
"code": 0,
"message": "ok",
"data": { ... }
}
字段 类型 说明
code int 状态码，0表示成功，非0表示失败
message string 状态信息
data object 返回数据
📚
接口目录
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 1/89

## 第 2 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
1. 基本信息
2. 云机操作
3. 云机备份
4. 终端连接
5. myt_bridge网卡管理
6. 魔云腾VPC
7. 本地机型数据管理
8. 接口认证
9. 服务管理
一、基本信息
1. 获取API版本信息
功能说明：获取当前API版本信息
请求方式：GET
请求URL：
http://{主机IP}:8000/info
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/info"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"latestVersion": 110,
"currentVersion": 108
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 2/89

## 第 3 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
}
}
返回字段说明：
字段 类型 说明
latestVersion int 线上最新版本号
currentVersion int 当前本地版本号
失败返回：
{
"code": 500,
"message": "获取版本信息失败",
"data": null
}
注意事项：
当 currentVersion < latestVersion 时，建议更新SDK
2. 获取设备基本信息
功能说明：获取当前设备的硬件和系统信息
请求方式：GET
请求URL：
http://{主机IP}:8000/info/device
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/info/device"
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 3/89

## 第 4 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"ip": "192.168.99.108",
"ip_1": "192.168.100.108",
"hwaddr": "AA:BB:CC:DD:EE:FF",
"hwaddr_1": "AA:BB:CC:DD:EE:F1",
"cputemp": 45,
"cpuload": "1.5",
"memtotal": "8GB",
"memuse": "4.2GB",
"mmctotal": "256GB",
"mmcuse": "120GB",
"version": "v1.1.0",
"deviceId": "MYT-P1-001",
"model": "P1",
"speed": "1000Mbps",
"mmcread": "150MB/s",
"mmcwrite": "120MB/s",
"sysuptime": "10天5小时",
"mmcmodel": "Samsung EVO",
"mmctemp": "38",
"network4g": "未连接",
"netWork_eth0": "已连接"
}
}
返回字段说明：
字段 类型 说明
ip string 网口IP
ip_1 string 网口1的IP
hwaddr string MAC地址
hwaddr_1 string MAC1地址
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 4/89

## 第 5 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
字段 类型 说明
cputemp int CPU温度
cpuload string CPU负载
memtotal string 内存总大小
memuse string 内存已使用大小
mmctotal string 磁盘总大小
mmcuse string 磁盘已使用大小
version string 固件版本
deviceId string 设备ID
model string 型号版本
speed string 网口速率
mmcread string 磁盘读取量
mmcwrite string 磁盘写入量
sysuptime string 设备运行时间
mmcmodel string 磁盘型号
mmctemp string 磁盘温度
network4g string 4G网卡状态
netWork_eth0 string ETH0网卡状态
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 5/89

## 第 6 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "获取设备信息失败",
"data": null
}
二、云机操作
1. 获取安卓云机列表
功能说明：获取设备上所有安卓云机容器列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android
请求参数：
参数名 必选 类型 说明
name 否 string 根据云机名过滤
running 否 bool 根据云机是否运行过滤，false查询所有
indexNum 否 int 根据云机实例位序号过滤(0-24)
请求示例：
# 获取所有云机
curl "http://192.168.99.108:8000/android"
# 根据名称过滤
curl "http://192.168.99.108:8000/android?name=test"
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 6/89

## 第 7 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
# 只获取运行中的云机
curl "http://192.168.99.108:8000/android?running=true"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 2,
"list": [
{
"id": "abc123def456",
"name": "android-01",
"status": "running",
"indexNum": 1,
"dataPath": "/myt/data/android-01",
"modelPath": "/myt/model/android-01",
"image": "registry.example.com/android:v12",
"ip": "192.168.100.101",
"networkName": "myt_bridge",
"portBindings": {},
"dns": "223.5.5.5",
"doboxFps": "60",
"doboxWidth": "1080",
"doboxHeight": "1920",
"doboxDpi": "480",
"mgenable": "0",
"gmsenable": "0",
"s5User": "",
"s5Password": "",
"s5IP": "",
"s5Port": "",
"s5Type": "0",
"created": "2024-01-15 10:30:00",
"started": "2024-01-15 10:31:00",
"finished": "",
"customBinds": [],
"PINCode": ""
}
]
}
}
返回字段说明：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 7/89

## 第 8 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
字段 类型 说明
id string 云机容器ID
name string 云机名称
status string 状态(running/stopped)
indexNum int 云机实例位序号
dataPath string 云机Data文件在设备里的路径
modelPath string 云机机型文件在设备里的路径
image string 云机所用的镜像
ip string 云机局域网IP
networkName string 容器网卡名称
dns string 云机DNS
doboxFps string 云机FPS
doboxWidth string 云机分辨率的宽
doboxHeight string 云机分辨率的高
doboxDpi string 云机DPI
mgenable string magisk开关，0-关，1-开
gmsenable string gms开关，0-关，1-开
s5User string s5代理用户名
s5Password string s5代理密码
s5IP string s5代理IP
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 8/89

## 第 9 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
字段 类型 说明
s5Port string s5代理端口
s5Type string 代理类型，0-不开启，1-本地域名解析，2-服务器域名解析
created string 云机容器创建时间
started string 云机容器上次开启时间
finished string 云机容器上次关闭时间
customBinds array 自定义文件映射
PINCode string 自定义屏幕锁屏密码
失败返回：
{
"code": 500,
"message": "获取云机列表失败",
"data": null
}
2. 创建安卓云机
功能说明：创建一个新的安卓云机容器
请求方式：POST
请求URL：
http://{主机IP}:8000/android
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 9/89

## 第 10 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
name 是 string 云机名称
imageUrl 是 string 镜像完整地址
dns 是 string 云机DNS，例如223.5.5.5
modelId 否 string 线上机型ID
modelName 否 string 线上机型名称
LocalModel 否 string 本地机型名称
modelStatic 否 string 本地静态机型名称(优先级最高)
indexNum 否 int 实例序号，P1范围1-24，Q1范围1-12，传0自动分配
sandboxSize 否 string 沙盒大小，例如16GB，32GB
offset 否 string 云机的开机时间
doboxFps 否 string 云机FPS
doboxWidth 否 string 云机分辨率的宽
doboxHeight 否 string 云机分辨率的高
doboxDpi 否 string 云机DPI
network 否 object 独立IP设置
start 否 bool 创建完成是否开机，默认true
mgenable 否 string magisk开关，0-关，1-开，默认0
gmsenable 否 string gms开关，0-关，1-开，默认0
latitude 否 float 纬度
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 10/89

## 第 11 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
longitude 否 float 经度
countryCode 否 string 国家代码，例如CN，US
portMappings 否 array 自定义端口映射
s5User 否 string s5代理用户名
s5Password 否 string s5代理密码
s5IP 否 string s5代理IP
s5Port 否 string s5代理端口
s5Type 否 string 代理类型，0-不开启，1-tun2socks，2-tun2proxy
mytBridgeName 否 string myt_bridge网卡名
customBinds 否 array 自定义文件映射
PINCode 否 string 屏幕锁屏密码，4-8位数字
network对象结构：
字段 类型 说明
gw string 网关，例如192.168.100.1
ip string 云机要设置的IP
subnet string 掩码，例如192.168.100.0/24
portMappings数组元素结构：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 11/89

## 第 12 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
字段 类型 说明
containerPort int 容器内端口
hostPort int 主机端口
hostIP string 主机IP
protocol string 协议(tcp/udp)，默认tcp
请求示例：
curl -X POST "http://192.168.99.108:8000/android" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"imageUrl": "registry.example.com/android:v12",
"dns": "223.5.5.5",
"modelId": "1",
"indexNum": 1,
"doboxFps": "60",
"doboxWidth": "1080",
"doboxHeight": "1920",
"doboxDpi": "480",
"start": true
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"id": "abc123def456789"
}
}
失败返回：
{
"code": 500,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 12/89

## 第 13 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"message": "创建云机失败: 镜像不存在",
"data": null
}
注意事项：
name必须唯一，不能与已有云机重名
imageUrl必须是已拉取到本地的镜像地址
indexNum范围：P1设备1-24，Q1设备1-12
modelStatic优先级高于LocalModel和线上机型
3. 重置安卓云机
功能说明：重置指定的安卓云机
请求方式：PUT
请求URL：
http://{主机IP}:8000/android
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
latitude 否 float 纬度
longitude 否 float 经度
countryCode 否 string 国家代码，例如CN，US
请求示例：
curl -X PUT "http://192.168.99.108:8000/android" \
-H "Content-Type: application/json" \
-d '{
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 13/89

## 第 14 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"name": "android-01",
"latitude": 39.9042,
"longitude": 116.4074,
"countryCode": "CN"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "重置云机失败: 云机不存在",
"data": null
}
注意事项：
重置会清除云机内的所有数据
重置前请确保已备份重要数据
4. 删除安卓云机
功能说明：删除指定的安卓云机容器
请求方式：DELETE
请求URL：
http://{主机IP}:8000/android
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 14/89

## 第 15 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
name 是 string 云机名称
请求示例：
curl -X DELETE "http://192.168.99.108:8000/android" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "删除云机失败: 云机正在运行",
"data": null
}
注意事项：
删除操作不可恢复
建议删除前先停止云机
5. 切换安卓镜像
功能说明：切换云机使用的安卓镜像
请求方式：POST
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 15/89

## 第 16 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求URL：
http://{主机IP}:8000/android/switchImage
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
imageUrl 是 string 镜像完整地址
modelId 否 string 机型ID
LocalModel 否 string 本地机型名称
modelStatic 否 string 本地静态机型名称
dns 否 string 云机DNS
offset 否 string 云机的开机时间
doboxFps 否 string 云机FPS
doboxWidth 否 string 云机分辨率的宽
doboxHeight 否 string 云机分辨率的高
doboxDpi 否 string 云机DPI
network 否 object 独立IP设置
start 否 bool 切换完成是否开机，默认true
mgenable 否 string magisk开关，0-关，1-开
gmsenable 否 string gms开关，0-关，1-开
latitude 否 float 纬度
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 16/89

## 第 17 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
longitude 否 float 经度
countryCode 否 string 国家代码
s5User 否 string s5代理用户名
s5Password 否 string s5代理密码
s5IP 否 string s5代理IP
s5Port 否 string s5代理端口
s5Type 否 string 代理类型
customBinds 否 array 自定义文件映射
PINCode 否 string 屏幕锁屏密码
请求示例：
curl -X POST "http://192.168.99.108:8000/android/switchImage" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"imageUrl": "registry.example.com/android:v13",
"start": true
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"message": "镜像切换成功"
}
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 17/89

## 第 18 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
失败返回：
{
"code": 500,
"message": "切换镜像失败: 镜像不存在",
"data": null
}
注意事项：
切换镜像会重置云机数据
确保目标镜像已拉取到本地
6. 切换机型
功能说明：切换云机的机型配置
请求方式：POST
请求URL：
http://{主机IP}:8000/android/switchModel
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
modelId 否 string 机型ID
localModel 否 string 本地机型名称
modelStatic 否 string 本地静态机型名称
latitude 否 float 纬度
longitude 否 float 经度
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 18/89

## 第 19 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
countryCode 否 string 国家代码
请求示例：
curl -X POST "http://192.168.99.108:8000/android/switchModel" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"modelId": "2",
"countryCode": "US"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "切换机型失败: 机型不存在",
"data": null
}
7. 拉取安卓镜像
功能说明：从镜像仓库拉取安卓镜像到本地
请求方式：POST
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 19/89

## 第 20 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/android/pullImage
请求参数：
参数名 必选 类型 说明
imageUrl 是 string 镜像完整地址
请求示例：
curl -X POST "http://192.168.99.108:8000/android/pullImage" \
-H "Content-Type: application/json" \
-d '{
"imageUrl": "registry.example.com/android:v12"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "拉取镜像失败: 网络连接超时",
"data": null
}
注意事项：
拉取镜像可能需要较长时间，取决于网络速度和镜像大小
确保设备有足够的磁盘空间
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 20/89

## 第 21 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
8. 启动安卓云机
功能说明：启动指定的安卓云机
请求方式：POST
请求URL：
http://{主机IP}:8000/android/start
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/start" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "启动云机失败: 云机已在运行",
"data": null
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 21/89

## 第 22 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
9. 关闭安卓云机
功能说明：关闭指定的安卓云机
请求方式：POST
请求URL：
http://{主机IP}:8000/android/stop
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/stop" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "关闭云机失败: 云机未运行",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 22/89

## 第 23 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
10. 重启安卓云机
功能说明：重启指定的安卓云机
请求方式：POST
请求URL：
http://{主机IP}:8000/android/restart
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/restart" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 23/89

## 第 24 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "重启云机失败",
"data": null
}
11. 获取本地镜像列表
功能说明：获取设备上已拉取的Docker镜像列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android/image
请求参数：
参数名 必选 类型 说明
imageName 否 string 根据镜像名过滤
请求示例：
curl "http://192.168.99.108:8000/android/image"
# 根据名称过滤
curl "http://192.168.99.108:8000/android/image?imageName=android"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 2,
"list": [
{
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 24/89

## 第 25 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"id": "sha256:abc123",
"imageUrl": "registry.example.com/android:v12",
"size": "2.5GB",
"created": "2024-01-10 08:00:00",
"labels": {
"version": "12",
"type": "android"
}
},
{
"id": "sha256:def456",
"imageUrl": "registry.example.com/android:v13",
"size": "2.8GB",
"created": "2024-01-15 10:00:00",
"labels": {
"version": "13",
"type": "android"
}
}
]
}
}
返回字段说明：
字段 类型 说明
id string 镜像ID
imageUrl string 镜像完整地址
size string 镜像大小
created string 创建时间
labels object 镜像labels
失败返回：
{
"code": 500,
"message": "获取镜像列表失败",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 25/89

## 第 26 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
12. 删除本地镜像
功能说明：删除设备上的本地Docker镜像
请求方式：DELETE
请求URL：
http://{主机IP}:8000/android/image
请求参数：
参数名 必选 类型 说明
imageUrl 是 string 要删除的镜像完整地址
请求示例：
curl -X DELETE "http://192.168.99.108:8000/android/image" \
-H "Content-Type: application/json" \
-d '{
"imageUrl": "registry.example.com/android:v12"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 26/89

## 第 27 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "删除镜像失败: 镜像正在被使用",
"data": null
}
注意事项：
正在被云机使用的镜像无法删除
删除前请确保没有云机依赖该镜像
13. 获取本地镜像压缩包列表
功能说明：获取设备上的镜像压缩包文件列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android/imageTar
请求参数：
参数名 必选 类型 说明
filename 否 string 根据文件名过滤
请求示例：
curl "http://192.168.99.108:8000/android/imageTar"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 2,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 27/89

## 第 28 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"list": [
{
"name": "android_v12.tar",
"size": "2.5GB"
},
{
"name": "android_v13.tar",
"size": "2.8GB"
}
]
}
}
失败返回：
{
"code": 500,
"message": "获取镜像压缩包列表失败",
"data": null
}
14. 删除本地镜像压缩包
功能说明：删除设备上的镜像压缩包文件
请求方式：DELETE
请求URL：
http://{主机IP}:8000/android/imageTar
请求参数：
参数名 必选 类型 说明
filename 是 string 要删除的镜像压缩包名称
请求示例：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 28/89

## 第 29 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
curl -X DELETE "http://192.168.99.108:8000/android/imageTar" \
-H "Content-Type: application/json" \
-d '{
"filename": "android_v12.tar"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "删除镜像压缩包失败: 文件不存在",
"data": null
}
15. 导出安卓镜像
功能说明：将本地镜像导出为压缩包文件
请求方式：POST
请求URL：
http://{主机IP}:8000/android/image/export
请求参数：
参数名 必选 类型 说明
imageUrl 是 string 要导出的镜像完整地址
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 29/89

## 第 30 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求示例：
curl -X POST "http://192.168.99.108:8000/android/image/export" \
-H "Content-Type: application/json" \
-d '{
"imageUrl": "registry.example.com/android:v12"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"filename": "android_v12_20240115.tar"
}
}
失败返回：
{
"code": 500,
"message": "导出镜像失败: 磁盘空间不足",
"data": null
}
注意事项：
导出过程可能需要较长时间
确保设备有足够的磁盘空间
16. 下载导出后的安卓镜像包
功能说明：下载已导出的镜像压缩包文件
请求方式：GET
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 30/89

## 第 31 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/android/image/download
请求参数：
参数名 必选 类型 说明
filename 是 string 要下载的镜像包名
请求示例：
curl "http://192.168.99.108:8000/android/image/download?
filename=android_v12.tar" -o android_v12.tar
成功返回：
返回文件的二进制数据，浏览器会自动下载
失败返回：
{
"code": 500,
"message": "下载失败: 文件不存在",
"data": null
}
17. 导入安卓镜像
功能说明：通过上传tar文件导入安卓镜像
请求方式：POST
请求URL：
http://{主机IP}:8000/android/image/import
Content-Type：multipart/form-data
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 31/89

## 第 32 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求参数：
参数名 必选 类型 说明
file 是 file 导入镜像包文件，tar格式
请求示例：
curl -X POST "http://192.168.99.108:8000/android/image/import" \
-F "file=@android_v12.tar"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "导入镜像失败: 文件格式错误",
"data": null
}
注意事项：
仅支持tar格式的镜像包
导入过程可能需要较长时间
18. 导出安卓云机
功能说明：将安卓云机导出为压缩包
请求方式：POST
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 32/89

## 第 33 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求URL：
http://{主机IP}:8000/android/export
请求参数：
参数名 必选 类型 说明
name 是 string 云机名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/export" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"exportName": "android-01_20240115.zip"
}
}
失败返回：
{
"code": 500,
"message": "导出云机失败: 云机正在运行",
"data": null
}
注意事项：
建议导出前先停止云机
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 33/89

## 第 34 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
导出文件包含云机的完整数据
19. 导入安卓云机
功能说明：通过上传文件导入安卓云机
请求方式：POST
请求URL：
http://{主机IP}:8000/android/import
Content-Type：multipart/form-data
请求参数：
参数名 必选 类型 说明
file 是 file 导入使用本SDK导出的安卓云机
indexNum 是 int 实例序号，P1范围1-24，Q1范围1-12
name 否 string 导入后云机名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/import" \
-F "file=@android-01_20240115.zip" \
-F "indexNum=2" \
-F "name=android-02"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"name": "android-02"
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 34/89

## 第 35 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
}
}
失败返回：
{
"code": 500,
"message": "导入云机失败: 实例位已被占用",
"data": null
}
注意事项：
仅支持本SDK导出的云机文件
indexNum不能与已有云机冲突
20. 获取机型列表
功能说明：获取线上可用的机型列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android/phoneModel
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/android/phoneModel"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 35/89

## 第 36 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"total": 50,
"list": [
{
"id": "1",
"name": "Samsung Galaxy S23",
"md5": "abc123def456",
"status": "active",
"currentVersion": 1,
"sdk_ver": "v1.1.0",
"createdAt": 1705286400
},
{
"id": "2",
"name": "Xiaomi 14",
"md5": "def456ghi789",
"status": "active",
"currentVersion": 1,
"sdk_ver": "v1.1.0",
"createdAt": 1705286400
}
]
}
}
返回字段说明：
字段 类型 说明
id string 机型ID
name string 机型名称
md5 string 机型文件MD5
status string 状态
currentVersion int 当前版本
sdk_ver string 对应SDK版本
createdAt int64 创建时间戳
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 36/89

## 第 37 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "获取机型列表失败",
"data": null
}
21. 获取国家代码列表
功能说明：获取可用的国家代码列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android/countryCode
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/android/countryCode"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 200,
"list": [
{
"countryName": "中国",
"countryCode": "CN"
},
{
"countryName": "美国",
"countryCode": "US"
},
{
"countryName": "日本",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 37/89

## 第 38 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"countryCode": "JP"
}
]
}
}
失败返回：
{
"code": 500,
"message": "获取国家代码列表失败",
"data": null
}
22. 设置Macvlan
功能说明：设置Macvlan网络配置
请求方式：POST
请求URL：
http://{主机IP}:8000/android/macvlan
请求参数：
参数名 必选 类型 说明
gw 是 string 网关，例如192.168.100.1
subnet 是 string 掩码，例如192.168.100.0/24
请求示例：
curl -X POST "http://192.168.99.108:8000/android/macvlan" \
-H "Content-Type: application/json" \
-d '{
"gw": "192.168.100.1",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 38/89

## 第 39 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"subnet": "192.168.100.0/24"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "设置Macvlan失败: 网关格式错误",
"data": null
}
注意事项：
设置后需要重启相关云机才能生效
确保网关和子网配置正确
23. 设置云机容器IP (Macvlan模式)
功能说明：在Macvlan模式下设置云机容器的IP地址
请求方式：POST
请求URL：
http://{主机IP}:8000/android/macvlan
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 39/89

## 第 40 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
name 是 string 云机名称
ip 是 string 云机要设置的IP
请求示例：
curl -X POST "http://192.168.99.108:8000/android/macvlan" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"ip": "192.168.100.101"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "设置IP失败: IP已被占用",
"data": null
}
24. 修改云机容器名称
功能说明：修改云机容器的名称
请求方式：POST
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 40/89

## 第 41 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/android/rename
请求参数：
参数名 必选 类型 说明
name 是 string 云机当前名称
newName 是 string 云机新名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/rename" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"newName": "my-android"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "修改名称失败: 新名称已存在",
"data": null
}
注意事项：
新名称不能与已有云机重名
建议在云机停止状态下修改
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 41/89

## 第 42 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
25. 获取机型备份列表
功能说明：获取已备份的机型数据列表
请求方式：GET
请求URL：
http://{主机IP}:8000/android/backup/model
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/android/backup/model"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 3,
"list": [
{
"name": "samsung_s23_backup"
},
{
"name": "xiaomi_14_backup"
}
]
}
}
失败返回：
{
"code": 500,
"message": "获取机型备份列表失败",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 42/89

## 第 43 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
26. 删除机型备份
功能说明：删除指定的机型备份数据
请求方式：DELETE
请求URL：
http://{主机IP}:8000/android/backup/model
请求参数：
参数名 必选 类型 说明
name 是 string 机型备份文件名称
请求示例：
curl -X DELETE "http://192.168.99.108:8000/android/backup/model" \
-H "Content-Type: application/json" \
-d '{
"name": "samsung_s23_backup"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 43/89

## 第 44 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "删除机型备份失败: 文件不存在",
"data": null
}
27. 备份机型数据
功能说明：将V3镜像创建的云机里的机型数据完整备份
请求方式：POST
请求URL：
http://{主机IP}:8000/android/backup/model
请求参数：
参数名 必选 类型 说明
name 是 string 要备份机型数据的云机名称
suffix 是 string 备份后机型数据的后缀名
请求示例：
curl -X POST "http://192.168.99.108:8000/android/backup/model" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"suffix": "backup_20240115"
}'
成功返回：
{
"code": 0,
"message": "ok",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 44/89

## 第 45 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": {}
}
失败返回：
{
"code": 500,
"message": "备份机型数据失败: 云机不存在",
"data": null
}
注意事项：
仅支持V3镜像创建的云机
备份前建议停止云机
28. 导出机型备份数据
功能说明：导出已备份的机型数据
请求方式：POST
请求URL：
http://{主机IP}:8000/android/backup/modelExport
请求参数：
参数名 必选 类型 说明
name 是 string 备份机型数据文件名称
请求示例：
curl -X POST "http://192.168.99.108:8000/android/backup/modelExport" \
-H "Content-Type: application/json" \
-d '{
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 45/89

## 第 46 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"name": "samsung_s23_backup"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "导出机型备份失败: 文件不存在",
"data": null
}
29. 导入备份机型数据
功能说明：通过上传ZIP包导入备份的机型数据
请求方式：POST
请求URL：
http://{主机IP}:8000/android/backup/modelImport
Content-Type：multipart/form-data
请求参数：
参数名 必选 类型 说明
file 是 file 导入备份机型数据ZIP包
请求示例：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 46/89

## 第 47 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
curl -X POST "http://192.168.99.108:8000/android/backup/modelImport" \
-F "file=@samsung_s23_backup.zip"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "导入机型备份失败: 文件格式错误",
"data": null
}
注意事项：
仅支持ZIP格式的备份文件
30. 安卓云机执行命令
功能说明：在安卓云机内执行命令
请求方式：POST
请求URL：
http://{主机IP}:8000/android/exec
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 47/89

## 第 48 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
name 是 string 云机名称
command 是 array 执行的命令，数组形式
请求示例：
curl -X POST "http://192.168.99.108:8000/android/exec" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01",
"command": ["sd", "-c", "ping -c 5 223.5.5.5"]
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "执行命令失败: 云机未运行",
"data": null
}
注意事项：
云机必须处于运行状态
command参数为数组格式，例如 ["sd", "-c", "ls -la"]
31. 清理所有未被使用镜像
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 48/89

## 第 49 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
功能说明：清理设备上所有未被云机使用的镜像
请求方式：POST
请求URL：
http://{主机IP}:8000/android/pruneImages
请求参数：无
请求示例：
curl -X POST "http://192.168.99.108:8000/android/pruneImages"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"pruneCount": 5,
"releaseSpace": "12.5GB"
}
}
返回字段说明：
字段 类型 说明
pruneCount int 清理数量
releaseSpace string 释放空间
失败返回：
{
"code": 500,
"message": "清理镜像失败",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 49/89

## 第 50 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
注意事项：
此操作不可恢复
仅清理未被任何云机使用的镜像
三、云机备份
1. 获取备份压缩包文件列表
功能说明：获取设备上的云机备份压缩包文件列表
请求方式：GET
请求URL：
http://{主机IP}:8000/backup
请求参数：
参数名 必选 类型 说明
name 否 string 根据文件名过滤
请求示例：
curl "http://192.168.99.108:8000/backup"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 3,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 50/89

## 第 51 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"list": [
{
"name": "android-01_20240115.zip",
"size": "1.2GB"
},
{
"name": "android-02_20240116.zip",
"size": "1.5GB"
}
]
}
}
返回字段说明：
字段 类型 说明
name string 备份压缩包文件名
size string 备份压缩包大小
失败返回：
{
"code": 500,
"message": "获取备份列表失败",
"data": null
}
2. 下载备份压缩包文件
功能说明：下载指定的云机备份压缩包
请求方式：GET
请求URL：
http://{主机IP}:8000/backup/download
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 51/89

## 第 52 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求参数：
参数名 必选 类型 说明
name 是 string 备份压缩包文件名
请求示例：
curl "http://192.168.99.108:8000/backup/download?name=android-01_20240115.zip"
-o android-01_20240115.zip
成功返回：
返回文件的二进制数据，浏览器会自动下载
失败返回：
{
"code": 500,
"message": "下载失败: 文件不存在",
"data": null
}
3. 删除备份压缩包文件
功能说明：删除指定的云机备份压缩包
请求方式：DELETE
请求URL：
http://{主机IP}:8000/backup
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 52/89

## 第 53 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
name 是 string 备份压缩包文件名
请求示例：
curl -X DELETE "http://192.168.99.108:8000/backup" \
-H "Content-Type: application/json" \
-d '{
"name": "android-01_20240115.zip"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "删除备份失败: 文件不存在",
"data": null
}
四、终端连接
1. 连接设备SSH
功能说明：通过Web页面连接设备SSH终端
请求方式：GET
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 53/89

## 第 54 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/link/ssh
或直接访问：
http://{主机IP}:8000/ssh
请求参数：无
请求示例：
# 在浏览器中直接访问
http://192.168.99.108:8000/ssh
成功返回：
返回SSH终端Web页面
注意事项：
需要在浏览器中访问
默认用户名：user
2. 修改SSH登录用户密码
功能说明：修改SSH登录用户的密码
请求方式：POST
请求URL：
http://{主机IP}:8000/link/ssh/changePwd
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 54/89

## 第 55 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
username 否 string 用户名，默认user
password 是 string 新密码
请求示例：
curl -X POST "http://192.168.99.108:8000/link/ssh/changePwd" \
-H "Content-Type: application/json" \
-d '{
"username": "user",
"password": "newpassword123"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "修改密码失败",
"data": null
}
注意事项：
密码修改后立即生效
请牢记新密码
3. 开关SSH root登录
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 55/89

## 第 56 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
功能说明：启用或禁止SSH root用户登录
请求方式：POST
请求URL：
http://{主机IP}:8000/link/ssh/switchRoot
请求参数：
参数名 必选 类型 说明
enable 是 bool true-启用root登录，false-禁止root登录
请求示例：
curl -X POST "http://192.168.99.108:8000/link/ssh/switchRoot" \
-H "Content-Type: application/json" \
-d '{
"enable": true
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "设置失败",
"data": null
}
注意事项：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 56/89

## 第 57 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
出于安全考虑，建议禁用root登录
4. 开关SSH服务
功能说明：启用或关闭SSH服务
请求方式：POST
请求URL：
http://{主机IP}:8000/link/ssh/enable
请求参数：
参数名 必选 类型 说明
enable 是 bool true-启用ssh服务，false-关闭ssh服务
请求示例：
curl -X POST "http://192.168.99.108:8000/link/ssh/enable" \
-H "Content-Type: application/json" \
-d '{
"enable": true
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 57/89

## 第 58 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"message": "设置SSH服务失败",
"data": null
}
5. 连接容器终端
功能说明：通过Web页面连接云机容器终端
请求方式：GET
请求URL：
http://{主机IP}:8000/link/exec
或直接访问：
http://{主机IP}:8000/container/exec
请求参数：无
请求示例：
# 在浏览器中直接访问
http://192.168.99.108:8000/container/exec
成功返回：
返回容器终端Web页面
注意事项：
需要在浏览器中访问
可以选择要连接的云机容器
五、myt_bridge网卡管理
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 58/89

## 第 59 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
1. 获取myt_bridge网卡列表
功能说明：获取设备上的myt_bridge网卡列表
请求方式：GET
请求URL：
http://{主机IP}:8000/mytBridge
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/mytBridge"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 2,
"list": [
{
"name": "myt_bridge",
"cidr": "172.17.0.1/16"
},
{
"name": "myt_bridge_lan",
"cidr": "10.0.0.1/16"
}
]
}
}
失败返回：
{
"code": 500,
"message": "获取网卡列表失败",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 59/89

## 第 60 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
2. 创建myt_bridge网卡
功能说明：创建新的myt_bridge网卡
请求方式：POST
请求URL：
http://{主机IP}:8000/mytBridge
请求参数：
参数名 必选 类型 说明
customName 是 string 自定义名(最多4字符)，会拼接在myt_bridge后面
cidr 是 string CIDR，例如10.0.0.1/16
请求示例：
curl -X POST "http://192.168.99.108:8000/mytBridge" \
-H "Content-Type: application/json" \
-d '{
"customName": "lan",
"cidr": "10.0.0.1/16"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 60/89

## 第 61 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
失败返回：
{
"code": 500,
"message": "创建网卡失败: 名称已存在",
"data": null
}
注意事项：
customName最多4个字符
创建后网卡名为 myt_bridge_customName
3. 更新myt_bridge网卡
功能说明：更新myt_bridge网卡的CIDR配置
请求方式：PUT
请求URL：
http://{主机IP}:8000/mytBridge
请求参数：
参数名 必选 类型 说明
name 是 string 网卡名(全称或自定义名)
newCidr 是 string 新CIDR，例如10.0.0.1/16
请求示例：
curl -X PUT "http://192.168.99.108:8000/mytBridge" \
-H "Content-Type: application/json" \
-d '{
"name": "myt_bridge_lan",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 61/89

## 第 62 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"newCidr": "10.0.0.1/24"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "更新网卡失败: 网卡不存在",
"data": null
}
4. 删除myt_bridge网卡
功能说明：删除指定的myt_bridge网卡
请求方式：DELETE
请求URL：
http://{主机IP}:8000/mytBridge
请求参数：
参数名 必选 类型 说明
name 是 string 网卡名(全称或自定义名)
请求示例：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 62/89

## 第 63 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
curl -X DELETE "http://192.168.99.108:8000/mytBridge" \
-H "Content-Type: application/json" \
-d '{
"name": "myt_bridge_lan"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "删除网卡失败: 网卡正在被使用",
"data": null
}
注意事项：
正在被云机使用的网卡无法删除
删除前请确保没有云机依赖该网卡
六、魔云腾VPC
1. 获取网络分组列表
功能说明：查询所有网络分组列表，支持按别名过滤
请求方式：GET
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 63/89

## 第 64 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/mytVpc/group
请求参数：
参数名 必选 类型 说明
alias 否 string 分组别名，传空查询所有
请求示例：
# 查询所有分组
http://{主机IP}:8000/mytVpc/group
# 按别名过滤
curl "http://192.168.99.108:8000/mytVpc/group?alias=test-group"
成功返回：
{
"code": 0,
"message": "OK",
"data": {
"count": 1,
"list": [
{
"id": 11,
"alias": "111saa",
"url": "",
"vpcs": {
"vpcCount": 1,
"list": [
{
"id": 289,
"groupId": 11,
"remarks": "socks_220csx",
"protocol": "socks",
"profile": "
{\"configType\":3,\"remarks\":\"socks_220csx\",\"server\":\"nub2ccs1.user.wuyouip
"outConfig": "{\"protocol\":\"socks\",\"sendThrough\":null,\"tag\"
[{\"address\":\"nub2ccs1.user.wuyouip.com\",\"port\":xxxx,\"level\":8,\"users\":
[{\"user\":\"xxxxx\",\"pass\":\"xxxxxx\",\"level\":8}]}]},\"streamSettings\":null
{\"enabled\":false,\"concurrency\":-1,\"xudpConcurrency\":0,\"xudpProxyUDP443\":\
"source": 2,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 64/89

## 第 65 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"tag": "socks_220csx_11_1769492725191"
}
]
}
}
]
}
}
2. 增加网络分组列表
功能说明：创建新的网络分组，支持订阅地址或节点地址模式
请求方式：POST
请求URL：
http://{主机IP}:8000/mytVpc/group
请求参数：
参数名 必选 类型 说明
alias 是 string 网络分组别名
addresses 否 array 批量添加节点列表（source=2 时必填）
source 否 int 1-订阅地址，2-节点地址，默认
 
url 否 string 批量添加节点列表（source=1 时必填）
请求示例：
# 订阅地址模式
curl -X POST "http://192.168.99.108:8000/mytVpc/group" \
-H "Content-Type: application/json" \
-d '{
"alias": "test-group",
"source": 1,
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 65/89

## 第 66 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"url": "http://example.com/subscribe"
}'
# 节点地址模式
curl -X POST "http://192.168.99.108:8000/mytVpc/group" \
-H "Content-Type: application/json" \
-d '{
"alias": "node-group",
"source": 2,
"addresses": ["192.168.1.100:8080", "192.168.1.101:8080"]
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
# 分组名称未填
{
"code": 51,
"message": "The alias field is required",
"data": null
}
# 填错地址
{
"code": 50,
"message": "Get \"\": unsupported protocol scheme \"\"",
"data": null
}
# 分组已存在
{
"code": 10021,
"message": "Error: 此订阅分组已存在无法新建",
"data": null
}
3. 更新网络分组名
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 66/89

## 第 67 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
功能说明：修改指定网络分组的别名
请求方式：POST
请求URL：
http://{主机IP}:8000/mytVpc/group/alias
请求参数：
参数名 必选 类型 说明
id 是 int 网络分组ID
newAlias 是 string 分组新别名
请求示例：
curl http://192.168.99.108:8000/mytVpc/group/alias \
--request POST \
--header 'Content-Type: application/json' \
--data '{
"id": 1,
"newAlias": "111"
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
{
"code": 500,
"message": "更新分组别名失败: 新别名已存在",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 67/89

## 第 68 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
4. 删除网络分组列表
功能说明：删除指定的网络分组，删除前需确保分组内无 VPC 节点
请求方式：DELETE
请求URL：
http://{主机IP}:8000/mytVpc/group
请求参数：
参数名 必选 类型 说明
id 是 int 网络分组ID
请求示例：
curl -X DELETE "http://192.168.99.108:8000/mytVpc/group" \
-H "Content-Type: application/json" \
-d '{
"id": 2
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 68/89

## 第 69 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 10022,
"message": "Error: 此订阅分组不存在",
"data": null
}
5. 指定云机 VPC 节点
功能说明：为指定云机绑定 VPC 节点及 DNS 白名单
请求方式：POST
请求URL：
http://{主机IP}:8000/mytVpc/addRule
请求参数：
参数名 必选 类型 说明
name 是 string 云机容器名称
vpcID 是 int VPC 节点 ID
WhiteListDns 否 array VDNS 白名单列表
请求示例：
curl http://192.168.99.108:8000/mytVpc/addRule \
--request POST \
--header 'Content-Type: application/json' \
--data '{
"name": "p738c384c1581ad24c3fcf199684f5f5_13_T00013",
"vpcID": 1,
"WhiteListDns": [
""
]
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 69/89

## 第 70 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
{
"code": 51,
"message": "The name field is required",
"data": null
}
或
{
"code": 10023,
"message": "Error: 此VPC节点不存在",
"data": null
}
6. 已设置云机 VPC 节点
功能说明：查询已绑定 VPC 节点的云机规则列表
请求方式：GET
请求URL：
http://{主机IP}:8000/mytVpc/containerRule
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/mytVpc/containerRule"
成功返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 70/89

## 第 71 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 0,
"message": "OK",
"data": {
"count": 2,
"list": [
{
"id": 1,
"containerID":
"5fd727704a60691f7ed5c13575ac261c0f28eebb9aea8141412818f74fa110d5",
"containerIP": "",
"containerName": "Test_1",
"containerState": "running",
"status": 1,
"groupName": "111saa",
"vpcRemarks": "socks_220csx",
"WhiteListDns": []
},
{
"id": 2,
"containerID":
"e2e38a2d7ea53d40e58ba5d54327b807a714139dca0ec69faeb176336686a060",
"containerIP": "172.17.0.7",
"containerName": "p738c384c1581ad24c3fcf199684f5f5_13_T00013",
"containerState": "running",
"status": 1,
"groupName": "test-grup",
"vpcRemarks": "澳洲AX01 50500进阶版 0.3x",
"WhiteListDns": []
}
]
}
}
8. 删除网络分组内节点
功能说明：从指定网络分组中移除一个云机节点。
请求方式：DELETE
请求URL：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 71/89

## 第 72 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
http://{主机IP}:8000/mytVpc
请求参数：
参数名 必选 类型 说明
vpcID 是 int 要删除的 VPC 节点 ID
请求示例：
curl -X DELETE "http://192.168.99.108:8000/mytVpc" \
-H "Content-Type: application/json" \
-d '{
"vpcID": 1
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
{
"code": 10023,
"message": "Error: 此VPC节点不存在",
"data": null
}
9. 更新指定网络分组
功能说明：更新指定网络分组的配置信息。
请求方式：POST
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 72/89

## 第 73 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求URL：
http://{主机IP}:8000/mytVpc/group/update
请求参数：
参数名 必选 类型 说明
ID 是 int 网络分组ID
请求示例：
curl -X DELETE "http://192.168.99.108:8000/mytVpc" \
-H "Content-Type: application/json" \
-d '{
"vpcID": 1
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
{
"code": 10022,
"message": "Error: 此订阅分组不存在",
"data": null
}
10. 增加socks5节点
功能说明：向指定网络分组添加 socks5 节点。
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 73/89

## 第 74 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求方式：POST
请求URL：
http://{主机IP}:8000/mytVpc/socks
请求参数：
参数 必
类型 说明
名 选
订阅分组别名，如果别名不存在将创建新分组，若存在则加入到此
alias 是 string
分组中
list 是 array socks5 节点列表
list 数组元素结构：
字段 类型 说明
remarks string 节点别名
socksIp string s5 IP
socksPort int s5 端口
socksUser string s5 用户名
socksPassword istring s5 密码
请求示例：
curl -X POST "http://192.168.99.108:8000/mytVpc/socks" \
-H "Content-Type: application/json" \
-d '{
"alias": "socks-group",
"list": [
{
"remarks": "node1",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 74/89

## 第 75 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"socksIp": "192.168.1.100",
"socksPort": 1080,
"socksUser": "user1",
"socksPassword": "pass123"
}
]
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
失败返回：
{
"code": 51,
"message": "The alias field is required",
"data": null
}
11. 开关DNS白名单
功能说明：启用 / 禁用指定 VPC 规则的 DNS 白名单。
请求方式：POST
请求URL：
http://{主机IP}:8000/mytVpc/whiteListDns
请求参数：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 75/89

## 第 76 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
参数名 必选 类型 说明
ruleID 是 int 规则 ID
enable 否 bool 是否启用，默认 true
whiteListDns 否 array DNS 白名单列表
请求示例：
curl http://192.168.99.108:8000/mytVpc/whiteListDns \
--request POST \
--header 'Content-Type: application/json' \
--data '{
"ruleID": 1,
"enable": true,
"whiteListDns": [
""
]
}'
成功返回：
{
"code": 0,
"message": "OK",
"data": null
}
12. VPC节点延迟测试
功能说明：测试指定 VPC 节点的网络延迟。
请求方式：GET
请求URL：
http://{主机IP}:8000/mytVpc/test
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 76/89

## 第 77 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求参数：
必
参数名 类型 说明
选
节点地址，address 格式如 "1.1.1.1:80" 或
address 是 string
"www.google.com:443"
请求示例：
curl 'http://192.168.99.108:8000/mytVpc/test?address=50500.b-
vm915x.8h2jssajkd.g-songs.ting-wo-shuo-xiexieni.com'
成功返回：
{
"code": 0,
"message": "OK",
"data": {
"msg": "dial tcp: address 50500.b-vm915x.8h2jssajkd.g-songs.ting-wo-shuo-
xiexieni.com: missing port in address",
"latency": "0ms"
}
}
七、本地机型数据管理
1. 获取本地机型列表
功能说明：获取设备上的本地机型数据列表
请求方式：GET
请求URL：
http://{主机IP}:8000/phoneModel
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 77/89

## 第 78 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求参数：无
请求示例：
curl "http://192.168.99.108:8000/phoneModel"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"count": 5,
"list": [
{
"name": "samsung_s23"
},
{
"name": "xiaomi_14"
},
{
"name": "pixel_8"
}
]
}
}
返回字段说明：
字段 类型 说明
name string 机型文件名称
失败返回：
{
"code": 500,
"message": "获取本地机型列表失败",
"data": null
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 78/89

## 第 79 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
2. 删除本地机型数据
功能说明：删除指定的本地机型数据
请求方式：DELETE
请求URL：
http://{主机IP}:8000/phoneModel
请求参数：
参数名 必选 类型 说明
name 是 string 机型文件名称
请求示例：
curl -X DELETE "http://192.168.99.108:8000/phoneModel" \
-H "Content-Type: application/json" \
-d '{
"name": "samsung_s23"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "删除本地机型失败: 文件不存在",
"data": null
}
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 79/89

## 第 80 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
3. 导出本地机型数据
功能说明：导出指定的本地机型数据
请求方式：POST
请求URL：
http://{主机IP}:8000/phoneModel/export
请求参数：
参数名 必选 类型 说明
name 是 string 机型文件名称
请求示例：
curl -X POST "http://192.168.99.108:8000/phoneModel/export" \
-H "Content-Type: application/json" \
-d '{
"name": "samsung_s23"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "导出本地机型失败: 文件不存在",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 80/89

## 第 81 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"data": null
}
4. 导入机型数据
功能说明：通过上传ZIP包导入机型数据
请求方式：POST
请求URL：
http://{主机IP}:8000/phoneModel/import
Content-Type：multipart/form-data
请求参数：
参数名 必选 类型 说明
file 是 file 导入修改后的机型ZIP包
请求示例：
curl -X POST "http://192.168.99.108:8000/phoneModel/import" \
-F "file=@samsung_s23.zip"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 81/89

## 第 82 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
{
"code": 500,
"message": "导入机型数据失败: 文件格式错误",
"data": null
}
注意事项：
仅支持ZIP格式的机型数据包
八、接口认证
1. 修改认证密码
功能说明：修改API接口认证密码（默认用户名admin）
请求方式：POST
请求URL：
http://{主机IP}:8000/auth/password
请求参数：
参数名 必选 类型 说明
newPassword 是 string 新密码
confirmPassword 是 string 确认新密码
请求示例：
curl -X POST "http://192.168.99.108:8000/auth/password" \
-H "Content-Type: application/json" \
-d '{
"newPassword": "newpassword123",
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 82/89

## 第 83 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
"confirmPassword": "newpassword123"
}'
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "修改密码失败: 两次密码不一致",
"data": null
}
注意事项：
两次输入的密码必须一致
默认用户名为admin
密码修改后立即生效
2. 关闭接口认证
功能说明：关闭API接口认证功能
请求方式：POST
请求URL：
http://{主机IP}:8000/auth/close
请求参数：无
请求示例：
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 83/89

## 第 84 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
curl -X POST "http://192.168.99.108:8000/auth/close"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "关闭认证失败",
"data": null
}
注意事项：
关闭认证后，所有接口将无需认证即可访问
出于安全考虑，建议在内网环境下使用
九、服务管理
1. 更新服务
功能说明：在线更新SDK服务到最新版本
请求方式：GET
请求URL：
http://{主机IP}:8000/server/upgrade
请求参数：无
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 84/89

## 第 85 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求示例：
curl "http://192.168.99.108:8000/server/upgrade"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"msg": "更新成功，服务将自动重启"
}
}
失败返回：
{
"code": 500,
"message": "更新失败: 网络连接超时",
"data": null
}
注意事项：
更新成功后服务会自动重启
更新过程中请勿断电或断网
2. 通过上传SDK更新服务
功能说明：通过上传SDK压缩包更新服务
请求方式：POST
请求URL：
http://{主机IP}:8000/server/upgrade/upload
Content-Type：multipart/form-data
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 85/89

## 第 86 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求参数：
参数名 必选 类型 说明
file 是 file SDK压缩包文件，zip格式
请求示例：
curl -X POST "http://192.168.99.108:8000/server/upgrade/upload" \
-F "file=@myt-sdk-v1.2.0.zip"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "更新失败: 文件格式错误",
"data": null
}
注意事项：
仅支持zip格式的SDK压缩包
更新成功后服务会自动重启
3. 清空设备磁盘数据
功能说明：清空设备磁盘上的所有数据（高危操作！）
请求方式：POST
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 86/89

## 第 87 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求URL：
http://{主机IP}:8000/server/device/reset
请求参数：无
请求示例：
curl -X POST "http://192.168.99.108:8000/server/device/reset"
成功返回：
{
"code": 0,
"message": "ok",
"data": {}
}
失败返回：
{
"code": 500,
"message": "清空数据失败",
"data": null
}
注意事项：
⚠
高危操作！此操作将清空设备上的所有数据，不可恢复！
执行前请确保已备份所有重要数据
操作完成后设备将恢复出厂状态
4. 重启设备
功能说明：重启设备
请求方式：POST
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 87/89

## 第 88 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
请求URL：
http://{主机IP}:8000/server/device/reboot
请求参数：无
请求示例：
curl -X POST "http://192.168.99.108:8000/server/device/reboot"
成功返回：
{
"code": 0,
"message": "ok",
"data": {
"message": "设备将在5秒后重启"
}
}
失败返回：
{
"code": 500,
"message": "重启设备失败",
"data": null
}
注意事项：
重启过程中所有云机将停止运行
重启完成后需要手动启动云机
附录
错误码说明
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 88/89

## 第 89 页
2026/2/2 15:21 盒⼦内SDK API 开发⽂档 | 魔云腾
错误码 说明
0 成功
400 请求参数错误
401 未授权/认证失败
404 资源不存在
500 服务器内部错误
常见问题
1. 接口返回401错误
检查是否开启了接口认证
确认认证信息是否正确
2. 云机创建失败
检查镜像是否已拉取到本地
确认实例序号是否被占用
检查磁盘空间是否充足
3. 无法连接设备
确认设备IP地址是否正确
检查网络连接是否正常
确认端口8000是否开放
Last updated on Jan 29, 2026
https://dev.moyunteng.com/docs/NewMYTOS/heziSDKAPI 89/89

