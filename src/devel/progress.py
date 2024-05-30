from textual.app import App, ComposeResult
from textual.containers import Center
from textual.widgets import ProgressBar
import os
import subprocess
import json

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

def get_battery_percentage():
    if is_android():
        if is_termux():
            termux_battery_status_path = '/data/data/com.termux/files/usr/bin/termux-battery-status'
            result = subprocess.run([termux_battery_status_path], stdout=subprocess.PIPE, text=True)
            battery_info = json.loads(result.stdout)
            return battery_info['percentage']
        elif is_proot():
            # Return battery percentage for Proot environment
            return "Battery percentage not available in Proot environment"
        else:
            # Return battery percentage for Android devices without Termux or Proot
            return "Battery percentage not available in this Android environment"
    else:
        # Return battery percentage for non-Android environments
        return "Battery percentage not available in non-Android environment"




class FundingProgressApp(App[None]):
    DEFAULT_CSS = """

            Container {
                overflow: hidden hidden;
                height: auto;
            }

            Center {
                margin-top: 1;
                margin-bottom: 1;
                layout: horizontal;
            }
            Bar {
                width: 10;
            }

            ProgressBar {
                padding-left: 3;
                color: rgb(233, 84, 32);
            }
            """
    def compose(self) -> ComposeResult:
        with Center():
            yield ProgressBar(total=100, show_eta=False)  


    def on_mount(self) -> None:
        battery = get_battery_percentage()
        self.query_one(ProgressBar).update(progress=battery)
        self.set_interval(10, self.update_battery)
    def update_battery(self) -> None:
        battery = get_battery_percentage()
        current = self.query_one(ProgressBar).percentage * 100
        self.query_one(ProgressBar).update(progress=battery)



if __name__ == "__main__":
    FundingProgressApp().run()
