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

    file_path = os.path.join("data", "usage_log.csv")
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Start Time", "End Time", "Duration", "Window Title", "Process Name"])

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
                        log_session(idle_start_time, datetime.now(), category, category, file_path)
                    idle_start_time = None  # Reset after handling

            # Active window tracking (only when not idle)
            if not is_idle and (current_window != last_window or current_process != last_process):
                end_time = datetime.now()
                if last_window:
                    log_session(start_time, end_time, last_window, last_process, file_path)
                last_window = current_window
                last_process = current_process
                start_time = datetime.now()

            print(f"{'Idle' if is_idle else 'Active'}: {idle_secs} seconds")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Tracking stopped.")
        end_time = datetime.now()
        if last_window:
            log_session(start_time, end_time, last_window, last_process, file_path)


# This function logs the session data to a CSV file.
# It records the start time, end time, duration, window title, and process name.
def log_session(start_time, end_time, window_title, process_name, file_path):
    duration = end_time - start_time
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            str(duration).split('.')[0],
            window_title,
            process_name
        ])
