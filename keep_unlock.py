import time
import threading
try:
    import pyautogui
except Exception as e:
    print("Error importing pyautogui:", e)
    raise
try:
    import keyboard
except Exception:
    keyboard = None
from pynput import keyboard as pynput_keyboard

pyautogui.FAILSAFE = True

# Configuration
INTERVAL_SECONDS = 60       # wait between bursts
BURST_DURATION = 2         # how long the quick visible movement lasts
OFFSET = 150               # pixels left/right from center
STEP_PIXELS = 8            # pixels per small move step
STEP_DELAY = 0.02          # seconds between small steps (smaller = faster)


def burst_move_center(stop_event: threading.Event):
    """Move the mouse left-right around center for BURST_DURATION seconds."""
    width, height = pyautogui.size()
    cx = width // 2
    cy = height // 2
    left_x = max(0, cx - OFFSET)
    right_x = min(width - 1, cx + OFFSET)

    start = time.time()
    x = cx
    direction = -1
    while time.time() - start < BURST_DURATION and not stop_event.is_set():
        # update screen size in case of display changes
        width, height = pyautogui.size()
        cy = height // 2
        left_x = max(0, width // 2 - OFFSET)
        right_x = min(width - 1, width // 2 + OFFSET)

        if direction == -1:
            x = max(x - STEP_PIXELS, left_x)
        else:
            x = min(x + STEP_PIXELS, right_x)

        try:
            pyautogui.moveTo(x, cy, duration=0)
        except Exception:
            pass

        if x <= left_x:
            direction = 1
        elif x >= right_x:
            direction = -1

        # small sleep to control visible speed and allow stop_event check
        slept = 0.0
        while slept < STEP_DELAY and not stop_event.is_set():
            time.sleep(min(0.005, STEP_DELAY - slept))
            slept += 0.005


def keep_unlock_loop(stop_event: threading.Event):
    last_burst = time.time() - INTERVAL_SECONDS  # trigger immediately if desired
    while not stop_event.is_set():
        now = time.time()
        if now - last_burst >= INTERVAL_SECONDS:
            # perform visible quick movement for BURST_DURATION seconds
            burst_move_center(stop_event)
            last_burst = time.time()
        # sleep a little and re-check
        time.sleep(0.5)


def main():
    print("keep_unlock: moves mouse left-right for 2s every 60s. Press Ctrl+T to stop.")
    stop_event = threading.Event()
    # try keyboard hotkey first
    if keyboard:
        try:
            keyboard.add_hotkey('ctrl+t', stop_event.set)
        except Exception:
            pass

    # also register pynput hotkey as fallback
    def on_activate():
        stop_event.set()

    hotkeys = pynput_keyboard.GlobalHotKeys({'<ctrl>+t': on_activate})
    hotkeys.start()

    try:
        keep_unlock_loop(stop_event)
    except KeyboardInterrupt:
        stop_event.set()

    hotkeys.stop()
    print('Stopped.')


if __name__ == '__main__':
    main()
