from pathlib import Path
import subprocess
import time


def desktop_candidates() -> list[Path]:
    home = Path.home()
    candidates = [home / "Desktop", home / "OneDrive" / "Desktop"]
    return [path for path in candidates if path.exists()]


def find_bat(desktop_dirs: list[Path], expected_name: str) -> Path | None:
    for desktop in desktop_dirs:
        candidate = desktop / expected_name
        if candidate.exists():
            return candidate
    return None


def launch_bat(bat_file: Path) -> None:
    # Start each .bat in its own cmd window.
    subprocess.Popen(["cmd", "/c", "start", "", str(bat_file)], shell=False)


def close_scrcpy_processes() -> None:
    subprocess.run(
        ["taskkill", "/F", "/IM", "scrcpy.exe", "/T"],
        capture_output=True,
        text=True,
        check=False,
    )


def close_all_cmd_processes() -> None:
    subprocess.run(
        ["taskkill", "/F", "/IM", "cmd.exe", "/T"],
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    expected_bats = [
        "1_Rec_HUAWEI ELE-L09 (Android 10).bat",
        "2_Madoka_Galaxy A23 5G.bat",
    ]

    desktops = desktop_candidates()
    if not desktops:
        print("Nu am gasit un folder Desktop valid.")
        return 1

    resolved_bats: list[Path] = []
    missing: list[str] = []

    for bat_name in expected_bats:
        bat_path = find_bat(desktops, bat_name)
        if bat_path is None:
            missing.append(bat_name)
        else:
            resolved_bats.append(bat_path)

    if missing:
        print("Nu am gasit urmatoarele fisiere:")
        for bat_name in missing:
            print(f"- {bat_name}")
        return 1

    close_scrcpy_processes()
    close_all_cmd_processes()
    time.sleep(0.5)

    for bat_file in resolved_bats:
        launch_bat(bat_file)
        time.sleep(0.5)

    print("Am pornit ambele scripturi .bat.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
