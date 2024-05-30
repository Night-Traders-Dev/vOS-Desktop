import subprocess
import json
from rich.console import Console

def get_battery_percentage():
    try:
        # Path to the termux-battery-status binary
        termux_battery_status_path = '/data/data/com.termux/files/usr/bin/termux-battery-status'

        # Run the termux-battery-status command directly
        result = subprocess.run([termux_battery_status_path], stdout=subprocess.PIPE, text=True)

        # Check if the command executed successfully and the output is not empty
        if result.returncode == 0 and result.stdout:
            # Parse the JSON output
            battery_info = json.loads(result.stdout)
            percentage = battery_info['percentage']
            return percentage
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def draw_battery_indicator(percentage):
    # Battery width and height
    battery_width = 10
    battery_height = 5

    # Calculate the number of filled cells
    filled_cells = int((percentage / 100) * battery_width)

    # Generate battery string
    battery_string = ""
    for i in range(battery_width):
        if i < filled_cells:
            battery_string += "█"  # Filled cell
        else:
            battery_string += "░"  # Empty cell

    # Add percentage to the battery string
    battery_string += f" {percentage}%"
    return battery_string

def main():
    # Get battery percentage
    percentage = get_battery_percentage()

    if percentage is not None:
        # Draw battery indicator
        battery_string = draw_battery_indicator(percentage)

        # Display battery indicator
        console = Console()
        console.print(battery_string)
    else:
        print("Failed to get battery status")

if __name__ == "__main__":
    main()
