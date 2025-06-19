 # main.py
from backend.categorizer import categorize_sessions
from backend.tracker import track_active_window

if __name__ == "__main__":
    track_active_window()
    categorize_sessions()

