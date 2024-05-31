#from textual.app import App, ComposeResult
from textual.widgets import Static
from rich_pixels import Pixels
from PIL import Image as PILImage

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
        data = self.load_image(self.file_path, resize)
        super().__init__(data, name=name, id=id, classes=classes)

    def load_image(self, file_path: str, resize: tuple[int, int] | None = None):
        image = PILImage.open(file_path)
        if resize:
            image = image.resize(resize, PILImage.Resampling.LANCZOS)
        return Pixels.from_image(image)


    def set_image(self, file_path: str, resize: tuple[int, int] | None = None):
        self.file_path = file_path
        data = Pixels.from_image_path(self.file_path, resize)
        self.update(data)


#class Test(App):

#    def compose(self) -> ComposeResult:
#        yield Image("components/vos.jpg", (80, 60))

#if __name__ == "__main__":
#    testapp = Test()
#    testapp.run()
