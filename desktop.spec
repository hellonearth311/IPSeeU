# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import subprocess
from PyInstaller.utils.hooks import collect_all


def _collect(name):
    try:
        datas, binaries, hiddenimports = collect_all(name)
        return datas, binaries, hiddenimports
    except Exception:
        return [], [], []


datas = []
binaries = []
hiddenimports = []

# Collect resources for packages Streamlit relies on (dynamic imports, assets)
for pkg in [
    'streamlit',
    'altair',
    'pydeck',
    'pandas',
    'numpy',
    'pyarrow',
    'watchdog',
    'jinja2',
    'tornado',
    'protobuf',
    'pywebview',
]:
    d, b, h = _collect(pkg)
    datas += d
    binaries += b
    hiddenimports += h

# Project app and assets
datas += [
    ('src/app.py', '.'),
    ('src/scan.py', '.'),
    ('src/animation.py', '.'),
    ('src/assets', 'assets'),
]

# Add local modules to hidden imports
hiddenimports += ['scan', 'animation']

a = Analysis(
    ['src/desktop.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

is_macos = sys.platform == 'darwin'
is_windows = sys.platform.startswith('win')

name = 'IPSeeU'

if is_windows:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon='src/assets/icon.ico',
        onefile=True,
    )

if is_macos:
    def _ensure_icns_from_png(png_path: str, icns_path: str) -> str:
        """On macOS, generate an .icns from a .png using sips and iconutil.
        Requires building on macOS. If conversion fails, returns None.
        """
        try:
            if os.path.exists(icns_path):
                return icns_path
            if not os.path.exists(png_path):
                return None
            iconset_dir = os.path.join('build', 'IPSeeU.iconset')
            os.makedirs(iconset_dir, exist_ok=True)

            sizes = [16, 32, 128, 256, 512]
            for size in sizes:
                out = os.path.join(iconset_dir, f'icon_{size}x{size}.png')
                subprocess.run(['sips', '-z', str(size), str(size), png_path, '--out', out], check=True)
                out2x = os.path.join(iconset_dir, f'icon_{size}x{size}@2x.png')
                subprocess.run(['sips', '-z', str(size*2), str(size*2), png_path, '--out', out2x], check=True)

            # Add 512x512@2x (1024x1024)
            out_1024 = os.path.join(iconset_dir, 'icon_512x512@2x.png')
            subprocess.run(['sips', '-z', '1024', '1024', png_path, '--out', out_1024], check=True)

            subprocess.run(['iconutil', '-c', 'icns', '-o', icns_path, iconset_dir], check=True)
            return icns_path if os.path.exists(icns_path) else None
        except Exception:
            return None

    # Prefer icns; if only PNG exists, convert it
    mac_icon = 'src/assets/icon.icns' if os.path.exists('src/assets/icon.icns') else None
    if mac_icon is None:
        maybe_icns = _ensure_icns_from_png('src/assets/icon.png', 'src/assets/icon.icns')
        mac_icon = maybe_icns if maybe_icns else None
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name=name,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=True,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=mac_icon,
        onefile=True,
    )
    app = BUNDLE(
        exe,
        name=f'{name}.app',
        icon=mac_icon,
        bundle_identifier=None,
    )
