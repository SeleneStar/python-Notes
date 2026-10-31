# TTS Toolkit - 微软语音合成工具包

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Edge-TTS](https://img.shields.io/badge/edge--tts-latest-orange.svg)](https://github.com/rany2/edge-tts)

一个功能完整的文本转语音(TTS)工具包,基于微软Azure认知服务(Edge TTS),支持命令行和图形界面。完全免费,无需API密钥。

---

## 📑 目录

- [特性](#-特性)
- [快速开始](#-快速开始)
- [安装指南](#-安装指南)
- [使用教程](#-使用教程)
- [打包发布](#-打包为exe可执行文件)
- [项目结构](#-项目结构)
- [支持的语音](#-支持的语音)
- [开发指南](#-开发指南)
- [常见问题](#-常见问题)
- [许可证](#-许可证)

---

## ✨ 特性

- 🎯 **简单易用** - 支持命令行(CLI)和图形界面(GUI)两种方式
- 🌐 **完全免费** - 无需API密钥,基于微软Edge TTS服务
- 🎨 **多种语言** - 支持中文(普通话、粤语、台湾话)和英语(美式、英式等)
- 🗣️ **丰富音色** - 数十种Neural高质量语音可选
- ⚙️ **参数调节** - 可调节语速、音量、音调
- 📦 **多种格式** - 支持MP3、WAV、OGG输出格式
- 🚀 **高性能** - 异步处理,快速合成
- 📝 **批量处理** - 支持批量文本转语音
- 💻 **跨平台** - 支持Windows、Linux、macOS
- 📦 **可打包** - 可打包成独立exe文件,无需Python环境

---

## 🚀 快速开始

### 方法1: 使用图形界面(推荐新手)

**Windows:**
```cmd
# 安装依赖
scripts\install.bat

# 启动GUI
scripts\run_gui.bat
```

**Linux/macOS:**
```bash
# 安装依赖
chmod +x scripts/install.sh
./scripts/install.sh

# 启动GUI
chmod +x scripts/run_gui.sh
./scripts/run_gui.sh
```

### 方法2: 使用命令行

```bash
# 基本用法
python -m tts_toolkit.cli -t "你好世界" -o output.mp3

# 指定声音和参数
python -m tts_toolkit.cli \
  -t "测试文本" \
  -v zh-CN-XiaoxiaoNeural \
  --rate +20% \
  --pitch +5Hz \
  -o output.mp3

# 列出所有可用声音
python -m tts_toolkit.cli --list
```

### 方法3: Python代码集成

```python
from tts_toolkit import TTSEngine

# 创建引擎
engine = TTSEngine()

# 合成语音
engine.synthesize(
    text="你好世界",
    voice="zh-CN-XiaoxiaoNeural",
    output="output.mp3",
    rate="+20%"
)
```

---

## 📦 安装指南

### 环境要求

- Python 3.7+
- 网络连接(用于访问微软Azure API)

### 方法1: 使用安装脚本(推荐)

**Windows:**
```cmd
cd tts-toolkit\scripts
install.bat
```

**Linux/macOS:**
```bash
cd tts-toolkit/scripts
chmod +x install.sh
./install.sh
```

### 方法2: 手动安装

```bash
# 克隆或下载项目
cd tts-toolkit

# 安装依赖
pip install -r requirements.txt

# 可选: 安装PyQt5支持(更好的GUI体验)
pip install PyQt5

# 开发模式安装(可编辑)
pip install -e .
```

### 方法3: 仅安装核心依赖

```bash
pip install edge-tts
```

### 验证安装

```bash
# 测试导入
python -c "from tts_toolkit import TTSEngine; print('安装成功')"

# 运行示例
python examples/basic_usage.py

# 运行测试
python -m pytest tests/
```

### 使用Conda环境

```bash
# 创建新环境
conda create -n tts python=3.10
conda activate tts

# 安装依赖
pip install -r requirements.txt
```

### 故障排除

#### edge-tts安装失败

使用国内镜像:
```bash
pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### GUI乱码问题

Linux系统安装中文字体:
```bash
sudo apt-get install fonts-noto-cjk
```

#### 网络问题

确保能访问微软Azure服务:
```bash
ping speech.platform.bing.com
```

---

## 📖 使用教程

### 命令行(CLI)使用

#### 基本命令

```bash
# 查看帮助
python -m tts_toolkit.cli --help

# 列出所有声音
python -m tts_toolkit.cli --list

# 基本合成
python -m tts_toolkit.cli -t "你好世界" -o output.mp3

# 从文件读取
python -m tts_toolkit.cli -f input.txt -o output.mp3
```

#### 高级参数

```bash
# 指定声音
python -m tts_toolkit.cli -t "文本" -v zh-CN-XiaoxiaoNeural -o output.mp3

# 调整语速 (范围: -50% ~ +100%)
python -m tts_toolkit.cli -t "文本" --rate +20% -o output.mp3

# 调整音量 (范围: -50% ~ +50%)
python -m tts_toolkit.cli -t "文本" --volume +10% -o output.mp3

# 调整音调 (范围: -50Hz ~ +50Hz)
python -m tts_toolkit.cli -t "文本" --pitch +5Hz -o output.mp3

# 组合使用
python -m tts_toolkit.cli \
  -t "测试文本" \
  -v zh-CN-YunyangNeural \
  --rate +30% \
  --volume +10% \
  --pitch +10Hz \
  -o output.mp3
```

### Python API使用

#### 基础合成

```python
from tts_toolkit import TTSEngine

engine = TTSEngine()

# 同步方式
engine.synthesize(
    text="要合成的文本",
    output="output.mp3",
    voice="zh-CN-XiaoxiaoNeural",
    rate="+20%",
    volume="+10%",
    pitch="+5Hz"
)
```

#### 异步合成

```python
import asyncio
from tts_toolkit import TTSEngine

async def main():
    engine = TTSEngine()

    await engine.synthesize_async(
        text="异步合成",
        output="output.mp3"
    )

asyncio.run(main())
```

#### 批量处理

```python
from tts_toolkit import TTSEngine

engine = TTSEngine()

texts = [
    "第一段文本",
    "第二段文本",
    "第三段文本"
]

results = engine.batch_synthesize(
    texts=texts,
    output_dir="output",
    prefix="audio"
)

for file in results:
    print(f"生成: {file}")
```

#### 流式处理

```python
import asyncio
from tts_toolkit import TTSEngine

async def stream_example():
    engine = TTSEngine()

    async for audio_chunk in engine.synthesize_stream(
        text="流式合成示例",
        voice="zh-CN-XiaoxiaoNeural"
    ):
        # 处理音频块
        print(f"收到音频块: {len(audio_chunk)} 字节")

asyncio.run(stream_example())
```

### 常见用例

#### 1. 文章朗读

```python
from tts_toolkit import TTSEngine

engine = TTSEngine()

# 读取文章
with open("article.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 合成
engine.synthesize(
    text=text,
    output="article.mp3",
    rate="+10%"  # 稍快
)
```

#### 2. 多语言混合

```python
# 中文
engine.synthesize(
    text="这是中文",
    output="chinese.mp3",
    voice="zh-CN-XiaoxiaoNeural"
)

# 英文
engine.synthesize(
    text="This is English",
    output="english.mp3",
    voice="en-US-AriaNeural"
)
```

---

## 📦 打包为EXE可执行文件

### 为什么需要打包?

打包后的exe文件可以:
- ✅ 在没有Python环境的电脑上运行
- ✅ 双击即可使用,无需命令行
- ✅ 分发给其他用户使用
- ✅ 独立运行,不依赖Python安装

### 快速打包

**Windows一键打包:**
```cmd
# 运行打包脚本
scripts\build_exe.bat

# 等待打包完成,可执行文件在 release\ 目录
```

**Linux/macOS打包:**
```bash
# 运行打包脚本
chmod +x scripts/build_exe.sh
./scripts/build_exe.sh
```

### 打包选项

运行打包脚本时会提示选择:

```
1. PyQt5 GUI版本 (推荐) - 现代化界面
2. Tkinter GUI版本 - 轻量级界面
3. CLI命令行版本 - 命令行工具
4. 全部打包 - 打包所有版本
```

### 打包输出

打包完成后,在 `release/` 目录会有:

```
release/
├── TTS-Toolkit-GUI-PyQt5.exe     # GUI版本(PyQt5)
├── TTS-Toolkit-GUI-Tkinter.exe   # GUI版本(Tkinter)
├── tts-cli.exe                   # CLI版本
└── README.txt                    # 使用说明
```

### 手动打包(高级)

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包GUI版本
pyinstaller --name TTS-GUI \
  --onefile \
  --noconsole \
  --hidden-import edge_tts \
  src/tts_toolkit/gui_pyqt5.py

# 打包CLI版本
pyinstaller --name tts-cli \
  --onefile \
  --hidden-import edge_tts \
  src/tts_toolkit/cli.py
```

### 打包后使用

**GUI版本:**
- 双击 `TTS-Toolkit-GUI-PyQt5.exe`
- 在界面中输入文本、选择语音、调整参数
- 点击"合成语音"按钮

**CLI版本:**
```cmd
# 打开命令提示符
tts-cli.exe -t "你好世界" -o output.mp3

# 查看帮助
tts-cli.exe --help
```

### 系统要求

- Windows 7/8/10/11 (64位)
- 至少100MB可用空间
- 网络连接(首次使用)

---

## 🛠️ 项目结构

```
tts-toolkit/
├── src/tts_toolkit/          # 源代码
│   ├── __init__.py           # 包初始化
│   ├── engine.py             # TTS引擎核心
│   ├── cli.py                # 命令行工具
│   ├── gui.py                # GUI界面(Tkinter)
│   ├── gui_pyqt5.py          # GUI界面(PyQt5)
│   └── utils.py              # 工具函数
│
├── tests/                    # 测试代码
│   ├── __init__.py
│   └── test_engine.py        # 引擎测试
│
├── docs/                     # 文档(已合并到README)
│   ├── installation.md       # 安装指南
│   └── usage.md              # 使用教程
│
├── examples/                 # 示例代码
│   ├── basic_usage.py        # 基础使用
│   └── batch_process.py      # 批量处理
│
├── scripts/                  # 辅助脚本
│   ├── install.bat           # Windows安装脚本
│   ├── install.sh            # Linux/macOS安装脚本
│   ├── run_gui.bat           # Windows启动GUI
│   ├── run_gui.sh            # Linux/macOS启动GUI
│   ├── run_cli.bat           # Windows运行CLI
│   ├── run_cli.sh            # Linux/macOS运行CLI
│   ├── build_exe.py          # 打包主脚本
│   ├── build_exe.bat         # Windows打包脚本
│   ├── build_exe.sh          # Linux/macOS打包脚本
│   └── README.md             # 脚本使用说明
│
├── output/                   # 输出目录(自动创建)
├── output_audio/             # GUI输出目录(自动创建)
│
├── setup.py                  # 项目安装配置
├── requirements.txt          # 依赖列表
├── README.md                 # 本文件
├── LICENSE                   # MIT开源许可证
├── .gitignore                # Git忽略规则
└── run_gui.py                # GUI启动入口
```

### 核心模块说明

#### 1. engine.py - TTS引擎
```
TTSEngine类
├── synthesize()          # 同步合成
├── synthesize_async()    # 异步合成
├── synthesize_stream()   # 流式合成
└── batch_synthesize()    # 批量合成
```

#### 2. cli.py - 命令行工具
- 参数解析(argparse)
- 命令执行
- 调用engine进行合成

#### 3. gui.py / gui_pyqt5.py - GUI界面
```
MicrosoftTTSGUI类 / TTSMainWindow类
├── create_widgets()      # 创建界面
├── load_voices()         # 加载语音列表
├── synthesize_speech()   # 合成按钮
└── play_audio()          # 播放按钮
```

#### 4. utils.py - 工具函数
- list_voices() - 列出声音
- validate_voice() - 验证声音
- format_rate() - 格式化语速
- format_pitch() - 格式化音调

---

## 🎨 支持的语音

### 中文语音

#### 普通话(zh-CN)
**女声:**
- `zh-CN-XiaoxiaoNeural` - 晓晓(温柔自然,推荐)
- `zh-CN-XiaoyiNeural` - 晓伊(活泼可爱)
- `zh-CN-XiaochenNeural` - 晓辰(专业播音)
- `zh-CN-XiaohanNeural` - 晓涵(温暖亲切)
- `zh-CN-XiaomengNeural` - 晓梦(甜美温柔)
- `zh-CN-XiaomoNeural` - 晓墨(知性优雅)
- `zh-CN-XiaoqiuNeural` - 晓秋(成熟稳重)
- `zh-CN-XiaoruiNeural` - 晓睿(清脆明亮)
- `zh-CN-XiaoshuangNeural` - 晓双(可爱少女)
- `zh-CN-XiaoxuanNeural` - 晓萱(温柔体贴)
- `zh-CN-XiaoyanNeural` - 晓颜(新闻播音)
- `zh-CN-XiaoyouNeural` - 晓悠(儿童音)
- `zh-CN-XiaozhenNeural` - 晓甄(方言特色)

**男声:**
- `zh-CN-YunyangNeural` - 云扬(成熟专业,推荐)
- `zh-CN-YunxiNeural` - 云希(年轻活力)
- `zh-CN-YunjianNeural` - 云健(浑厚有力)
- `zh-CN-YunxiaNeural` - 云霞(少年音)
- `zh-CN-YunfengNeural` - 云枫(新闻播音)
- `zh-CN-YunhaoNeural` - 云皓(广告配音)

**方言:**
- `zh-CN-liaoning-XiaobeiNeural` - 晓北(东北口音)
- `zh-CN-shaanxi-XiaoniNeural` - 晓妮(陕西口音)

#### 粤语(zh-HK)
- `zh-HK-HiuGaaiNeural` - 晓佳(女声,粤语)
- `zh-HK-HiuMaanNeural` - 晓曼(女声,粤语)
- `zh-HK-WanLungNeural` - 云龙(男声,粤语)

#### 台湾话(zh-TW)
- `zh-TW-HsiaoChenNeural` - 晓臻(女声,台湾国语)
- `zh-TW-HsiaoYuNeural` - 晓语(女声,台湾国语)
- `zh-TW-YunJheNeural` - 云哲(男声,台湾国语)

### 英语语音

#### 美式英语(en-US)
**女声:**
- `en-US-AriaNeural` - Aria(自然流畅,推荐)
- `en-US-JennyNeural` - Jenny(温柔亲切)
- `en-US-MichelleNeural` - Michelle(专业播音)
- `en-US-AshleyNeural` - Ashley(年轻活力)
- `en-US-CoraNeural` - Cora(成熟稳重)
- `en-US-ElizabethNeural` - Elizabeth(优雅知性)
- `en-US-MonicaNeural` - Monica(商务专业)

**男声:**
- `en-US-GuyNeural` - Guy(自然流畅,推荐)
- `en-US-ChristopherNeural` - Christopher(沉稳专业)
- `en-US-EricNeural` - Eric(年轻活力)
- `en-US-JacobNeural` - Jacob(友好亲切)
- `en-US-TonyNeural` - Tony(新闻播音)

#### 英式英语(en-GB)
- `en-GB-SoniaNeural` - Sonia(女声,标准英音)
- `en-GB-RyanNeural` - Ryan(男声,标准英音)
- `en-GB-LibbyNeural` - Libby(女声,年轻)

#### 澳式英语(en-AU)
- `en-AU-NatashaNeural` - Natasha(女声,澳洲口音)
- `en-AU-WilliamNeural` - William(男声,澳洲口音)

#### 其他英语
- `en-CA-ClaraNeural` - Clara(加拿大英语)
- `en-IN-NeerjaNeural` - Neerja(印度英语)
- `en-IE-EmilyNeural` - Emily(爱尔兰英语)
- `en-NZ-MollyNeural` - Molly(新西兰英语)

### 查看完整列表

```bash
# 命令行查看
python -m tts_toolkit.cli --list

# Python代码查看
from tts_toolkit.utils import list_voices
voices = list_voices()
for voice in voices:
    print(voice)
```

---

## 🔧 开发指南

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/yourusername/tts-toolkit.git
cd tts-toolkit

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_engine.py -v

# 查看覆盖率
pytest tests/ --cov=tts_toolkit --cov-report=html
```

### 代码格式化

```bash
# 使用black格式化代码
black src/ tests/ examples/

# 使用isort整理导入
isort src/ tests/ examples/

# 类型检查
mypy src/
```

### 添加新功能

1. 在src/tts_toolkit/创建新模块
2. 编写功能代码
3. 在tests/添加测试
4. 更新文档
5. 提交Pull Request

### 发布新版本

```bash
# 1. 更新版本号(setup.py)
# 2. 构建包
python setup.py sdist bdist_wheel

# 3. 检查包
twine check dist/*

# 4. 上传到PyPI
twine upload dist/*
```

---

## ❓ 常见问题

### Q1: 为什么没有声音输出?

**A:** 检查以下几点:
1. 确保网络连接正常
2. 确认输出文件路径正确
3. 检查文本内容是否为空
4. 尝试使用其他语音

### Q2: 如何调整语音的语速、音量、音调?

**A:**
- 语速: 使用 `--rate` 参数,范围 -50% ~ +100%
- 音量: 使用 `--volume` 参数,范围 -50% ~ +50%
- 音调: 使用 `--pitch` 参数,范围 -50Hz ~ +50Hz

```bash
python -m tts_toolkit.cli -t "测试" --rate +20% --volume +10% --pitch +5Hz -o test.mp3
```

### Q3: 支持哪些输出格式?

**A:** 目前支持:
- MP3 (推荐,文件小)
- WAV (无损,文件大)
- OGG (开源格式)

### Q4: 可以离线使用吗?

**A:** 不可以。本工具基于微软在线TTS服务,需要网络连接。

### Q5: 有字数限制吗?

**A:** 单次合成建议不超过5000字。如需处理更长文本,建议使用批量处理功能。

### Q6: GUI启动失败怎么办?

**A:** 尝试以下方法:
1. 确认PyQt5已安装: `pip install PyQt5`
2. 如果PyQt5有问题,使用Tkinter版本: `python -m tts_toolkit.gui`
3. 检查Python版本是否 >= 3.7

### Q7: 打包的exe文件太大?

**A:** 这是正常的。PyInstaller会打包整个Python运行时和依赖库。
- 典型大小: 50-100MB
- 可以使用UPX压缩: `pyinstaller --upx-dir=/path/to/upx ...`

### Q8: 如何添加自定义语音?

**A:** Edge TTS使用的是微软云端语音,不支持自定义。但可以:
1. 使用 `--list` 查看所有可用语音
2. 选择最接近需求的语音
3. 调整参数(语速、音调等)来达到期望效果

### Q9: 商业使用是否允许?

**A:**
- 本项目代码: MIT许可证,可商用
- 微软TTS服务: 需遵守微软服务条款
- 建议: 大规模商用请咨询微软官方

### Q10: 如何贡献代码?

**A:**
1. Fork项目
2. 创建功能分支: `git checkout -b feature/AmazingFeature`
3. 提交更改: `git commit -m 'Add some AmazingFeature'`
4. 推送分支: `git push origin feature/AmazingFeature`
5. 提交Pull Request

---

## 🤝 贡献

欢迎贡献!请查看以下指南:

### 贡献类型

- 🐛 报告Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码

### 贡献流程

1. Fork本项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

### 代码规范

- 遵循PEP 8
- 添加类型注解
- 编写文档字符串
- 添加单元测试

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

### MIT License

```
Copyright (c) 2024 TTS Toolkit Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 致谢

- [edge-tts](https://github.com/rany2/edge-tts) - 微软Edge TTS Python库
- [Microsoft Azure](https://azure.microsoft.com/) - 认知服务TTS API
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 跨平台GUI框架
- [PyInstaller](https://www.pyinstaller.org/) - Python打包工具

---

## 📞 支持与反馈

### 获取帮助

- 📚 [查看文档](docs/)
- 💬 [GitHub Discussions](https://github.com/yourusername/tts-toolkit/discussions)
- 🐛 [报告问题](https://github.com/yourusername/tts-toolkit/issues)

### 联系方式

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/tts-toolkit/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/yourusername/tts-toolkit/discussions)

---

## 🎯 路线图

### 当前版本 v1.0.0
- ✅ 基础TTS功能
- ✅ CLI和GUI支持
- ✅ 中文和英文支持
- ✅ 参数调节
- ✅ 批量处理
- ✅ 打包为exe

### 计划功能
- ⭕ Web界面版本
- ⭕ 更多语言支持
- ⭕ SSML高级控制
- ⭕ 音频后处理
- ⭕ 插件系统
- ⭕ 云端存储集成

---

## 📊 项目统计

- ⭐ Stars: 欢迎Star支持
- 🍴 Forks: 欢迎Fork贡献
- 📝 License: MIT
- 🐍 Language: Python 3.7+
- 📦 Size: ~500KB (源码)
- 🎯 Platform: Windows, Linux, macOS

---

## 🔗 相关链接

- **项目主页**: https://github.com/yourusername/tts-toolkit
- **文档**: https://tts-toolkit.readthedocs.io (待建设)
- **PyPI**: https://pypi.org/project/tts-toolkit (待发布)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

## ⚡ 快速参考

### 最常用命令

```bash
# 1. 快速合成
python -m tts_toolkit.cli -t "你好世界" -o output.mp3

# 2. 启动GUI
python -m tts_toolkit.gui_pyqt5

# 3. 列出声音
python -m tts_toolkit.cli --list

# 4. 批量处理
python examples/batch_process.py

# 5. 打包exe
scripts\build_exe.bat
```

### 最常用代码

```python
# 导入并快速合成
from tts_toolkit import TTSEngine
engine = TTSEngine()
engine.synthesize("你好", "output.mp3")
```

---

**使用愉快! 🎉**

如有问题,欢迎提Issue或PR。

---

*最后更新: 2024年*
