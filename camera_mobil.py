import argparse
import os
import subprocess
import threading
import time

import pyautogui
import pygetwindow as gw
import keyboard
from pynput import keyboard as pynput_keyboard

"""Utility for mobile camera window.

- launches the bat file on desktop
- clicks the title bar of the active window and drags it ~4cm to the right
- then positions the cursor at the center of that window

"""

# constants
CM_TO_PIXELS = 37.8  # approx for 96 DPI
DEFAULT_DRAG_CM = 8  # default how far to move the window (in centimeters)
CLICK_DELAY = 0.5     # seconds to wait after launching


def launch_batch():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    bat = os.path.join(desktop, "1_Rec_HUAWEI ELE-L09 (Android 10).bat")
    if os.path.exists(bat):
        subprocess.Popen(bat, shell=True)
        return True
    return False


def find_scrcpy_window(device_hint: str = None):
    """Return a window object whose title appears to be the scrcpy stream.
    If device_hint is provided, match that substring first, otherwise choose the
    active window or the first window named like a device.
    """
    # try active window first
    win = gw.getActiveWindow()
    if win and ("scrcpy" in win.title.lower() or (device_hint and device_hint in win.title)):
        return win
    # otherwise search all windows
    for w in gw.getAllWindows():
        title = w.title.lower()
        if "scrcpy" in title or (device_hint and device_hint.lower() in title.lower()):
            return w
    return None


def shift_active_window_right(cm: float, device_hint: str = None):
    win = find_scrcpy_window(device_hint)
    if not win:
        return False
    px = int(cm * CM_TO_PIXELS)
    # click approximately on the title bar (left of window)
    title_y = win.top + 10
    click_x = win.left + 50
    pyautogui.moveTo(click_x, title_y, duration=0.2)
    pyautogui.mouseDown()
    pyautogui.moveRel(px, 0, duration=0.5)
    pyautogui.mouseUp()
    return True


def center_cursor_on_active_window():
    win = gw.getActiveWindow()
    if not win:
        return False
    cx = win.left + win.width // 2
    cy = win.top + win.height // 2
    pyautogui.moveTo(cx, cy, duration=0.2)
    return True


def parse_args():
    parser = argparse.ArgumentParser(description="Launch camera script and adjust its window")
    parser.add_argument("--device", help="device identifier (e.g. ELE_L09)")
    parser.add_argument("--drag-cm", type=float, default=DEFAULT_DRAG_CM,
                        help="how many centimetres to shift the window to the right")
    return parser.parse_args()


def click_loop(stop_event: threading.Event, interval: float = 10.0):
    """Click at current cursor location every `interval` seconds until stopped."""
    last = time.time()
    while not stop_event.is_set():
        now = time.time()
        if now - last >= interval:
            pyautogui.click()
            last = now
        time.sleep(0.1)


if __name__ == "__main__":
    args = parse_args()
    print("camera_mobil: launching bat and adjusting window")
    if args.device:
        print(f"(requested device: {args.device})")

    stop_event = threading.Event()
    try:
        keyboard.add_hotkey('ctrl+t', stop_event.set)
    except Exception:
        pass
    # also register pynput
    def on_activate():
        stop_event.set()
    hotkeys = pynput_keyboard.GlobalHotKeys({'<ctrl>+t': on_activate})
    hotkeys.start()

    launched = launch_batch()
    if launched:
        # give the application a bit of time to appear/move focus
        time.sleep(CLICK_DELAY)
    # now shift and center using requested drag distance
    shifted = shift_active_window_right(args.drag_cm, device_hint=args.device)
    if shifted:
        time.sleep(0.1)
        center_cursor_on_active_window()

    # begin clicking loop until stopped
    print("Starting click loop (Ctrl+T to quit)...")
    try:
        click_loop(stop_event, interval=10.0)
    except KeyboardInterrupt:
        stop_event.set()
    print("Done.")
