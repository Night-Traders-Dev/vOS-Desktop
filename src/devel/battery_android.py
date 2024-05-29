import subprocess
import json

def get_battery_status():
    # Path to the termux-battery-status binary
    termux_battery_status_path = '/data/data/com.termux/files/usr/bin/termux-battery-status'
    
    # Run the termux-battery-status command directly
    result = subprocess.run([termux_battery_status_path], stdout=subprocess.PIPE, text=True)
    
    # Check if the command executed successfully and the output is not empty
    if result.returncode == 0 and result.stdout:
        # Parse the JSON output
        battery_info = json.loads(result.stdout)
        return battery_info
    else:
        raise RuntimeError("Failed to get battery status")

if __name__ == "__main__":
    try:
        battery_status = get_battery_status()
        print("Battery Status:")
        print(f"Health: {battery_status['health']}")
        print(f"Percentage: {battery_status['percentage']}%")
        print(f"Plugged: {battery_status['plugged']}")
        print(f"Status: {battery_status['status']}")
        print(f"Temperature: {battery_status['temperature']}°C")
        print(f"Voltage: {battery_status['voltage']}mV")
    except Exception as e:
        print(f"Error: {e}")
