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

# This function tracks the active window and logs the usage data to a CSV file.
def track_active_window():
    last_window = None
    last_process = None
    start_time = datetime.now()

    file_path = os.path.join("data", "usage_log.csv")

    # Write header if file doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Start Time", "End Time", "Duration", "Window Title", "Process Name"])

    print("Tracking started. Press Ctrl+C to stop.")

    try:
        while True:
            current_window, current_process = get_active_window_title_and_process()
            if current_window and (current_window != last_window):
                end_time = datetime.now()
                if last_window:
                    duration = end_time - start_time
                    with open(file_path, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            start_time.strftime("%Y-%m-%d %H:%M:%S"),
                            end_time.strftime("%Y-%m-%d %H:%M:%S"),
                            str(duration).split('.')[0],
                            last_window,
                            last_process
                        ])
                # Update tracker
                last_window = current_window
                last_process = current_process
                start_time = datetime.now()

            time.sleep(1)

    except KeyboardInterrupt:
        print("Tracking stopped.")
        # Log the final window before exit
        end_time = datetime.now()
        if last_window:
            duration = end_time - start_time
            with open(file_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    str(duration).split('.')[0],
                    last_window,
                    last_process
                ])
