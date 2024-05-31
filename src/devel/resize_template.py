from textual.app import App, ComposeResult
from textual.widgets import Static, Label
from textual.events import Resize
from textual.geometry import Region, Size
from textual import on, events

class ResizableWidget(Static):
    """A resizable widget that updates its offset on resize."""

    def __init__(self, label: str) -> None:
        self.label = label
        super().__init__()

    def on_mount(self) -> None:
        self.update(self.label)

    def update_offset(self, x: int, y: int) -> None:
        """Update the widget's offset based on the new width and height."""
        # Calculate the new offset
        if x != 0:
            new_offset_x = x - 6
        else:
            new_offset_x = 0
        if y != 0:
            new_offset_y = y - 1
        else:
            new_offset_y = 0
            self.styles.offset = (new_offset_x, new_offset_y)

    def render(self) -> str:
        return self.label


class ResizeApp(App):
    def compose(self) -> ComposeResult:
        self.resizable_widget = ResizableWidget(label="#Test#")
        self.info = Label(f"Widget: {self.resizable_widget.region}\nTerminal: {self.size}")
        yield self.resizable_widget
        yield self.info



    def on_resize(self, event: Resize) -> None:
        # Handle the resize event and update the widget's offset
        x, y = self.size
        self.resizable_widget.update_offset((x), (y))
        self.info.update(f"Widget: {self.resizable_widget.region}\nTerminal: {self.size}")
        self.refresh()



if __name__ == "__main__":
    app = ResizeApp()
    app.run()
