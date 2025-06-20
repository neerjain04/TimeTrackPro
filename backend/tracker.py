import sys, os
print(f"[DEBUG] tracker.py started. CWD: {os.getcwd()}")
# Always resolve project root, regardless of CWD
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
labeled_abs = os.path.join(project_root, "data", "labeled_log.csv")
print(f"[DEBUG] Absolute path to labeled_log.csv: {labeled_abs}")
sys.path.append(project_root)

# This script tracks the active window and process on a Windows machine and logs the usage data to a CSV file.
# It captures the window title, process name, and duration of usage for each active window.
import time
import csv
from datetime import datetime
import psutil
import pygetwindow as gw
import pygetwindow._pygetwindow_win as win
import win32gui
import win32process
import os
from backend.idle_detector import get_idle_duration

# This function retrieves the title of the currently active window and the name of the process associated with it.
def get_active_window_title_and_process():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        process_name = process.name()
        window_title = win32gui.GetWindowText(hwnd)
        return window_title, process_name
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None, None

# This function tracks the active window and logs the usage data.
# It checks for idle time and categorizes the usage into "Meal" or "Idle"
def track_active_window():
    last_window = None
    last_process = None
    is_idle = False
    idle_start_time = None
    start_time = datetime.now()
    short_idle_threshold = 5
    meal_idle_duration = 1800  # 30 minutes

    labeled_path = labeled_abs
    os.makedirs(os.path.dirname(labeled_path), exist_ok=True)
    if not os.path.exists(labeled_path):
        with open(labeled_path, "w", newline="", encoding="utf-8") as lf:
            writer = csv.writer(lf)
            writer.writerow(["Start Time", "End Time", "Duration", "Category", "Window Title", "Process Name"])

    print("Tracking started. Press Ctrl+C to stop.")

    try:
        while True:
            current_window, current_process = get_active_window_title_and_process()
            idle_secs = get_idle_duration()

            # User just went idle
            if not is_idle and idle_secs > short_idle_threshold:
                is_idle = True
                idle_start_time = datetime.now()

            # User came back after being idle
            if is_idle and idle_secs < short_idle_threshold:
                is_idle = False
                if idle_start_time:
                    idle_duration = datetime.now() - idle_start_time
                    if idle_duration.total_seconds() >= meal_idle_duration:
                        category = "Meal" if 11 <= idle_start_time.hour <= 14 else "Idle"
                        log_session(idle_start_time, datetime.now(), category, category, labeled_path)
                    idle_start_time = None  # Reset after handling

            # Active window tracking (only when not idle)
            if not is_idle and (current_window != last_window or current_process != last_process):
                end_time = datetime.now()
                if last_window:
                    log_session(start_time, end_time, last_window, last_process, labeled_path)
                last_window = current_window
                last_process = current_process
                start_time = datetime.now()

            print(f"{'Idle' if is_idle else 'Active'}: {idle_secs} seconds")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Tracking stopped.")
        end_time = datetime.now()
        if last_window:
            log_session(start_time, end_time, last_window, last_process, labeled_path)


# This function logs the session data to labeled_log.csv only.
def log_session(start_time, end_time, window_title, process_name, labeled_path):
    duration = end_time - start_time
    try:
        import json
        print(f"[DEBUG] log_session called: {start_time} - {end_time}, window: {window_title}, process: {process_name}, file: {labeled_path}")
        category_map = {}
        with open(os.path.join(os.path.dirname(__file__), "..", "app_categories.json"), "r", encoding="utf-8") as catf:
            category_map = json.load(catf)
        file_exists = os.path.exists(labeled_path)
        with open(labeled_path, "a", newline="", encoding="utf-8") as lf:
            writer = csv.writer(lf)
            if not file_exists:
                writer.writerow(["Start Time", "End Time", "Duration", "Category", "Window Title", "Process Name"])
            category = category_map.get(process_name, "other")
            print(f"[DEBUG] Writing row: {start_time.strftime('%Y-%m-%d %H:%M:%S')}, {end_time.strftime('%Y-%m-%d %H:%M:%S')}, {str(duration).split('.')[0]}, {category}, {window_title}, {process_name}")
            writer.writerow([
                start_time.strftime("%Y-%m-%d %H:%M:%S"),
                end_time.strftime("%Y-%m-%d %H:%M:%S"),
                str(duration).split('.')[0],
                category,
                window_title,
                process_name
            ])
    except Exception as e:
        print(f"[log_session] Could not update labeled_log.csv: {e}")

if __name__ == "__main__":
    track_active_window()
