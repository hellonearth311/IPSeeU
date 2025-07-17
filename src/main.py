import os
import platform

from ui import build_main_ui

if platform.system() == "Darwin":
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = "YES"

if __name__ == "__main__":
    build_main_ui()