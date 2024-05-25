from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, Horizontal, Container
from textual.reactive import reactive
from textual.widgets import Placeholder, Static, Label, ListView, ListItem, Button
from textual.events import Resize
from textual.geometry import Region, Size
from components.alphawidget import Alpha as BlockDigits


PAGES_COUNT = 3

class Receive(Button):
    def update_offset(self, x: int, y: int) -> None:
        """Update the widget's offset based on the new width and height."""
        # Calculate the new offset
        if x != 0:
            new_offset_x = x - 6
        else:
            new_offset_x = 0
        if y != 0:
            new_offset_y = y - 15
        else:
            new_offset_y = 0
        self.styles.offset = (new_offset_x, new_offset_y)

class Wallet(Static):

    def compose(self) -> ComposeResult:
       self.WalletPage = Container(id="WalletPage")
       with self.WalletPage:
#            yield BlockDigits("wallet", id="WalletBanner")
#            yield ListView(
#                ListItem(Label("QSE: 0", id="qse_balance")),
#                id="user_balance")
            with Horizontal(id="WalletButton"):
                yield Button("Send", classes="button send")
                self.Receive = Receive("Receive")
                yield self.Receive
                self.info = Label(f"Widget: {self.Receive.region}\nContainer: {self.WalletPage.size}")
                yield self.info


    def on_resize(self, event: Resize) -> None:
        # Handle the resize event and update the widget's offset
        x, y = self.WalletPage.size
        self.Receive.update_offset((x), (y))
        self.info.update(f"Widget: {self.Receive.region}\nContainer: {self.WalletPage.size}")
        self.refresh()

    def on_mount(self) -> None:
        # Initial offset update when the app is first mounted
        x, y = self.WalletPage.size
        self.Receive.update_offset((x - x), (y - y))
        self.refresh()

class WalletScreen(App):
    BINDINGS = [
        ("ctrl+right", "next", "Next"),
        ("ctrl+left", "previous", "Previous"),
    ]

    CSS_PATH = "Desktop.tcss"

    page_no = reactive(0)

    def compose(self) -> ComposeResult:
        with HorizontalScroll(id="page-container"):
            for page_no in range(PAGES_COUNT):
                if page_no == 0:
                    yield Wallet(id=f"page-{page_no}")
                elif page_no == 1:
                    yield Placeholder(f"Transactions", id=f"page-{page_no}")
                else:
                    yield Placeholder(f"About", id=f"page-{page_no}")

    def action_next(self) -> None:
        self.page_no += 1
        self.refresh_bindings()  
        self.query_one(f"#page-{self.page_no}").scroll_visible()

    def action_previous(self) -> None:
        self.page_no -= 1
        self.refresh_bindings()  
        self.query_one(f"#page-{self.page_no}").scroll_visible()

    def check_action(
        self, action: str, parameters: tuple[object, ...]
    ) -> bool | None:  
        """Check if an action may run."""
        if action == "next" and self.page_no == PAGES_COUNT - 1:
            self.notify("End of the line", title="vOS Notification", timeout=1)
            return False
        if action == "previous" and self.page_no == 0:
            self.notify("End of the line", title="vOS Notification", timeout=1)
            return False
        return True


if __name__ == "__main__":
    app = WalletScreen()
    app.run()
