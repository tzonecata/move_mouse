import time
import pyautogui
import threading
import keyboard
from pynput import keyboard as pynput_keyboard

"""Simple clicker: after optionally launching a batch, place mouse over target
window/app and run. It will click every 10 seconds until Ctrl+T is pressed."""

CLICK_INTERVAL = 10  # seconds


def click_loop(stop_event: threading.Event):
    last_click = time.time()
    while not stop_event.is_set():
        now = time.time()
        if now - last_click >= CLICK_INTERVAL:
            pyautogui.click()
            last_click = now
        time.sleep(0.1)


if __name__ == "__main__":
    print("Launcher clicker (Ctrl+T to stop). Make sure the desired window is
active and mouse positioned.")
    stop_event = threading.Event()
    try:
        keyboard.add_hotkey('ctrl+t', stop_event.set)
    except Exception:
        pass

    # optional: launch batch file if present on desktop
    import subprocess, os
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    bat = os.path.join(desktop, "1_Rec_HUAWEI ELE-L09 (Android 10).bat")
    if os.path.exists(bat):
        print(f"Running batch: {bat}")
        subprocess.Popen(bat, shell=True)
        time.sleep(2)

    try:
        click_loop(stop_event)
    except KeyboardInterrupt:
        stop_event.set()
        print("Stopped by user (KeyboardInterrupt).")
    finally:
        print("Exiting.")
