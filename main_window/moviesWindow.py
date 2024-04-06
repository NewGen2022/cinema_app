from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5.uic import loadUi
from db_connection import database
from main_window.movieCard import MovieCard

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("./main_window/moviesUI.ui", self)

        self.setWindowTitle("MainWindow")

        screen_height = QApplication.desktop().screenGeometry().height()
        self.setMinimumHeight(screen_height - 450)
        screen_width = QApplication.desktop().screenGeometry().width()
        self.setMinimumWidth(screen_width - 1000)

        self.show()

        self.connect_all_events()
        query_movie_info = "SELECT image_kino, name_kino FROM db_findtick.kino;"
        self.movie_info = database.execute_query(query_movie_info)
        self.movie_titles = []
        self.movie_posters = []
        for item in self.movie_info:
            self.movie_titles.append(item[1])
            self.movie_posters.append(item[0])

        self.display_all_movies()

    def handle_search(self):
        print("Search")

    def display_all_movies(self):
        scroll_area = self.findChild(QScrollArea, "scroll_area")
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)

        for title, poster in zip(self.movie_titles, self.movie_posters):
            movie_card = MovieCard()
            movie_card.movieClicked.connect(self.on_movie_clicked)
            movie_card.set_card(title, poster)
            scroll_layout.addWidget(movie_card)

        scroll_widget.setLayout(scroll_layout)

        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_area.setWidget(scroll_widget)

    def connect_all_events(self):
        self.search.returnPressed.connect(self.handle_search)

    def on_movie_clicked(self, title):
        print("Movie clicked:", title)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            scroll_area = self.findChild(QScrollArea, "scroll_area")
            horizontal_bar = scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            horizontal_bar.setValue(horizontal_bar.value() - delta // 2)
            return
        super().wheelEvent(event)