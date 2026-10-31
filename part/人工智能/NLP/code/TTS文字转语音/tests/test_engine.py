#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试TTS引擎
"""

import pytest
import asyncio
from pathlib import Path
import sys

# 添加src到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tts_toolkit import TTSEngine


@pytest.fixture
def engine():
    """创建测试引擎"""
    return TTSEngine()


@pytest.fixture
def output_dir(tmp_path):
    """创建临时输出目录"""
    return tmp_path / "test_output"


def test_engine_initialization():
    """测试引擎初始化"""
    engine = TTSEngine()
    assert engine.default_voice == "zh-CN-XiaoxiaoNeural"

    engine2 = TTSEngine(default_voice="zh-CN-YunyangNeural")
    assert engine2.default_voice == "zh-CN-YunyangNeural"


def test_synthesize_basic(engine, output_dir):
    """测试基本合成"""
    output_file = output_dir / "test.mp3"
    output_dir.mkdir(parents=True, exist_ok=True)

    success = engine.synthesize(
        text="测试文本",
        output=output_file
    )

    assert success
    assert output_file.exists()
    assert output_file.stat().st_size > 0


@pytest.mark.asyncio
async def test_synthesize_async(engine, output_dir):
    """测试异步合成"""
    output_file = output_dir / "test_async.mp3"
    output_dir.mkdir(parents=True, exist_ok=True)

    await engine.synthesize_async(
        text="异步测试",
        output=output_file
    )

    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_synthesize_with_params(engine, output_dir):
    """测试带参数的合成"""
    output_file = output_dir / "test_params.mp3"
    output_dir.mkdir(parents=True, exist_ok=True)

    success = engine.synthesize(
        text="参数测试",
        output=output_file,
        rate="+20%",
        pitch="+5Hz"
    )

    assert success
    assert output_file.exists()


def test_batch_synthesize(engine, output_dir):
    """测试批量合成"""
    output_dir.mkdir(parents=True, exist_ok=True)

    texts = ["文本1", "文本2", "文本3"]
    results = engine.batch_synthesize(
        texts=texts,
        output_dir=output_dir,
        prefix="batch"
    )

    assert len(results) == len(texts)
    for output_file in results:
        assert output_file.exists()
        assert output_file.stat().st_size > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
