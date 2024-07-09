from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QLabel, QGridLayout, QWidget


class MovieCard(QWidget):
    movieClicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.make_card()

    def make_card(self):
        self.setMaximumSize(300, 570)

        layout = QGridLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)

        self.poster_label = QLabel(self)
        self.poster_label.setAlignment(Qt.AlignCenter)
        self.poster_label.setScaledContents(True)

        self.title_label = QLabel(self)
        self.title_label.setFixedHeight(50)
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Century Gothic", 14, QFont.Bold)
        self.title_label.setStyleSheet("color: #ffffff;")
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)

        layout.addWidget(self.poster_label, 1, 0, 1, 2)
        layout.addWidget(self.title_label, 2, 0, 1, 2)

        self.mousePressEvent = self.on_mouse_press

    def set_card(self, title, poster_path):
        self.title_label.setText(title)
        self.set_movie_poster(poster_path)

    def set_movie_poster(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.poster_label.setMaximumSize(300, 443)
        self.poster_label.setMinimumSize(300, 443)
        self.poster_label.setPixmap(pixmap)

    def on_mouse_press(self, event):
        # print(f"Movie card clicked: {self.title_label.text()}")
        self.movieClicked.emit(self.title_label.text())
