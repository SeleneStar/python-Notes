#!/bin/bash
# TTS Toolkit 快速启动脚本

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$SCRIPT_DIR/src:$PYTHONPATH"

# 激活conda环境（如果需要）
if [ -n "$CONDA_DEFAULT_ENV" ]; then
    eval "$(conda shell.bash hook)"
    conda activate ResNet 2>/dev/null || true
fi

# 执行命令
python -m tts_toolkit.cli "$@"
