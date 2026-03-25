# Misca_Mouse

This folder contains scripts to automate mouse movement and clicking on Windows.

## Scripts

- `misca_mouse.py` – records the first 10 seconds of mouse movement then replays
  it indefinitely, clicking every minute. Stop with Ctrl+T.
- `clicker.py` – simple tool that optionally launches a batch file from the desktop
  and then clicks at the current cursor location every 10 seconds until Ctrl+T is
  pressed. Place the mouse over your target application before running.
- `camera_mobil.py` – launches the desktop batch, optionally takes a `--device`
  identifier. It then looks for the scrcpy window (by title or device name) and
  drags that window, not merely the currently active one (default 8 cm, modify
  with `--drag-cm`). After repositioning, it moves the mouse to the window centre
  and starts clicking there every 10 seconds; press **Ctrl+T** to stop the clicks.

## Setup

```powershell
cd C:\__tz_pers\CCS\Misca_Mouse\
python -m pip install -r requirements.txt
```

## Usage

1. Double-click or run the batch file `1_Rec_HUAWEI ELE-L09 (Android 10).bat` on
   your desktop if you want the application launched automatically.
2. Position the mouse pointer over the desired window.
3. Run the clicker script:

    ```powershell
    python clicker.py
    ```

4. Press `Ctrl+T` (or Ctrl+C in the terminal) to stop.


The `clicker.py` script is lightweight and only depends on pyautogui/keyboard.
