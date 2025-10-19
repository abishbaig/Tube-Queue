# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

import os

# __file__ may not be defined when PyInstaller executes the spec; use CWD
project_root = os.path.abspath(os.getcwd())

# Path to ffmpeg executable that you want to bundle (relative to project root)
ffmpeg_bin = os.path.join(project_root, 'ffmpeg/bin', 'ffmpeg.exe')

# Data files: (source, dest)
datas = [
    (os.path.join(project_root, 'assets'), 'assets'),
]

# Binaries: (source, dest)
binaries = []
if os.path.exists(ffmpeg_bin):
    binaries.append((ffmpeg_bin, 'bin'))

a = Analysis(
    ['src/app.py'],
    pathex=[os.path.join(project_root, 'src')],
    binaries=binaries,
    datas=datas,
    hiddenimports=['yt_dlp'],
    hookspath=[],
    runtime_hooks=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='TubeQueue',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='TubeQueue',
)
