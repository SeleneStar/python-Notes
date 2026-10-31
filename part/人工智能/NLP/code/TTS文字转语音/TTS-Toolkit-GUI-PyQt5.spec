# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\BaiduNetdiskDownload\\AI\\tts-toolkit\\src\\tts_toolkit\\gui_pyqt5.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['edge_tts', 'asyncio', 'aiohttp', 'certifi'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TTS-Toolkit-GUI-PyQt5',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\BaiduNetdiskDownload\\AI\\tts-toolkit\\resources\\logo.ico'],
)
