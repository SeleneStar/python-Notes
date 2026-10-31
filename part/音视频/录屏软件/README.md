# Screen Recorder - 跨平台屏幕录制程序

基于FFmpeg的跨平台屏幕录制程序，支持Linux、Windows和macOS。

## 功能特性

- 🖥️ 跨平台支持：Linux (X11)、Windows (GDI/DirectShow)、macOS (AVFoundation)
- 🎥 高质量屏幕录制
- 📼 MPEG4/H.264编码
- ⚙️ 可配置的录制参数

## 系统要求

### 通用要求
- FFmpeg 4.0+
- C++11 编译器

### Linux
- X11 显示服务器 (不支持Wayland)
- libX11, libXext, libXfixes

### Windows
- Windows 7+ 
- 支持GDI桌面录制

### macOS
- macOS 10.12+
- AVFoundation框架

## 快速开始

### 1. 构建程序

#### 方法一：使用构建脚本（推荐）
```bash
# Linux版本
./build.sh linux

# Windows版本（交叉编译）
./build.sh -s windows

# 包含部署文件
./build.sh -d windows
```

#### 方法二：使用Makefile
```bash
# Linux版本
make linux

# Windows版本
make setup-windows-cross  # 首次构建需要
make windows

# 查看帮助
make help
```

### 2. 运行程序

#### Linux
```bash
./screen_recorder
# 或
make run
```

#### Windows
```bash
# 在Windows系统中
screen_recorder.exe

# 或使用Wine在Linux中测试
wine screen_recorder.exe
```

## 安装依赖

### 自动安装（推荐）
```bash
./install_deps.sh
```

### 手动安装（Ubuntu/Debian）
```bash
sudo apt update
sudo apt install -y \
    build-essential \
    pkg-config \
    ffmpeg \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libx11-dev \
    libxext-dev \
    libxfixes-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev
```

## 编译和运行

### 编译程序
```bash
make
```

### 运行程序
```bash
make run
# 或者直接运行
./screen_recorder
```

### 清理编译文件
```bash
make clean
```

## 使用说明

1. 运行程序后，会提示输入要录制的帧数
2. 输入一个数字（例如：100表示录制100帧）
3. 程序会开始录制屏幕
4. 录制完成后，视频文件会保存在`media/output.mp4`

## 录制参数

程序默认配置：
- **录制区域**: 全屏（从坐标10,250开始）
- **输出分辨率**: 1920x1080
- **帧率**: 30fps
- **编码格式**: MPEG4
- **输出文件**: media/output.mp4

## 修改录制参数

如果需要修改录制参数，可以编辑`recording.cpp`文件中的以下部分：

### 修改录制区域
```cpp
// 在openCamera()函数中
value = avformat_open_input(&pAVFormatContext, ":0.0+10,250", pAVInputFormat, NULL);
// 修改 ":0.0+10,250" 来改变录制起始位置
```

### 修改输出分辨率
```cpp
// 在init_outputfile()函数中
outAVCodecContext->width = 1920;   // 宽度
outAVCodecContext->height = 1080;  // 高度
```

### 修改帧率
```cpp
// 在openCamera()函数中
value = av_dict_set( &options,"framerate","30",0 );  // 修改"30"为其他值

// 在init_outputfile()函数中
outAVCodecContext->time_base.den = 30;  // 修改30为其他值
```

## 故障排除

### 编译错误
- 确保安装了所有FFmpeg开发库
- 检查系统是否为X11环境
- 确保gcc/g++编译器可用

### 运行错误
- 确保在X11环境下运行（不支持Wayland）
- 检查是否有足够的磁盘空间
- 确保对输出目录有写权限

### 性能优化
- 如果录制卡顿，可以降低帧率
- 如果文件太大，可以调整bit_rate参数
- 对于长时间录制，建议使用更高效的编码器如H.264

## 注意事项

- 程序使用了一些已废弃的FFmpeg API，编译时会有警告，但不影响运行
- 录制时会占用较多CPU资源
- 确保有足够的磁盘空间存储视频文件
- 程序仅在X11环境下工作，不支持Wayland

## 许可证

本程序仅供学习和研究使用。
