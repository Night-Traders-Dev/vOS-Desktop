from textual.app import App, ComposeResult
from components.alphawidget import Alpha as BlockDigits

class HelloApp(App):

    def compose(self) -> ComposeResult:
        alphabet = "H E L L O"
        rendered_output = ""

        for letter in alphabet:
            rendered_output += letter + " "

        yield BlockDigits(rendered_output)


if __name__ == "__main__":
    app = HelloApp()
    app.run()
