from textual.app import App
from components.windows import Window


id = "test_window"
title = "Test Window"
label = "Hello World!"

class TestWindow(App[None]):
    def on_ready(self) -> None:
        try:
            window = self.query_one(f"#[id]")
            if window:
                return
        except Exception as e:
            pass

        self.mount(
            Window(
                x=0,
                y=0,
                width=50,
                height=20,
                label=label,
                title=title,
                id=id
        ))

if __name__ == "__main__":
    TestWindow().run()
