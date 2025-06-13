import time
import csv
import os
import psutil
import pygetwindow as gw
import win32gui
import win32process

def get_active_window_info():
    try:
        hwnd = win32gui.GetForegroundWindow()  # handle to active window
        window_title = win32gui.GetWindowText(hwnd)

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        process = psutil.Process(pid)
        process_name = process.name()

        return window_title, process_name
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None, None

def log_active_windows():
    last_title = None
    log_file = "data/usage_log.csv"

    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Create the file and write headers if it doesn't exist
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Window Title", "Process Name"])

    print("Tracking started. Press Ctrl+C to stop.")

    try:
        while True:
            window_title, process_name = get_active_window_info()

            # Only log if the window has changed
            if window_title and window_title != last_title:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] {window_title} ({process_name})")

                with open(log_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, window_title, process_name])

                last_title = window_title

            time.sleep(5)
    except KeyboardInterrupt:
        print("\nTracking stopped.")
