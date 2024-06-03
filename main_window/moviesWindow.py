# Assuming this is already implemented as shown earlier
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QHBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWheelEvent
from PyQt5.uic import loadUi
from main_window.movieCard import MovieCard
from functools import partial

from HALL.test import SessionWindow


class MainWindow(QMainWindow):
    def __init__(self, app, database):
        super(MainWindow, self).__init__()
        self.app = app
        self.database = database

        self.session_window = None

        loadUi("./main_window/moviesUI.ui", self)

        self.setWindowTitle("MainWindow")

        screen_height = QApplication.desktop().screenGeometry().height()
        self.setMinimumHeight(screen_height - 450)
        screen_width = QApplication.desktop().screenGeometry().width()
        self.setMinimumWidth(screen_width - 1000)

        self.show()

        self.connect_all_events()
        query_movie_info = """SELECT DISTINCT Sessions.id_kino,  kino.name_kino, kino.image_kino FROM db_findtick.Sessions
join db_findtick.kino on Sessions.id_kino = kino.id_kino;"""
        self.movie_info = self.database.execute_query(query_movie_info)
        self.movie_ids = []
        self.movie_titles = []
        self.movie_posters = []
        for item in self.movie_info:
            self.movie_ids.append(item[0])
            self.movie_titles.append(item[1])
            self.movie_posters.append(item[2])

        self.display_all_movies()

    def handle_search(self):
        print("Search")

    def display_all_movies(self):
        scroll_area = self.findChild(QScrollArea, "scroll_area")
        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)

        for movie_id, title, poster in zip(
            self.movie_ids, self.movie_titles, self.movie_posters
        ):
            movie_card = MovieCard()
            movie_card.set_card(title, poster)
            movie_card.movieClicked.connect(partial(self.on_movie_clicked, movie_id))
            scroll_layout.addWidget(movie_card)

        scroll_widget.setLayout(scroll_layout)

        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        scroll_area.setWidget(scroll_widget)

    def connect_all_events(self):
        self.search.returnPressed.connect(self.handle_search)

    def on_movie_clicked(self, movie_id):
        print("Movie clicked, ID:", movie_id)

        self.session_window = SessionWindow(movie_id, self.database)
        self.session_window.show()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            scroll_area = self.findChild(QScrollArea, "scroll_area")
            horizontal_bar = scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            horizontal_bar.setValue(horizontal_bar.value() - delta // 2)
            return
        super().wheelEvent(event)
