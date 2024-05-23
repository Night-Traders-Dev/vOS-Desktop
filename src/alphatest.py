from textual.app import App, ComposeResult
from components.alphawidget import Alpha as BlockDigits

class HelloApp(App):

    def compose(self) -> ComposeResult:
        alphabet = "Wallet"

        yield BlockDigits(alphabet)

if __name__ == "__main__":
    app = HelloApp()
    app.run()
