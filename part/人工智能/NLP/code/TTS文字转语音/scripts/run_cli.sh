#!/bin/bash
# TTS Toolkit 一键运行脚本
# 使用方法: ./run.sh -t "你好" -o output.mp3

cd "$(dirname "$0")"

# 激活conda环境（如果存在）
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook)"
    conda activate ResNet 2>/dev/null || conda activate base 2>/dev/null || true
fi

# 设置Python路径
export PYTHONPATH="src:$PYTHONPATH"

# 运行程序
python -m tts_toolkit.cli "$@"
