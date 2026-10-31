# 安装指南

## 环境要求

- Python 3.7+
- 网络连接（用于访问微软Azure API）

## 安装方法

### 方法1：从源码安装（推荐）

```bash
# 克隆或下载项目
cd tts-toolkit

# 安装依赖
pip install -r requirements.txt

# 开发模式安装（可编辑）
pip install -e .
```

### 方法2：使用安装脚本

**Windows:**
```bash
install.bat
```

**Linux/macOS:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### 方法3：直接使用pip

```bash
pip install edge-tts
```

## 验证安装

```bash
# 测试导入
python -c "from tts_toolkit import TTSEngine; print('安装成功')"

# 运行测试
python -m pytest tests/

# 运行示例
python examples/basic_usage.py
```

## Conda环境

如果使用Conda：

```bash
# 创建新环境
conda create -n tts python=3.10
conda activate tts

# 安装依赖
pip install -r requirements.txt
```

## 故障排除

### edge-tts安装失败

使用国内镜像：
```bash
pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### GUI乱码问题

Linux系统安装中文字体：
```bash
sudo apt-get install fonts-noto-cjk
```

### 网络问题

确保能访问微软Azure服务：
```bash
ping speech.platform.bing.com
```
