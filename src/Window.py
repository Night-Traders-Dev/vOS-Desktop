from textual.app import App
from components.dashboard import Window


id = "dashboard_window"
title = "vOS Dashboard"

class Dashboard(App[None]):
    def on_ready(self) -> None:
        try:
            window = self.query_one(f"#[id]")
            if window:
                return
        except Exception as e:
            pass

        self.mount(Window(0, 0, 50, 20, "", title, id))

if __name__ == "__main__":
    Dashboard().run()
