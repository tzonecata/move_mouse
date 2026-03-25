import ctypes
import time
from ctypes import wintypes
from datetime import datetime

INTERVAL_SECONDS = 300
MOVE_DURATION_SECONDS = 3
MOVE_DISTANCE_CM = 3
STEP_DELAY_SECONDS = 0.2

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]


def get_system_dpi():
    try:
        user32.SetProcessDPIAware()
    except Exception:
        pass

    try:
        get_dpi_for_system = user32.GetDpiForSystem
        get_dpi_for_system.restype = ctypes.c_uint
        dpi = int(get_dpi_for_system())
        if dpi > 0:
            return dpi
    except Exception:
        pass

    hdc = user32.GetDC(0)
    logpixelsx = 88
    dpi = int(gdi32.GetDeviceCaps(hdc, logpixelsx))
    user32.ReleaseDC(0, hdc)
    return dpi if dpi > 0 else 96


def cm_to_pixels(cm, dpi):
    return max(1, int(round((cm / 2.54) * dpi)))


def get_cursor_pos():
    point = POINT()
    user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y


def set_cursor_pos(x, y):
    user32.SetCursorPos(int(x), int(y))


def wiggle_mouse(distance_px, duration_seconds, step_delay_seconds):
    start_x, start_y = get_cursor_pos()
    end_time = time.time() + duration_seconds
    direction = 1

    while time.time() < end_time:
        set_cursor_pos(start_x + direction * distance_px, start_y)
        direction *= -1
        time.sleep(step_delay_seconds)

    set_cursor_pos(start_x, start_y)


def main():
    dpi = get_system_dpi()
    distance_px = cm_to_pixels(MOVE_DISTANCE_CM, dpi)
    print(
        f"Pornit. Distanta miscarii este ~{MOVE_DISTANCE_CM} cm (~{distance_px} pixeli)."
    )
    print("La fiecare 5 minute va misca mouse-ul stanga-dreapta timp de 3 secunde.")
    print("Apasa Ctrl+C pentru oprire.")

    try:
        print(f"Incepe miscare la {datetime.now().strftime('%H:%M:%S')}.")
        wiggle_mouse(distance_px, MOVE_DURATION_SECONDS, STEP_DELAY_SECONDS)
        next_run = time.time() + INTERVAL_SECONDS
        print(
            f"Urmatoarea miscare este programata la {datetime.fromtimestamp(next_run).strftime('%H:%M:%S')}."
        )
        while True:
            wait_seconds = max(0, next_run - time.time())
            time.sleep(wait_seconds)
            print(f"Incepe miscare la {datetime.now().strftime('%H:%M:%S')}.")
            wiggle_mouse(distance_px, MOVE_DURATION_SECONDS, STEP_DELAY_SECONDS)
            next_run += INTERVAL_SECONDS
            print(
                f"Urmatoarea miscare este programata la {datetime.fromtimestamp(next_run).strftime('%H:%M:%S')}."
            )
    except KeyboardInterrupt:
        print("\nOprit.")


if __name__ == "__main__":
    main()
