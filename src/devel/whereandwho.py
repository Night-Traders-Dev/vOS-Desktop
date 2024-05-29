import os
import platform
import subprocess

def is_android():
    """Check if the operating system is Android."""
    return 'ANDROID_ROOT' in os.environ

def is_termux():
    """Check if the environment is Termux."""
    return os.path.exists('/data/data/com.termux/files/usr/bin/bash')

def is_proot():
    """Check if the environment is Proot."""
    # A common indicator of Proot is the existence of the /usr/bin/env or /usr/bin/proot path
    proot_check = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE, text=True).stdout
    return 'proot' in proot_check.lower()

def is_windows():
    """Check if the operating system is Windows."""
    return platform.system() == 'Windows'

def is_macos():
    """Check if the operating system is macOS."""
    return platform.system() == 'Darwin'

def is_wsl():
    """Check if the environment is WSL (Windows Subsystem for Linux)."""
    if platform.system() == 'Linux':
        with open('/proc/version', 'r') as f:
            version_info = f.read().lower()
        return 'microsoft' in version_info or 'wsl' in version_info
    return False

if __name__ == "__main__":
    running_on_android = is_android()
    running_in_termux = is_termux()
    running_in_proot = is_proot()
    running_on_windows = is_windows()
    running_on_macos = is_macos()
    running_in_wsl = is_wsl()

    print(f"Running on Android: {running_on_android}")
    print(f"Running in Termux: {running_in_termux}")
    print(f"Running in Proot: {running_in_proot}")
    print(f"Running on Windows: {running_on_windows}")
    print(f"Running on macOS: {running_on_macos}")
    print(f"Running in WSL: {running_in_wsl}")
