from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QFont, QPixmap, QWheelEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)
from main_window.movieCard import MovieCard
from hall.session import SessionWindow


class MainWindow(QMainWindow):
    def __init__(self, app, database):
        super().__init__()
        self.app = app
        self.database = database
        self.session_window = None
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setup_ui()
        self.connect_all_events()

        connection = self.database.connection
        cursor = connection.cursor()
        query_movie_info = """SELECT DISTINCT Sessions.id_kino,  kino.name_kino, kino.image_kino FROM db_findtick.Sessions
                              JOIN db_findtick.kino ON Sessions.id_kino = kino.id_kino;"""
        cursor.execute(query_movie_info)
        self.movie_info = cursor.fetchall()
        self.movie_ids = []
        self.movie_titles = []
        self.movie_posters = []
        for item in self.movie_info:
            self.movie_ids.append(item[0])
            self.movie_titles.append(item[1])
            self.movie_posters.append(item[2])

        self.display_all_movies()

    def setup_ui(self):
        self.resize(1920, 1080)

        font = QFont()
        font.setFamilies(["Century Gothic"])
        font.setPointSize(12)
        font.setBold(True)
        self.setFont(font)
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("centralwidget")
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("verticalLayout")
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed
        )

        self.vertical_layout.addItem(self.verticalSpacer)

        self.horizontal_layout = QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontalLayout")
        self.horizontal_spacer_3 = QSpacerItem(
            150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontal_layout.addItem(self.horizontal_spacer_3)

        self.logo_label = QLabel(self.central_widget)
        self.logo_label.setObjectName("logo_label")
        self.logo_label.setMinimumSize(QSize(120, 70))
        self.logo_label.setMaximumSize(QSize(120, 70))
        self.logo_label.setPixmap(QPixmap("./main_window/fintick-logo.png"))
        self.logo_label.setScaledContents(True)

        self.horizontal_layout.addWidget(self.logo_label)

        self.horizontal_spacer = QSpacerItem(
            120, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )

        self.horizontal_layout.addItem(self.horizontal_spacer)

        self.search = QLineEdit(self.central_widget)
        self.search.setObjectName("search")
        self.search.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamilies(["Century Gothic"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.search.setFont(font1)

        self.search.setStyleSheet(
            "border-radius: 10px;\n"
            "padding-left: 10px;\n"
            "background-color: rgb(230, 230, 230);\n"
            ""
        )
        self.horizontal_layout.addWidget(self.search)

        self.horizontalSpacer_2 = QSpacerItem(
            120, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum
        )

        self.horizontal_layout.addItem(self.horizontalSpacer_2)

        self.help_button = QPushButton(self.central_widget)
        self.help_button.setObjectName("help_button")
        self.help_button.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.help_button.setMinimumSize(QSize(90, 35))
        self.help_button.setMaximumSize(QSize(100, 40))

        self.horizontal_layout.addWidget(self.help_button)

        self.horizontalSpacer_4 = QSpacerItem(
            150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontal_layout.addItem(self.horizontalSpacer_4)

        self.vertical_layout.addLayout(self.horizontal_layout)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.vertical_layout.addItem(self.verticalSpacer_2)

        self.scroll_area = QScrollArea(self.central_widget)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setObjectName("scrollAreaWidgetContents")
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 1171, 429))
        self.scroll_area.setWidget(self.scroll_area_widget_contents)

        self.vertical_layout.addWidget(self.scroll_area)

        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("MainWindow")
        self.search.setPlaceholderText("Пошук")
        self.help_button.setText("? Help")

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

            movie_card.movieClicked.connect(
                lambda _, mid=movie_id: self.on_movie_clicked(mid)
            )
            scroll_layout.addWidget(movie_card)

        scroll_widget.setLayout(scroll_layout)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.horizontalScrollBar().setStyleSheet(
            """
            QScrollArea {
                border: none;
            }  
            QScrollBar:horizontal {
                height: 7px;
                border: none;
            }
            QScrollBar::handle:horizontal {
                background-color: #2622fb;
                border: none;
            }
            QScrollBar::add-page:horizontal {  
                background-color: rgb(255, 255, 255);
            }
            QScrollBar::sub-page:horizontal {  
                background-color: rgb(255, 255, 255); 
            }
            """
        )

        self.scroll_area.setWidget(scroll_widget)

    def connect_all_events(self):
        self.search.returnPressed.connect(self.handle_search)

    def on_movie_clicked(self, movie_id):
        self.session_window = SessionWindow(self.app, movie_id, self.database)
        self.session_window.show()

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            scroll_area = self.findChild(QScrollArea, "scroll_area")
            horizontal_bar = scroll_area.horizontalScrollBar()
            delta = event.angleDelta().y()
            horizontal_bar.setValue(horizontal_bar.value() - delta // 2)
            return
        super().wheelEvent(event)
