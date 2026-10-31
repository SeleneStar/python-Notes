#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微软语音合成工具 - 重新实现版本
基于对原软件的分析，重新创建类似功能
"""

import os
import sys
import asyncio
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path
import json

# 尝试导入edge-tts (微软Azure TTS)
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("[!] edge-tts未安装。运行: pip install edge-tts")


class MicrosoftTTSGUI:
    """微软语音合成GUI应用"""

    # 语言映射：将locale映射到中文描述
    LANGUAGE_MAP = {
        'zh-CN': '普通话',
        'zh-HK': '粤语',
        'zh-TW': '台湾话',
        'en-US': '英语(美)',
        'en-GB': '英语(英)',
        'en-AU': '英语(澳)',
        'en-CA': '英语(加)',
        'en-IN': '英语(印)',
        'en-IE': '英语(爱)',
        'en-NZ': '英语(新)',
        'en-ZA': '英语(南非)',
        'en-SG': '英语(新加坡)',
    }

    def __init__(self, root):
        self.root = root
        self.root.title("微软语音合成助手 - 重制版")
        self.root.geometry("800x600")

        # 配置文件路径
        self.config_file = Path("tts_config.json")
        self.load_config()

        # 创建界面
        self.create_widgets()

        # 加载可用的声音
        if EDGE_TTS_AVAILABLE:
            self.load_voices()

    def load_config(self):
        """加载配置"""
        self.config = {
            "last_voice": "zh-CN-XiaoxiaoNeural",
            "output_dir": "output_audio",
            "rate": "+0%",
            "volume": "+0%",
            "pitch": "+0Hz"
        }

        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
            except:
                pass

    def save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """创建GUI组件"""

        # 顶部工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(toolbar, text="微软Azure语音合成", font=("Arial", 14, "bold")).pack(side=tk.LEFT)

        # 主容器
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 左侧面板 - 文本输入
        left_frame = ttk.LabelFrame(main_frame, text="文本输入", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.text_input = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            width=40,
            height=20,
            font=("Microsoft YaHei", 10)
        )
        self.text_input.pack(fill=tk.BOTH, expand=True)
        self.text_input.insert("1.0", "请输入要合成的文本...")

        # 右侧面板 - 设置
        right_frame = ttk.LabelFrame(main_frame, text="语音设置", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))

        # 声音选择
        ttk.Label(right_frame, text="选择声音:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.voice_var = tk.StringVar(value=self.config.get("last_voice", ""))
        self.voice_combo = ttk.Combobox(
            right_frame,
            textvariable=self.voice_var,
            width=30,
            state="readonly"
        )
        self.voice_combo.grid(row=0, column=1, pady=5, sticky=tk.W)

        # 语速
        ttk.Label(right_frame, text="语速:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.rate_var = tk.StringVar(value=self.config.get("rate", "+0%"))
        rate_frame = ttk.Frame(right_frame)
        rate_frame.grid(row=1, column=1, pady=5, sticky=tk.W)

        self.rate_label = ttk.Label(rate_frame, text="+0%", width=8)
        self.rate_label.pack(side=tk.LEFT, padx=5)

        self.rate_scale = ttk.Scale(
            rate_frame,
            from_=-50,
            to=50,
            orient=tk.HORIZONTAL,
            length=150,
            command=self.update_rate
        )
        self.rate_scale.pack(side=tk.LEFT)
        self.rate_scale.set(0)

        # 音量
        ttk.Label(right_frame, text="音量:").grid(row=2, column=0, sticky=tk.W, pady=5)
        volume_frame = ttk.Frame(right_frame)
        volume_frame.grid(row=2, column=1, pady=5, sticky=tk.W)

        self.volume_label = ttk.Label(volume_frame, text="+0%", width=8)
        self.volume_label.pack(side=tk.LEFT, padx=5)

        self.volume_scale = ttk.Scale(
            volume_frame,
            from_=-50,
            to=50,
            orient=tk.HORIZONTAL,
            length=150,
            command=self.update_volume
        )
        self.volume_scale.pack(side=tk.LEFT)
        self.volume_scale.set(0)

        # 音调
        ttk.Label(right_frame, text="音调:").grid(row=3, column=0, sticky=tk.W, pady=5)
        pitch_frame = ttk.Frame(right_frame)
        pitch_frame.grid(row=3, column=1, pady=5, sticky=tk.W)

        self.pitch_label = ttk.Label(pitch_frame, text="+0Hz", width=8)
        self.pitch_label.pack(side=tk.LEFT, padx=5)

        self.pitch_scale = ttk.Scale(
            pitch_frame,
            from_=-50,
            to=50,
            orient=tk.HORIZONTAL,
            length=150,
            command=self.update_pitch
        )
        self.pitch_scale.pack(side=tk.LEFT)
        self.pitch_scale.set(0)

        # 输出格式
        ttk.Label(right_frame, text="输出格式:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(
            right_frame,
            textvariable=self.format_var,
            values=["mp3", "wav", "ogg"],
            width=28,
            state="readonly"
        )
        format_combo.grid(row=4, column=1, pady=5, sticky=tk.W)

        # 输出目录
        ttk.Label(right_frame, text="输出目录:").grid(row=5, column=0, sticky=tk.W, pady=5)
        dir_frame = ttk.Frame(right_frame)
        dir_frame.grid(row=5, column=1, pady=5, sticky=tk.W)

        self.output_dir_var = tk.StringVar(value=self.config.get("output_dir", "output_audio"))
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=20)
        dir_entry.pack(side=tk.LEFT)

        ttk.Button(dir_frame, text="浏览", command=self.browse_directory, width=8).pack(side=tk.LEFT, padx=5)

        # 按钮区域
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(
            button_frame,
            text="🔊 合成语音",
            command=self.synthesize_speech,
            width=15
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="▶️ 播放",
            command=self.play_audio,
            width=10
        ).pack(side=tk.LEFT, padx=5)

        # 状态栏
        self.status_bar = ttk.Label(
            self.root,
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 进度条
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate'
        )
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)

    def update_rate(self, value):
        """更新语速显示"""
        rate = int(float(value))
        sign = "+" if rate >= 0 else ""
        self.rate_label.config(text=f"{sign}{rate}%")
        self.rate_var.set(f"{sign}{rate}%")

    def update_volume(self, value):
        """更新音量显示"""
        volume = int(float(value))
        sign = "+" if volume >= 0 else ""
        self.volume_label.config(text=f"{sign}{volume}%")

    def update_pitch(self, value):
        """更新音调显示"""
        pitch = int(float(value))
        sign = "+" if pitch >= 0 else ""
        self.pitch_label.config(text=f"{sign}{pitch}Hz")

    def browse_directory(self):
        """浏览选择输出目录"""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def load_voices(self):
        """加载可用的语音列表"""
        async def get_voices():
            voices = await edge_tts.list_voices()
            return voices

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            voices = loop.run_until_complete(get_voices())

            # 筛选中文和英文声音
            supported_voices = [
                v for v in voices
                if v['Locale'].startswith('zh-') or v['Locale'].startswith('en-')
            ]

            # 格式化显示名称
            voice_display_list = []
            for v in supported_voices:
                locale = v['Locale']
                language_label = self.LANGUAGE_MAP.get(locale, locale)
                # 显示格式：[语言类型] 声音名称
                display_name = f"[{language_label}] {v['FriendlyName']}"
                voice_display_list.append(display_name)

            # 保存原始voice数据用于映射
            self.voice_data = {
                f"[{self.LANGUAGE_MAP.get(v['Locale'], v['Locale'])}] {v['FriendlyName']}": v['ShortName']
                for v in supported_voices
            }

            self.voice_combo['values'] = voice_display_list
            if voice_display_list:
                self.voice_combo.current(0)

            self.status_bar.config(text=f"已加载 {len(supported_voices)} 个语音")

        except Exception as e:
            messagebox.showerror("错误", f"加载语音列表失败: {e}")

    def synthesize_speech(self):
        """合成语音"""
        if not EDGE_TTS_AVAILABLE:
            messagebox.showerror("错误", "edge-tts未安装!\n请运行: pip install edge-tts")
            return

        text = self.text_input.get("1.0", tk.END).strip()
        if not text or text == "请输入要合成的文本...":
            messagebox.showwarning("警告", "请输入要合成的文本")
            return

        # 获取选中的声音
        voice_selection = self.voice_var.get()
        if not voice_selection:
            messagebox.showwarning("警告", "请选择语音")
            return

        # 从映射中获取实际的voice名称
        voice_name = self.voice_data.get(voice_selection, voice_selection)

        # 创建输出目录
        output_dir = Path(self.output_dir_var.get())
        output_dir.mkdir(exist_ok=True)

        # 生成输出文件名
        import time
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"tts_{timestamp}.{self.format_var.get()}"

        # 开始合成
        self.status_bar.config(text="正在合成语音...")
        self.progress.start()

        async def synthesize():
            communicate = edge_tts.Communicate(
                text,
                voice_name,
                rate=self.rate_var.get(),
                volume=self.rate_var.get(),
                pitch=self.pitch_label.cget("text")
            )
            await communicate.save(str(output_file))

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(synthesize())

            self.progress.stop()
            self.status_bar.config(text=f"✓ 合成完成: {output_file}")
            messagebox.showinfo("成功", f"语音已保存到:\n{output_file}")

            # 保存配置
            self.config["last_voice"] = voice_name
            self.config["output_dir"] = str(output_dir)
            self.config["rate"] = self.rate_var.get()
            self.save_config()

            # 记录最后的输出文件
            self.last_output_file = output_file

        except Exception as e:
            self.progress.stop()
            self.status_bar.config(text="❌ 合成失败")
            messagebox.showerror("错误", f"合成失败:\n{e}")

    def play_audio(self):
        """播放音频"""
        if not hasattr(self, 'last_output_file') or not self.last_output_file.exists():
            messagebox.showwarning("警告", "没有可播放的音频文件")
            return

        # 使用系统默认播放器
        import subprocess
        import platform

        try:
            if platform.system() == 'Windows':
                os.startfile(str(self.last_output_file))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', str(self.last_output_file)])
            else:  # Linux
                subprocess.run(['xdg-open', str(self.last_output_file)])

            self.status_bar.config(text=f"正在播放: {self.last_output_file.name}")

        except Exception as e:
            messagebox.showerror("错误", f"播放失败:\n{e}")


def main():
    """主函数"""
    root = tk.Tk()
    app = MicrosoftTTSGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
