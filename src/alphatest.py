from textual.app import App, ComposeResult
from components.alphawidget import Alpha as BlockDigits

class HelloApp(App):

    CSS = """
    .wallet {
        border: round rgb(233, 84, 32);
        text-align: center;
        color: rgb(119, 33, 111);
    }
    """

    def compose(self) -> ComposeResult:
        wallet = "Wallet"

        yield BlockDigits(wallet, classes="wallet")

if __name__ == "__main__":
    app = HelloApp()
    app.run()
