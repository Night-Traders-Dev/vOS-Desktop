from textual.app import App, ComposeResult
from components.alphawidget import Alpha as BlockDigits

class HelloApp(App):

    def compose(self) -> ComposeResult:
        alphabet = "HELLO"

        for index, letter in enumerate(alphabet):
            yield BlockDigits(letter, id=f"alpha-{letter.lower()}-{index}", classes="block-alphabet")

if __name__ == "__main__":
    app = HelloApp()
    app.run()
