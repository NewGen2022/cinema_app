from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class MovieCard(QWidget):
    movieClicked = pyqtSignal(
        str
    )  # Signal emitted when the movie card is clicked, passing the movie title

    def __init__(self, parent=None):
        super().__init__(parent)
        self.make_card()  # Set up the UI components

    def make_card(self):
        self.setMaximumSize(300, 500)

        # Create layout
        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        # Create label for movie poster
        self.poster_label = QLabel(self)
        self.poster_label.setAlignment(Qt.AlignCenter)
        self.poster_label.setScaledContents(True)

        # Create label for movie title
        self.title_label = QLabel(self)
        self.title_label.setFixedHeight(50)
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Century Gothic", 14, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

        # Add widgets to layout with vertical spacers
        layout.addWidget(self.poster_label, 1, 0, 1, 2)
        layout.addWidget(self.title_label, 2, 0, 1, 2)

        # Connect the mouse press event to the on_mouse_press method
        self.mousePressEvent = self.on_mouse_press

    def set_card(self, title, poster_path):
        self.title_label.setText(title)  # Set the movie title
        self.set_movie_poster(poster_path)  # Set the movie poster

    def set_movie_poster(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)  # Load the image data into the pixmap
        self.poster_label.setMaximumSize(233, 344)
        self.poster_label.setPixmap(pixmap)  # Set the pixmap on the poster label

    def on_mouse_press(self, event):
        self.movieClicked.emit(
            self.title_label.text()
        )  # Emit the movieClicked signal with the movie title when clicked
