from __future__ import annotations

from rich.console import Console, ConsoleOptions, RenderResult
from rich.measure import Measurement
from rich.segment import Segment
from rich.style import Style, StyleType

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET5X3 = """
 ▄█▄
█▀█▀█
▀ ▀ ▀

█▀█
█▀▀█
█▄▄█

▄▀▀█
█
 ▀▄▄█

█▀▀▄
█   █
█▄▄▀

█▀▀▀
█▀▀
█▄▄▄

█▀▀▀
█▀▀
█

▄▀▀▀█
█
█ ▀▀█

█   █
█▀▀▀█
█   █

 ▀█▀
  █
▄▀█▀▄

   ▀█
    █
█▄▄▄█

█  ▄▀
█▀▀
█  ▀▄

█
█
█▄▄▄█

█▄ ▄█
█ █ █
█   █

█▄  █
█ █ █
█  ▀█

▄▀▀▀▄
█   █
 ▀▀▀

█▀▀█
█▄▄▀
█

▄▀▀▀▄
█ ▄▀█
 ▀▀▀█

█▀▀█
█▄▄▀
█  █

▄▀▀▀█
█▄▄▀
 ▀▄▄▀

▀▀█▀▀
  █
  █

█   █
█   █
 ▀▀▀

█   █
█   █
 ▀▄▀

█   █
█ █ █
 ▀▄▀

▀▄ ▄▀
  █
▄▀ ▀▄

█   █
 ▀▄▀
  █

▀▀▀█
  ▄▀
▄▀▀▀
""".splitlines()


class Alphabet:
    """Renders a 5x3 unicode 'font' for alphabet values.

    Args:
        text: Text to display.
        style: Style to apply to the alphabet characters.

    """

    def __init__(self, text: str, style: StyleType = "") -> None:
        self._text = text.upper()
        self._style = style

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        style = console.get_style(self._style)
        yield from self.render(style)

    def render(self, style: Style) -> RenderResult:
        """Render with the given style

        Args:
            style: Rich Style.

        Returns:
            Result of render.
        """
        letter_pieces: list[list[str]] = [[], [], []]
        row1 = letter_pieces[0].append
        row2 = letter_pieces[1].append
        row3 = letter_pieces[2].append

        for character in self._text:
            try:
                position = ALPHABET.index(character) * 3
            except ValueError:
                row1("   ")
                row2("   ")
                row3("   ")
            else:
                row1(ALPHABET5X3[position].ljust(3))
                row2(ALPHABET5X3[position + 1].ljust(3))
                row3(ALPHABET5X3[position + 2].ljust(3))

        new_line = Segment.line()
        for line in letter_pieces:
            yield Segment("".join(line), style)
            yield new_line

    @classmethod
    def get_width(cls, text: str) -> int:
        """Calculate the width without rendering.

        Args:
            text: Text which may be displayed in the `Alphabet` widget.

        Returns:
            Width of the text (in cells).
        """
        width = sum(3 if character in ALPHABET else 1 for character in text)
        return width

    def __rich_measure__(
        self, console: Console, options: ConsoleOptions
    ) -> Measurement:
        width = self.get_width(self._text)
        return Measurement(width, width)
