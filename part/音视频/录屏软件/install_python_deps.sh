#!/bin/bash

# Python屏幕录制工具 - 依赖安装脚本
# 支持 Ubuntu/Debian, CentOS/RHEL, macOS, Windows(WSL)

set -e

echo "🚀 Python屏幕录制工具 - 依赖安装脚本"
echo "=================================================="

# 检测操作系统
OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if [ -f /etc/debian_version ]; then
        OS="debian"
    elif [ -f /etc/redhat-release ]; then
        OS="redhat"
    else
        OS="linux"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "🖥️  检测到操作系统: $OS"

# 安装系统依赖
install_system_deps() {
    echo "📦 安装系统依赖..."
    
    case $OS in
        "debian")
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-tk
            sudo apt-get install -y libopencv-dev python3-opencv
            sudo apt-get install -y scrot xorg-dev libx11-dev
            ;;
        "redhat")
            sudo yum update -y
            sudo yum install -y python3 python3-pip tkinter
            sudo yum install -y opencv-python3
            sudo yum install -y scrot libX11-devel
            ;;
        "macos")
            # 检查是否安装了brew
            if ! command -v brew &> /dev/null; then
                echo "❌ 请先安装Homebrew: https://brew.sh/"
                exit 1
            fi
            brew install python3 python-tk
            ;;
        "windows")
            echo "ℹ️  Windows环境，请确保已安装Python3"
            ;;
        *)
            echo "⚠️  未知操作系统，跳过系统依赖安装"
            ;;
    esac
}

# 安装Python依赖
install_python_deps() {
    echo "🐍 安装Python依赖..."
    
    # 升级pip
    python3 -m pip install --upgrade pip --user
    
    # 安装必需的包
    echo "安装基础依赖..."
    python3 -m pip install --user \
        opencv-python \
        pillow \
        numpy \
        pyautogui \
        tkinter
    
    # 检查安装结果
    echo "🔍 检查依赖安装状态..."
    python3 -c "
import sys
packages = ['cv2', 'PIL', 'numpy', 'pyautogui', 'tkinter']
failed = []

for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        print(f'❌ {pkg}')
        failed.append(pkg)

if failed:
    print(f'\\n⚠️  以下包安装失败: {failed}')
    sys.exit(1)
else:
    print('\\n🎉 所有依赖安装成功!')
"
}

# 创建桌面快捷方式 (Linux)
create_desktop_shortcut() {
    if [[ "$OS" == "debian" ]] || [[ "$OS" == "linux" ]]; then
        echo "🖥️  创建桌面快捷方式..."
        
        DESKTOP_FILE="$HOME/Desktop/ScreenRecorder.desktop"
        CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Python屏幕录制工具
Comment=高级Python屏幕录制工具
Exec=python3 "$CURRENT_DIR/advanced_screen_recorder.py"
Icon=applications-multimedia
Terminal=false
Categories=AudioVideo;Video;
EOF
        
        chmod +x "$DESKTOP_FILE"
        echo "✅ 桌面快捷方式已创建: $DESKTOP_FILE"
    fi
}

# 测试录制功能
test_recording() {
    echo "🧪 测试录制功能..."
    
    python3 -c "
import pyautogui
import os

try:
    # 测试截图
    screenshot = pyautogui.screenshot()
    test_file = 'test_screenshot.png'
    screenshot.save(test_file)
    
    if os.path.exists(test_file):
        os.remove(test_file)
        print('✅ 屏幕截图功能正常')
    else:
        print('❌ 屏幕截图功能异常')
        
except Exception as e:
    print(f'❌ 测试失败: {e}')
"
}

# 主函数
main() {
    echo "开始安装..."
    
    # 检查Python3
    if ! command -v python3 &> /dev/null; then
        echo "❌ 未找到Python3，请先安装Python3"
        exit 1
    fi
    
    echo "✅ Python3版本: $(python3 --version)"
    
    # 安装依赖
    if [[ "$1" != "--python-only" ]]; then
        install_system_deps
    fi
    
    install_python_deps
    
    # 创建快捷方式
    if [[ "$1" == "--with-shortcut" ]]; then
        create_desktop_shortcut
    fi
    
    # 测试功能
    test_recording
    
    echo ""
    echo "🎉 安装完成!"
    echo "=================================================="
    echo "📖 使用方法:"
    echo "   图形界面版本: python3 advanced_screen_recorder.py"
    echo "   简单版本:     python3 screen_recorder.py"
    echo "   命令行版本:   python3 simple_recorder.py --help"
    echo ""
    echo "📝 示例命令:"
    echo "   录制10秒:     python3 simple_recorder.py -t 10"
    echo "   交互模式:     python3 simple_recorder.py -i"
    echo "   自定义区域:   python3 simple_recorder.py -r '100,100,800,600'"
    echo ""
}

# 显示帮助
show_help() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --python-only     只安装Python依赖，跳过系统依赖"
    echo "  --with-shortcut   创建桌面快捷方式 (仅Linux)"
    echo "  --help           显示此帮助信息"
    echo ""
}

# 命令行参数处理
case "$1" in
    "--help"|"-h")
        show_help
        ;;
    *)
        main "$@"
        ;;
esac
