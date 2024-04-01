from tkinter import ttk
from PIL import Image, ImageTk

class ResizedImage(ttk.Label):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_original = Image.open(image_path)
        self.image_tk = self.resize_image()
        self.configure(image=self.image_tk)

    def resize_image(self, frame_width=630, frame_height=800):
        resized_image = self.image_original.resize((frame_width, frame_height))
        return ImageTk.PhotoImage(resized_image)
