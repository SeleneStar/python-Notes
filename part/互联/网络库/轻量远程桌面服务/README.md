# P2P 局域网远程控制（输入对方IP直连）

功能
- 远程屏幕查看（JPEG over UDP），鼠标、键盘控制（TCP）
- 同一局域网直连；公网需做端口转发（TCP 50021、UDP 50020）
- 预共享密码校验（简单安全，适合内网）
- 新增图形界面：被控端 server_gui.py、控制端 client_gui.py

依赖安装（两端）
pip install -r requirements.txt

图形界面使用
1) 被控端（目标电脑）
   - 运行：python server_gui.py
   - 设置密码/FPS/质量，点击“启动服务”
   - 确保放行 Windows 防火墙：TCP 50021、UDP 50020（或临时关闭防火墙测试）
   - 必要时以管理员运行，以确保输入注入权限

2) 控制端（操作者）
   - 运行：python client_gui.py
   - 输入对方IP、本机UDP端口（如 55000）、密码，点击“连接”
   - 窗口内直接鼠标移动/点击/按键即可控制；点击“断开”结束

命令行使用（可选）
- 被控端：python server.py
- 控制端：python client.py <被控端IP> <本机UDP端口> [密码]
  示例：python client.py 192.168.1.10 55000 123456

注意事项
- 初版为简化实现：当前使用控件坐标发送，未做屏幕分辨率比例映射；若与被控端分辨率不同，坐标可能有偏差。可后续升级为握手同步屏幕尺寸并做比例换算。
- JPEG 帧带宽较大，必要时在 server_gui.py 中调低 JPEG 质量或缩放；后续可升级到 H.264。
- 公网使用：在被控端路由器做端口转发（TCP 50021、UDP 50020），控制端用公网IP连接。

扩展计划（可选）
- 尺寸同步与坐标精确映射
- 简易对称加密（基于预共享密钥）
- 声音转发、剪贴板、文件传输
- 打包为 EXE（PyInstaller）

浏览器版（Web 控制端）
- 被控端运行 Web 服务：py -3 web_server.py
- 在控制端浏览器访问：http://被控端IP:8080/?token=123456
- 页面会自动播放画面并可直接鼠标/键盘控制
- 参数说明：
  - 修改 web_server.py 顶部 PASSWORD/TARGET_FPS/JPEG_QUALITY/DOWNSCALE 调优
  - 若浏览器无法显示，请确认防火墙放行 8080 端口
- 安全提示：当前使用 URL token 简单鉴权，建议仅在内网使用；公网请额外加反向代理与 TLS/访问名单