from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
import sys


class MovieCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()

    def setupUi(self):
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

        vertical_spacer_top = QSpacerItem(50, 100, QSizePolicy.Expanding, QSizePolicy.Expanding)
        vertical_spacer_bottom = QSpacerItem(50, 100, QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add widgets to layout with vertical spacers
        # layout.addItem(vertical_spacer_top, 0, 0, 1, 2)
        layout.addWidget(self.poster_label, 1, 0, 1, 2)
        layout.addWidget(self.title_label, 2, 0, 1, 2)
        # layout.addItem(vertical_spacer_bottom, 3, 0, 1, 2)

    def set_card(self, title, poster_path):
        self.title_label.setText(title)
        self.set_movie_poster(poster_path)

    def set_movie_poster(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.poster_label.setMaximumSize(233, 344)
        self.poster_label.setPixmap(pixmap)
