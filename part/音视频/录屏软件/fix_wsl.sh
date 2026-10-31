#!/bin/bash

# WSL环境录屏修复脚本

echo "=== WSL环境录屏程序修复 ==="

# 检查是否在WSL环境中
if grep -qEi "(Microsoft|WSL)" /proc/version &> /dev/null; then
    echo "✓ 检测到WSL环境"
    WSL_ENV=true
else
    echo "ℹ 普通Linux环境"
    WSL_ENV=false
fi

# 检查X11环境
echo ""
echo "=== 检查X11环境 ==="

if [ -z "$DISPLAY" ]; then
    echo "⚠ DISPLAY环境变量未设置"
    if [ "$WSL_ENV" = true ]; then
        echo "WSL用户请确保:"
        echo "1. 安装了X11服务器 (如VcXsrv, Xming)"
        echo "2. 启动了X11服务器"
        echo "3. 设置了DISPLAY变量，例如:"
        echo "   export DISPLAY=:0.0"
        echo "   或"
        echo "   export DISPLAY=localhost:10.0"
    fi
else
    echo "✓ DISPLAY=$DISPLAY"
fi

# 测试X11连接
if command -v xwininfo &> /dev/null; then
    if xwininfo -root &> /dev/null; then
        echo "✓ X11连接正常"
    else
        echo "✗ X11连接失败"
        echo "请检查X11服务器是否运行"
    fi
else
    echo "! 未安装xwininfo，无法测试X11连接"
    echo "安装: sudo apt install x11-utils"
fi

echo ""
echo "=== 修复建议 ==="

if [ "$WSL_ENV" = true ]; then
    echo "WSL环境录屏设置步骤:"
    echo "1. 安装VcXsrv (Windows X11服务器)"
    echo "2. 启动VcXsrv，勾选 'Disable access control'"
    echo "3. 在WSL中设置DISPLAY变量:"
    echo "   echo 'export DISPLAY=:0.0' >> ~/.bashrc"
    echo "   source ~/.bashrc"
    echo "4. 重新运行录屏程序"
    echo ""
    echo "测试命令:"
    echo "   xclock  # 如果能显示时钟，说明X11工作正常"
else
    echo "Linux环境检查:"
    echo "1. 确保在X11会话中运行 (不支持Wayland)"
    echo "2. 检查DISPLAY变量设置"
    echo "3. 尝试运行 xwininfo -root 测试X11"
fi

echo ""
echo "如果问题仍然存在，请运行程序并查看具体错误信息"
