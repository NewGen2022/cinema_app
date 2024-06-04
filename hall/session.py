from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QStatusBar,
    QPushButton,
)
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QFont, QImage, QPixmap
from hall.hall import HallWindow


class SessionWindow(QMainWindow):
    def __init__(self, app, id_kino, database):
        super().__init__()
        self.app = app
        self.id_kino = id_kino
        self.database = database
        self.hall_window = None
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("SessionWindow")
        self.setWindowIconText("SessionWindow")
        self.resize(1920, 1080)

        font = QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(False)
        self.setFont(font)
        self.setStyleSheet("")

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("")

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(100, 80, 1720, 820))

        self.main_counteiner = QVBoxLayout(self.widget)
        self.main_counteiner.setObjectName("main_counteiner")
        self.main_counteiner.setContentsMargins(0, 0, 0, 0)

        self.kino_conteiner = QHBoxLayout()
        self.kino_conteiner.setObjectName("kino_conteiner")

        self.image = QLabel(self.widget)
        self.image.setObjectName("image")
        self.image.setMinimumSize(QSize(400, 600))
        self.image.setMaximumSize(QSize(400, 600))
        self.image.setScaledContents(True)
        self.image.setAlignment(Qt.AlignCenter)
        self.kino_conteiner.addWidget(self.image)

        self.info_conteiner = QVBoxLayout()
        self.info_conteiner.setObjectName("info_conteiner")

        font1 = QFont()
        font1.setFamily("Century Gothic")
        font1.setPointSize(16)
        font1.setBold(True)

        # Name Container
        self.name_conteiner = QHBoxLayout()
        self.name_conteiner.setSpacing(12)
        self.name_conteiner.setObjectName("name_conteiner")

        self.name = QLabel(self.widget)
        self.name.setObjectName("name")
        self.name.setText("Назва:")
        self.name.setMaximumSize(QSize(250, 200))
        self.name.setFont(font1)
        self.name_conteiner.addWidget(self.name)

        self.label_name = QLabel(self.widget)
        self.label_name.setObjectName("label_name")
        self.label_name.setFont(font)
        self.name_conteiner.addWidget(self.label_name)
        self.info_conteiner.addLayout(self.name_conteiner)

        # Age Limit Container
        self.age_limit_container = QHBoxLayout()
        self.age_limit_container.setSpacing(12)
        self.age_limit_container.setObjectName("age_limit_container")

        self.age_limit = QLabel(self.widget)
        self.age_limit.setObjectName("age_limit")
        self.age_limit.setMaximumSize(QSize(250, 200))
        self.age_limit.setFont(font1)
        self.age_limit.setText("Вікове обмеження:")
        self.age_limit_container.addWidget(self.age_limit)

        self.label_age_limit = QLabel(self.widget)
        self.label_age_limit.setObjectName("label_age_limit")
        self.label_age_limit.setFont(font)
        self.age_limit_container.addWidget(self.label_age_limit)
        self.info_conteiner.addLayout(self.age_limit_container)

        # Country Container
        self.country_container = QHBoxLayout()
        self.country_container.setObjectName("country_container")

        self.country = QLabel(self.widget)
        self.country.setObjectName("country")
        self.country.setMaximumSize(QSize(250, 200))
        self.country.setFont(font1)
        self.country.setText("Країна:")
        self.country_container.addWidget(self.country)

        self.label_country = QLabel(self.widget)
        self.label_country.setObjectName("label_country")
        self.country_container.addWidget(self.label_country)
        self.info_conteiner.addLayout(self.country_container)

        # Graduation Year Container
        self.graduation_year_container = QHBoxLayout()
        self.graduation_year_container.setSpacing(12)
        self.graduation_year_container.setObjectName("graduation_year_container")

        self.graduation_year = QLabel(self.widget)
        self.graduation_year.setObjectName("graduation_year")
        self.graduation_year.setMaximumSize(QSize(250, 200))
        self.graduation_year.setFont(font1)
        self.graduation_year.setText("Рік випуску:")
        self.graduation_year_container.addWidget(self.graduation_year)

        self.label_graduation_year = QLabel(self.widget)
        self.label_graduation_year.setObjectName("label_graduation_year")
        self.label_graduation_year.setFont(font)
        self.graduation_year_container.addWidget(self.label_graduation_year)
        self.info_conteiner.addLayout(self.graduation_year_container)

        # Genre Container
        self.genre_conteiner = QHBoxLayout()
        self.genre_conteiner.setSpacing(12)
        self.genre_conteiner.setObjectName("genre_conteiner")

        self.genre = QLabel(self.widget)
        self.genre.setObjectName("genre")
        self.genre.setMaximumSize(QSize(250, 200))
        self.genre.setFont(font1)
        self.genre.setText("Жанр:")
        self.genre_conteiner.addWidget(self.genre)

        self.label_genre = QLabel(self.widget)
        self.label_genre.setObjectName("label_genre")
        self.label_genre.setFont(font)
        self.genre_conteiner.addWidget(self.label_genre)
        self.info_conteiner.addLayout(self.genre_conteiner)

        # Duration Container
        self.duration_conteiner = QHBoxLayout()
        self.duration_conteiner.setSpacing(12)
        self.duration_conteiner.setObjectName("duration_conteiner")

        self.duration = QLabel(self.widget)
        self.duration.setObjectName("duration")
        self.duration.setMaximumSize(QSize(250, 200))
        self.duration.setFont(font1)
        self.duration.setText("Тривалість:")
        self.duration_conteiner.addWidget(self.duration)

        self.label_duration = QLabel(self.widget)
        self.label_duration.setObjectName("label_duration")
        self.label_duration.setFont(font)
        self.duration_conteiner.addWidget(self.label_duration)
        self.info_conteiner.addLayout(self.duration_conteiner)

        # Description Container
        self.description_conteiner = QHBoxLayout()
        self.description_conteiner.setSpacing(12)
        self.description_conteiner.setObjectName("description_conteiner")

        self.description = QLabel(self.widget)
        self.description.setObjectName("description")
        self.description.setMaximumSize(QSize(250, 200))
        self.description.setFont(font1)
        self.description.setText("Короткий опис:")
        self.description.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.description_conteiner.addWidget(self.description)

        self.label_description = QLabel(self.widget)
        self.label_description.setObjectName("label_description")
        self.label_description.setFont(font)
        self.label_description.setWordWrap(True)
        self.description_conteiner.addWidget(self.label_description)
        self.info_conteiner.addLayout(self.description_conteiner)

        # Spacer
        self.Spacer_info = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.kino_conteiner.addItem(self.Spacer_info)
        self.kino_conteiner.addLayout(self.info_conteiner)
        self.main_counteiner.addLayout(self.kino_conteiner)

        # Bottom Container
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )
        self.main_counteiner.addItem(self.verticalSpacer)
        self.Botton_conteiner = QHBoxLayout()
        self.Botton_conteiner.setSpacing(15)
        self.Botton_conteiner.setObjectName("Botton_conteiner")
        self.Botton_conteiner.setContentsMargins(100, 0, 0, 0)
        self.Botton_conteiner.setAlignment(Qt.AlignCenter)
        self.main_counteiner.addLayout(self.Botton_conteiner)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.fetch_and_display_movie_info()
        self.generate_session_buttons()

    def fetch_and_display_movie_info(self):
        connection = self.database.connection
        cursor = connection.cursor()

        query = """
                SELECT DISTINCT kino.image_kino, kino.name_kino, Catalog_age.age_restrictions,
                                Catalog_countries.countries, kino.graduation_year, Catalog_of_genres.genre_kino,
                                kino.duration_film, kino.s_description
                FROM db_findtick.kino
                JOIN db_findtick.Sessions ON Sessions.id_kino = kino.id_kino
                JOIN db_findtick.Catalog_age ON kino.id_age_restrictions = Catalog_age.id_age
                JOIN db_findtick.Catalog_countries ON kino.id_countries = Catalog_countries.id_countries
                JOIN db_findtick.Catalog_of_genres ON kino.genre_kino = Catalog_of_genres.id_genres
                WHERE Sessions.id_kino = %s;
            """
        cursor.execute(query, (self.id_kino,))
        result = cursor.fetchone()

        if result:
            (
                image_kino,
                name_kino,
                age_restrictions,
                countries,
                graduation_year,
                genre_kino,
                duration_film,
                s_description,
            ) = result

            self.label_name.setText(name_kino)
            self.label_age_limit.setText(age_restrictions)
            self.label_country.setText(countries)
            self.label_graduation_year.setNum(graduation_year)
            self.label_genre.setText(genre_kino)

            duration_minutes = int(duration_film.total_seconds() / 60)
            duration_str = f"{duration_minutes} хвилин"
            self.label_duration.setText(duration_str)
            self.label_description.setText(s_description)

            image_data = result[0]
            image = QImage.fromData(image_data)
            pixmap = QPixmap.fromImage(image)
            self.image.setPixmap(pixmap)

    def button_click(self):
        sender = self.sender()
        session_info = sender.property("session_info")

        hall_id = session_info["id_Hall"]
        nomer_s = session_info["nomer_S"]
        self.hall_window = HallWindow(hall_id, nomer_s, self.database)
        self.hall_window.setFixedSize(1920, 1080)
        self.hall_window.showFullScreen()

    def generate_session_buttons(self):
        connection = self.database.connection
        cursor = connection.cursor()

        query = """
            SELECT Sessions.id_Session, Sessions.nomer_S, Sessions.id_Hall, 
                    DATE_FORMAT(Sessions.start_s, '%%H:%%i') AS start_s, 
                    DATE_FORMAT(Sessions.end_s, '%%H:%%i') AS end_s, 
                    Sessions.price, Sessions.currency, All_Halls.name_hall
            FROM db_findtick.Sessions
            JOIN db_findtick.All_Halls ON Sessions.id_Hall = All_Halls.id_Hall
            WHERE Sessions.id_kino = %s;
        """
        cursor.execute(query, (self.id_kino,))
        sessions = cursor.fetchall()

        self.session_info_list = []

        for result in sessions:
            (
                session_id,
                nomer_S,
                id_Hall,
                start_time,
                end_time,
                price,
                currency,
                hall_name,
            ) = result

            button_text = f"{start_time} - {end_time}\n{price} {currency}"

            if not hall_name.startswith("Зал"):
                button_text += f"\n{hall_name}"

            button = QPushButton(button_text)
            button.setFixedSize(200, 70)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #FF8000;
                    border-radius: 30px;
                    color: white; 
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FF5000;
                }
                QPushButton:pressed {
                    background-color: #FFF000;
                }
            """
            )

            button.setVisible(True)
            self.Botton_conteiner.addWidget(button)

            session_info = {
                "session_id": session_id,
                "nomer_S": nomer_S,
                "id_Hall": id_Hall,
            }
            self.session_info_list.append(session_info)

            button.setProperty("session_info", session_info)
            button.clicked.connect(self.button_click)

        cursor.close()
