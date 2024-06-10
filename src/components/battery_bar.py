from textual.widgets import ProgressBar
from textual import on, work
import os
import subprocess
from subprocess import Popen
import json
from components.os_check import EnvironmentChecker as os_check


def get_battery_percentage():
    if os_check.is_android() and os_check.is_termux():
        """Retrieve the battery percentage from Android via TermuxAPI"""
        try:
            termux_battery_status_path = '/data/data/com.termux/files/usr/bin/termux-battery-status'
            result = subprocess.run([termux_battery_status_path], stdout=subprocess.PIPE, text=True)
            battery_info = json.loads(result.stdout)
            return battery_info['percentage']
        except:
            return "0"
    elif os_check.is_windows():
         """Retrieve the battery percentage on Windows."""
         try:
             result = subprocess.run(
                 ["powershell", "-Command", "Get-WmiObject -Query 'select * from Win32_Battery'"],
                 stdout=subprocess.PIPE, text=True
             )
             for line in result.stdout.splitlines():
                 if "EstimatedChargeRemaining" in line:
                     percentage = int(line.split()[-1])
                     return percentage
         except:
             return "0"
    elif os_check.is_linux():
        try:
            result = subprocess.run(['acpi', '-b'], stdout=subprocess.PIPE, text=True)
            output = result.stdout

            if output:
                for line in output.splitlines():
                    if 'Battery' in line:
                        percentage = line.split(", ")[1].split("%")[0]
                        return int(percentage)
        except:
            return "0"
    elif os_check.is_macos():
         try:
             result = subprocess.run(['pmset', '-g', 'batt'], stdout=subprocess.PIPE, text=True)
             output = result.stdout

             if output:
                 for line in output.splitlines():
                     if 'InternalBattery' in line:
                         percentage = line.split(';')[1].strip().split('%')[0]
                         return int(percentage)
         except:
             return "0"



class BatteryBar(ProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total = 100
        self.show_eta = False


    DEFAULT_CSS = """

            BatteryBar {
                color: rgb(233, 84, 32);
            }
            BatteryBar Bar {
                width: 4;
            }
            """

    def update_circles(self):
        # Calculate the number of circles to display based on the percentage
        num_circles = int(self.progress / 10)
        filled_circles = "[b #74c7ec]•[/]" * num_circles
        empty_circles = "[b gray]•[/]" * (10 - num_circles)
        self.border_subtitle += f" {filled_circles}{empty_circles}"

    def on_mount(self) -> None:
        battery = get_battery_percentage()
        self.update(progress=battery)
        self.set_interval(10, self.update_battery)

    @work(thread=True, exclusive=True)
    async def update_battery(self) -> None:
        battery = get_battery_percentage()
        self.update(progress=battery)





