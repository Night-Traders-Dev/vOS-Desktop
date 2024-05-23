from textual.app import App, ComposeResult
from components.alphawidget import Alpha as BlockDigits

class HelloApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    .block-alphabet {
        height: 15;  /* Adjusted height for 5x3 */
        width: 9;    /* Adjusted width for 5x3 */
        /* Define styling for the block alphabet here */
    }
    """

    def compose(self) -> ComposeResult:
        alphabet = "HELLO"

        for index, letter in enumerate(alphabet):
            yield BlockDigits(letter, id=f"alpha-{letter.lower()}-{index}", classes="block-alphabet")

if __name__ == "__main__":
    app = HelloApp()
    app.run()
