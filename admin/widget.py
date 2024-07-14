from PySide6.QtCore import Qt, QSize, QDateTime
from PySide6.QtGui import QImage, QPixmap, QColor, QFont, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
    QDialog,
    QHBoxLayout,
    QTableWidget,
    QSpacerItem,
    QSizePolicy,
    QMenu,
    QDateTimeEdit,
)
from io import BytesIO
from PIL import Image
import re
import datetime
from admin.ui_widget import Ui_admin_widget
from admin.aboutWindow import AboutWindow
from admin.helpWindow import HelpWindow


class Widget(QWidget, Ui_admin_widget):
    def __init__(self, db, login_name):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Адміністративна підсистема")
        self.user_name = login_name
        self.show_pointer = ""
        self.zvit_pointer = ""
        self.database = db
        self.zvit_window = Zvit_Window(self)
        self.add_dialog = CustomDialog(self)

        icon = QIcon("./assets/icon.ico")
        self.setWindowIcon(icon)

        self.film_button.clicked.connect(self.show_table_film)
        self.hall_button.clicked.connect(self.show_table_halls)
        self.session_button.clicked.connect(self.show_table_session)
        self.user_button.clicked.connect(self.show_table_users)
        self.add_object_button.clicked.connect(self.add_item)
        self.go_to_zvit_button.clicked.connect(self.zvit_window_show)
        self.about.clicked.connect(self.handle_about)
        self.help.clicked.connect(self.handle_help)
        self.tableWidget.cellChanged.connect(self.change_value)

        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.open_context_menu)

        self.zvit_window.session_zvit_button.clicked.connect(self.zvit_show_session)
        self.zvit_window.film_zvit_button.clicked.connect(self.zvit_show_film)
        self.zvit_window.hall_zvit_button.clicked.connect(self.zvit_show_hall)
        self.zvit_window.action_zvit_button.clicked.connect(self.zvit_show_action)

        self.show_table_session()

    def open_context_menu(self, position):
        index = self.tableWidget.indexAt(position)
        if not index.isValid():
            return 0

        row = index.row()
        column = index.column()
        context_menu = QMenu(self)

        context_menu.setStyleSheet(
            """
            background-color: white;
            color: black;
            """
        )

        action_1 = context_menu.addAction("Редагувати")
        action_2 = context_menu.addAction("Видалити")
        action_1.triggered.connect(lambda: self.clicked_value(row, column))
        action_2.triggered.connect(lambda: self.delete_item(row, column))

        context_menu.exec(self.tableWidget.viewport().mapToGlobal(position))

    def show_add_film_window(self):
        self.add_dialog.setWindowTitle(f"Додавання нового фільму")

        self.add_dialog.setGeometry(700, 300, 100, 380)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout_1 = QHBoxLayout()

        self.add_dialog.verticalLayout_1.insertLayout(0, self.horizontalLayout)
        self.add_dialog.verticalLayout_1.insertLayout(1, self.horizontalLayout_1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_10 = QVBoxLayout()

        self.name_label = QLabel("Назва фільму", self.add_dialog)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_kino = QLineEdit(self.add_dialog)
        self.name_kino.setMinimumSize(QSize(0, 40))
        self.name_layout = QVBoxLayout()
        self.name_layout.addWidget(self.name_label)
        self.name_layout.addWidget(self.name_kino)
        self.verticalLayout_5.insertLayout(0, self.name_layout)

        self.duration_label = QLabel(
            "Тривалість фільму (год:хвил:секунди)", self.add_dialog
        )
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.duration_film = QLineEdit(self.add_dialog)
        self.duration_film.setMinimumSize(QSize(0, 40))
        self.duration_layout = QVBoxLayout()
        self.duration_layout.addWidget(self.duration_label)
        self.duration_layout.addWidget(self.duration_film)
        self.verticalLayout_5.insertLayout(1, self.duration_layout)

        self.graduation_label = QLabel("Рік випуску", self.add_dialog)
        self.graduation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graduation_year = QLineEdit(self.add_dialog)
        self.graduation_year.setMinimumSize(QSize(0, 40))
        self.graduation_layout = QVBoxLayout()
        self.graduation_layout.addWidget(self.graduation_label)
        self.graduation_layout.addWidget(self.graduation_year)
        self.verticalLayout_5.insertLayout(2, self.graduation_layout)

        self.s_description = QTextEdit(self.add_dialog)
        self.s_description.setPlaceholderText("Введіть короткий опис фільму")
        self.s_description.setFixedSize(400, 200)
        self.verticalLayout_5.insertWidget(3, self.s_description)

        self.age_label = QLabel("Вікові обмеження:", self.add_dialog)
        self.age_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.age_restrictions = QComboBox(self)
        self.age_restrictions.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog("age_restrictions", "Catalog_age")
        for i in options:
            self.age_restrictions.addItem(i[0])

        self.age_layout = QVBoxLayout()
        self.age_layout.addWidget(self.age_label)
        self.age_layout.addWidget(self.age_restrictions)
        self.verticalLayout_10.insertLayout(0, self.age_layout)

        self.countries_label = QLabel("Країна:", self.add_dialog)
        self.countries_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countries = QComboBox(self)
        self.countries.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog("countries", "Catalog_countries")
        for i in options:
            self.countries.addItem(i[0])

        self.countries_layout = QVBoxLayout()
        self.countries_layout.addWidget(self.countries_label)
        self.countries_layout.addWidget(self.countries)
        self.verticalLayout_10.insertLayout(1, self.countries_layout)

        self.genre_label = QLabel("Жанр:", self.add_dialog)
        self.genre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.genre = QComboBox(self)
        self.genre.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog("genre_kino", "Catalog_of_genres")
        for i in options:
            self.genre.addItem(i[0])

        self.genre_layout = QVBoxLayout()
        self.genre_layout.addWidget(self.genre_label)
        self.genre_layout.addWidget(self.genre)
        self.verticalLayout_10.insertLayout(2, self.genre_layout)

        self.choose_image = QPushButton("Вибрати зображення", self.add_dialog)
        self.choose_image.setMinimumSize(QSize(0, 50))
        self.choose_image.clicked.connect(self.choose_foto)
        self.verticalLayout_10.insertWidget(3, self.choose_image)

        self.verticalLayout_10.insertItem(4, self.verticalSpacer_3)
        self.verticalLayout_5.insertItem(4, self.verticalSpacer_4)
        self.horizontalLayout.insertLayout(0, self.verticalLayout_5)
        self.horizontalLayout.insertLayout(1, self.verticalLayout_10)

        # КНОПКА ДОДАВАННЯ

        self.add_object_button_window = QPushButton("Додати фільм", self.add_dialog)
        self.add_object_button_window.setMaximumSize(QSize(250, 50))
        self.add_object_button_window.clicked.connect(self.add_kino)

        self.cancel_button = QPushButton("Скасувати", self.add_dialog)
        self.cancel_button.setMaximumSize(QSize(250, 50))
        self.cancel_button.clicked.connect(self.cancel_add)

        self.horizontalLayout_1.insertWidget(0, self.add_object_button_window)
        self.horizontalLayout_1.insertWidget(1, self.cancel_button)

        self.add_dialog.show()

    def show_table_film(self):
        if self.show_pointer == "":
            self.change_color(self.film_button)
        elif self.show_pointer == "hall":
            self.change_color(self.film_button, self.hall_button)
        elif self.show_pointer == "session":
            self.change_color(self.film_button, self.session_button)
        elif self.show_pointer == "user":
            self.change_color(self.film_button, self.user_button)
        self.show_pointer = "kino"
        self.clear_table()
        self.change_pointer = False
        self.tableWidget_label.setText("Фільми")

        temp_cursor = self.database.connection.cursor()
        request = """
        SELECT kino.id_kino, kino.name_kino, Catalog_age.age_restrictions, Catalog_countries.countries, Catalog_of_genres.genre_kino, kino.graduation_year, kino.duration_film, kino.image_kino, kino.s_description
        FROM db_findtick.kino
        JOIN Catalog_age ON kino.id_age_restrictions = Catalog_age.id_age
        JOIN Catalog_countries ON kino.id_countries = Catalog_countries.id_countries
        JOIN Catalog_of_genres ON kino.genre_kino = Catalog_of_genres.id_genres
        ORDER BY kino.id_kino;
        """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()
        columns = [
            "ІД",
            "Назва",
            "Вікові обмеження",
            "Країна",
            "Жанр",
            "Рік випуску",
            "Тривалість",
            "Фото",
            "Опис",
        ]
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                if col_idx == 7:
                    image_data = value
                    if image_data:
                        image = Image.open(BytesIO(image_data))
                        image = image.resize((300, 200), Image.LANCZOS)
                        image_qt = self.pil2pixmap(image)
                        label = QLabel()
                        label.setPixmap(image_qt)
                        label.setAlignment(Qt.AlignCenter)
                        self.tableWidget.setCellWidget(row_idx, col_idx, label)
                    else:
                        self.tableWidget.setItem(
                            row_idx, col_idx, QTableWidgetItem("No Image")
                        )
                else:
                    item = QTableWidgetItem(str(value))
                    font = QFont()
                    font.setBold(False)
                    item.setFont(font)
                    self.tableWidget.setItem(row_idx, col_idx, item)
            self.tableWidget.setRowHeight(row_idx, 200)

        self.tableWidget.setColumnWidth(8, 400)
        self.tableWidget.setColumnWidth(7, 300)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 150)
        self.tableWidget.setColumnWidth(5, 150)
        self.tableWidget.setColumnWidth(6, 150)

        self.change_pointer = True

    def pil2pixmap(self, image):
        data = image.convert("RGBA").tobytes("raw", "RGBA")
        qim = QImage(data, image.width, image.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qim)
        return pixmap

    def show_add_hall_window(self):
        self.add_dialog.setGeometry(850, 100, 0, 0)
        self.add_dialog.setFixedSize(0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout_1 = QHBoxLayout()
        self.add_dialog.setWindowTitle(f"Додавання нового залу")

        self.add_dialog.verticalLayout_1.insertLayout(0, self.horizontalLayout)
        self.add_dialog.verticalLayout_1.insertLayout(1, self.horizontalLayout_1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_10 = QVBoxLayout()

        def display_ryads():
            if not re.match(r"\b(?:[1-9]|[1-4]\d|50)\b", self.ryad.text()):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical, "Не коректно задано к-сть рядів!"
                )
                return 0
            self.clear_layout(self.verticalLayout_10)
            self.num_list = list()
            for i in range(int(self.ryad.text())):
                name_ryad = QLabel(
                    f"Введіть кількість місць в {i+1} ряді:", self.add_dialog
                )
                name_ryad.setAlignment(Qt.AlignmentFlag.AlignCenter)
                num_place = QLineEdit(self.add_dialog)
                num_place.setMinimumSize(QSize(0, 35))
                ryad_layout = QVBoxLayout()
                ryad_layout.addWidget(name_ryad)
                ryad_layout.addWidget(num_place)
                self.verticalLayout_10.insertLayout(i, ryad_layout)
                self.num_list.append(num_place)

        self.name_zal_label = QLabel("Назва Зали", self.add_dialog)
        self.name_zal_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_zal = QLineEdit(self.add_dialog)
        self.name_zal.setMinimumSize(QSize(150, 40))
        self.name_zal.setMaximumSize(QSize(150, 40))
        self.name_zal_layout = QVBoxLayout()
        self.name_zal_layout.addWidget(self.name_zal_label)
        self.name_zal_layout.addWidget(self.name_zal)
        self.verticalLayout_5.insertLayout(0, self.name_zal_layout)

        self.ryad_label = QLabel("Кількість рядів", self.add_dialog)
        self.ryad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ryad = QLineEdit(self.add_dialog)
        self.ryad.setMinimumSize(QSize(150, 40))
        self.ryad.setMaximumSize(QSize(150, 40))
        self.ryad_layout = QVBoxLayout()
        self.ryad_layout.addWidget(self.ryad_label)
        self.ryad_layout.addWidget(self.ryad)
        self.verticalLayout_5.insertLayout(1, self.ryad_layout)
        self.verticalLayout_5.insertItem(2, self.verticalSpacer_5)

        self.ryad.editingFinished.connect(display_ryads)

        self.horizontalLayout.insertLayout(0, self.verticalLayout_5)
        self.horizontalLayout.insertLayout(1, self.verticalLayout_10)

        self.add_object_button_window = QPushButton("Додати зал", self.add_dialog)
        self.add_object_button_window.setMaximumSize(QSize(250, 50))
        self.add_object_button_window.clicked.connect(self.add_hall)

        self.cancel_button = QPushButton("Скасувати", self.add_dialog)
        self.cancel_button.setMaximumSize(QSize(250, 50))
        self.cancel_button.clicked.connect(self.cancel_add)

        self.horizontalLayout_1.insertWidget(0, self.add_object_button_window)
        self.horizontalLayout_1.insertWidget(1, self.cancel_button)

        self.add_dialog.show()

    def show_table_halls(self):
        if self.show_pointer == "":
            self.change_color(self.hall_button)
        elif self.show_pointer == "kino":
            self.change_color(self.hall_button, self.film_button)
        elif self.show_pointer == "session":
            self.change_color(self.hall_button, self.session_button)
        elif self.show_pointer == "user":
            self.change_color(self.hall_button, self.user_button)
        self.change_pointer = False
        self.show_pointer = "hall"
        self.clear_table()
        self.tableWidget_label.setText("Зали")

        temp_cursor = self.database.connection.cursor()
        request = """
                SELECT
                    Seats.id_Hall,
                    All_Halls.name_hall,
                    All_Halls.seats,
                    Seats.id_Rows,
                    COUNT(DISTINCT Seats.num_seats) AS sum_seats
                FROM 
                    Seats
                JOIN All_Halls ON Seats.id_Hall = All_Halls.id_Hall
                GROUP BY
                    Seats.id_Hall,
                    Seats.id_Rows;
                
                """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()

        columns = [
            "ІD зала",
            "Назва зали",
            "Загальна кількість місць",
            "Номер ряду",
            "Кількість місць в ряді",
        ]
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                font = QFont()
                font.setBold(False)
                item.setFont(font)
                self.tableWidget.setItem(row_idx, col_idx, item)

        self.change_pointer = True
        self.tableWidget.setColumnWidth(1, 160)
        self.tableWidget.setColumnWidth(2, 260)
        self.tableWidget.setColumnWidth(3, 260)
        self.tableWidget.setColumnWidth(4, 260)

    def show_add_session_window(self):
        self.add_dialog.setGeometry(850, 320, 0, 0)
        self.add_dialog.setFixedSize(0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout_1 = QHBoxLayout()
        self.add_dialog.setWindowTitle(f"Додавання нового сеансу")

        self.add_dialog.verticalLayout_1.insertLayout(0, self.horizontalLayout)
        self.add_dialog.verticalLayout_1.insertLayout(1, self.horizontalLayout_1)

        self.verticalLayout_5 = QVBoxLayout()

        self.kino_session_label = QLabel("Виберіть фільм:", self.add_dialog)
        self.kino_session_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.kino_session = QComboBox(self)
        self.kino_session.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog("name_kino", "kino")
        for i in options:
            self.kino_session.addItem(i[0])

        self.kino_session_layout = QVBoxLayout()
        self.kino_session_layout.addWidget(self.kino_session_label)
        self.kino_session_layout.addWidget(self.kino_session)
        self.verticalLayout_5.insertLayout(0, self.kino_session_layout)

        self.hall_session_label = QLabel("Виберіть зал:", self.add_dialog)
        self.hall_session_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hall_session = QComboBox(self)
        self.hall_session.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog("name_hall", "All_Halls")
        for i in options:
            self.hall_session.addItem(i[0])

        self.hall_session_layout = QVBoxLayout()
        self.hall_session_layout.addWidget(self.hall_session_label)
        self.hall_session_layout.addWidget(self.hall_session)
        self.verticalLayout_5.insertLayout(1, self.hall_session_layout)

        self.session_time_label = QLabel(self.add_dialog)
        self.session_time_label.setText(
            "Введіть час початку сеансу\n(Рік-місяць-день год:хв:сек"
        )
        self.session_time_label.setMaximumSize(280, 100)
        self.session_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.session_time = QDateTimeEdit()
        self.session_time.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.session_time.setDateTime(QDateTime.currentDateTime())

        self.session_time_layout = QVBoxLayout()
        self.session_time_layout.addWidget(self.session_time_label)
        self.session_time_layout.addWidget(self.session_time)
        self.verticalLayout_5.insertLayout(2, self.session_time_layout)

        self.session_price_label = QLabel("Введіть ціну за сеанс", self.add_dialog)
        self.session_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.session_price = QLineEdit(self.add_dialog)
        self.session_price.setMinimumSize(QSize(0, 40))
        self.session_price_layout = QVBoxLayout()
        self.session_price_layout.addWidget(self.session_price_label)
        self.session_price_layout.addWidget(self.session_price)
        self.verticalLayout_5.insertLayout(3, self.session_price_layout)

        self.horizontalLayout.insertLayout(0, self.verticalLayout_5)

        self.add_object_button_window = QPushButton("Додати сеанс", self.add_dialog)
        self.add_object_button_window.setMaximumSize(QSize(250, 50))
        self.add_object_button_window.clicked.connect(self.add_session)

        self.cancel_button = QPushButton("Скасувати", self.add_dialog)
        self.cancel_button.setMaximumSize(QSize(250, 50))
        self.cancel_button.clicked.connect(self.cancel_add)

        self.horizontalLayout_1.insertWidget(0, self.add_object_button_window)
        self.horizontalLayout_1.insertWidget(1, self.cancel_button)

        self.add_dialog.show()

    def show_table_session(self):
        if self.show_pointer == "":
            self.change_color(self.session_button)
        elif self.show_pointer == "kino":
            self.change_color(self.session_button, self.film_button)
        elif self.show_pointer == "hall":
            self.change_color(self.session_button, self.hall_button)
        elif self.show_pointer == "user":
            self.change_color(self.session_button, self.user_button)
        self.change_pointer = False
        self.show_pointer = "session"
        self.clear_table()
        self.tableWidget_label.setText("Сеанси")

        temp_cursor = self.database.connection.cursor()
        request = """
                        SELECT
                            Sessions.id_Session,
                            kino.name_kino,
                            All_Halls.name_hall,
                            Sessions.start_s,
                            Sessions.end_s,
                            Sessions.price
                            
                        FROM 
                            Sessions
                        JOIN All_Halls ON Sessions.id_Hall = All_Halls.id_Hall
                        JOIN kino ON Sessions.id_kino = kino.id_kino
                        ORDER BY 
                            Sessions.start_s;
                        """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()

        columns = [
            "ІD cеансу",
            "Назва фільму",
            "Назва зали",
            "Час початку",
            "Час закінчення",
            "До наступного сеансу",
            "Ціна сеансу",
        ]
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))

        self.tableWidget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                if col_idx == 5:
                    item = QTableWidgetItem(str(value))
                    font = QFont()
                    font.setBold(False)
                    item.setFont(font)
                    self.tableWidget.setItem(row_idx, col_idx + 1, item)
                else:
                    item = QTableWidgetItem(str(value))
                    font = QFont()
                    font.setBold(False)
                    item.setFont(font)
                    self.tableWidget.setItem(row_idx, col_idx, item)

        self.tableWidget.setColumnWidth(1, 350)
        self.tableWidget.setColumnWidth(2, 160)
        self.tableWidget.setColumnWidth(3, 250)
        self.tableWidget.setColumnWidth(4, 250)
        self.tableWidget.setColumnWidth(5, 220)
        self.tableWidget.setColumnWidth(6, 140)

        self.find_time_difference()

        def toggle_sorting(column):
            if column in [0, 1, 2, 3, 4, 5, 6]:
                self.tableWidget.setSortingEnabled(True)
                order = self.tableWidget.horizontalHeader().sortIndicatorOrder()
                self.tableWidget.sortItems(column, order)
                self.tableWidget.setSortingEnabled(False)

        self.tableWidget.horizontalHeader().sectionClicked.connect(toggle_sorting)

        self.change_pointer = True

    def find_time_difference(self):
        temp_cursor = self.database.connection.cursor()
        request = "SELECT id_Hall,name_hall FROM All_Halls"
        temp_cursor.execute(request)
        id_halls = temp_cursor.fetchall()

        for i in id_halls:
            id_hall = i[0]
            name_hall = i[1]
            request = (
                "SELECT start_s,end_s FROM Sessions WHERE id_Hall = %s ORDER BY start_s"
            )
            temp_cursor.execute(request, (id_hall))
            times = temp_cursor.fetchall()
            for j in range(len(times)):
                if j == len(times) - 1:
                    item_time = self.tableWidget.findItems(
                        datetime.datetime.strftime(times[j][0], "%Y-%m-%d %H:%M:%S"),
                        Qt.MatchExactly,
                    )
                    if len(item_time) > 1:
                        item_hall = self.tableWidget.findItems(
                            name_hall, Qt.MatchExactly
                        )
                        for k in range(len(item_time)):
                            item_time_value = item_time[k].row()
                            for m in range(len(item_hall)):
                                item_hall_value = item_hall[m].row()
                                if item_time_value == item_hall_value:
                                    self.change_pointer = False
                                    item = QTableWidgetItem("-- -- --")
                                    font = QFont()
                                    font.setBold(False)
                                    item.setFont(font)
                                    self.tableWidget.setItem(
                                        item_time[k].row(), 5, item
                                    )
                                    self.change_pointer = True
                    else:
                        self.change_pointer = False
                        item = QTableWidgetItem("-- -- --")
                        font = QFont()
                        font.setBold(False)
                        item.setFont(font)
                        self.tableWidget.setItem(item_time[0].row(), 5, item)
                        self.change_pointer = True

                else:
                    time_difference = times[j + 1][0] - times[j][1]
                    item_time = self.tableWidget.findItems(
                        datetime.datetime.strftime(times[j][0], "%Y-%m-%d %H:%M:%S"),
                        Qt.MatchExactly,
                    )
                    if len(item_time) > 1:
                        item_hall = self.tableWidget.findItems(
                            name_hall, Qt.MatchExactly
                        )
                        for k in range(len(item_time)):
                            item_time_value = item_time[k].row()
                            for m in range(len(item_hall)):
                                item_hall_value = item_hall[m].row()
                                if item_time_value == item_hall_value:
                                    item = QTableWidgetItem(str(time_difference))
                                    font = QFont()
                                    font.setBold(False)
                                    item.setFont(font)
                                    self.tableWidget.setItem(
                                        item_time[k].row(), 5, item
                                    )

                                    if time_difference > datetime.timedelta(
                                        hours=1, minutes=0, seconds=0
                                    ) and time_difference < datetime.timedelta(
                                        hours=2, minutes=0, seconds=0
                                    ):
                                        item = self.tableWidget.item(
                                            item_time[k].row(), 5
                                        )
                                        item.setBackground(QColor(255, 255, 0))
                                    elif time_difference > datetime.timedelta(
                                        hours=2, minutes=0, seconds=0
                                    ):
                                        item = self.tableWidget.item(
                                            item_time[k].row(), 5
                                        )
                                        item.setBackground(QColor(255, 0, 0))
                                    else:
                                        item = self.tableWidget.item(
                                            item_time[k].row(), 5
                                        )
                                        item.setBackground(QColor(0, 255, 0))
                                    self.change_pointer = True
                    else:
                        self.change_pointer = False
                        item = QTableWidgetItem(str(time_difference))
                        font = QFont()
                        font.setBold(False)
                        item.setFont(font)
                        self.tableWidget.setItem(item_time[0].row(), 5, item)
                        if time_difference > datetime.timedelta(
                            hours=1, minutes=0, seconds=0
                        ) and time_difference < datetime.timedelta(
                            hours=2, minutes=0, seconds=0
                        ):
                            item = self.tableWidget.item(item_time[0].row(), 5)
                            item.setBackground(QColor(255, 255, 0))
                        elif time_difference > datetime.timedelta(
                            hours=2, minutes=0, seconds=0
                        ):
                            item = self.tableWidget.item(item_time[0].row(), 5)
                            item.setBackground(QColor(255, 0, 0))
                        else:
                            item = self.tableWidget.item(item_time[0].row(), 5)
                            item.setBackground(QColor(0, 255, 0))
                        self.change_pointer = True

    def show_table_users(self):
        if self.show_pointer == "":
            self.change_color(self.user_button)
        elif self.show_pointer == "kino":
            self.change_color(self.user_button, self.film_button)
        elif self.show_pointer == "hall":
            self.change_color(self.user_button, self.hall_button)
        elif self.show_pointer == "session":
            self.change_color(self.user_button, self.session_button)

        self.change_pointer = False
        self.show_pointer = "user"
        self.clear_table()
        self.tableWidget_label.setText("Користувачі")

        temp_cursor = self.database.connection.cursor()
        request = """
                        SELECT
                            authorization.id_login,
                            authorization.password,
                            Catalog_access_rights.access_rights
                        FROM 
                            authorization
                        JOIN Catalog_access_rights ON authorization.access_id = Catalog_access_rights.id_access
                        """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()
        columns = ["Логін", "Пароль", "Права доступу"]
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                font = QFont()
                font.setBold(False)
                item.setFont(font)
                self.tableWidget.setItem(row_idx, col_idx, item)

        self.tableWidget.setColumnWidth(0, 180)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 250)

        self.change_pointer = True

    def show_add_user_window(self):
        self.add_dialog.setGeometry(850, 350, 0, 0)
        self.add_dialog.setFixedSize(0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout_1 = QHBoxLayout()
        self.add_dialog.setWindowTitle(f"Додавання нового користувача")

        self.add_dialog.verticalLayout_1.insertLayout(0, self.horizontalLayout)
        self.add_dialog.verticalLayout_1.insertLayout(1, self.horizontalLayout_1)

        self.verticalLayout_5 = QVBoxLayout()

        self.user_login_label = QLabel(
            "Введіть логін нового користувача", self.add_dialog
        )
        self.user_login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_login = QLineEdit(self.add_dialog)
        self.user_login.setMinimumSize(QSize(0, 40))
        self.user_login_layout = QVBoxLayout()
        self.user_login_layout.addWidget(self.user_login_label)
        self.user_login_layout.addWidget(self.user_login)
        self.verticalLayout_5.insertLayout(0, self.user_login_layout)

        self.user_password_label = QLabel(
            "Введіть пароль нового користувача", self.add_dialog
        )
        self.user_password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_password = QLineEdit(self.add_dialog)
        self.user_password.setMinimumSize(QSize(0, 40))
        self.user_password_layout = QVBoxLayout()
        self.user_password_layout.addWidget(self.user_password_label)
        self.user_password_layout.addWidget(self.user_password)
        self.verticalLayout_5.insertLayout(1, self.user_password_layout)

        self.user_permission_label = QLabel("Виберіть права доступу:", self.add_dialog)
        self.user_permission_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_permission = QComboBox(self)
        self.user_permission.setMinimumSize(QSize(150, 40))

        options = self.database.options_fr_catalog(
            "access_rights", "Catalog_access_rights"
        )
        for i in options:
            self.user_permission.addItem(i[0])

        self.user_permission_layout = QVBoxLayout()
        self.user_permission_layout.addWidget(self.user_permission_label)
        self.user_permission_layout.addWidget(self.user_permission)
        self.verticalLayout_5.insertLayout(2, self.user_permission_layout)

        self.horizontalLayout.insertLayout(0, self.verticalLayout_5)

        self.add_object_button_window = QPushButton(
            "Додати користувача", self.add_dialog
        )
        self.add_object_button_window.setMaximumSize(QSize(250, 50))
        self.add_object_button_window.clicked.connect(self.add_user)

        self.cancel_button = QPushButton("Скасувати", self.add_dialog)
        self.cancel_button.setMaximumSize(QSize(250, 50))
        self.cancel_button.clicked.connect(self.cancel_add)

        self.horizontalLayout_1.insertWidget(0, self.add_object_button_window)
        self.horizontalLayout_1.insertWidget(1, self.cancel_button)

        self.add_dialog.show()

    def change_color(self, button, button_1=None):
        new_style = """
                    QPushButton {
                        background-color: #bd0240; 
                        color: white; 
                        font-size: 30px; 
                        border-radius: 10px;
                        margin: 0 30px;
                        font-family: Franklin Gothic Heavy, sans-serif; 
                    }
                    QPushButton:pressed { 
                        background-color: white; 
                        color: #ff0055; 
                    }
                    """
        button.setStyleSheet(new_style)
        if button_1 != None:
            old_style = """
                        QPushButton {
                            background-color: #ff0055; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 15px;
                            margin: 0 20px;
                            font-family: Franklin Gothic Heavy, sans-serif; 
                        }
                        QPushButton:pressed { 
                            background-color: white; 
                            color: #ff0055; 
                        }
                        """
            button_1.setStyleSheet(old_style)
        else:
            return 0

    def add_item(self):
        if self.show_pointer == "kino":
            self.show_add_film_window()
        elif self.show_pointer == "hall":
            self.show_add_hall_window()
        elif self.show_pointer == "session":
            self.show_add_session_window()
        elif self.show_pointer == "user":
            self.show_add_user_window()

    def cancel_add(self):
        self.add_dialog.clear_area()
        self.add_dialog.accept()

    def add_kino(self):
        if self.name_kino.text() == "":
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не введено назву фільма!"
            )
            return 0
        if not re.match(
            r"^([0-1]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$",
            self.duration_film.text(),
        ):
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не правильно задано тривалість фільму!"
            )
            return 0
        if not re.match(
            r"^(18\d{2}|19\d{2}|20[0-3]\d|2040)$", self.graduation_year.text()
        ):
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не правильно вказаний рік випуску!"
            )
            return 0
        if self.s_description.toPlainText() == "":
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не введено опис фільму!"
            )
            return 0
        try:
            temp_cursor = self.database.connection.cursor()
            request = "SELECT `id_age` FROM `Catalog_age` WHERE `age_restrictions` = %s"
            temp_cursor.execute(request, self.age_restrictions.currentText())
            age_rest_id = temp_cursor.fetchall()

            request = (
                "SELECT `id_countries` FROM `Catalog_countries` WHERE `countries` = %s"
            )
            temp_cursor.execute(request, self.countries.currentText())
            countrie_id = temp_cursor.fetchall()

            request = (
                "SELECT `id_genres` FROM `Catalog_of_genres` WHERE `genre_kino` = %s"
            )
            temp_cursor.execute(request, self.genre.currentText())
            genre_kino_id = temp_cursor.fetchall()

            objects = (
                self.name_kino.text(),
                age_rest_id[0][0],
                countrie_id[0][0],
                genre_kino_id[0][0],
                self.graduation_year.text(),
                self.duration_film.text(),
                self.image_binary_data,
                self.s_description.toPlainText(),
            )

            request = (
                "INSERT INTO kino "
                "(name_kino,id_age_restrictions,id_countries,genre_kino,graduation_year,duration_film,image_kino,s_description) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
            self.show_dialog_message(
                QMessageBox.Icon.Information, "Новий фільм додано успішно:"
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ДОДАНО {self.name_kino.text()} в таблицю kino",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
            self.add_dialog.clear_area()
            self.add_dialog.accept()
            self.show_table_film()

        except AttributeError:
            self.show_dialog_message(QMessageBox.Icon.Warning, "Не вибрано зображення!")

    def add_hall(self):
        if self.name_zal.text() == "":
            self.show_dialog_message(QMessageBox.Icon.Critical, "Не введено ім'я зали!")
            return 0
        if self.ryad.text() == "":
            self.show_dialog_message(
                QMessageBox.Icon.Critical, "Не введено кількість рядів!"
            )
            return 0
        place_list = list()
        for i in self.num_list:
            if not re.match(r"\b(?:[1-9]|[1-9]\d|100)\b", i.text()):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical, "Не коректно задано к-сть міцсь в ряді!"
                )
                return 0
            place_list.append(int(i.text()))
        all_places = sum(place_list)

        temp_cursor = self.database.connection.cursor()
        request = "INSERT INTO All_Halls (name_hall,seats) VALUES (%s,%s);"
        values = (self.name_zal.text(), all_places)
        temp_cursor.execute(request, values)
        self.database.connection.commit()
        id_hall = temp_cursor.lastrowid

        request_1 = (
            "INSERT INTO Seats (id_Hall,nomer_S,id_Rows,num_seats) VALUES (%s,%s,%s,%s)"
        )
        for i in range(int(self.ryad.text())):
            for j in range(place_list[i]):
                objects = (id_hall, 0, i + 1, j + 1)
                temp_cursor.execute(request_1, objects)
                self.database.connection.commit()

        self.show_dialog_message(
            QMessageBox.Icon.Information, "Новий зал додано успішно:"
        )
        request = "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
        objects = (
            self.user_name,
            f"ДОДАНО зал {self.name_zal.text()} в таблицю All_Halls",
            datetime.datetime.now(),
        )
        temp_cursor.execute(request, objects)
        self.database.connection.commit()
        self.add_dialog.clear_area()
        self.add_dialog.accept()
        self.show_table_halls()

    def add_session(self):
        if not re.match(
            r"^\s*(18[0-9]{2}|19[0-9]{2}|20[0-9]{2})\s*-\s*(0?[1-9]|1[0-2])\s*-\s*(0?[1-9]|[12][0-9]|3[01])\s+(0?[0-9]|1[0-9]|2[0-3])\s*:\s*(0?[0-9]|[1-5][0-9])\s*:\s*(0?[0-9]|[1-5][0-9])\s*$",
            self.session_time.text(),
        ):
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не правильно задано час початку сесії!"
            )
            return 0
        if not re.match(
            r"^[+-]?\$?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{2})?$",
            self.session_price.text(),
        ):
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Не правильно задано валюту!"
            )
            return 0
        temp_cursor = self.database.connection.cursor()
        request = "SELECT `id_kino` FROM `kino` WHERE `name_kino` = %s"
        temp_cursor.execute(request, self.kino_session.currentText())
        film_id = temp_cursor.fetchall()[0][0]

        request = "SELECT duration_film FROM kino WHERE id_kino = %s"
        temp_cursor.execute(request, film_id)
        film_duration = temp_cursor.fetchall()[0][0]

        request = "SELECT `id_Hall` FROM `All_Halls` WHERE `name_hall` = %s"
        temp_cursor.execute(request, self.hall_session.currentText())
        hall_id = temp_cursor.fetchall()[0][0]

        request = "SELECT nomer_S,start_s,end_s FROM Sessions WHERE id_Hall = %s ORDER BY start_s"
        temp_cursor.execute(request, hall_id)
        times = temp_cursor.fetchall()

        entered_time = datetime.datetime.strptime(
            self.session_time.text(), "%Y-%m-%d %H:%M:%S"
        )

        for i in range(len(times)):
            if entered_time >= times[i][1] and entered_time <= times[i][2]:
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час початку сеансу співпадє з показом {i+1} сеансу!",
                )
                return 0
            elif (
                i > 0
                and entered_time >= times[i - 1][2]
                and entered_time <= times[i][1]
                and entered_time + film_duration > times[i][1]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i+1} сеансу!",
                )
                return 0
            elif (
                i == 0
                and entered_time <= times[i][1]
                and entered_time + film_duration >= times[i][1]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i+1} сеансу!",
                )
                return 0

        request = "SELECT MAX(nomer_S) FROM Seats WHERE id_Hall = %s"
        temp_cursor.execute(request, (hall_id))
        max_session = temp_cursor.fetchall()[0][0]

        request = "SELECT id_Rows,MAX(num_seats) FROM Seats WHERE id_Hall = %s GROUP BY id_Rows;"
        temp_cursor.execute(request, (hall_id))
        data = temp_cursor.fetchall()

        main_request = "INSERT INTO Sessions (nomer_S,id_kino,id_Hall,start_s,price) VALUES (%s,%s,%s,%s,%s)"

        request_1 = (
            "INSERT INTO Seats (id_Hall,nomer_S,id_Rows,num_seats) VALUES (%s,%s,%s,%s)"
        )
        for i in data:
            for j in range(i[1]):
                objects = (hall_id, max_session + 1, i[0], j + 1)
                temp_cursor.execute(request_1, objects)
                self.database.connection.commit()

        values = (
            max_session + 1,
            film_id,
            hall_id,
            entered_time,
            self.session_price.text(),
        )
        temp_cursor.execute(main_request, values)
        self.database.connection.commit()
        self.show_dialog_message(QMessageBox.Icon.Information, "Сеанс додано успішно")
        request = "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
        objects = (
            self.user_name,
            f"ДОДАНО сеанс на {entered_time} в залі {hall_id}",
            datetime.datetime.now(),
        )
        temp_cursor.execute(request, objects)
        self.database.connection.commit()
        self.add_dialog.accept()
        self.add_dialog.clear_area()
        self.show_table_session()

    def add_user(self):
        if self.user_login.text() == "":
            self.show_dialog_message(QMessageBox.Icon.Warning, "Не введено логін!")
            return 0
        if self.user_password.text() == "":
            self.show_dialog_message(QMessageBox.Icon.Warning, "Не введено пароль!")
            return 0
        temp_cursor = self.database.connection.cursor()
        if self.user_permission.currentText() == "Адміністратор":
            id_access = 1
        elif self.user_permission.currentText() == "Касир":
            id_access = 2

        objects = (self.user_login.text(), self.user_password.text(), id_access)
        request = (
            "INSERT INTO authorization "
            "(id_login,password,access_id) "
            "VALUES (%s, %s, %s);"
        )
        temp_cursor.execute(request, objects)
        self.database.connection.commit()
        self.show_dialog_message(
            QMessageBox.Icon.Information, "Користувача додано успішно:"
        )
        request = "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
        objects = (
            self.user_name,
            f"ДОДАНО користувача {self.user_login.text()}",
            datetime.datetime.now(),
        )
        temp_cursor.execute(request, objects)
        self.database.connection.commit()
        self.add_dialog.clear_area()
        self.add_dialog.accept()
        self.show_table_users()

    def delete_item(self, row, column):
        if self.show_pointer == "kino":
            self.delete_kino(row, column)
        elif self.show_pointer == "hall":
            self.delete_hall(row, column)
        elif self.show_pointer == "session":
            self.delete_session(row, column)
        elif self.show_pointer == "user":
            self.delete_user(row, column)

    def delete_kino(self, row, column):
        temp_cursor = self.database.connection.cursor()

        msg_box = QMessageBox(self)
        msg_box.setText(
            f"Ви впевнені, що хочете видалити фільм {self.tableWidget.item(row,1).text()}?"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet(
            """
                  QMessageBox {
                      background-color: white;
                      font-size: 16px;
                  }
                  QLabel {
                    background-color: white;
                    color: black;
                  }
                  QPushButton {
                      background-color: white;
                      border: 1px solid black;
                      padding: 5px 20px;
                      color: black;
                  }
              """
        )

        reply = msg_box.exec()
        id_kino = self.tableWidget.item(row, 0).text()
        if reply == QMessageBox.No:
            return 0
        else:

            request = "DELETE FROM Sessions WHERE id_kino = %s;"
            temp_cursor.execute(request, id_kino)

            request = "DELETE FROM kino WHERE id_kino = %s"
            temp_cursor.execute(request, id_kino)
            self.database.connection.commit()

            request = "ALTER TABLE db_findtick.kino AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)
            request = "ALTER TABLE db_findtick.Sessions AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)
            self.show_dialog_message(
                QMessageBox.Icon.Information, "Фільм видалено успішно"
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ВИДАЛЕНО фільм {self.tableWidget.item(row,1).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
            self.show_table_film()

    def delete_hall(self, row, column):
        temp_cursor = self.database.connection.cursor()

        msg_box = QMessageBox(self)
        msg_box.setText(
            f"Ви впевнені, що хочете видалити зал {self.tableWidget.item(row,1).text()}?"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet(
            """
                  QMessageBox {
                      background-color: white;
                      font-size: 16px;
                  }
                  QLabel {
                    background-color: white;
                    color: black;
                  }
                  QPushButton {
                      background-color: white;
                      border: 1px solid black;
                      padding: 5px 20px;
                      color: black;
                  }
              """
        )

        reply = msg_box.exec()

        if reply == QMessageBox.No:
            return 0
        else:
            id_hall = self.tableWidget.item(row, 0).text()

            request = "DELETE FROM Sessions WHERE id_Hall = %s;"
            temp_cursor.execute(request, id_hall)

            temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            request = "DELETE FROM Seats WHERE id_Hall = %s;"
            temp_cursor.execute(request, id_hall)

            temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            self.database.connection.commit()
            request = "DELETE FROM All_Halls WHERE id_Hall = %s"
            temp_cursor.execute(request, id_hall)
            self.database.connection.commit()

            request = "ALTER TABLE db_findtick.All_Halls AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)

            request = "ALTER TABLE db_findtick.Seats AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)
            request = "ALTER TABLE db_findtick.Sessions AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)

            self.database.connection.commit()
            self.show_dialog_message(
                QMessageBox.Icon.Information, "Зал видалено успішно"
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ВИДАЛЕНО залу {self.tableWidget.item(row,1).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
            self.show_table_halls()

    def delete_session(self, row, column):
        temp_cursor = self.database.connection.cursor()

        msg_box = QMessageBox(self)
        msg_box.setText(
            f"Ви впевнені, що хочете видалити сеанс з зали {self.tableWidget.item(row,2).text()}?"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet(
            """
                  QMessageBox {
                      background-color: white;
                      font-size: 16px;
                  }
                  QLabel {
                    background-color: white;
                    color: black;
                  }
                  QPushButton {
                      background-color: white;
                      border: 1px solid black;
                      padding: 5px 20px;
                      color: black;
                  }
              """
        )

        reply = msg_box.exec()

        if reply == QMessageBox.No:
            return 0
        else:
            request = "SELECT id_Hall FROM All_Halls WHERE name_hall =%s"
            temp_cursor.execute(request, self.tableWidget.item(row, 2).text())
            id_hall = temp_cursor.fetchall()[0][0]

            request = "SELECT id_Session,nomer_S FROM Sessions WHERE id_Hall =%s AND start_s = %s"
            temp_cursor.execute(
                request, (id_hall, self.tableWidget.item(row, 3).text())
            )
            data = temp_cursor.fetchall()

            id_session = data[0][0]
            nomer_s = data[0][1]
            temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            request = "DELETE FROM Sessions WHERE id_Session = %s"
            temp_cursor.execute(request, id_session)

            request = "DELETE FROM Seats WHERE id_Hall = %s AND nomer_S = %s"
            temp_cursor.execute(request, (id_hall, nomer_s))

            request = "ALTER TABLE db_findtick.Sessions AUTO_INCREMENT = 0;"
            temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            temp_cursor.execute(request)
            self.database.connection.commit()

            self.show_dialog_message(
                QMessageBox.Icon.Information, "Сеанс видалено успішно"
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ВИДАЛЕНО сеанс на {self.tableWidget.item(row,3).text()} в залі {self.tableWidget.item(row,2).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()

            self.show_table_session()

    def delete_user(self, row, column):
        temp_cursor = self.database.connection.cursor()

        msg_box = QMessageBox(self)
        msg_box.setText(
            f"Ви впевнені, що хочете видалити користувача {self.tableWidget.item(row,0).text()}?"
        )
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet(
            """
                  QMessageBox {
                      background-color: white;
                      font-size: 16px;
                  }
                  QLabel {
                    background-color: white;
                    color: black;
                  }
                  QPushButton {
                      background-color: white;
                      border: 1px solid black;
                      padding: 5px 20px;
                      color: black;
                  }
              """
        )

        reply = msg_box.exec()

        if reply == QMessageBox.No:
            return 0
        else:
            request = "DELETE FROM authorization WHERE id_login = %s"
            temp_cursor.execute(request, self.tableWidget.item(row, 0).text())

            request = "ALTER TABLE db_findtick.authorization AUTO_INCREMENT = 0;"
            temp_cursor.execute(request)

            self.database.connection.commit()
            self.show_dialog_message(
                QMessageBox.Icon.Information, "Користувача видалено успішно"
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ВИДАЛЕНО користувача {self.tableWidget.item(row,0).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
            self.show_table_users()

    def change_value(self, row, column):
        if self.show_pointer == "kino":
            self.change_value_kino(row, column)
        if self.show_pointer == "hall":
            self.change_value_hall(row, column)
        if self.show_pointer == "session":
            self.change_value_session(row, column)
        if self.show_pointer == "user":
            self.change_value_user(row, column)

    def clicked_value(self, row, column):
        if self.show_pointer == "kino":
            self.clicked_value_kino(row, column)
        if self.show_pointer == "hall":
            self.clicked_value_hall(row, column)
        if self.show_pointer == "session":
            self.clicked_value_session(row, column)
        if self.show_pointer == "user":
            self.clicked_value_user(row, column)

    def change_value_kino(
        self, row, column
    ):  # columns: 5 - year,  6 - time,  8 - textbox
        if self.change_pointer == False:
            return 0
        else:
            temp_cursor = self.database.connection.cursor()
            self.id_film = self.tableWidget.item(row, 0).text()
            if column == 1:
                item = self.tableWidget.item(row, column).text()
                if item == "":
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Назву фільму введено некоректно"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                column_name = self.tableWidget.horizontalHeaderItem(column).text()
                request = f"UPDATE kino SET name_kino = %s WHERE id_kino = %s"
                values = (item, self.id_film)
                temp_cursor.execute(request, values)
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Назву фільму змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО НАЗВУ ФІЛЬМУ: {self.previous_value} --> {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            elif column == 5:
                item = self.tableWidget.item(row, column).text()
                if item == "" or not re.match(
                    r"^(18\d{2}|19\d{2}|20[0-3]\d|2040)$", item
                ):
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Не правильно вказаний рік випуску!"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                column_name = self.tableWidget.horizontalHeaderItem(column).text()
                request = f"UPDATE kino SET graduation_year = %s WHERE id_kino = %s"
                values = (item, self.id_film)
                temp_cursor.execute(request, values)
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Рік випуску змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО РІК ВИПУСКУ ФІЛЬМУ {self.tableWidget.item(row,1).text()}: {self.previous_value} --> {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            elif column == 8:
                item = self.tableWidget.item(row, column).text()
                if item == "":
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Опис заповнено некоректно"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                column_name = self.tableWidget.horizontalHeaderItem(column).text()
                request = f"UPDATE kino SET s_description = %s WHERE id_kino = %s"
                values = (item, self.id_film)
                temp_cursor.execute(request, values)
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Опис фільму змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ОПИС ФІЛЬМУ {self.tableWidget.item(row,1).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            self.show_table_film()

    def clicked_value_kino(self, row, column):
        temp_cursor = self.database.connection.cursor()
        self.id_film = self.tableWidget.item(row, 0).text()

        def temp_window(
            table,
            id_table,
            value_table,
            id_main_table,
            label_1,
            label_2,
            row=row,
            column=column,
        ):
            dialog = QDialog(self)
            font = QFont()
            font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
            font.setPointSize(16)
            dialog.setFont(font)
            dialog.setWindowTitle(f"Зміна значення для фільму {label_1}")
            dialog.setGeometry(700, 350, 250, 150)

            dialog.setStyleSheet(
                """
                background-color: white;
                """
            )

            horizontal_layout = QHBoxLayout()
            vertical_layout = QVBoxLayout()
            label = QLabel(f"Виберіть нове значення для параметру\n {label_2}:", dialog)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vertical_layout.addWidget(label)

            combo_box = QComboBox(self)
            combo_box.setMinimumSize(QSize(150, 40))
            options = self.database.options_fr_catalog(value_table, table)
            for i in options:
                combo_box.addItem(i[0])
            vertical_layout.addWidget(combo_box)
            combo_box.setCurrentText(self.tableWidget.item(row, column).text())

            submit_but = QPushButton("Підтвердити зміну", dialog)
            submit_but.clicked.connect(
                lambda: save_changes(
                    dialog,
                    combo_box,
                    table,
                    id_table,
                    value_table,
                    id_main_table,
                    label_2,
                )
            )
            submit_but.setMinimumSize(QSize(100, 40))
            vertical_layout.addWidget(submit_but)
            horizontal_layout.insertLayout(0, vertical_layout)
            dialog.setLayout(horizontal_layout)

            dialog.show()

        def save_changes(
            dialog, combo_box, table, id_table, value_table, id_main_table, label_2
        ):
            request = f"SELECT {id_table} FROM {table} WHERE {value_table} = %s"
            temp_cursor.execute(request, combo_box.currentText())
            age_rest_id = temp_cursor.fetchall()
            request = f"UPDATE kino SET {id_main_table} = %s WHERE id_kino = %s"
            temp_cursor.execute(request, (age_rest_id, self.id_film))
            self.database.connection.commit()
            self.show_dialog_message(
                QMessageBox.Icon.Information, f"{label_2} змінено успішно"
            )
            dialog.accept()
            self.show_table_film()

        if column == 7:
            self.choose_foto()
            if self.image_binary_data == "":
                self.show_dialog_message(
                    QMessageBox.Icon.Warning, "Не вибрано зображення!"
                )
                return 0
            else:
                request = f"UPDATE kino SET image_kino = %s WHERE id_kino = %s"
                temp_cursor.execute(request, (self.image_binary_data, self.id_film))
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Зображення змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ЗОБРАЖЕННЯ ФІЛЬМУ: {self.tableWidget.item(row,1).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()
                self.show_table_film()
                return 0

        self.previous_value = self.tableWidget.item(row, column).text()

        if column == 2:  # Age restriction column
            temp_window(
                "Catalog_age",
                "id_age",
                "age_restrictions",
                "id_age_restrictions",
                self.tableWidget.item(row, 1).text(),
                "Вікові обмеження",
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО ВІКОВІ ОБМЕЖЕННЯ ФІЛЬМУ:{self.tableWidget.item(row, 1).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        elif column == 3:
            temp_window(
                "Catalog_countries",
                "id_countries",
                "countries",
                "id_countries",
                self.tableWidget.item(row, 1).text(),
                "Країна",
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО КРАЇНУ ВИПУСКУ ФІЛЬМУ: {self.tableWidget.item(row, 1).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        elif column == 4:
            temp_window(
                "Catalog_of_genres",
                "id_genres",
                "genre_kino",
                "genre_kino",
                self.tableWidget.item(row, 1).text(),
                "Жанр",
            )
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО ЖАНР ФІЛЬМУ: {self.tableWidget.item(row, 1).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        elif column == 5:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 6:
            self.show_dialog_message(
                QMessageBox.Icon.Warning,
                "Тривалість фільму не можу бути змінена вручну!",
            )
            return 0
        elif column == 8:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 1:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 0:
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Запис про ID не може бути змінено вручну!"
            )
            return 0

    def change_value_hall(self, row, column):
        if self.change_pointer == False:
            return 0
        else:
            temp_cursor = self.database.connection.cursor()
            if column == 1:
                item = self.tableWidget.item(row, column).text()
                if item == "":
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Назва залу введена некоректно"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                id_hall = self.tableWidget.item(row, 0).text()

                request = "UPDATE All_Halls SET name_hall = %s WHERE id_Hall = %s"
                temp_cursor.execute(request, (item, id_hall))
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Назва залу змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО НАЗВУ ЗАЛИ: {self.previous_value} --> {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            elif column == 4:
                item = self.tableWidget.item(row, column).text()
                if not re.match(r"\b(?:[1-9]|[1-9]\d|100)\b", item):
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "К-сть місць введено некоректно"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                id_hall = self.tableWidget.item(row, 0).text()
                id_row = self.tableWidget.item(row, 3).text()
                riz = int(item) - int(self.previous_value)

                request = "SELECT MAX(nomer_S) FROM Seats WHERE id_Hall = %s"
                temp_cursor.execute(request, id_hall)
                max_session = temp_cursor.fetchall()

                temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                request = "DELETE FROM Seats WHERE id_Hall = %s AND id_Rows = %s"
                temp_cursor.execute(request, (id_hall, id_row))
                temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                self.database.connection.commit()

                request_1 = "INSERT INTO Seats (id_Hall,nomer_S,id_Rows,num_seats) VALUES (%s,%s,%s,%s)"
                if max_session[0][0] == 0:
                    for j in range(int(item)):
                        objects = (id_hall, 0, id_row, j + 1)
                        temp_cursor.execute(request_1, objects)
                        self.database.connection.commit()
                else:
                    for k in range(max_session[0][0]):
                        for j in range(int(item)):
                            objects = (id_hall, k + 1, id_row, j + 1)
                            temp_cursor.execute(request_1, objects)
                            self.database.connection.commit()

                request = "UPDATE All_Halls SET seats = seats + %s WHERE id_Hall = %s"
                temp_cursor.execute(request, (riz, id_hall))
                self.database.connection.commit()

                self.show_dialog_message(
                    QMessageBox.Icon.Information,
                    f"К-сть місць в ряду {id_row} змінено успішно",
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО К-СТЬ МІСЦЬ В РЯДІ №{id_row} ЗАЛИ {self.tableWidget.item(row,1).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            self.show_table_halls()

    def clicked_value_hall(self, row, column):
        self.previous_value = self.tableWidget.item(row, column).text()
        temp_cursor = self.database.connection.cursor()

        if column == 3:

            def temp_window(id_hall, row_id):
                dialog = QDialog(self)
                dialog.setWindowTitle("Зміна рядів")
                dialog.setGeometry(700, 350, 250, 150)
                font = QFont()
                font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
                font.setPointSize(16)
                dialog.setFont(font)

                dialog.setStyleSheet(
                    """
                    background-color: white;
                    """
                )

                vertical_layout_1 = QVBoxLayout()

                label = QLabel("Виберіть дію з рядами:", dialog)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                vertical_layout_1.insertWidget(0, label)

                horizontal_layout_1 = QHBoxLayout()
                vertical_layout_2 = QVBoxLayout()

                label = QLabel("Виберіть кількість місць\n для нового ряду:", dialog)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                edit = QLineEdit(dialog)

                add_ryad_button = QPushButton("Додати ряд", dialog)
                add_ryad_button.clicked.connect(
                    lambda: add_ryad(dialog, id_hall, edit.text(), row_id)
                )
                add_ryad_button.setMinimumSize(QSize(100, 40))

                vertical_layout_2.insertWidget(0, label)
                vertical_layout_2.insertWidget(1, edit)
                vertical_layout_2.insertWidget(2, add_ryad_button)

                horizontal_layout_1.insertLayout(0, vertical_layout_2)

                vertical_layout = QVBoxLayout()
                delete_ryad_button = QPushButton("Видалити ряд", dialog)
                delete_ryad_button.clicked.connect(
                    lambda: delete_ryad(dialog, id_hall, row_id)
                )
                delete_ryad_button.setMinimumSize(QSize(250, 50))
                vertical_layout.addWidget(delete_ryad_button)
                horizontal_layout_1.insertLayout(1, vertical_layout)

                vertical_layout_1.insertLayout(1, horizontal_layout_1)

                dialog.setLayout(vertical_layout_1)

                dialog.show()

            def add_ryad(dialog, id_hall, item, id_row):
                if not re.match(r"\b(?:[1-9]|[1-9]\d|100)\b", item):
                    self.show_dialog_message(
                        QMessageBox.Icon.Critical,
                        "Не коректно задано к-сть міцсь в ряді!",
                    )
                    return 0
                request = "SELECT MAX(nomer_S) FROM Seats WHERE id_Hall = %s"
                temp_cursor.execute(request, self.tableWidget.item(row, 0).text())
                max_session = temp_cursor.fetchall()[0][0]

                request_1 = "INSERT INTO Seats (id_Hall,nomer_S,id_Rows,num_seats) VALUES (%s,%s,%s,%s)"
                if max_session == 0:
                    for j in range(int(item)):
                        objects = (id_hall, 0, id_row + 1, j + 1)
                        temp_cursor.execute(request_1, objects)
                        self.database.connection.commit()
                for k in range(max_session):
                    for j in range(int(item)):
                        objects = (id_hall, k + 1, id_row + 1, j + 1)
                        temp_cursor.execute(request_1, objects)
                        self.database.connection.commit()

                request = "UPDATE All_Halls SET seats = seats + %s WHERE id_Hall = %s"
                temp_cursor.execute(request, (int(item), id_hall))
                self.database.connection.commit()

                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Ряд додано успішно"
                )
                self.show_table_halls()
                dialog.accept()

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ДОДАНО РЯД В ЗАЛ: {self.tableWidget.item(row,1).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            def delete_ryad(dialog, id_hall, id_row):

                request_1 = "SELECT MAX(num_seats) FROM Seats WHERE id_Hall = %s AND id_Rows = %s"
                temp_cursor.execute(request_1, (id_hall, id_row))
                data = temp_cursor.fetchall()

                request = "UPDATE All_Halls SET seats = seats - %s WHERE id_Hall = %s"
                temp_cursor.execute(request, (data, id_hall))
                self.database.connection.commit()

                temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                request = "DELETE FROM Seats WHERE id_Hall = %s AND id_Rows = %s"
                temp_cursor.execute(request, (id_hall, id_row))
                temp_cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                self.database.connection.commit()

                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Ряд видалено успішно"
                )
                self.show_table_halls()
                dialog.accept()

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ВИДАЛЕНО РЯД З ЗАЛИ {self.tableWidget.item(row,1).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            request = "SELECT MAX(id_Rows) FROM Seats WHERE id_Hall = %s"
            temp_cursor.execute(request, (self.tableWidget.item(row, 0).text()))
            data = temp_cursor.fetchall()

            temp_window(self.tableWidget.item(row, 0).text(), data[0][0])

        elif column == 1:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 4:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 0 or column == 2:
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Запис не може бути змінено вручну!"
            )
            return 0

    def change_value_session(
        self, row, column
    ):  # 0 - id, 1 - film, 2 - hall, 3- start, 4-end, 5 - price
        if self.change_pointer == False:
            return 0
        else:
            temp_cursor = self.database.connection.cursor()

            if column == 6:
                item = self.tableWidget.item(row, column).text()
                if not re.match(
                    r"^[+-]?\$?(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{2})?$", item
                ):
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Вартість сеансу введено некоректно"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0

                id_session = self.tableWidget.item(row, 0).text()
                request = "UPDATE Sessions SET price = %s WHERE id_Session = %s"
                temp_cursor.execute(request, (item, id_session))
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Вартість сеансу змінено успішно"
                )

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ВАРТІСТЬ СЕАНСУ НА {self.tableWidget.item(row,3).text()} ЗАЛИ {self.tableWidget.item(row,2).text()}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

            elif column == 3:
                item = self.tableWidget.item(row, column).text()
                if not re.match(
                    r"^\s*(18[0-9]{2}|19[0-9]{2}|20[0-9]{2})\s*-\s*(0?[1-9]|1[0-2])\s*-\s*(0?[1-9]|[12][0-9]|3[01])\s+(0?[0-9]|1[0-9]|2[0-3])\s*:\s*(0?[0-9]|[1-5][0-9])\s*:\s*(0?[0-9]|[1-5][0-9])\s*$",
                    item,
                ):
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning,
                        "Час початку сеансу введено некоректно",
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                film_duration = datetime.datetime.strptime(
                    self.tableWidget.item(row, 4).text(), "%Y-%m-%d %H:%M:%S"
                ) - datetime.datetime.strptime(self.previous_value, "%Y-%m-%d %H:%M:%S")

                request = "SELECT id_Hall FROM All_Halls WHERE name_hall = %s"
                temp_cursor.execute(request, self.tableWidget.item(row, 2).text())
                id_hall = temp_cursor.fetchall()[0][0]

                request = "SELECT start_s,end_s FROM Sessions WHERE id_Hall = %s AND start_s!= %s ORDER BY start_s"
                temp_cursor.execute(request, (id_hall, self.previous_value))
                times = temp_cursor.fetchall()
                entered_time = datetime.datetime.strptime(item, "%Y-%m-%d %H:%M:%S")

                for i in range(len(times)):
                    if entered_time >= times[i][0] and entered_time <= times[i][1]:
                        self.show_dialog_message(
                            QMessageBox.Icon.Critical,
                            f"Час початку сеансу співпадє з показом {i + 1} сеансу!",
                        )
                        self.tableWidget.blockSignals(True)
                        self.tableWidget.setItem(
                            row, column, QTableWidgetItem(self.previous_value)
                        )
                        self.tableWidget.blockSignals(False)
                        return 0
                    elif (
                        i > 0
                        and entered_time >= times[i - 1][1]
                        and entered_time <= times[i][0]
                        and entered_time + film_duration > times[i][0]
                    ):
                        self.show_dialog_message(
                            QMessageBox.Icon.Critical,
                            f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                        )
                        self.tableWidget.blockSignals(True)
                        self.tableWidget.setItem(
                            row, column, QTableWidgetItem(self.previous_value)
                        )
                        self.tableWidget.blockSignals(False)
                        return 0
                    elif (
                        i == 0
                        and entered_time <= times[i][0]
                        and entered_time + film_duration >= times[i][0]
                    ):
                        self.show_dialog_message(
                            QMessageBox.Icon.Critical,
                            f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                        )
                        self.tableWidget.blockSignals(True)
                        self.tableWidget.setItem(
                            row, column, QTableWidgetItem(self.previous_value)
                        )
                        self.tableWidget.blockSignals(False)
                        return 0

                request = "UPDATE Sessions SET start_s=%s WHERE id_Session = %s"
                temp_cursor.execute(
                    request, (item, self.tableWidget.item(row, 0).text())
                )
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Час початку сеансу змінено успішно"
                )
                self.show_table_session()

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ЧАС ПОЧАТКУ СЕАНСУ ЗАЛИ {self.tableWidget.item(row,2).text()} З {self.previous_value} НА {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

    def clicked_value_session(self, row, column):
        self.previous_value = self.tableWidget.item(row, column).text()
        temp_cursor = self.database.connection.cursor()

        def temp_window(table, value_table, row, pointer, text):
            dialog = QDialog(self)
            dialog.setWindowTitle("Змінна параметру сеансу")
            dialog.setGeometry(700, 350, 250, 150)
            font = QFont()
            font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
            font.setPointSize(16)
            dialog.setFont(font)

            dialog.setStyleSheet(
                """
                background-color: white;
                """
            )

            horizontal_layout = QHBoxLayout()
            vertical_layout = QVBoxLayout()
            label = QLabel(f"Виберіть нов{text}:", dialog)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vertical_layout.addWidget(label)

            combo_box = QComboBox(self)
            combo_box.setMinimumSize(QSize(150, 40))
            options = self.database.options_fr_catalog(value_table, table)
            for i in options:
                combo_box.addItem(i[0])
            vertical_layout.addWidget(combo_box)

            submit_but = QPushButton("Підтвердити зміну", dialog)
            if pointer == "film":
                submit_but.clicked.connect(
                    lambda: self.session_kino_edit(dialog, combo_box, row)
                )
                combo_box.setCurrentText(self.tableWidget.item(row, 1).text())
            elif pointer == "hall":
                submit_but.clicked.connect(
                    lambda: self.session_hall_edit(dialog, combo_box, row)
                )
                combo_box.setCurrentText(self.tableWidget.item(row, 2).text())
            submit_but.setMinimumSize(QSize(100, 40))
            vertical_layout.addWidget(submit_but)
            horizontal_layout.insertLayout(0, vertical_layout)
            dialog.setLayout(horizontal_layout)

            dialog.show()

        if column == 1:
            temp_window("kino", "name_kino", row, "film", "ий фільм")
            self.show_table_session()
            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО ФІЛЬМ СЕАНСУ НА {self.tableWidget.item(row, 3).text()} ЗАЛИ {self.tableWidget.item(row, 2).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        if column == 2:
            temp_window("All_Halls", "name_hall", row, "hall", "у залу")
            self.show_table_session()

            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО ЗАЛУ СЕАНСУ НА {self.tableWidget.item(row, 3).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        if column == 0 or column == 4 or column == 5:
            self.show_dialog_message(
                QMessageBox.Icon.Warning, "Запис не може бути змінено вручну!"
            )
            return 0
        elif column == 3:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 6:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)

    def change_value_user(self, row, column):
        if self.change_pointer == False:
            return 0
        else:
            temp_cursor = self.database.connection.cursor()
            if column == 0:
                item = self.tableWidget.item(row, column).text()
                request = "SELECT id_login FROM authorization"
                temp_cursor.execute(request)
                data = temp_cursor.fetchall()
                item_1 = (item,)

                if item == "":
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Значення логіну задано не коректно!"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                elif item_1 in data:
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning,
                        "Значення логіну співпадає з вже існуючим!",
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0

                request = "UPDATE authorization SET id_login = %s WHERE id_login = %s"
                temp_cursor.execute(request, (item, self.previous_value))
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Логін змінено успішно!"
                )
                self.show_table_users()

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ЛОГІН З {self.previous_value} НА {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()
            elif column == 1:
                item = self.tableWidget.item(row, column).text()
                if item == "":
                    self.show_dialog_message(
                        QMessageBox.Icon.Warning, "Значення паролю задано не коректно!"
                    )
                    self.change_pointer = False
                    self.tableWidget.setItem(
                        row, column, QTableWidgetItem(self.previous_value)
                    )
                    self.change_pointer = True
                    return 0
                request = "UPDATE authorization SET password = %s WHERE id_login = %s"
                temp_cursor.execute(
                    request, (item, self.tableWidget.item(row, 0).text())
                )
                self.database.connection.commit()
                self.show_dialog_message(
                    QMessageBox.Icon.Information, "Пароль змінено успішно!"
                )
                self.show_table_users()

                request = (
                    "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
                )
                objects = (
                    self.user_name,
                    f"ЗМІНЕНО ПАРОЛЬ КОРИСТУВАЧА {self.tableWidget.item(row,0).text()} З {self.previous_value} НА {item}",
                    datetime.datetime.now(),
                )
                temp_cursor.execute(request, objects)
                self.database.connection.commit()

    def clicked_value_user(self, row, column):
        self.previous_value = self.tableWidget.item(row, column).text()
        temp_cursor = self.database.connection.cursor()

        def temp_window(table, value_table, user, row=row, column=column):
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Зміна прав користувача {user}")
            dialog.setGeometry(700, 350, 250, 150)
            font = QFont()
            font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
            font.setPointSize(16)
            dialog.setFont(font)

            dialog.setStyleSheet(
                """
                background-color: white;
                """
            )

            horizontal_layout = QHBoxLayout()
            vertical_layout = QVBoxLayout()
            label = QLabel("Виберіть нові права доступу користувача", dialog)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            vertical_layout.addWidget(label)

            combo_box = QComboBox(self)
            combo_box.setMinimumSize(QSize(150, 40))
            options = self.database.options_fr_catalog(value_table, table)
            for i in options:
                combo_box.addItem(i[0])
            combo_box.setCurrentText(self.tableWidget.item(row, column).text())
            vertical_layout.addWidget(combo_box)
            submit_but = QPushButton("Підтвердити зміну", dialog)
            submit_but.clicked.connect(lambda: save_change(dialog, combo_box, row))
            submit_but.setMinimumSize(QSize(100, 40))
            vertical_layout.addWidget(submit_but)
            horizontal_layout.insertLayout(0, vertical_layout)
            dialog.setLayout(horizontal_layout)

            dialog.show()

        def save_change(dialog, combo_box, row):
            if combo_box.currentText() == "Адміністратор":
                id_access = 1
            elif combo_box.currentText() == "Касир":
                id_access = 2

            request = "UPDATE authorization SET access_id = %s WHERE id_login = %s"
            temp_cursor.execute(
                request, (id_access, self.tableWidget.item(row, 0).text())
            )
            self.database.connection.commit()
            self.show_dialog_message(
                QMessageBox.Icon.Information, "Права доступу змінено успішно"
            )
            dialog.accept()
            self.show_table_users()

        if column == 2:
            temp_window(
                "Catalog_access_rights",
                "access_rights",
                self.tableWidget.item(row, 0).text(),
            )
            self.show_table_users()

            request = (
                "INSERT INTO actions (user,actions,date_actions) VALUES (%s,%s,%s)"
            )
            objects = (
                self.user_name,
                f"ЗМІНЕНО ПРАВА ДОСТУПУ КОРИСТУВАЧА {self.tableWidget.item(row, 0).text()}",
                datetime.datetime.now(),
            )
            temp_cursor.execute(request, objects)
            self.database.connection.commit()
        elif column == 0:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)
        elif column == 1:
            item = self.tableWidget.item(row, column)
            if item:
                self.tableWidget.editItem(item)

    def session_kino_edit(self, dialog, combo_box, row):
        temp_cursor = self.database.connection.cursor()
        request = "SELECT id_kino,duration_film FROM kino WHERE name_kino = %s"
        temp_cursor.execute(request, combo_box.currentText())
        textbox_value = temp_cursor.fetchall()
        film_duration = textbox_value[0][1]
        film_id = textbox_value[0][0]

        request = "SELECT id_Hall,start_s FROM Sessions WHERE id_Session = %s"
        temp_cursor.execute(request, self.tableWidget.item(row, 0).text())
        temp = temp_cursor.fetchall()
        id_hall = temp[0][0]
        entered_time = temp[0][1]

        request = "SELECT start_s,end_s FROM Sessions WHERE id_Hall = %s AND start_s!= %s ORDER BY start_s"
        temp_cursor.execute(request, (id_hall, entered_time))
        times = temp_cursor.fetchall()

        for i in range(len(times)):
            if entered_time >= times[i][0] and entered_time <= times[i][1]:
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час початку сеансу співпадє з показом {i + 1} сеансу!",
                )
                return 0
            elif (
                i > 0
                and entered_time >= times[i - 1][1]
                and entered_time <= times[i][0]
                and entered_time + film_duration > times[i][0]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                )
                return 0
            elif (
                i == 0
                and entered_time <= times[i][0]
                and entered_time + film_duration >= times[i][0]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                )
                return 0

        request = "UPDATE Sessions SET id_kino = %s WHERE id_Session = %s"
        temp_cursor.execute(request, (film_id, self.tableWidget.item(row, 0).text()))
        self.database.connection.commit()
        self.show_dialog_message(
            QMessageBox.Icon.Information, "Фільм для вказаного сеансу успішно змінено!"
        )
        self.show_table_session()
        dialog.accept()

    def session_hall_edit(self, dialog, combo_box, row):
        if self.previous_value == combo_box.currentText():
            self.show_dialog_message(QMessageBox.Icon.Warning, "Вибрано той же зал!")
            return 0

        temp_cursor = self.database.connection.cursor()
        request = "SELECT id_Hall FROM All_Halls WHERE name_hall = %s"
        temp_cursor.execute(request, combo_box.currentText())
        textbox_value = temp_cursor.fetchall()
        id_hall = textbox_value[0][0]

        request = (
            "SELECT start_s,end_s FROM Sessions WHERE id_Hall = %s ORDER BY start_s"
        )
        temp_cursor.execute(request, (id_hall))
        times = temp_cursor.fetchall()

        entered_time = datetime.datetime.strptime(
            self.tableWidget.item(row, 3).text(), "%Y-%m-%d %H:%M:%S"
        )
        film_duration = datetime.datetime.strptime(
            self.tableWidget.item(row, 4).text(), "%Y-%m-%d %H:%M:%S"
        ) - datetime.datetime.strptime(
            self.tableWidget.item(row, 3).text(), "%Y-%m-%d %H:%M:%S"
        )

        for i in range(len(times)):
            if entered_time >= times[i][0] and entered_time <= times[i][1]:
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час початку сеансу співпадє з показом {i + 1} сеансу!",
                )
                return 0
            elif (
                i > 0
                and entered_time >= times[i - 1][1]
                and entered_time <= times[i][0]
                and entered_time + film_duration > times[i][0]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                )
                return 0
            elif (
                i == 0
                and entered_time <= times[i][0]
                and entered_time + film_duration >= times[i][0]
            ):
                self.show_dialog_message(
                    QMessageBox.Icon.Critical,
                    f"Час закінчення сеансу співпадатиме з початком показу {i + 1} сеансу!",
                )
                return 0

        request = "UPDATE Sessions SET id_Hall = %s WHERE id_Session = %s"
        temp_cursor.execute(request, (id_hall, self.tableWidget.item(row, 0).text()))
        self.database.connection.commit()
        self.show_dialog_message(
            QMessageBox.Icon.Information, "Залу для вказаного сеансу успішно змінено!"
        )
        self.show_table_session()
        dialog.accept()

    def clear_table(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

    def clear_layout(self, current_layout):
        while current_layout.count():
            item = current_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                inner_layout = item.layout()
                if inner_layout is not None:
                    self.clear_layout(inner_layout)
                    inner_layout.deleteLater()

    def show_dialog_message(self, type, text):
        popup = QMessageBox()
        font = QFont()
        font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
        font.setPointSize(16)
        popup.setFont(font)
        popup.setWindowTitle("Повідомлення")
        popup.setText(text)
        popup.setIcon(type)
        popup.addButton(QMessageBox.StandardButton.Ok)
        popup.exec()

    def choose_foto(self):
        self.image_binary_data = ""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Image files (*.jpg *.jpeg *.png)"
        )
        if file_path:
            with open(file_path, "rb") as file:
                self.image_binary_data = file.read()

    def zvit_window_show(self):
        self.zvit_window.show()
        self.zvit_show_session()

    def zvit_show_session(self):
        if self.zvit_pointer == "":
            self.change_color(self.zvit_window.session_zvit_button)
        elif self.zvit_pointer == "kino":
            self.change_color(
                self.zvit_window.session_zvit_button, self.zvit_window.film_zvit_button
            )
        elif self.zvit_pointer == "hall":
            self.change_color(
                self.zvit_window.session_zvit_button, self.zvit_window.hall_zvit_button
            )
        elif self.zvit_pointer == "general":
            self.change_color(
                self.zvit_window.session_zvit_button,
                self.zvit_window.action_zvit_button,
            )
        self.zvit_pointer = "session"

        temp_cursor = self.database.connection.cursor()
        request = """
                SELECT DISTINCT
                     Profit_journal.num_S,
                     Profit_journal.id,
                     kino.name_kino,
                     All_Halls.name_hall,
                     Profit_journal.sold_seats,
                     Profit_journal.session_profit
                     
                FROM
                    Profit_journal
                JOIN All_Halls ON Profit_journal.name_hall = All_Halls.id_Hall
                JOIN kino ON Profit_journal.name_kino = kino.id_kino
                JOIN Sessions ON Profit_journal.num_S = Sessions.nomer_S
                                    """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()

        columns = [
            "ІD запису",
            "Назва фільму",
            "Назва зали",
            "Час початку сеансу",
            "К-сть проданих місць",
            "Загальний прибуток",
        ]
        self.zvit_window.tableWidget.setRowCount(len(data))
        self.zvit_window.tableWidget.setColumnCount(len(columns))
        self.zvit_window.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            n_session = data[row_idx][0]
            request = "SELECT id_Hall FROM All_Halls WHERE name_hall = %s"
            temp_cursor.execute(request, data[row_idx][3])
            id_hall = temp_cursor.fetchall()[0][0]
            request = "SELECT start_s FROM Sessions WHERE nomer_S = %s AND id_Hall = %s"
            temp_cursor.execute(request, (n_session, id_hall))
            start_s = temp_cursor.fetchall()[0][0]
            for col_idx, value in enumerate(row):
                if col_idx == 0:
                    continue
                elif col_idx == 4:
                    self.zvit_window.tableWidget.setItem(
                        row_idx, col_idx - 1, QTableWidgetItem(str(start_s))
                    )
                    self.zvit_window.tableWidget.setItem(
                        row_idx, col_idx, QTableWidgetItem(str(value))
                    )
                elif col_idx == 5:
                    self.zvit_window.tableWidget.setItem(
                        row_idx, col_idx, QTableWidgetItem(str(value))
                    )
                else:
                    self.zvit_window.tableWidget.setItem(
                        row_idx, col_idx - 1, QTableWidgetItem(str(value))
                    )
        self.zvit_window.tableWidget.setColumnWidth(3, 250)
        self.zvit_window.tableWidget.setColumnWidth(1, 300)
        self.zvit_window.tableWidget.setColumnWidth(5, 250)
        self.zvit_window.tableWidget.setColumnWidth(4, 250)
        self.zvit_window.tableWidget.setColumnWidth(0, 100)
        self.zvit_window.tableWidget.setColumnWidth(2, 140)

        def toggle_sorting(column):
            if column in [0, 1, 2, 3, 4, 5, 6]:
                self.zvit_window.tableWidget.setSortingEnabled(True)
                order = (
                    self.zvit_window.tableWidget.horizontalHeader().sortIndicatorOrder()
                )
                self.zvit_window.tableWidget.sortItems(column, order)
                self.zvit_window.tableWidget.setSortingEnabled(False)

        self.zvit_window.tableWidget.horizontalHeader().sectionClicked.connect(
            toggle_sorting
        )

    def zvit_show_film(self):
        if self.zvit_pointer == "":
            self.change_color(self.zvit_window.film_zvit_button)
        elif self.zvit_pointer == "hall":
            self.change_color(
                self.zvit_window.film_zvit_button, self.zvit_window.hall_zvit_button
            )
        elif self.zvit_pointer == "session":
            self.change_color(
                self.zvit_window.film_zvit_button, self.zvit_window.session_zvit_button
            )
        elif self.zvit_pointer == "general":
            self.change_color(
                self.zvit_window.film_zvit_button, self.zvit_window.action_zvit_button
            )
        self.zvit_pointer = "kino"
        self.zvit_window.tableWidget_label.setText("Звіти по фільмам")

        temp_cursor = self.database.connection.cursor()
        request = """
                SELECT 
                     kino.name_kino,
                     SUM(Profit_journal.sold_seats) as total_sold_seats,
                     SUM(Profit_journal.session_profit) as total_session_profit
                FROM
                    Profit_journal
                JOIN kino ON Profit_journal.name_kino = kino.id_kino
                GROUP BY
                    kino.name_kino;
                """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()
        columns = ["Фільм", "К-сть проданих місць", "Загальний прибуток"]
        self.zvit_window.tableWidget.setRowCount(len(data))
        self.zvit_window.tableWidget.setColumnCount(len(columns))
        self.zvit_window.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.zvit_window.tableWidget.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(value))
                )

        self.zvit_window.tableWidget.setColumnWidth(0, 350)
        self.zvit_window.tableWidget.setColumnWidth(1, 250)
        self.zvit_window.tableWidget.setColumnWidth(2, 250)

    def zvit_show_hall(self):
        if self.zvit_pointer == "":
            self.change_color(self.zvit_window.hall_zvit_button)
        elif self.zvit_pointer == "kino":
            self.change_color(
                self.zvit_window.hall_zvit_button, self.zvit_window.film_zvit_button
            )
        elif self.zvit_pointer == "session":
            self.change_color(
                self.zvit_window.hall_zvit_button, self.zvit_window.session_zvit_button
            )
        elif self.zvit_pointer == "general":
            self.change_color(
                self.zvit_window.hall_zvit_button, self.zvit_window.action_zvit_button
            )
        self.zvit_pointer = "hall"
        self.zvit_window.tableWidget_label.setText("Звіти по залам")

        temp_cursor = self.database.connection.cursor()
        request = """
                SELECT 
                     All_Halls.name_hall,
                     SUM(Profit_journal.sold_seats) as total_sold_seats,
                     SUM(Profit_journal.session_profit) as total_session_profit
                FROM
                    Profit_journal
                JOIN All_Halls ON Profit_journal.name_hall = All_Halls.id_Hall
                GROUP BY
                     All_Halls.name_hall;
                """
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()
        columns = ["Зала", "К-сть проданих місць", "Загальний прибуток"]
        self.zvit_window.tableWidget.setRowCount(len(data))
        self.zvit_window.tableWidget.setColumnCount(len(columns))
        self.zvit_window.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.zvit_window.tableWidget.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(value))
                )

        self.zvit_window.tableWidget.setColumnWidth(0, 160)
        self.zvit_window.tableWidget.setColumnWidth(1, 250)
        self.zvit_window.tableWidget.setColumnWidth(2, 250)

    def zvit_show_action(self):
        if self.zvit_pointer == "":
            self.change_color(self.zvit_window.action_zvit_button)
        elif self.zvit_pointer == "kino":
            self.change_color(
                self.zvit_window.action_zvit_button, self.zvit_window.film_zvit_button
            )
        elif self.zvit_pointer == "session":
            self.change_color(
                self.zvit_window.action_zvit_button,
                self.zvit_window.session_zvit_button,
            )
        elif self.zvit_pointer == "hall":
            self.change_color(
                self.zvit_window.action_zvit_button, self.zvit_window.hall_zvit_button
            )
        self.zvit_pointer = "general"
        self.zvit_window.tableWidget_label.setText("Дії користувачів")

        temp_cursor = self.database.connection.cursor()
        request = "SELECT user,actions,date_actions FROM actions"
        temp_cursor.execute(request)
        data = temp_cursor.fetchall()
        columns = ["Користувач", "Дія", "Час дії"]
        self.zvit_window.tableWidget.setRowCount(len(data))
        self.zvit_window.tableWidget.setColumnCount(len(columns))
        self.zvit_window.tableWidget.setHorizontalHeaderLabels(columns)
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.zvit_window.tableWidget.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(value))
                )
        self.zvit_window.tableWidget.setColumnWidth(0, 130)
        self.zvit_window.tableWidget.setColumnWidth(1, 615)
        self.zvit_window.tableWidget.setColumnWidth(2, 250)

    def handle_about(self):
        aboutWindow = AboutWindow()
        aboutWindow.exec_()

    def handle_help(self):
        help_window = HelpWindow(self)
        help_window.exec_()


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.verticalLayout_1 = QVBoxLayout()
        self.setLayout(self.verticalLayout_1)
        font = QFont()
        font.setFamilies(["Franklin Gothic Heavy, sans - serif"])
        font.setPointSize(16)
        self.setFont(font)

        self.setStyleSheet(
            """
            background-color: white;
        """
        )

    def clear_area(self):
        self.clear_layout(self.verticalLayout_1)

    def clear_layout(self, current_layout):
        while current_layout.count():
            item = current_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                inner_layout = item.layout()
                if inner_layout is not None:
                    self.clear_layout(inner_layout)
                    inner_layout.deleteLater()

    def closeEvent(self, event):
        self.clear_area()


class Zvit_Window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Вікно фінансової звітності")
        self.horizontalLayout = QHBoxLayout()
        self.setLayout(self.horizontalLayout)
        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        font = QFont()
        font.setFamilies(["Franklin Gothic, sans - serif"])
        font.setPointSize(18)
        self.setFont(font)

        self.verticalLayout_1 = QVBoxLayout()
        self.verticalLayout_2 = QVBoxLayout()
        self.horizontalLayout.insertLayout(0, self.verticalLayout_1)
        self.horizontalLayout.insertLayout(1, self.verticalLayout_2)

        self.tableWidget_label = QLabel("Звіти по сеансам", self)
        self.tableWidget_label.setFont(QFont("Franklin Gothic", 18, QFont.Bold))
        self.tableWidget_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableWidget_label.setStyleSheet("color: white;")
        self.tableWidget = QTableWidget(self)

        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
                font-size: 18px;
            }
            QHeaderView::section {
                font-size: 20px;
                font-weight: bold;
            }
            QScrollBar:vertical {
                background: #ff0055;
            }
            QScrollBar::handle:vertical {
                background: #ff0055;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: #ff0055;
            }
            QScrollBar:horizontal {
                background: #ff0055;
            }
            QScrollBar::handle:horizontal {
                background: #ff0055;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: #ff0055;
            }
            """
        )

        self.tableWidget.setFixedSize(QSize(1100, 700))
        self.verticalLayout_2.insertWidget(0, self.tableWidget_label)
        self.verticalLayout_2.insertWidget(1, self.tableWidget)

        self.verticalLayout_1.insertItem(0, self.verticalSpacer_2)
        self.film_zvit_button = QPushButton("Звіти по фільмам", self)
        self.film_zvit_button.setFixedSize(QSize(340, 60))
        self.film_zvit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff0055; 
                color: white; 
                font-size: 30px; 
                border-radius: 10px;
                padding: 5px 0;
                margin: 0 20px;
                font-family: Franklin Gothic Heavy, sans-serif; 
                
            }
            QPushButton:pressed { 
                background-color: white; 
                color: #ff0055; 
            }
            """
        )

        self.hall_zvit_button = QPushButton("Звіти по залам", self)
        self.hall_zvit_button.setFixedSize(QSize(340, 60))
        self.hall_zvit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff0055; 
                color: white; 
                font-size: 30px; 
                border-radius: 10px;
                padding: 5px 0;
                margin: 0 20px;
                font-family: Franklin Gothic Heavy, sans-serif; 

            }
            QPushButton:pressed { 
                background-color: white; 
                color: #ff0055; 
            }
            """
        )

        self.session_zvit_button = QPushButton("Звіти по сеансам", self)
        self.session_zvit_button.setFixedSize(QSize(340, 60))
        self.session_zvit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff0055; 
                color: white; 
                font-size: 30px; 
                border-radius: 10px;
                font-family: Franklin Gothic Heavy, sans-serif; 

            }
            QPushButton:pressed { 
                background-color: white; 
                color: #ff0055; 
            }
            """
        )
        self.verticalLayout_1.insertWidget(1, self.session_zvit_button)
        self.verticalLayout_1.insertWidget(2, self.film_zvit_button)
        self.verticalLayout_1.insertWidget(3, self.hall_zvit_button)

        self.action_zvit_button = QPushButton("Логи", self)
        self.action_zvit_button.setFixedSize(QSize(340, 60))
        self.action_zvit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #ff0055; 
                color: white; 
                font-size: 30px; 
                border-radius: 10px;
                padding: 5px 0;
                margin: 0 20px;
                font-family: Franklin Gothic Heavy, sans-serif; 

            }
            QPushButton:pressed { 
                background-color: white; 
                color: #ff0055; 
            }
            """
        )
        self.verticalLayout_1.insertItem(4, self.verticalSpacer_4)
        self.verticalLayout_1.insertWidget(5, self.action_zvit_button)
        self.verticalLayout_1.insertItem(6, self.verticalSpacer_3)

        header_font = QFont()
        header_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(header_font)
