import os
import shutil
import subprocess
import sys


def _notify_macos(title: str, message: str) -> bool:
    osascript = shutil.which("osascript")
    if not osascript:
        return False

    # Escape quotes for AppleScript string literals.
    t = title.replace('"', '\\"')
    m = message.replace('"', '\\"')
    script = f'display notification "{m}" with title "{t}"'
    subprocess.run(
        [osascript, "-e", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return True


def _notify_linux(title: str, message: str) -> bool:
    notify_send = shutil.which("notify-send")
    if not notify_send:
        return False
    subprocess.run(
        [notify_send, title, message],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return True


def _notify_windows_win10toast(title: str, message: str) -> bool:
    if not sys.platform.startswith("win"):
        return False
    try:
        from win10toast import ToastNotifier  # type: ignore
    except Exception:
        return False

    try:
        ToastNotifier().show_toast(title, message, duration=5, threaded=True)
    except Exception:
        return False
    return True


def notify_done(*, enabled: bool, ok: bool, label: str) -> None:
    if not enabled:
        return

    title = "fish"
    status = "done" if ok else "failed"
    message = f"{status}: {label}" if label else status

    # Best-effort: try OS-specific notifiers, ignore all failures.
    try:
        if _notify_macos(title, message):
            return
        if _notify_linux(title, message):
            return
        if _notify_windows_win10toast(title, message):
            return
    except Exception:
        return
