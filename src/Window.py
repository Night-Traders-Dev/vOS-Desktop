from textual.app import App
from components.dashboard import Window

class Dashboard(App[None]):
    def on_ready(self) -> None:
        try:
            window = self.query_one("#dashboard_window")
            if window:
                return
        except Exception as e:
            pass

        screen_width, screen_height = self.size

        center_x = screen_width // 2
        center_y = screen_height // 2

        center_x = center_x - (50 // 2)
        center_y = center_y - (20 // 2)

        self.mount(Window(center_x, center_y, 50, 20, "", "vOS Dashboard", "dashboard_window"))

if __name__ == "__main__":
    Dashboard().run()
