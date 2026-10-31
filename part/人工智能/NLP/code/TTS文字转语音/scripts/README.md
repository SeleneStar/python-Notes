# Scripts - 脚本使用说明

本目录包含所有项目辅助脚本。

## 📋 脚本列表

### 1. 安装脚本

#### `install.bat` (Windows)
**用途**: Windows系统下一键安装项目依赖

**使用方法**:
```cmd
cd tts-toolkit\scripts
install.bat
```

**功能**:
- 自动检测Python环境
- 安装edge-tts和其他依赖
- 可选安装PyQt5 GUI支持

---

#### `install.sh` (Linux/macOS)
**用途**: Linux/macOS系统下一键安装项目依赖

**使用方法**:
```bash
cd tts-toolkit/scripts
chmod +x install.sh
./install.sh
```

**功能**:
- 检测Python3环境
- 安装所有必需依赖
- 自动配置环境

---

### 2. 运行脚本

#### `run_cli.bat` / `run_cli.sh`
**用途**: 快速运行命令行版本

**Windows使用**:
```cmd
scripts\run_cli.bat "你好世界" output.mp3
```

**Linux/macOS使用**:
```bash
./scripts/run_cli.sh "你好世界" output.mp3
```

---

#### `run_gui.bat` (Windows)
**用途**: 启动图形界面(GUI)

**使用方法**:
```cmd
scripts\run_gui.bat
```

**选项**:
- 默认启动PyQt5版本
- 如果PyQt5未安装,自动降级到Tkinter版本

---

#### `run_gui.sh` (Linux/macOS)
**用途**: 启动图形界面(GUI)

**使用方法**:
```bash
chmod +x scripts/run_gui.sh
./scripts/run_gui.sh
```

---

#### `tts-cli.sh`
**用途**: Linux/macOS下的命令行快捷方式

**使用方法**:
```bash
# 添加到PATH (可选)
export PATH=$PATH:/path/to/tts-toolkit/scripts

# 使用
./scripts/tts-cli.sh -t "你好" -o output.mp3
```

---

### 3. 打包脚本

#### `build_exe.py`
**用途**: Python打包主脚本(使用PyInstaller)

**使用方法**:
```bash
python scripts/build_exe.py
```

**功能**:
- 将项目打包成独立可执行文件(.exe)
- 支持打包GUI和CLI版本
- 自动创建release发布包

**打包选项**:
1. PyQt5 GUI版本 (推荐)
2. Tkinter GUI版本
3. CLI命令行版本
4. 全部打包

**输出位置**: `release/` 目录

---

#### `build_exe.bat` (Windows)
**用途**: Windows一键打包脚本

**使用方法**:
```cmd
scripts\build_exe.bat
```

**功能**:
- 自动检查并安装PyInstaller
- 调用build_exe.py执行打包
- 生成Windows可执行文件

**系统要求**:
- Windows 7/8/10/11
- Python 3.7+
- 至少2GB可用空间

---

#### `build_exe.sh` (Linux/macOS)
**用途**: Linux/macOS一键打包脚本

**使用方法**:
```bash
chmod +x scripts/build_exe.sh
./scripts/build_exe.sh
```

**功能**:
- 打包成Linux/macOS可执行文件
- 自动处理依赖

---

## 🚀 快速开始指南

### 第一次使用

**Windows:**
```cmd
# 1. 安装依赖
scripts\install.bat

# 2. 运行GUI
scripts\run_gui.bat

# 或运行CLI
scripts\run_cli.bat "测试文本" test.mp3
```

**Linux/macOS:**
```bash
# 1. 安装依赖
chmod +x scripts/install.sh
./scripts/install.sh

# 2. 运行GUI
./scripts/run_gui.sh

# 或运行CLI
./scripts/run_cli.sh "测试文本" test.mp3
```

---

### 打包发布版本

**Windows:**
```cmd
# 一键打包
scripts\build_exe.bat

# 打包完成后在 release/ 目录找到exe文件
```

**Linux/macOS:**
```bash
# 一键打包
chmod +x scripts/build_exe.sh
./scripts/build_exe.sh
```

---

## 📝 脚本详细说明

### 安装脚本工作流程

1. **环境检测**
   - 检查Python版本 (需要3.7+)
   - 检查pip是否可用

2. **依赖安装**
   - 核心依赖: edge-tts
   - GUI依赖: PyQt5 (可选)
   - 开发依赖: pytest (可选)

3. **验证安装**
   - 测试导入模块
   - 显示安装摘要

### 打包脚本工作流程

1. **准备阶段**
   - 检查PyInstaller
   - 清理旧的构建文件

2. **打包阶段**
   - 分析依赖关系
   - 打包Python代码
   - 嵌入运行时

3. **后处理**
   - 创建release目录
   - 复制可执行文件
   - 生成使用说明

### 运行脚本参数说明

**run_cli.bat / run_cli.sh 参数:**
```bash
# 格式
run_cli.sh [文本] [输出文件] [声音] [语速]

# 示例
./scripts/run_cli.sh "你好" output.mp3
./scripts/run_cli.sh "测试" test.mp3 zh-CN-XiaoxiaoNeural +20%
```

---

## ⚙️ 高级用法

### 自定义打包配置

编辑 `build_exe.py` 中的配置:

```python
# 修改应用名称
APP_NAME = "我的TTS工具"

# 添加图标
GUI_PYQT5_CONFIG = {
    "name": "TTS-GUI",
    "icon": "path/to/icon.ico",
    ...
}
```

### 添加快捷启动

**Windows - 创建桌面快捷方式:**
1. 右键 `run_gui.bat` → 发送到 → 桌面快捷方式
2. 重命名为"语音合成工具"

**Linux - 创建.desktop文件:**
```bash
cat > ~/.local/share/applications/tts-toolkit.desktop <<EOF
[Desktop Entry]
Name=TTS Toolkit
Exec=/path/to/tts-toolkit/scripts/run_gui.sh
Icon=audio-card
Type=Application
Categories=AudioVideo;Audio;
EOF
```

---

## 🐛 故障排除

### 问题1: 脚本无法执行

**Windows:**
- 确保以管理员身份运行
- 检查执行策略: `Set-ExecutionPolicy RemoteSigned`

**Linux/macOS:**
```bash
# 添加执行权限
chmod +x scripts/*.sh
```

### 问题2: 依赖安装失败

**解决方法:**
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: 打包失败

**可能原因:**
- 磁盘空间不足
- PyInstaller版本过旧
- Python版本不兼容

**解决方法:**
```bash
# 更新PyInstaller
pip install --upgrade pyinstaller

# 清理缓存
pip cache purge
```

### 问题4: GUI启动失败

**检查PyQt5:**
```bash
python -c "import PyQt5; print('OK')"
```

**如果失败,使用Tkinter版本:**
```bash
# Tkinter是Python内置的,通常不需要额外安装
python -m tts_toolkit.gui
```

---

## 📚 相关文档

- [项目README](../README.md) - 项目总体说明
- [安装指南](../docs/installation.md) - 详细安装步骤
- [使用教程](../docs/usage.md) - 详细使用说明

---

## 🤝 贡献

如果您想添加新的脚本:

1. 在scripts目录创建脚本文件
2. 添加详细的注释说明
3. 更新此README文件
4. 提交Pull Request

---

## 📄 许可证

所有脚本遵循项目主许可证 (MIT License)

---

**提示**: 使用前请确保已阅读相应脚本的注释说明
