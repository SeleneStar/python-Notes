#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py - 项目安装配置文件
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# 读取requirements
requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="tts-toolkit",
    version="1.0.0",
    author="TTS Toolkit Team",
    author_email="support@example.com",
    description="微软语音合成工具包 - 基于edge-tts的文本转语音工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tts-toolkit",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/tts-toolkit/issues",
        "Documentation": "https://github.com/yourusername/tts-toolkit/docs",
        "Source Code": "https://github.com/yourusername/tts-toolkit",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tts-cli=tts_toolkit.cli:main",
            "tts-gui=tts_toolkit.gui:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="tts text-to-speech azure edge-tts speech-synthesis chinese",
)
