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

        self.mount(Window(0, 0, 50, 20, "", "vOS Dashboard", "dashboard_window"))

if __name__ == "__main__":
    Dashboard().run()
