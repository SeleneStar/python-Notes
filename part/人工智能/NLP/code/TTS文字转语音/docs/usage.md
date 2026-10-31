# 使用教程

## 快速开始

### 命令行使用

```bash
# 基本用法
python -m tts_toolkit.cli -t "你好世界" -o output.mp3

# 或使用安装后的命令
tts-cli -t "你好世界" -o output.mp3
```

### Python代码使用

```python
from tts_toolkit import TTSEngine

# 创建引擎
engine = TTSEngine()

# 合成语音
engine.synthesize(
    text="你好世界",
    output="output.mp3"
)
```

## 命令行参数

```bash
# 查看帮助
tts-cli --help

# 列出所有声音
tts-cli --list

# 指定声音
tts-cli -t "文本" -v zh-CN-XiaoxiaoNeural -o output.mp3

# 调整语速
tts-cli -t "文本" --rate +20% -o output.mp3

# 调整音调
tts-cli -t "文本" --pitch +5Hz -o output.mp3

# 从文件读取
tts-cli -f input.txt -o output.mp3

# 组合使用
tts-cli -t "文本" -v zh-CN-YunyangNeural --rate +30% --pitch +10Hz -o output.mp3
```

## API使用

### 基础合成

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

### 异步合成

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

### 批量处理

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

### 流式处理

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

## 声音列表

### 获取可用声音

```python
from tts_toolkit import list_voices, format_voice_info

# 获取中文声音
voices = list_voices(locale="zh-CN")

for voice in voices:
    print(format_voice_info(voice))
```

### 验证声音

```python
from tts_toolkit import validate_voice

if validate_voice("zh-CN-XiaoxiaoNeural"):
    print("声音有效")
else:
    print("声音无效")
```

## 参数说明

### 语速 (rate)
- 格式：`+数值%` 或 `-数值%`
- 范围：-50% ~ +100%
- 示例：`+20%` (加快20%), `-30%` (减慢30%)

### 音量 (volume)
- 格式：`+数值%` 或 `-数值%`
- 范围：-50% ~ +50%
- 示例：`+10%` (增大10%), `-20%` (减小20%)

### 音调 (pitch)
- 格式：`+数值Hz` 或 `-数值Hz`
- 范围：-50Hz ~ +50Hz
- 示例：`+5Hz` (升高5Hz), `-10Hz` (降低10Hz)

## 常见用例

### 1. 文章朗读

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

### 2. 多语言混合

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
    voice="en-US-JennyNeural"
)
```

### 3. 字幕转语音

```python
import re

def parse_srt(srt_file):
    """解析SRT字幕"""
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取文本
    texts = re.findall(
        r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n(.+?)\n\n',
        content,
        re.DOTALL
    )

    return ' '.join(texts)

# 使用
text = parse_srt("subtitle.srt")
engine.synthesize(text, "subtitle_audio.mp3")
```

## 更多示例

查看 `examples/` 目录获取完整示例代码。
