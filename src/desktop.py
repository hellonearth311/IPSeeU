import webview
import subprocess
import threading
import time

def start_streamlit():
    subprocess.Popen(
        ["streamlit", "run", "src/app.py", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)

if __name__ == "__main__":
    threading.Thread(target=start_streamlit, daemon=True).start()
    webview.create_window("IPSeeU", "http://localhost:8501", width=1200, height=900)
    webview.start()