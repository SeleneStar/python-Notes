
# TTS Toolkit - Windows发布版 v1.0.0

## 包含文件

1. TTS-Toolkit-GUI-PyQt5.exe - 图形界面版本(PyQt5, 推荐)
2. TTS-Toolkit-GUI-Tkinter.exe - 图形界面版本(Tkinter)
3. tts-cli.exe - 命令行版本

## 使用方法

### 方法1: 图形界面 (推荐)

双击运行 `TTS-Toolkit-GUI-PyQt5.exe` 或 `TTS-Toolkit-GUI-Tkinter.exe`

在界面中:
1. 输入要转换的文本
2. 选择语音类型
3. 调整语速、音量、音调
4. 点击"合成语音"按钮
5. 等待生成完成

### 方法2: 命令行

打开命令提示符(CMD)或PowerShell，运行:

```cmd
# 基本用法
tts-cli.exe -t "你好世界" -o output.mp3

# 查看帮助
tts-cli.exe --help

# 列出所有可用声音
tts-cli.exe --list

# 指定声音和参数
tts-cli.exe -t "测试文本" -v zh-CN-XiaoxiaoNeural --rate +20% -o output.mp3
```

## 支持的语言

- 中文（普通话、粤语、台湾话）
- 英语（美式、英式、澳式等）

## 注意事项

1. 首次运行需要联网下载语音数据
2. 生成的音频文件默认保存在 `output_audio` 目录
3. 支持的输出格式: MP3, WAV, OGG

## 系统要求

- Windows 7/8/10/11 (64位)
- 网络连接

## 问题反馈

如有问题，请访问: https://github.com/yourusername/tts-toolkit/issues

## 版本信息

版本: 1.0.0
构建时间: 2026-02-06 23:30:52

---
完全免费 | 基于微软Edge TTS
