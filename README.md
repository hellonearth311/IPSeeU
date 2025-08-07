# IPSeeU
A simple streamlit-based web app that scans your network for devices, similar to how your WiFi Router's app would.

## How to use
Download the app from the releases page on the right side, and run it! Then just press the scan button and that's it!

> Note: If an executable for your OS isn't available, follow the below instructions.

## Building from source

### Warnings
Building from source means you get the latest commits and new features, but it can also be unstable. Use at your own risk.

Also, you can build from source if the precompiled binaries don't have your OS. To get a stable version, simply select the release tag for the version you want to build.

### Prerequisites
- Python 3.13
- A semi-modern computer on one of the big 3 operating systems (Windows, Mac, Linux).

### To build from source:

1. Download the source code by pressing Code > Download ZIP
2. Extract it and open it in your IDE
3. Create a venv: `python3 -m venv venv` and activate it
 - On Mac / Linux: `source venv/bin/activate`
 - On Windows: `.\venv\Scripts\activate.bat`
4. Run the following commands:
 - `pip install -r requirements.txt`
 - `pyinstaller --noconfirm --onefile --windowed src/desktop.py`
5. Check in the `dist` folder for the executable.