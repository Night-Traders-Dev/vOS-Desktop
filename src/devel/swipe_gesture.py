from textual import events
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Static

class SwipeWidget(Static):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_position = None
        self.end_position = None

    async def on_mount(self):
        self.update("Swipe in any direction")

    async def on_mouse_down(self, event: events.MouseDown) -> None:
        self.start_position = (event.x, event.y)

    async def on_mouse_up(self, event: events.MouseUp) -> None:
        self.end_position = (event.x, event.y)
        self.detect_swipe()

    def detect_swipe(self):
        if not self.start_position or not self.end_position:
            return

        start_x, start_y = self.start_position
        end_x, end_y = self.end_position

        delta_x = end_x - start_x
        delta_y = end_y - start_y

        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                direction = "right"
            else:
                direction = "left"
        else:
            if delta_y > 0:
                direction = "down"
            else:
                direction = "up"

        self.update(f"Swipe detected: {direction}")
        self.start_position = None
        self.end_position = None

class SwipeApp(App):
    def compose(self) -> ComposeResult:
        swipe_widget = SwipeWidget()
        await self.view.dock(swipe_widget)

if __name__ == "__main__":
    SwipeApp.run()
