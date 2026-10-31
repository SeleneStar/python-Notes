# 跨平台构建总结

## 已完成的工作

✅ **代码修改**
- 修复了FFmpeg头文件包含问题
- 添加了平台检测宏定义
- 支持Linux (X11grab)、Windows (GDI)、macOS (AVFoundation)

✅ **构建系统**
- 创建了支持跨平台的Makefile
- 开发了自动化构建脚本 `build.sh`
- 支持Linux本地编译和Windows交叉编译

✅ **依赖管理**
- 自动安装系统依赖
- Windows版FFmpeg自动下载
- MinGW交叉编译器支持

## 文件结构

```
recording/
├── main.cpp              # 主程序入口
├── recording.cpp          # 录制功能实现 (支持多平台)
├── recording.h            # 头文件 (平台检测)
├── Makefile              # 跨平台构建规则
├── build.sh              # 构建脚本 (推荐使用)
├── install_deps.sh       # 依赖安装脚本  
├── README.md             # 详细说明文档
└── media/                # 输出目录
```

## 使用方法

### 🐧 Linux构建 (已测试)
```bash
# 方法1: 使用构建脚本
./build.sh linux

# 方法2: 使用Makefile
make linux

# 运行程序
./screen_recorder
```

### 🪟 Windows交叉编译
```bash
# 一键设置并构建
./build.sh -s windows

# 或分步进行:
# 1. 安装MinGW交叉编译器
sudo apt install -y mingw-w64 mingw-w64-tools wget unzip

# 2. 下载Windows版FFmpeg
make download-ffmpeg-windows

# 3. 编译Windows版本
make windows

# 4. 部署 (复制所需DLL)
make build-windows
```

### 🍎 macOS构建 (理论支持)
```bash
# 在macOS系统中
brew install ffmpeg
make macos
```

## 平台特性

| 平台 | 录制方式 | 输入格式 | 状态 |
|------|----------|----------|------|
| Linux | X11grab | `:0.0+10,250` | ✅ 已测试 |
| Windows | GDI/DirectShow | `desktop` | 🔧 待测试 |
| macOS | AVFoundation | `1:` | 🔧 待测试 |

## 编译输出

### Linux版本
- 可执行文件: `screen_recorder`
- 依赖: 系统FFmpeg库 + X11库
- 运行要求: X11显示服务器

### Windows版本  
- 可执行文件: `screen_recorder.exe`
- 依赖: FFmpeg DLL文件
- 运行要求: Windows 7+

### 部署包结构
```
deploy-windows/
├── screen_recorder.exe
├── avcodec-XX.dll
├── avdevice-XX.dll  
├── avfilter-XX.dll
├── avformat-XX.dll
├── avutil-XX.dll
├── swscale-XX.dll
└── README.md
```

## 注意事项

⚠️ **API警告**: 代码使用了一些废弃的FFmpeg API，但仍然兼容FFmpeg 4.4.2

⚠️ **平台限制**: 
- Linux需要X11环境 (不支持Wayland)
- Windows版本需要测试
- macOS需要屏幕录制权限

⚠️ **法律提醒**: 仅用于合法的屏幕录制，请遵守当地法律法规

## 下一步建议

1. **测试Windows版本**: 在实际Windows环境中测试
2. **API现代化**: 更新到新的FFmpeg API
3. **界面改进**: 添加GUI界面
4. **功能扩展**: 支持音频录制、区域选择等

## 快速命令参考

```bash
# 显示帮助
make help
./build.sh --help

# 构建所有平台 
./build.sh -c linux     # Linux (清理构建)
./build.sh -s windows   # Windows (设置+构建)  
./build.sh -d windows   # Windows (构建+部署)

# 清理文件
make clean

# 查看构建状态
ls -la screen_recorder*
```

---
**现在你的录屏程序已经具备了完整的跨平台构建能力！** 🎉
