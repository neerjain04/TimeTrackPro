 # This is the main entry point for the application.
# It initializes the tracker and categorizer modules to start tracking and categorizing application usage.
from backend.categorizer import categorize_sessions
from backend.tracker import track_active_window

if __name__ == "__main__":
    track_active_window()
    categorize_sessions()

