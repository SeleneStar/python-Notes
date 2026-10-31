#!/bin/bash

# 跨平台构建脚本 for Screen Recorder

set -e  # 出错时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${BLUE}Screen Recorder 跨平台构建脚本${NC}"
    echo ""
    echo "用法: $0 [选项] [平台]"
    echo ""
    echo "平台:"
    echo "  linux     - 构建Linux版本 (默认)"
    echo "  windows   - 构建Windows版本 (需要MinGW)"
    echo "  macos     - 构建macOS版本"
    echo ""
    echo "选项:"
    echo "  -h, --help     显示此帮助信息"
    echo "  -c, --clean    构建前清理"
    echo "  -s, --setup    安装依赖和设置环境"
    echo "  -d, --deploy   构建并准备部署包"
    echo ""
    echo "示例:"
    echo "  $0 linux          # 构建Linux版本"
    echo "  $0 -s windows     # 设置环境并构建Windows版本"
    echo "  $0 -d windows     # 构建Windows版本并准备部署"
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}错误: $1 未找到${NC}"
        return 1
    fi
    return 0
}

# 安装Linux依赖
install_linux_deps() {
    echo -e "${YELLOW}安装Linux依赖...${NC}"
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y ffmpeg libavcodec-dev libavdevice-dev libavfilter-dev \
                           libavformat-dev libavutil-dev libswscale-dev \
                           libx11-dev libxext-dev libxfixes-dev build-essential
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y ffmpeg-devel libX11-devel libXext-devel libXfixes-devel \
                           gcc-c++ make
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --needed base-devel ffmpeg libx11 libxext libxfixes libxcb
    else
        echo -e "${RED}不支持的Linux发行版，请手动安装依赖${NC}"
        exit 1
    fi
}

# 安装Windows交叉编译环境
install_windows_deps() {
    echo -e "${YELLOW}安装Windows交叉编译环境...${NC}"
    
    # 安装MinGW
    if ! check_command x86_64-w64-mingw32-g++; then
        echo "安装MinGW交叉编译器..."
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y mingw-w64 mingw-w64-tools wget unzip
        else
            echo -e "${RED}请手动安装MinGW交叉编译器${NC}"
            exit 1
        fi
    fi
    
    # 下载Windows版FFmpeg
    if [ ! -d "ffmpeg-win64/include" ]; then
        echo "下载Windows版FFmpeg..."
        mkdir -p ffmpeg-win64
        if [ ! -f "ffmpeg-win64.zip" ]; then
            wget -O ffmpeg-win64.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
        fi
        echo "解压FFmpeg..."
        unzip -q ffmpeg-win64.zip
        mv ffmpeg-master-latest-win64-gpl-shared/* ffmpeg-win64/
        rmdir ffmpeg-master-latest-win64-gpl-shared
        echo -e "${GREEN}FFmpeg Windows版本已准备就绪${NC}"
    fi
}

# 构建指定平台
build_platform() {
    local platform=$1
    echo -e "${BLUE}构建 $platform 版本...${NC}"
    
    if [ "$CLEAN" = "true" ]; then
        echo "清理旧文件..."
        make clean
    fi
    
    case $platform in
        linux)
            if [ "$SETUP" = "true" ]; then
                install_linux_deps
            fi
            make linux
            ;;
        windows)
            if [ "$SETUP" = "true" ]; then
                install_windows_deps
            fi
            make windows
            ;;
        macos)
            if [ "$SETUP" = "true" ]; then
                echo -e "${YELLOW}macOS构建需要在macOS系统上进行${NC}"
            fi
            make macos
            ;;
        *)
            echo -e "${RED}不支持的平台: $platform${NC}"
            exit 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}$platform 版本构建成功${NC}"
        
        if [ "$DEPLOY" = "true" ]; then
            prepare_deployment $platform
        fi
    else
        echo -e "${RED}$platform 版本构建失败${NC}"
        exit 1
    fi
}

# 准备部署包
prepare_deployment() {
    local platform=$1
    local deploy_dir="deploy-$platform"
    
    echo -e "${YELLOW}准备 $platform 部署包...${NC}"
    
    rm -rf $deploy_dir
    mkdir -p $deploy_dir
    
    case $platform in
        linux)
            cp screen_recorder $deploy_dir/
            cp README.md $deploy_dir/ 2>/dev/null || true
            echo -e "${GREEN}Linux部署包已准备完成: $deploy_dir/${NC}"
            ;;
        windows)
            cp screen_recorder.exe $deploy_dir/
            if [ -d "ffmpeg-win64/bin" ]; then
                echo "复制Windows DLL文件..."
                cp ffmpeg-win64/bin/*.dll $deploy_dir/ 2>/dev/null || true
            fi
            cp README.md $deploy_dir/ 2>/dev/null || true
            echo -e "${GREEN}Windows部署包已准备完成: $deploy_dir/${NC}"
            echo -e "${YELLOW}注意: 运行时需要所有DLL文件与可执行文件在同一目录${NC}"
            ;;
        macos)
            cp screen_recorder $deploy_dir/
            cp README.md $deploy_dir/ 2>/dev/null || true
            echo -e "${GREEN}macOS部署包已准备完成: $deploy_dir/${NC}"
            ;;
    esac
}

# 主函数
main() {
    # 解析命令行参数
    PLATFORM="linux"
    CLEAN="false"
    SETUP="false"
    DEPLOY="false"
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--clean)
                CLEAN="true"
                shift
                ;;
            -s|--setup)
                SETUP="true"
                shift
                ;;
            -d|--deploy)
                DEPLOY="true"
                shift
                ;;
            linux|windows|macos)
                PLATFORM=$1
                shift
                ;;
            *)
                echo -e "${RED}未知参数: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    echo -e "${BLUE}=== Screen Recorder 跨平台构建 ===${NC}"
    echo -e "目标平台: ${GREEN}$PLATFORM${NC}"
    echo -e "清理构建: $CLEAN"
    echo -e "安装依赖: $SETUP"
    echo -e "准备部署: $DEPLOY"
    echo ""
    
    # 检查Makefile是否存在
    if [ ! -f "Makefile" ]; then
        echo -e "${RED}错误: 未找到Makefile${NC}"
        exit 1
    fi
    
    # 开始构建
    build_platform $PLATFORM
    
    echo ""
    echo -e "${GREEN}=== 构建完成 ===${NC}"
}

# 运行主函数
main "$@"
