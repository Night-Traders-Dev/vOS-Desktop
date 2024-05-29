import os

def get_battery_status():
    battery_path = "/sys/class/power_supply/BAT0"
    battery_info = {}

    def read_file(file_name):
        with open(os.path.join(battery_path, file_name), 'r') as f:
            return f.read().strip()

    try:
        battery_info['status'] = read_file("status")
        battery_info['percentage'] = int(read_file("capacity"))
        battery_info['voltage_now'] = int(read_file("voltage_now")) // 1000  # in mV
        battery_info['current_now'] = int(read_file("current_now")) // 1000  # in mA
        battery_info['charge_now'] = int(read_file("charge_now")) // 1000    # in mAh
        battery_info['charge_full'] = int(read_file("charge_full")) // 1000  # in mAh
    except FileNotFoundError:
        raise RuntimeError("Battery information not available")

    return battery_info

if __name__ == "__main__":
    try:
        battery_status = get_battery_status()
        print("Battery Status:")
        print(f"Status: {battery_status['status']}")
        print(f"Percentage: {battery_status['percentage']}%")
        print(f"Voltage: {battery_status['voltage_now']} mV")
        print(f"Current: {battery_status['current_now']} mA")
        print(f"Charge Now: {battery_status['charge_now']} mAh")
        print(f"Charge Full: {battery_status['charge_full']} mAh")
    except Exception as e:
        print(f"Error: {e}")
