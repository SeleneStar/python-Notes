#!/bin/bash

# 屏幕录制程序依赖安装脚本

echo "=== 屏幕录制程序依赖安装 ==="

# 检测Linux发行版
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
elif type lsb_release >/dev/null 2>&1; then
    OS=$(lsb_release -si)
    VER=$(lsb_release -sr)
else
    OS=$(uname -s)
    VER=$(uname -r)
fi

echo "检测到系统: $OS $VER"

# 根据不同系统安装依赖
case $OS in
    *"Ubuntu"*|*"Debian"*)
        echo "正在为 Ubuntu/Debian 安装依赖..."
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
        ;;
    *"CentOS"*|*"Red Hat"*|*"Fedora"*)
        echo "正在为 CentOS/RHEL/Fedora 安装依赖..."
        if command -v dnf &> /dev/null; then
            sudo dnf install -y \
                gcc-c++ \
                make \
                pkg-config \
                ffmpeg-devel \
                libX11-devel \
                libXext-devel \
                libXfixes-devel \
                libxcb-devel
        else
            sudo yum install -y \
                gcc-c++ \
                make \
                pkg-config \
                ffmpeg-devel \
                libX11-devel \
                libXext-devel \
                libXfixes-devel \
                libxcb-devel
        fi
        ;;
    *"Arch"*)
        echo "正在为 Arch Linux 安装依赖..."
        sudo pacman -S --needed \
            base-devel \
            ffmpeg \
            libx11 \
            libxext \
            libxfixes \
            libxcb
        ;;
    *)
        echo "未识别的系统，请手动安装以下依赖:"
        echo "- FFmpeg 开发库 (libavcodec, libavdevice, libavfilter, libavformat, libavutil, libswscale)"
        echo "- X11 开发库 (libx11, libxext, libxfixes, libxcb)"
        echo "- 构建工具 (gcc/g++, make)"
        ;;
esac

# 检查FFmpeg是否正确安装
echo ""
echo "=== 检查依赖安装情况 ==="

if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg 已安装: $(ffmpeg -version | head -n1)"
else
    echo "✗ FFmpeg 未找到"
fi

if command -v pkg-config &> /dev/null; then
    if pkg-config --exists libavcodec; then
        echo "✓ libavcodec 开发库已安装"
    else
        echo "✗ libavcodec 开发库未找到"
    fi
    
    if pkg-config --exists libavformat; then
        echo "✓ libavformat 开发库已安装"
    else
        echo "✗ libavformat 开发库未找到"
    fi
    
    if pkg-config --exists libavdevice; then
        echo "✓ libavdevice 开发库已安装"
    else
        echo "✗ libavdevice 开发库未找到"
    fi
else
    echo "! pkg-config 未安装，无法检查开发库"
fi

echo ""
echo "=== 安装完成 ==="
echo "现在可以使用以下命令编译和运行程序:"
echo "1. 编译: make"
echo "2. 运行: make run"
echo ""
echo "注意：程序需要在X11环境下运行，不支持Wayland"
