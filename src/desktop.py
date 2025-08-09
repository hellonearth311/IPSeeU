import webview
import subprocess
import threading
import time
import sys
import os
import socket

def _has_streamlit(python_exe: str) -> bool:
    try:
        result = subprocess.run(
            [python_exe, "-c", "import streamlit"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.returncode == 0
    except Exception:
        return False


def _find_python_with_streamlit() -> str:
    here = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(here, os.pardir))

    candidates = []
    venv_py = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if os.name == "nt" and os.path.exists(venv_py):
        candidates.append(venv_py)

    candidates.append(sys.executable)

    if os.name == "nt":
        candidates.append("py")

    for py in candidates:
        if _has_streamlit(py):
            return py

    return sys.executable


def _wait_for_port(host: str, port: int, timeout: float = 15.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            try:
                if sock.connect_ex((host, port)) == 0:
                    return True
            except Exception:
                pass
        time.sleep(0.3)
    return False


def _resource_path(relative: str) -> str:
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(__file__)
    return os.path.join(base, relative)


def _run_streamlit_inproc(app_path: str) -> None:
    from streamlit.web import cli as stcli

    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.headless=true",
        "--server.port=8501",
    ]
    stcli.main()


def start_streamlit():
    app_path = _resource_path("app.py")

    if getattr(sys, "frozen", False):
        t = threading.Thread(target=_run_streamlit_inproc, args=(app_path,), daemon=True)
        t.start()
    else:
        python_exe = _find_python_with_streamlit()
        subprocess.Popen(
            [
                python_exe,
                "-m",
                "streamlit",
                "run",
                app_path,
                "--server.headless=true",
                "--server.port=8501",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )

    _wait_for_port("127.0.0.1", 8501, timeout=20.0)

if __name__ == "__main__":
    threading.Thread(target=start_streamlit, daemon=True).start()
    webview.create_window("IPSeeU", "http://localhost:8501", width=1200, height=900)
    webview.start()