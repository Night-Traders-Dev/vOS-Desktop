from textual.widgets import Static
from rich_pixels import Pixels

class Image(Static):
    def __init__(
        self,
        file_path: str, 
        resize: tuple[int, int] | None = None,
        name: str | None = None, 
        id: str | None = None, 
        classes: str | None = None
    ) -> None:
        self.file_path = file_path
        data = Pixels.from_image_path(self.file_path, resize)
        super().__init__(data, name=name, id=id, classes=classes)

    def set_image(self, file_path: str, resize: tuple[int, int] | None = None):
        self.file_path = file_path
        data = Pixels.from_image_path(self.file_path, resize)
        self.update(data)
