import argparse
import ctypes
import time
from datetime import datetime

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
DEFAULT_REFRESH_SECONDS = 180.0

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.SetThreadExecutionState.argtypes = [ctypes.c_uint]
kernel32.SetThreadExecutionState.restype = ctypes.c_uint


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def log(message):
    print(f"[{timestamp()}] {message}", flush=True)


def format_interval(seconds):
    if seconds.is_integer() and int(seconds) % 60 == 0:
        minutes = int(seconds) // 60
        unit = "minut" if minutes == 1 else "minute"
        return f"{minutes} {unit}"
    return f"{seconds:g} secunde"


def format_flags(value):
    names = []
    if value & ES_CONTINUOUS:
        names.append("ES_CONTINUOUS")
    if value & ES_SYSTEM_REQUIRED:
        names.append("ES_SYSTEM_REQUIRED")
    if value & ES_DISPLAY_REQUIRED:
        names.append("ES_DISPLAY_REQUIRED")

    if names:
        return f"0x{value:08X} ({', '.join(names)})"
    return f"0x{value:08X}"


def set_execution_state(flags, label):
    ctypes.set_last_error(0)
    previous_state = kernel32.SetThreadExecutionState(flags)
    last_error = ctypes.get_last_error()

    if previous_state == 0:
        log(
            f"{label}: EROARE. flags={format_flags(flags)} "
            f"GetLastError={last_error}"
        )
        return False

    log(
        f"{label}: OK. flags={format_flags(flags)} "
        f"previous={format_flags(previous_state)}"
    )
    return True


def enable_keep_awake():
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    return set_execution_state(flags, "Enable keep-awake")


def refresh_keep_awake():
    flags = ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    return set_execution_state(flags, "Refresh keep-awake")


def disable_keep_awake():
    return set_execution_state(ES_CONTINUOUS, "Disable keep-awake")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tine PC-ul activ fara sa miste mouse-ul."
    )
    parser.add_argument(
        "--refresh-seconds",
        type=float,
        default=DEFAULT_REFRESH_SECONDS,
        help="La cate secunde sa reaplice keep-awake si sa scrie heartbeat in consola.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.refresh_seconds <= 0:
        raise SystemExit("--refresh-seconds trebuie sa fie > 0")

    log("keep_unlock pornit.")
    log("Nu misca mouse-ul. Nu apasa taste.")
    log(
        "Foloseste doar Windows SetThreadExecutionState pentru a preveni idle, "
        "sleep si display-off."
    )
    log(f"Heartbeat la fiecare {format_interval(args.refresh_seconds)}.")
    log("Apasa Ctrl+C pentru oprire.")

    enabled = enable_keep_awake()
    if not enabled:
        log("Activarea keep-awake a esuat. Scriptul se opreste.")
        return 1

    log(
        "Verificare practica: lasa timeout-ul de lock/screen saver la 1 minut si "
        "urmareste daca sistemul ramane activ cat timp apar heartbeat-urile."
    )

    try:
        while True:
            time.sleep(args.refresh_seconds)
            refresh_keep_awake()
    except KeyboardInterrupt:
        log("Ctrl+C detectat. Oprire ceruta de utilizator.")
    finally:
        disable_keep_awake()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
