# 图标配置说明

## 已完成的修改

### 1. 图标文件位置
- **PNG图标**: `resources/logo.png` (已存在)
- **ICO图标**: `resources/logo.ico` (自动生成)

### 2. 修改的文件

#### `scripts/build_exe.py`
添加了以下功能：
- 自动检测 `resources/logo.png`
- 使用Pillow库将PNG转换为ICO格式
- 在打包时自动使用生成的ICO图标
- 所有exe文件（GUI和CLI）都会使用这个图标

关键代码：
```python
# 图标路径配置
RESOURCES_DIR = ROOT_DIR / "resources"
ICON_PNG = RESOURCES_DIR / "logo.png"
ICON_ICO = RESOURCES_DIR / "logo.ico"

# 配置中使用图标
GUI_PYQT5_CONFIG = {
    "icon": str(ICON_ICO) if ICON_ICO.exists() else None,
    ...
}
```

#### `scripts/build_exe.bat`
添加了Pillow依赖检查和自动安装：
```batch
REM Check and install Pillow (for icon conversion)
python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Pillow not installed. Installing for icon conversion...
    pip install Pillow
)
```

### 3. 工作流程

打包时会自动：
1. 检查 `resources/logo.png` 是否存在
2. 如果 `logo.ico` 不存在，自动转换PNG为ICO
3. 使用ICO图标打包所有exe文件
4. 打包的exe文件会显示自定义图标

### 4. 使用方法

#### 方法1: 自动打包（推荐）
```cmd
scripts\build_exe.bat
```
脚本会自动：
- 安装Pillow（如果需要）
- 转换图标
- 打包程序

#### 方法2: 手动测试图标转换
```cmd
python scripts/test_icon.py
```

#### 方法3: 直接运行打包脚本
```cmd
python scripts/build_exe.py
```

### 5. 图标要求

- **格式**: PNG (推荐) 或已有的ICO
- **位置**: `resources/logo.png`
- **推荐尺寸**: 256x256 或更大（方形）
- **背景**: 建议透明背景

### 6. 生成的ICO包含的尺寸

自动生成的ICO文件包含以下尺寸：
- 16x16 (小图标)
- 32x32 (常规)
- 48x48 (大图标)
- 64x64 (高清)
- 128x128 (超清)
- 256x256 (最高清)

### 7. 依赖要求

打包需要以下依赖：
- `pyinstaller` - 打包工具
- `edge-tts` - TTS核心
- `PyQt5` - GUI支持
- `Pillow` - 图标转换（新增）

所有依赖会由 `build_exe.bat` 自动安装。

### 8. 故障排除

#### 问题1: 图标未显示
**解决**:
- 确认 `resources/logo.png` 存在
- 运行 `python scripts/test_icon.py` 测试转换
- 检查是否生成了 `resources/logo.ico`

#### 问题2: Pillow安装失败
**解决**:
```cmd
pip install Pillow
# 或使用国内镜像
pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 问题3: 手动转换图标
如果自动转换失败，可以：
1. 使用在线工具转换PNG为ICO
   - https://convertio.co/zh/png-ico/
   - https://www.aconvert.com/cn/icon/png-to-ico/
2. 将转换后的ICO保存为 `resources/logo.ico`
3. 重新运行打包脚本

### 9. 输出文件

打包完成后，在 `release/` 目录会有：
```
release/
├── TTS-Toolkit-GUI-PyQt5.exe    ✓ 带图标
├── TTS-Toolkit-GUI-Tkinter.exe  ✓ 带图标
├── tts-cli.exe                  ✓ 带图标
└── README.txt
```

所有exe文件都会显示自定义图标！

### 10. 验证图标

打包完成后，验证图标：
1. 在文件资源管理器中查看exe图标
2. 右键exe -> 属性 -> 查看图标
3. 运行程序时任务栏和窗口也会显示图标

---

## 快速开始

```cmd
# 1. 确保logo.png在resources目录下
dir resources\logo.png

# 2. 运行打包脚本（会自动转换图标）
scripts\build_exe.bat

# 3. 查看生成的exe
dir release\*.exe

# 4. 验证图标
# 右键点击exe -> 属性，查看图标
```

完成！现在您的TTS Toolkit程序有了专业的自定义图标！
