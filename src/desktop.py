import webview
import subprocess
import time
import sys
import os
import socket
import urllib.request

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


def _wait_for_first_open_port(host: str, ports: list[int], timeout: float = 30.0) -> int | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        for port in ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.3)
                try:
                    if sock.connect_ex((host, port)) == 0:
                        return port
                except Exception:
                    pass
        time.sleep(0.3)
    return None


def _resource_path(relative: str) -> str:
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(__file__)
    return os.path.join(base, relative)


def _run_streamlit_inproc(app_path: str) -> None:
    import traceback
    from streamlit.web import cli as stcli
    try:
        # Log startup details
        with open("streamlit_error.log", "a", encoding="utf-8") as f:
            f.write(f"Starting Streamlit server for app: {app_path}\n")
            f.write(f"App exists: {os.path.exists(app_path)}\n")
        
        sys.argv = [
            "streamlit",
            "run",
            app_path,
            "--server.headless=true",
            "--server.address=127.0.0.1",
            "--global.developmentMode=false",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
        ]
        os.environ["STREAMLIT_GLOBAL_DEVELOPMENTMODE"] = "false"
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        
        with open("streamlit_error.log", "a", encoding="utf-8") as f:
            f.write(f"About to call stcli.main() with args: {sys.argv}\n")
        
        stcli.main()
    except Exception as e:
        with open("streamlit_error.log", "w", encoding="utf-8") as f:
            f.write("Streamlit in-process failed:\n")
            f.write(traceback.format_exc())


def _start_streamlit_server_subprocess() -> None:
    """Start a dedicated server process running this script in --server mode."""
    if getattr(sys, "frozen", False):
        cmd = [sys.executable, "--server"]
    else:
        cmd = [sys.executable, os.path.abspath(__file__), "--server"]
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    subprocess.Popen(cmd, creationflags=creationflags)


def start_streamlit() -> int | None:
    import traceback
    app_path = _resource_path("app.py")
    if not os.path.exists(app_path):
        with open("streamlit_error.log", "w", encoding="utf-8") as f:
            f.write(f"app.py not found at {app_path}\n")
        return None
    try:
        _start_streamlit_server_subprocess()
    except Exception:
        with open("streamlit_error.log", "w", encoding="utf-8") as f:
            f.write("Failed to start server subprocess:\n")
            f.write(traceback.format_exc())
    port = _wait_for_first_open_port("127.0.0.1", list(range(8501, 8511)), timeout=45.0)
    if port is None:
        with open("streamlit_error.log", "a", encoding="utf-8") as f:
            f.write("Timed out waiting for Streamlit to open a port.\n")
        return None

    deadline = time.time() + 30.0
    health_url = f"http://127.0.0.1:{port}/_stcore/health"
    root_url = f"http://127.0.0.1:{port}/"
    healthy = False
    
    with open("streamlit_error.log", "a", encoding="utf-8") as f:
        f.write(f"Waiting for health check on port {port}...\n")
    
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(health_url, timeout=2) as resp:
                body = resp.read().decode("utf-8", errors="ignore").strip().lower()
                if resp.status == 200 and body in ("ok", "healthy"):
                    healthy = True
                    with open("streamlit_error.log", "a", encoding="utf-8") as f:
                        f.write(f"Health check passed on port {port}.\n")
                    break
        except Exception as e:
            with open("streamlit_error.log", "a", encoding="utf-8") as f:
                f.write(f"Health check attempt failed: {e}\n")
        time.sleep(0.3)
    
    if not healthy:
        with open("streamlit_error.log", "a", encoding="utf-8") as f:
            f.write(f"Health check did not pass for port {port}.\n")
        return None
    
    try:
        with urllib.request.urlopen(root_url, timeout=5) as resp:
            with open("streamlit_error.log", "a", encoding="utf-8") as f:
                f.write(f"Root page check: {resp.status} (Length: {len(resp.read())})\n")
    except Exception as e:
        with open("streamlit_error.log", "a", encoding="utf-8") as f:
            f.write(f"Root page check failed: {e}\n")
            
        alt_paths = ["/", "/app", "/streamlit", f"/{os.path.basename(app_path)}", "/?"]
        for path in alt_paths:
            try:
                alt_url = f"http://127.0.0.1:{port}{path}"
                with urllib.request.urlopen(alt_url, timeout=2) as resp:
                    if resp.status == 200:
                        with open("streamlit_error.log", "a", encoding="utf-8") as f:
                            f.write(f"Found working path: {alt_url} -> {resp.status}\n")
                        break
            except Exception:
                continue
        else:
            diagnostic_urls = [
                f"http://127.0.0.1:{port}/_stcore/health",
                f"http://127.0.0.1:{port}/_stcore/static/",
                f"http://127.0.0.1:{port}/healthz",
                f"http://127.0.0.1:{port}/app",
                f"http://127.0.0.1:{port}/favicon.ico",
            ]
            with open("streamlit_error.log", "a", encoding="utf-8") as f:
                f.write("No working alternative paths found. Diagnostic checks:\n")
                for diag_url in diagnostic_urls:
                    try:
                        with urllib.request.urlopen(diag_url, timeout=2) as resp:
                            f.write(f"  {diag_url} -> {resp.status}\n")
                    except Exception as e:
                        f.write(f"  {diag_url} -> FAILED: {e}\n")
    
    return port

def _is_server_mode() -> bool:
    return any(arg == "--server" for arg in sys.argv[1:])


if __name__ == "__main__":
    if _is_server_mode():
        app_path = _resource_path("app.py")
        _run_streamlit_inproc(app_path)
    else:
        port = start_streamlit()
        if port is None:
            error_html = (
                "<html><body style='font-family:Segoe UI, sans-serif; padding:2rem'>"
                "<h2>IPSeeU failed to start</h2>"
                "<p>Streamlit server did not become healthy. Please check streamlit_error.log for details, then close and try again.</p>"
                "</body></html>"
            )
            webview.create_window("IPSeeU - Startup Error", html=error_html, width=700, height=300)
        else:
            url = f"http://localhost:{port}"
            webview.create_window("IPSeeU", url, width=1200, height=900)
        webview.start()