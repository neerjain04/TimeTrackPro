import os, sys, subprocess, webbrowser
import pystray
from pystray import MenuItem as item
from PIL import Image
import shutil

# === Path Helpers ===
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === Find Python Executable ===
def get_python_executable():
    if hasattr(sys, 'frozen'):
        # Running as exe
        return shutil.which("python") or shutil.which("python3")
    else:
        return sys.executable

# === Load Tray Icon ===
icon_path = resource_path("tray_app/tray_icon.png")
icon_image = Image.open(icon_path)

# === Global Process Trackers ===
tracker_process = None
backend_process = None
frontend_process = None

# === Actions ===
def start_tracking():
    global tracker_process
    if tracker_process is None or tracker_process.poll() is not None:
        tracker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "tracker.py"))
        python_exec = get_python_executable()
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        log_file = os.path.join(project_root, "tracker_output.log")
        tracker_process = subprocess.Popen(
            [python_exec, tracker_path],
            cwd=project_root,
            stdout=open(log_file, "w"),
            stderr=subprocess.STDOUT
        )
        print("🟢 Tracking started. Output will be logged to tracker_output.log.")
    else:
        print("Tracker already running.")

def stop_tracking():
    global tracker_process
    if tracker_process and tracker_process.poll() is None:
        tracker_process.terminate()
        tracker_process.wait(timeout=5)
        tracker_process = None
        print("🛑 Tracking stopped.")
    else:
        print("Tracker is not running.")

def start_backend():
    global backend_process
    if backend_process is None or backend_process.poll() is not None:
        backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "api.py"))
        python_exec = get_python_executable()
        backend_process = subprocess.Popen([python_exec, backend_path])
        print("🚀 Backend started.")
    else:
        print("Backend already running.")

def start_frontend():
    global frontend_process
    if frontend_process is None or frontend_process.poll() is not None:
        dashboard_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dashboard"))
        frontend_process = subprocess.Popen(["npm", "run", "dev"], cwd=dashboard_path, shell=True)
        print("🎨 Frontend started.")
    else:
        print("Frontend already running.")

def open_dashboard():
    webbrowser.open("http://localhost:5173")

def open_timesheet():
    webbrowser.open("http://localhost:5173/timesheet")

def start_all():
    start_backend()
    start_frontend()
    start_tracking()
    print("✅ All services started.")

def quit_app(icon, item):
    stop_tracking()
    global backend_process, frontend_process
    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        backend_process.wait(timeout=5)
    if frontend_process and frontend_process.poll() is None:
        frontend_process.terminate()
        frontend_process.wait(timeout=5)
    icon.stop()

# === Tray Menu ===
menu = pystray.Menu(
    item("📝 Open Employee Timesheet", open_timesheet),
    item("📊 Open Dashboard", open_dashboard),
    item("❌ Exit", quit_app)
)

if __name__ == "__main__":
    # === Run Tray Icon ===
    icon = pystray.Icon("TimeTrackPro", icon_image, "TimeTrackPro", menu)
    icon.run()
