# This module provides a function to detect user idle time on Windows.
# It uses the Windows API to get the last input time and calculates the idle duration.
import ctypes

def get_idle_duration():
    """
    Returns idle time in seconds (i.e., time since last user input)
    """
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LII := LASTINPUTINFO)

    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0  # convert to seconds
    else:
        return 0

