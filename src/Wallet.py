from textual import on, events
from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, Vertical
from textual.reactive import reactive
from textual.geometry import Region
from textual.widgets import Placeholder, Static, Label, ListView, ListItem, Button
from components.alphawidget import Alpha as BlockDigits


PAGES_COUNT = 3



class Wallet(Static):

    def compose(self) -> ComposeResult:
        yield BlockDigits("wallet", id="WalletBanner")
        yield ListView(
            ListItem(Label("QSE: 0", id="qse"), id="wallet"),
            id="wallet")
        yield Button("Send", id="send", classes="WalletButton")
        yield Button("Receive", id="receive", classes="WalletButton")

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
