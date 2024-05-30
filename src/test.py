from rich.console import Console
from rich.style import Style

def draw_battery_indicator(percentage):
    # Define battery and lightning Unicode characters
    battery_icon = "🔋"
    charge_symbol = "🪫"

    # Define colors for battery icon and charge symbol
    battery_color = "yellow"
    charge_color = "cyan"

    # Define battery width and height
    battery_width = 10

    # Calculate number of filled cells
    filled_cells = int((percentage / 100) * battery_width)

    # Create a Rich Console object
    console = Console()

    # Draw battery icon with charge symbol
    battery_string = f"{battery_icon} {charge_symbol} "
    battery_string += " " * filled_cells
    battery_string += " " * (battery_width - filled_cells)
    battery_string += f" {percentage}%"

    # Print battery icon with custom style
    console.print(battery_string, style=Style(color=battery_color))

def main():
    # Example battery percentage
    percentage = 75

    # Draw battery indicator
    draw_battery_indicator(percentage)

if __name__ == "__main__":
    main()
