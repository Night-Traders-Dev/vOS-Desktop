import os
import platform
import subprocess

class EnvironmentChecker:
    """Class to check various operating systems and environments."""

    @staticmethod
    def is_android():
        """Check if the operating system is Android."""
        return 'ANDROID_ROOT' in os.environ

    @staticmethod
    def is_termux():
        """Check if the environment is Termux."""
        return os.path.exists('/data/data/com.termux/files/usr/bin/bash')

    @staticmethod
    def is_proot():
        """Check if the environment is Proot."""
        proot_check = subprocess.run(['uname', '-a'], stdout=subprocess.PIPE, text=True).stdout
        return 'proot' in proot_check.lower()

    @staticmethod
    def is_windows():
        """Check if the operating system is Windows."""
        return platform.system() == 'Windows'

    @staticmethod
    def is_macos():
        """Check if the operating system is macOS."""
        return platform.system() == 'Darwin'

    @staticmethod
    def is_wsl():
        """Check if the environment is WSL (Windows Subsystem for Linux)."""
        if platform.system() == 'Linux':
            with open('/proc/version', 'r') as f:
                version_info = f.read().lower()
            return 'microsoft' in version_info or 'wsl' in version_info
        return False

