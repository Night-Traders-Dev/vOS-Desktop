from textual.app import App, ComposeResult
from textual.widgets import Static, Label
from textual.events import Resize, Click
from textual.geometry import Size
import random

class ResizableWidget(Static):
    """A resizable widget that updates its offset on resize."""

    def __init__(self, label: str) -> None:
        self.label = label
        super().__init__()

    def on_mount(self) -> None:
        self.update(self.label)

    def update_offset(self, x: int, y: int) -> None:
        """Update the widget's offset based on the new width and height."""
        new_offset_x = random.randint(0, x - 10)
        new_offset_y = random.randint(0, y - 10)
        self.styles.offset = (new_offset_x, new_offset_y)

    def render(self) -> str:
        return self.label


class ResizeApp(App):
    def __init__(self):
        super().__init__()
        self.widgets = []  # List to store widget references

    def compose(self) -> ComposeResult:
        self.resizable_widget = ResizableWidget(label=f"widget-{random.randint(0, 9999)}")
        self.info = Label()
        self.resizable_widget.styles.width = 10
        yield self.resizable_widget
        yield self.info

        self.widgets.append(self.resizable_widget)  # Add initial widget to the list
        self.update_info()

    def update_info(self):
        """Update the info label with the details of all widgets."""
        widget_info = "\n".join(
            [f"{widget.label}: {widget.region}" for widget in self.widgets]
        )
        self.info.update(f"Widgets:\n{widget_info}\nTerminal: {self.size}")

    def on_click(self, event: Click) -> None:
        if len(self.widgets) < 10:  # Limit to 10 widgets
            new_widget = ResizableWidget(label=f"widget-{random.randint(0, 9999)}")
            self.mount(new_widget)
            new_widget.styles.width = 10
            self.widgets.append(new_widget)  # Add new widget to the list
            self.update_info()  # Update info after adding a new widget

    def on_resize(self, event: Resize) -> None:
        x, y = self.size
        for widget in self.widgets:
            widget.update_offset(x, y)
        self.update_info()  # Update info after resizing
        self.refresh()

if __name__ == "__main__":
    app = ResizeApp()
    app.run()
