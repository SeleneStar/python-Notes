# Python屏幕录制工具使用指南

## 📖 简介

本项目提供了三个不同版本的Python屏幕录制工具，支持跨平台使用，具有以下特点：

- ✅ **跨平台支持**: Linux, Windows, macOS
- ✅ **可视化区域选择**: 直观的拖拽选择录制区域
- ✅ **多种录制模式**: 全屏、区域、窗口录制
- ✅ **高质量录制**: 支持多种格式和编码器
- ✅ **简单易用**: 图形界面和命令行版本
- ✅ **配置保存**: 自动保存用户设置
- ✅ **实时统计**: 显示录制状态和性能信息

## 🛠️ 安装

### 自动安装（推荐）

```bash
# 完整安装（包含系统依赖）
./install_python_deps.sh

# 仅安装Python依赖
./install_python_deps.sh --python-only

# 安装并创建桌面快捷方式（Linux）
./install_python_deps.sh --with-shortcut
```

### 手动安装

1. **安装Python依赖**
```bash
pip3 install opencv-python pillow numpy pyautogui tkinter --user
```

2. **Linux额外依赖**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk scrot xorg-dev libx11-dev

# CentOS/RHEL
sudo yum install tkinter scrot libX11-devel
```

3. **macOS额外依赖**
```bash
brew install python-tk
```

## 🚀 使用方法

### 1. 高级图形界面版本 (推荐)

```bash
python3 advanced_screen_recorder.py
```

**功能特点：**
- 🎯 可视化区域选择
- ⚙️ 详细的录制设置
- 📊 实时录制统计
- 💾 配置自动保存
- 🎨 现代化界面设计

**操作步骤：**
1. 点击"选择录制区域"按钮
2. 在弹出的全屏窗口中拖拽选择区域
3. 调整录制参数（帧率、质量、格式等）
4. 点击"开始录制"
5. 点击"停止录制"结束

### 2. 基础图形界面版本

```bash
python3 screen_recorder.py
```

**功能特点：**
- 简洁的用户界面
- 基本的录制功能
- 区域选择支持

### 3. 命令行版本

```bash
python3 simple_recorder.py [选项]
```

**常用命令：**

```bash
# 交互模式（推荐新手）
python3 simple_recorder.py -i

# 录制10秒全屏
python3 simple_recorder.py -t 10

# 录制指定区域30秒
python3 simple_recorder.py -r "100,100,800,600" -t 30

# 高帧率录制
python3 simple_recorder.py -f 60 -t 5

# 自定义输出文件
python3 simple_recorder.py -o "我的录制.mp4" -t 15

# 无限时长录制（按Ctrl+C停止）
python3 simple_recorder.py -t 0
```

**命令行参数：**
- `-o, --output`: 输出文件名
- `-t, --time`: 录制时长（秒），0为无限时长
- `-f, --fps`: 帧率（默认30）
- `-q, --quality`: 质量1-100（默认85）
- `-r, --region`: 录制区域 'x,y,width,height'
- `-i, --interactive`: 交互模式
- `--help`: 显示帮助信息

## 📊 性能说明

### 推荐配置

| 用途 | 帧率 | 分辨率 | 质量 | 格式 |
|------|------|--------|------|------|
| 演示录制 | 30fps | 1920x1080 | 85 | MP4 |
| 游戏录制 | 60fps | 1920x1080 | 90 | MP4 |
| 教程录制 | 20fps | 1280x720 | 75 | MP4 |
| 快速分享 | 15fps | 800x600 | 60 | MP4 |

### 性能优化建议

1. **降低帧率**: 对于一般用途，20-30fps已足够
2. **选择合适区域**: 避免录制不必要的屏幕区域
3. **调整质量**: 根据需要平衡文件大小和画质
4. **关闭其他程序**: 减少CPU和内存占用

## 🎨 界面功能说明

### 高级版本界面

```
┌─────────────────────────────────────┐
│      高级Python屏幕录制工具 v2.0      │
├─────────────────────────────────────┤
│ 🎯 录制区域设置                      │
│ [选择录制区域] [全屏录制] [选择窗口]    │
│ ✅ 区域: (100,100) 尺寸: 800×600    │
├─────────────────────────────────────┤
│ ⚙️ 录制设置                         │
│ 帧率: [30] 质量: [85]                │
│ 格式: [mp4] 编码: [mp4v]             │
├─────────────────────────────────────┤
│ 📁 输出设置                         │
│ 保存目录: recordings/                │
│ 文件前缀: screen_record              │
├─────────────────────────────────────┤
│ 🔧 高级选项                         │
│ ☑ 显示鼠标光标                       │
│ ☑ 录制时最小化窗口                   │
├─────────────────────────────────────┤
│ [🔴开始录制][📁打开目录][⚙️测试][❌退出]│
├─────────────────────────────────────┤
│ 🟢 就绪                            │
│ 帧数: 0 | 时间: 0.0s | FPS: 0.0     │
│ ████████████████████████████        │
└─────────────────────────────────────┘
```

## 🔧 高级功能

### 1. 区域选择技巧

- **精确选择**: 使用鼠标拖拽选择精确区域
- **键盘控制**: 
  - `Enter`: 确认选择
  - `Esc`: 取消选择
- **实时预览**: 显示选择区域的实时尺寸

### 2. 录制格式支持

| 格式 | 编码器 | 特点 | 推荐用途 |
|------|---------|------|----------|
| MP4 | mp4v | 通用性好，文件小 | 一般录制 |
| AVI | XVID | 兼容性强 | 老设备播放 |
| MOV | mp4v | Mac友好 | macOS用户 |
| MKV | X264 | 高质量 | 专业用途 |

### 3. 配置文件

配置自动保存在 `recordings/recorder_config.json`:

```json
{
  "fps": 30,
  "quality": 85,
  "format": "mp4",
  "codec": "mp4v",
  "output_path": "/path/to/recordings"
}
```

## 🐛 故障排除

### 常见问题

1. **导入错误**
```bash
ModuleNotFoundError: No module named 'cv2'
```
**解决**: 安装OpenCV
```bash
pip3 install opencv-python
```

2. **权限错误**
```bash
Permission denied
```
**解决**: 使用 `--user` 参数安装
```bash
pip3 install package_name --user
```

3. **录制黑屏**
- 检查录制区域是否正确
- 确认屏幕没有被其他窗口遮挡
- 运行测试命令验证功能

4. **性能问题**
- 降低帧率和分辨率
- 关闭不必要的程序
- 使用SSD存储

### 测试命令

```bash
# 测试截图功能
python3 -c "import pyautogui; pyautogui.screenshot('test.png'); print('测试完成')"

# 测试OpenCV
python3 -c "import cv2; print('OpenCV版本:', cv2.__version__)"

# 检查所有依赖
python3 advanced_screen_recorder.py --help
```

## 📱 平台特定说明

### Linux
- 需要X11图形环境
- WSL用户需要X11转发
- 推荐使用原生Linux环境

### Windows
- 支持原生Windows和WSL
- 可能需要配置防火墙
- 推荐使用PowerShell

### macOS
- 需要授权屏幕录制权限
- 系统偏好设置 > 安全性与隐私 > 屏幕录制

## 🤝 贡献

欢迎提交问题和改进建议！

## 📄 许可证

MIT License - 自由使用和修改

---

**享受录制！** 🎬✨
