import psutil

def get_battery_status():
    battery = psutil.sensors_battery()
    if battery is None:
        raise RuntimeError("No battery information available")
    
    return {
        "percentage": battery.percent,
        "plugged": battery.power_plugged,
        "time_left": battery.secsleft
    }

if __name__ == "__main__":
    try:
        battery_status = get_battery_status()
        print("Battery Status:")
        print(f"Percentage: {battery_status['percentage']}%")
        print(f"Plugged: {'Yes' if battery_status['plugged'] else 'No'}")
        time_left = battery_status['time_left']
        if time_left == psutil.POWER_TIME_UNLIMITED:
            print("Time Left: Unlimited")
        elif time_left == psutil.POWER_TIME_UNKNOWN:
            print("Time Left: Unknown")
        else:
            hours, rem = divmod(time_left, 3600)
            minutes, _ = divmod(rem, 60)
            print(f"Time Left: {hours}h {minutes}m")
    except Exception as e:
        print(f"Error: {e}")
