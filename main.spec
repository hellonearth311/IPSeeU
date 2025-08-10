# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

if sys.platform.startswith('win'):
    icon_file = os.path.join('src', 'assets', 'icon.ico')
elif sys.platform == 'darwin' or sys.platform.startswith('linux'):
    icon_file = os.path.join('src', 'assets', 'icon.png')
else:
    icon_file = None

main_script = os.path.join('src', 'main.py')

a = Analysis([
    main_script
],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join('src', 'assets', 'icon.ico'), 'assets'),
        (os.path.join('src', 'assets', 'icon.png'), 'assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='IPSeeU',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=icon_file if icon_file else None,
    onefile=True,
)

dist = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='dist'
)
