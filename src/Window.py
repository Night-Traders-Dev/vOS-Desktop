from textual.app import App
from components.dashboard import Window

class Dashboard(App[None]):

    DEFAULT_CSS = """
            WindowTemplate {
                align: center middle;
            }
            """

    def on_click(self) -> None:
        try:
            window = self.query_one("#window")
            if window:
                return
        except Exception as e:
            pass

        screen_width, screen_height = self.size

        center_x = screen_width // 2
        center_y = screen_height // 2

        center_x = center_x - (50 // 2)
        center_y = center_y - (20 // 2)

        self.mount(Window(center_x, center_y, 50, 20, f"\nTerm: {self.size}\nWindow: ({center_x}, {center_y})", "vOS UI", "window"))

if __name__ == "__main__":
    Dashboard().run()
