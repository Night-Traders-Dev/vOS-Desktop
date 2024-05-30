import os
import platform
import subprocess
import psutil
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import humanize

def is_android():
    """Check if the operating system is Android."""
    return 'ANDROID_ROOT' in os.environ

def is_termux():
    """Check if the environment is Termux."""
    return os.path.exists('/data/data/com.termux/files/usr/bin/bash')

def is_proot():
    """Check if the environment is Proot."""
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

def get_cpu_info():
    cpu_info = psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
    if cpu_info:
        for key, value in cpu_info.items():
            if key == 'current':
                cpu_info[key] = f"{value:.2f} MHz"
            else:
                cpu_info[key] = f"{value:.2f} GHz"
    return cpu_info

def get_memory_info():
    mem_info = psutil.virtual_memory()._asdict()
    for key, value in mem_info.items():
        if key != 'percent':
            mem_info[key] = humanize.naturalsize(value)
    return mem_info

def get_disk_usage():
    disk_info = psutil.disk_usage('/')._asdict()
    for key, value in disk_info.items():
        if key != 'percent':
            disk_info[key] = humanize.naturalsize(value)
    return disk_info

def get_network_info():
    try:
        net_io = psutil.net_io_counters(pernic=True)
        net_info = {iface: data._asdict() for iface, data in net_io.items()}
        for iface, data in net_info.items():
            for key, value in data.items():
                if key != 'bytes_sent' and key != 'bytes_recv':
                    net_info[iface][key] = humanize.naturalsize(value)
        return net_info
    except PermissionError as e:
        return str(e)

def get_system_uptime():
    return humanize.naturaldelta(psutil.boot_time())

def get_battery_status_termux():
    termux_battery_status_path = '/data/data/com.termux/files/usr/bin/termux-battery-status'
    result = subprocess.run([termux_battery_status_path], stdout=subprocess.PIPE, text=True)
    return json.loads(result.stdout)

def get_system_info():
    system_info = {
        "platform": platform.system(),
        "platform_version": platform.version(),
        "platform_release": platform.release(),
        "architecture": platform.machine()
    }
    return system_info

def main():
    console = Console()
    
    system_info = get_system_info()
    console.print(Panel(f"System Information: {system_info}", title="System Information", expand=False))

    if is_android():
        console.print("[bold green]Running on Android[/bold green]")
        if is_termux():
            console.print("[bold blue]Environment: Termux[/bold blue]")
            try:
                battery_status = get_battery_status_termux()
                console.print(Panel(f"Battery Status (Termux): {battery_status}", title="Battery Status", expand=False))
            except Exception as e:
                console.print(f"[bold red]Error retrieving Termux battery status: {e}[/bold red]")
        if is_proot():
            console.print("[bold blue]Environment: Proot[/bold blue]")
    elif is_windows():
        console.print("[bold green]Running on Windows[/bold green]")
    elif is_macos():
        console.print("[bold green]Running on macOS[/bold green]")
    elif is_wsl():
        console.print("[bold green]Running on WSL[/bold green]")
    else:
        console.print("[bold green]Running on Linux[/bold green]")

    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    disk_usage = get_disk_usage()
    network_info = get_network_info()
    system_uptime = get_system_uptime()

    cpu_table = Table(title="CPU Info")
    if cpu_info:
        for key, value in cpu_info.items():
            cpu_table.add_row(key, str(value))

    memory_table = Table(title="Memory Info")
    if memory_info:
        for key, value in memory_info.items():
            memory_table.add_row(key, str(value))

    disk_table = Table(title="Disk Usage")
    if disk_usage:
        for key, value in disk_usage.items():
            disk_table.add_row(key, str(value))

    network_table = Table(title="Network Info")
    if isinstance(network_info, str):
        network_table.add_row("Error", network_info)
    else:
        for iface, data in network_info.items():
            for key, value in data.items():
                network_table.add_row(f"{iface} - {key}", str(value))

    console.print(cpu_table)
    console.print(memory_table)
    console.print(disk_table)
    console.print(network_table)
    console.print(Panel(f"System Uptime: {system_uptime}", title="System Uptime", expand=False))

if __name__ == "__main__":
    main()
