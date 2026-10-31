#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微软语音合成工具 - PyQt5版本
提供现代化的图形界面
"""

import sys
import asyncio
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QComboBox, QSlider, QFileDialog,
    QMessageBox, QProgressBar, QGroupBox, QLineEdit, QSplitter,
    QStatusBar, QAction, QMenu
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False


class SynthesisWorker(QThread):
    """语音合成工作线程"""
    finished = pyqtSignal(str)  # 完成信号，传递输出文件路径
    error = pyqtSignal(str)  # 错误信号

    def __init__(self, text, voice, output_file, rate, volume, pitch):
        super().__init__()
        self.text = text
        self.voice = voice
        self.output_file = output_file
        self.rate = rate
        self.volume = volume
        self.pitch = pitch

    def run(self):
        """执行语音合成"""
        try:
            asyncio.run(self._synthesize())
            self.finished.emit(str(self.output_file))
        except Exception as e:
            self.error.emit(str(e))

    async def _synthesize(self):
        """异步合成语音"""
        communicate = edge_tts.Communicate(
            text=self.text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch
        )
        await communicate.save(str(self.output_file))


class VoiceLoaderWorker(QThread):
    """语音列表加载工作线程"""
    finished = pyqtSignal(list)  # 完成信号，传递语音列表
    error = pyqtSignal(str)  # 错误信号

    def run(self):
        """加载语音列表"""
        try:
            voices = asyncio.run(self._load_voices())
            self.finished.emit(voices)
        except Exception as e:
            self.error.emit(str(e))

    async def _load_voices(self):
        """异步加载语音列表"""
        voices = await edge_tts.list_voices()
        # 筛选中文和英文语音
        supported_voices = [
            v for v in voices
            if v['Locale'].startswith('zh-') or v['Locale'].startswith('en-')
        ]
        return supported_voices


class TTSMainWindow(QMainWindow):
    """TTS主窗口"""

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

    def __init__(self):
        super().__init__()
        self.last_output_file = None
        self.voices = []
        self.init_ui()

        # 启动后自动加载语音列表
        if EDGE_TTS_AVAILABLE:
            QTimer.singleShot(100, self.load_voices)

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("语音合成工具 - 华坐标研究院")
        self.setGeometry(100, 100, 1000, 700)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)

        # 左侧面板 - 文本输入
        left_panel = self.create_text_panel()
        splitter.addWidget(left_panel)

        # 右侧面板 - 设置和控制
        right_panel = self.create_control_panel()
        splitter.addWidget(right_panel)

        # 设置分割比例
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # 创建状态栏
        self.create_status_bar()

    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')

        open_action = QAction('打开文本文件(&O)...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_text_file)
        file_menu.addAction(open_action)

        save_action = QAction('保存文本(&S)...', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_text_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')

        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_text_panel(self):
        """创建文本输入面板"""
        group = QGroupBox("文本输入")
        layout = QVBoxLayout()

        # 文本编辑器
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入要合成的文本...")
        self.text_edit.setFont(QFont("Microsoft YaHei", 11))
        layout.addWidget(self.text_edit)

        # 字符计数
        self.char_count_label = QLabel("字符数: 0")
        layout.addWidget(self.char_count_label)

        # 连接文本变化信号
        self.text_edit.textChanged.connect(self.update_char_count)

        group.setLayout(layout)
        return group

    def create_control_panel(self):
        """创建控制面板"""
        widget = QWidget()
        layout = QVBoxLayout()

        # 语音设置组
        voice_group = QGroupBox("语音设置")
        voice_layout = QVBoxLayout()

        # 声音选择
        voice_select_layout = QHBoxLayout()
        voice_select_layout.addWidget(QLabel("选择声音:"))
        self.voice_combo = QComboBox()
        self.voice_combo.setMinimumWidth(250)
        voice_select_layout.addWidget(self.voice_combo)
        voice_layout.addLayout(voice_select_layout)

        # 语速控制
        rate_layout = QVBoxLayout()
        rate_label_layout = QHBoxLayout()
        rate_label_layout.addWidget(QLabel("语速:"))
        self.rate_value_label = QLabel("+0%")
        self.rate_value_label.setMinimumWidth(50)
        rate_label_layout.addWidget(self.rate_value_label)
        rate_label_layout.addStretch()
        rate_layout.addLayout(rate_label_layout)

        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setMinimum(-50)
        self.rate_slider.setMaximum(100)
        self.rate_slider.setValue(0)
        self.rate_slider.setTickPosition(QSlider.TicksBelow)
        self.rate_slider.setTickInterval(10)
        self.rate_slider.valueChanged.connect(self.update_rate_label)
        rate_layout.addWidget(self.rate_slider)
        voice_layout.addLayout(rate_layout)

        # 音量控制
        volume_layout = QVBoxLayout()
        volume_label_layout = QHBoxLayout()
        volume_label_layout.addWidget(QLabel("音量:"))
        self.volume_value_label = QLabel("+0%")
        self.volume_value_label.setMinimumWidth(50)
        volume_label_layout.addWidget(self.volume_value_label)
        volume_label_layout.addStretch()
        volume_layout.addLayout(volume_label_layout)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(-50)
        self.volume_slider.setMaximum(50)
        self.volume_slider.setValue(0)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.valueChanged.connect(self.update_volume_label)
        volume_layout.addWidget(self.volume_slider)
        voice_layout.addLayout(volume_layout)

        # 音调控制
        pitch_layout = QVBoxLayout()
        pitch_label_layout = QHBoxLayout()
        pitch_label_layout.addWidget(QLabel("音调:"))
        self.pitch_value_label = QLabel("+0Hz")
        self.pitch_value_label.setMinimumWidth(50)
        pitch_label_layout.addWidget(self.pitch_value_label)
        pitch_label_layout.addStretch()
        pitch_layout.addLayout(pitch_label_layout)

        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setMinimum(-50)
        self.pitch_slider.setMaximum(50)
        self.pitch_slider.setValue(0)
        self.pitch_slider.setTickPosition(QSlider.TicksBelow)
        self.pitch_slider.setTickInterval(10)
        self.pitch_slider.valueChanged.connect(self.update_pitch_label)
        pitch_layout.addWidget(self.pitch_slider)
        voice_layout.addLayout(pitch_layout)

        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)

        # 输出设置组
        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout()

        # 输出格式
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("输出格式:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["mp3", "wav", "ogg"])
        format_layout.addWidget(self.format_combo)
        output_layout.addLayout(format_layout)

        # 输出目录
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("输出目录:"))
        self.output_dir_edit = QLineEdit("output_audio")
        dir_layout.addWidget(self.output_dir_edit)
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(browse_btn)
        output_layout.addLayout(dir_layout)

        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # 操作按钮
        button_layout = QVBoxLayout()

        self.synthesize_btn = QPushButton("🔊 合成语音")
        self.synthesize_btn.setMinimumHeight(45)
        self.synthesize_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.synthesize_btn.clicked.connect(self.synthesize_speech)
        button_layout.addWidget(self.synthesize_btn)

        self.play_btn = QPushButton("▶️ 播放音频")
        self.play_btn.setMinimumHeight(40)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 13px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0a6ebd;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.play_btn.clicked.connect(self.play_audio)
        self.play_btn.setEnabled(False)
        button_layout.addWidget(self.play_btn)

        self.open_folder_btn = QPushButton("📁 打开输出文件夹")
        self.open_folder_btn.setMinimumHeight(35)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        button_layout.addWidget(self.open_folder_btn)

        layout.addLayout(button_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        layout.addStretch()

        widget.setLayout(layout)
        return widget

    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def update_char_count(self):
        """更新字符计数"""
        text = self.text_edit.toPlainText()
        count = len(text)
        self.char_count_label.setText(f"字符数: {count}")

    def update_rate_label(self, value):
        """更新语速标签"""
        sign = "+" if value >= 0 else ""
        self.rate_value_label.setText(f"{sign}{value}%")

    def update_volume_label(self, value):
        """更新音量标签"""
        sign = "+" if value >= 0 else ""
        self.volume_value_label.setText(f"{sign}{value}%")

    def update_pitch_label(self, value):
        """更新音调标签"""
        sign = "+" if value >= 0 else ""
        self.pitch_value_label.setText(f"{sign}{value}Hz")

    def browse_directory(self):
        """浏览选择输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择输出目录", self.output_dir_edit.text()
        )
        if directory:
            self.output_dir_edit.setText(directory)

    def open_text_file(self):
        """打开文本文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开文本文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.text_edit.setPlainText(f.read())
                self.status_bar.showMessage(f"已加载: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法打开文件:\n{e}")

    def save_text_file(self):
        """保存文本文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存文本文件", "", "文本文件 (*.txt);;所有文件 (*.*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.status_bar.showMessage(f"已保存: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法保存文件:\n{e}")

    def load_voices(self):
        """加载语音列表"""
        if not EDGE_TTS_AVAILABLE:
            return

        self.status_bar.showMessage("正在加载语音列表...")
        self.synthesize_btn.setEnabled(False)

        self.voice_loader = VoiceLoaderWorker()
        self.voice_loader.finished.connect(self.on_voices_loaded)
        self.voice_loader.error.connect(self.on_voice_load_error)
        self.voice_loader.start()

    def on_voices_loaded(self, voices):
        """语音列表加载完成"""
        self.voices = voices
        self.voice_combo.clear()

        for voice in voices:
            locale = voice['Locale']
            language_label = self.LANGUAGE_MAP.get(locale, locale)
            # 显示格式：[语言类型] 声音名称
            display_name = f"[{language_label}] {voice['FriendlyName']}"
            self.voice_combo.addItem(display_name, voice['ShortName'])

        self.status_bar.showMessage(f"已加载 {len(voices)} 个语音")
        self.synthesize_btn.setEnabled(True)

    def on_voice_load_error(self, error):
        """语音列表加载失败"""
        self.status_bar.showMessage("语音列表加载失败")
        QMessageBox.warning(self, "警告", f"加载语音列表失败:\n{error}")
        self.synthesize_btn.setEnabled(True)

    def synthesize_speech(self):
        """合成语音"""
        if not EDGE_TTS_AVAILABLE:
            QMessageBox.critical(
                self, "错误",
                "edge-tts未安装!\n\n请运行: pip install edge-tts"
            )
            return

        # 获取文本
        text = self.text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "请输入要合成的文本")
            return

        # 获取选中的语音
        if self.voice_combo.currentIndex() < 0:
            QMessageBox.warning(self, "警告", "请选择语音")
            return

        voice = self.voice_combo.currentData()

        # 创建输出目录
        output_dir = Path(self.output_dir_edit.text())
        output_dir.mkdir(exist_ok=True, parents=True)

        # 生成输出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_format = self.format_combo.currentText()
        output_file = output_dir / f"tts_{timestamp}.{file_format}"

        # 获取参数
        rate = self.rate_value_label.text()
        volume = self.volume_value_label.text()
        pitch = self.pitch_value_label.text()

        # 开始合成
        self.status_bar.showMessage("正在合成语音...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 无限进度条
        self.synthesize_btn.setEnabled(False)

        self.synthesis_worker = SynthesisWorker(
            text, voice, output_file, rate, volume, pitch
        )
        self.synthesis_worker.finished.connect(self.on_synthesis_finished)
        self.synthesis_worker.error.connect(self.on_synthesis_error)
        self.synthesis_worker.start()

    def on_synthesis_finished(self, output_file):
        """语音合成完成"""
        self.progress_bar.setVisible(False)
        self.synthesize_btn.setEnabled(True)
        self.status_bar.showMessage(f"✓ 合成完成: {Path(output_file).name}")

        self.last_output_file = Path(output_file)
        self.play_btn.setEnabled(True)

        QMessageBox.information(
            self, "成功",
            f"语音已保存到:\n{output_file}"
        )

    def on_synthesis_error(self, error):
        """语音合成失败"""
        self.progress_bar.setVisible(False)
        self.synthesize_btn.setEnabled(True)
        self.status_bar.showMessage("❌ 合成失败")

        QMessageBox.critical(self, "错误", f"合成失败:\n{error}")

    def play_audio(self):
        """播放音频"""
        if not self.last_output_file or not self.last_output_file.exists():
            QMessageBox.warning(self, "警告", "没有可播放的音频文件")
            return

        try:
            import subprocess
            import platform

            if platform.system() == 'Windows':
                os.startfile(str(self.last_output_file))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', str(self.last_output_file)])
            else:  # Linux
                subprocess.run(['xdg-open', str(self.last_output_file)])

            self.status_bar.showMessage(f"正在播放: {self.last_output_file.name}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"播放失败:\n{e}")

    def open_output_folder(self):
        """打开输出文件夹"""
        output_dir = Path(self.output_dir_edit.text())
        output_dir.mkdir(exist_ok=True, parents=True)

        try:
            import subprocess
            import platform

            if platform.system() == 'Windows':
                os.startfile(str(output_dir))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', str(output_dir)])
            else:  # Linux
                subprocess.run(['xdg-open', str(output_dir)])

        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法打开文件夹:\n{e}")

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(
            self, "关于",
            "<h3>微软语音合成工具</h3>"
            "<p>版本: 1.0.0</p>"
            "<p>基于微软Edge TTS的文本转语音工具</p>"
            "<p>使用PyQt5构建</p>"
            "<p><b>功能特性:</b></p>"
            "<ul>"
            "<li>支持多种中文语音</li>"
            "<li>可调节语速、音量、音调</li>"
            "<li>支持多种输出格式</li>"
            "<li>完全免费，无需API密钥</li>"
            "</ul>"
        )


def main():
    """主函数"""
    # 检查edge-tts是否安装
    if not EDGE_TTS_AVAILABLE:
        print("=" * 60)
        print("错误: edge-tts未安装!")
        print("=" * 60)
        print("\n请先安装依赖:")
        print("  pip install edge-tts PyQt5\n")
        print("=" * 60)
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格，更现代

    window = TTSMainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
