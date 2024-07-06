from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import QMessageBox
from functools import partial
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import qrcode
from PySide6.QtCore import Qt
from datetime import datetime, timedelta


class HelpWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: rgba(204, 204, 204, 250);")
        self.draggable = False
        self.drag_pos = QtCore.QPoint()

        layout = QtWidgets.QVBoxLayout(self)

        self.help_container = QtWidgets.QWidget()
        self.help_container.setStyleSheet(
            "background-color: rgb(192, 192, 192); border: 6px solid rgb(192, 192, 192);"
        )

        layout.addWidget(self.help_container)

        help_layout = QtWidgets.QVBoxLayout(self.help_container)

        top_widget = QtWidgets.QWidget()
        top_widget.setStyleSheet("background-color: rgb(192, 192, 192);")
        top_layout = QtWidgets.QHBoxLayout(top_widget)

        title_label = QtWidgets.QLabel("Довідка")
        title_label.setStyleSheet("font-weight: 500; color: black;")
        title_label.setFont(QtGui.QFont("Arial", 22))

        close_button = QtWidgets.QPushButton()
        close_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./hall/close.png")))
        close_button.setIconSize(QtCore.QSize(40, 40))
        close_button.setStyleSheet("background-color: transparent; border: none;")
        close_button.clicked.connect(self.close)

        top_layout.addWidget(title_label)
        top_layout.addSpacing(600)
        top_layout.addWidget(close_button)

        help_layout.setAlignment(top_widget, QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        self.text_widget = QtWidgets.QTextEdit()

        text = """
        <p>Місця позначенні <strong><font color="blue" style="letter-spacing: 1px;">СИНІМ КОЛІРОМ</font></strong> - вільні місця які покупець може купити або забронювати.
        Після вибору вільного місця лівою кнопкою миші, воно змінює колір на <strong><font color="darkblue" style="letter-spacing: 1px;">ТЕМНО-СИНІЙ</font></strong> .</p>
        <p>Місця позначені <strong><font color="grey" style="letter-spacing: 1px;">СІРИМ КОЛІРОМ</font></strong> - заброньовані місця які може купити покупець протягом 15 хвилин, в іншому випадку місця автоматично <strong><font color="blue">звільняться</font></strong>. 
        Після вибору заброньованого місця, воно змінює колір на <strong><font color="#484848" style="letter-spacing: 1px;">ТЕМНО-СІРИЙ</font></strong>.</p>
        <p>Місця позначені <strong><font color="red" style="letter-spacing: 1px;">ЧЕРВОНИМ КОЛЬОРОМ</font></strong> - продані місця. 
        Після вибору проданого місця, воно змінює колір на <strong><font color="darkred" style="letter-spacing: 1px;">ТЕМНО-ЧЕРВОНИЙ</font></strong>.</p>
        <p>Після вибору будь-якого місця (окрім <strong><font color="red">проданого</font></strong>) з'являється вікно ЗАМОВЛЕННЯ із списком вибраних білетів та загальною вартістю за обрані білети. 
        Коли покупець вибрав білети які хоче купити/забронювати, касир вводить електронну пошту покупця та натискає на кнопку <strong><font color="red">Купити місце</font>/<font color="grey">Забронювати місце</font></strong>.</p>
        <p>Після повторного обрання будь-якого місця в вікні Замовлення, це місце видаляється зі списку</p>
        <p>Коли клієнт <strong><font color="grey">забронював місце</font></strong> - йому на електронну пошту прийде лист з інформацією про <strong><font color="grey">заброньоване місце</font></strong>. Касир за даним електронним листом обирає <strong><font color="grey">заброньовані місця</strong></font> та позначає їх як<strong><font color="red"> продані</font></strong>.</p>
        <p>Якщо термін дії <strong><font color="grey">броні</font></strong> завершився і клієнт не встиг придбати білети - лист з заброньованими місцями стає не дійсним.</p>
        <p>Якщо клієнт <strong><font color="red">купив місце</font></strong> - йому на електронну пошту прийде лист з білетами, які він придбав.</p>
        <p>Після закінчення сеансу касир повинен вибрати звільнити всі місця за допомогою кнопки <strong><font color="blue">Звільнити залу</font></strong>.</p>
        <p>Якщо покупець відмовився від білету - касир може повернути білет за допомогою кнопки <strong><font color="green">Повернути білет</font></strong>.</p>
        """

        self.text_widget.setHtml(text)
        self.text_widget.setReadOnly(True)
        self.text_widget.setStyleSheet(
            "background-color: rgb(255, 255, 255); border-top: none; color: black;"
        )
        self.text_widget.setFont(QtGui.QFont("Arial", 18))
        self.text_widget.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

        self.text_widget.verticalScrollBar().setStyleSheet(
            """
            QScrollArea {
                border: none;
            }  
            QScrollBar:vertical {
                width: 6px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(255, 0, 0);
                border: none;
            }
            QScrollBar::add-page:vertical {  
                background-color: rgb(255, 255, 255);
            }
            QScrollBar::sub-page:vertical {  
                background-color: rgb(255, 255, 255); 
            }
        """
        )

        help_layout.setContentsMargins(0, 0, 0, 0)

        help_layout.addWidget(
            top_widget,
            alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignRight | QtCore.Qt.AlignLeft,
        )
        help_layout.addWidget(self.text_widget)

        spacer_item = QtWidgets.QSpacerItem(
            600, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        top_layout.addItem(spacer_item)

    def mousePressEvent(self, event):
        if (
            event.buttons() == QtCore.Qt.LeftButton
            and self.help_container.geometry().contains(event.position().toPoint())
        ):
            self.draggable = True
            self.drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.draggable:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.draggable = False


class SeatInfoDialog(QtWidgets.QWidget):
    def __init__(self, reservation_button, buy_button, total_price_label, parent=None):
        super().__init__(parent)

        self.setFixedSize(390, parent.height())
        self.setStyleSheet("background-color: rgb(204, 204, 204);")
        self.move(-self.width(), 0)

        self.animation = QtCore.QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)

        layout = QtWidgets.QVBoxLayout(self)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.ticket_container = QtWidgets.QWidget()
        ticket_layout = QtWidgets.QVBoxLayout(self.ticket_container)
        self.ticket_container.setStyleSheet(
            "background-color: rgb(204, 204, 204); border: none;"
        )

        self.ticket_label_container_layout = QtWidgets.QVBoxLayout()
        ticket_layout.addLayout(self.ticket_label_container_layout)
        self.ticket_container.setLayout(ticket_layout)

        self.scroll_area.setWidget(self.ticket_container)

        close_button = QtWidgets.QPushButton()
        close_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./hall/close.png")))
        close_button.setIconSize(QtCore.QSize(40, 40))
        close_button.setStyleSheet("background-color: transparent; border: none;")
        close_button.clicked.connect(self.toggle_visibility)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)

        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet(
            "background-color: rgb(204, 204, 204); border: none;"
        )
        title_layout = QtWidgets.QHBoxLayout(title_container)
        title_label = QtWidgets.QLabel("ЗАМОВЛЕННЯ")
        title_label.setStyleSheet("color: black; font-weight: 500;")
        title_label.setFont(QtGui.QFont("Arial", 22))
        title_layout.addWidget(title_label)

        email_label = QtWidgets.QLabel("Електронна пошта:")
        email_label.setStyleSheet("color: black; font-size: 22px;")
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setStyleSheet(
            "background-color: white; border: 1px solid gray; color: black; font-size: 22px;"
        )
        self.email_input.setPlaceholderText("Введіть електронну пошту")

        email_layout = QtWidgets.QVBoxLayout()
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)

        main_container = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(main_container)
        main_container.setStyleSheet(
            "background-color: rgb(204, 204, 204); border: none;"
        )
        main_layout.addLayout(button_layout)
        main_layout.addWidget(title_container, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.scroll_area)
        main_layout.addSpacing(15)
        main_layout.addWidget(total_price_label)
        main_layout.addSpacing(1)
        main_layout.addLayout(email_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(buy_button, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(reservation_button, alignment=QtCore.Qt.AlignCenter)
        main_layout.addSpacing(10)

        layout.addWidget(main_container)

        self.buy_button = buy_button
        self.buy_button.clicked.connect(self.buy_tickets)
        self.reservation_button = reservation_button
        self.reservation_button.clicked.connect(self.reserve_tickets)

        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
            }  
            QScrollBar:vertical {
                width: 6px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(255, 0, 0);
                border: none;
            }
            QScrollBar::add-page:vertical {  
                background-color: rgb(204, 204, 204);
            }
            QScrollBar::sub-page:vertical {  
                background-color: rgb(204, 204, 204); 
            }
        """
        )

        self.hide()

    def buy_tickets(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.critical(
                self, "Помилка", "Будь ласка, введіть електронну пошту."
            )
            return
        self.email_input.clear()

    def reserve_tickets(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.critical(
                self, "Помилка", "Будь ласка, введіть електронну пошту."
            )
            return
        self.email_input.clear()

    def toggle_visibility(self):
        if self.isVisible():
            self.hide_from_left()
        else:
            self.show_from_left()

    def hide_from_left(self):
        if self.isVisible():
            current_pos = self.pos()
            end_pos = QtCore.QPoint(-self.width(), 0)
            self.animation.setStartValue(current_pos)
            self.animation.setEndValue(end_pos)
            self.animation.start()
            QtCore.QTimer.singleShot(500, self.hide)

    def show_from_left(self):
        if not self.isVisible():
            start_pos = QtCore.QPoint(-self.width(), 0)
            self.move(start_pos)
            end_pos = QtCore.QPoint(0, 0)
            self.animation.setStartValue(start_pos)
            self.animation.setEndValue(end_pos)
            self.animation.start()
            self.show()

    def update_ticket_image(self, image):
        ticket_label = QtWidgets.QLabel()
        ticket_label.setPixmap(image)
        ticket_label.setFixedSize(333, 70)
        self.ticket_label_container_layout.addWidget(ticket_label)

    def update_seat_info_dialog(self, ticket_images):
        for i in reversed(range(self.ticket_label_container_layout.count())):
            self.ticket_label_container_layout.itemAt(i).widget().setParent(None)
        for ticket_image in ticket_images:
            self.update_ticket_image(ticket_image)


class HallWindow(QtWidgets.QWidget):
    def __init__(self, id_Hall, nomer_S, database):
        super().__init__()
        self.setWindowTitle("Кинотеатр")
        self.setGeometry(0, 0, 1920, 1080)
        self.help_window = None
        self.database = database

        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.id_Hall = id_Hall
        self.nomer_S = nomer_S

        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(10)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        top_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(top_layout)

        close_button = QtWidgets.QPushButton()
        close_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./hall/exit.png")))
        close_button.setIconSize(QtCore.QSize(30, 30))
        close_button.setStyleSheet("background-color: transparent; border: none;")
        close_button.clicked.connect(self.close)

        help_button = QtWidgets.QPushButton()
        help_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./hall/help.png")))
        help_button.setIconSize(QtCore.QSize(30, 30))
        help_button.setStyleSheet("background-color: transparent; border: none;")
        help_button.clicked.connect(self.show_help_window)

        ########################################Змінити#############################################
        top_info = QtWidgets.QWidget()
        top_info_layout = QtWidgets.QHBoxLayout(top_info)

        self.text_container1 = QtWidgets.QVBoxLayout()
        self.text_label1 = QtWidgets.QLabel()
        self.text_label1.setStyleSheet("font-size: 16px; font-weight: 600;")
        self.text_label1.setFixedWidth(350)
        self.text_container1.addWidget(self.text_label1)
        self.info_details()

        text_container2 = QtWidgets.QVBoxLayout()
        text_label2 = QtWidgets.QLabel()
        text_label2.setText(
            "<font color='blue'>Вільні місця</font><br><font color='red'>Куплені місця</font></br><br><font color='grey'>Заброньовані місця</font></br>"
        )
        text_label2.setStyleSheet("font-size: 16px; font-weight: 600;")
        text_container2.addWidget(text_label2)

        top_info_layout.addLayout(self.text_container1)
        top_info_layout.addSpacing(520)
        top_info_layout.addLayout(text_container2)

        top_layout.addWidget(top_info)

        top_layout.addStretch()

        top_layout.addWidget(
            help_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop
        )
        top_layout.addWidget(
            close_button, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignTop
        )

        top_layout.setAlignment(QtCore.Qt.AlignTop)

        screen_container = QtWidgets.QLabel()

        s_pixmap = QtGui.QIcon("./hall/screen.png")
        screen_container.setPixmap(s_pixmap.pixmap(QtCore.QSize(1180, 960)))

        screen_container.setAlignment(QtCore.Qt.AlignCenter)
        ##############################################################################################
        sub_container = QtWidgets.QHBoxLayout()

        self.button_container = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QVBoxLayout(self.button_container)
        self.button_layout.setSpacing(5)

        self.row_labels_container = QtWidgets.QWidget()
        self.row_labels_layout = QtWidgets.QVBoxLayout(self.row_labels_container)
        self.row_labels_layout.setSpacing(5)
        self.row_labels_container.setMaximumWidth(100)

        self.row_labels2_container = QtWidgets.QWidget()
        self.row_labels2_layout = QtWidgets.QVBoxLayout(self.row_labels2_container)
        self.row_labels2_layout.setSpacing(5)
        self.row_labels2_container.setMaximumWidth(100)

        vbox_layout = QtWidgets.QVBoxLayout()
        vbox_layout.addWidget(screen_container)
        vbox_layout.addSpacing(70)
        vbox_layout.addLayout(sub_container)
        vbox_layout.setContentsMargins(0, 40, 0, 0)
        vbox_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.selected_seats = set()
        self.buttons_dict = {}
        self.selected_seats_info = []

        self.load_seats()

        layout.addLayout(vbox_layout)

        sub_container.addWidget(self.row_labels_container)
        sub_container.addWidget(self.button_container)
        sub_container.addWidget(self.row_labels2_container)
        sub_container.setAlignment(QtCore.Qt.AlignCenter)

        button_container_bottom = QtWidgets.QWidget()
        button_layout_bottom = QtWidgets.QHBoxLayout(button_container_bottom)
        button_layout_bottom.setSpacing(20)

        buy_button = QtWidgets.QPushButton("Купити місце")
        buy_button.setFixedSize(230, 50)
        buy_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: red; 
                            color: white; 
                            font-size: 22px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: darkred; 
                            color: lightgray; 
                        }
                        """
        )

        reservation_button = QtWidgets.QPushButton("Забронювати місце")
        reservation_button.setFixedSize(230, 50)
        reservation_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: grey; 
                            color: white; 
                            font-size: 22px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: darkgrey; 
                            color: lightgray; 
                        }
                        """
        )

        free_button = QtWidgets.QPushButton("Повернути білет")
        free_button.setFixedSize(230, 50)
        free_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: green; 
                            color: white; 
                            font-size: 22px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: green; 
                            color: lightgray; 
                        }
                        """
        )

        free_all_button = QtWidgets.QPushButton("Звільнити залу")
        free_all_button.setFixedSize(230, 50)
        free_all_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: blue; 
                            color: white; 
                            font-size: 22px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: darkblue; 
                            color: lightgray; 
                        }
                        """
        )

        button_layout_bottom.addWidget(free_button)
        button_layout_bottom.addWidget(free_all_button)

        layout.addWidget(button_container_bottom)

        buy_button.clicked.connect(self.buy_seats)
        reservation_button.clicked.connect(self.reservation_seats)
        free_button.clicked.connect(self.free_seats)
        free_all_button.clicked.connect(self.free_all_seats)

        self.total_price_label = QtWidgets.QLabel()
        self.update_total_price_label()

        total_price_container = QtWidgets.QWidget()
        total_price_layout = QtWidgets.QHBoxLayout(total_price_container)
        total_price_layout.addWidget(QtWidgets.QLabel("Загальна ціна:"))
        total_price_layout.addWidget(self.total_price_label)

        self.seat_info_dialog = SeatInfoDialog(
            reservation_button, buy_button, self.total_price_label, parent=self
        )

    def show_help_window(self):
        if self.help_window is not None:
            self.help_window.close()
        self.help_window = HelpWindow(self)
        self.help_window.move(
            self.geometry().center() - self.help_window.rect().center()
        )
        self.help_window.show()

    def load_seats(self):
        connection = self.database.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id_Rows, num_seats, status FROM db_findtick.Seats WHERE id_Hall = %s and nomer_S = %s",
            (self.id_Hall, self.nomer_S),
        )
        seats = cursor.fetchall()

        max_seats_per_row = max(
            len(set(seat[1] for seat in seats if seat[0] == r))
            for r in set(seat[0] for seat in seats)
        )
        self.max_seats_per_row = max_seats_per_row

        for r in sorted(set(seat[0] for seat in seats)):
            row_seats = [seat for seat in seats if seat[0] == r]
            num_seats = len(row_seats)
            extra_seats = max_seats_per_row - num_seats
            num_empty_left = extra_seats // 2
            num_empty_right = extra_seats - num_empty_left

            row_label = QtWidgets.QLabel("Ряд " + str(r))
            row_label.setStyleSheet("color: black; font-size: 22px;")
            row_label.setFixedSize(70, 55)
            self.row_labels_layout.addWidget(row_label)
            row_layout = QtWidgets.QHBoxLayout()

            row_label2 = QtWidgets.QLabel("  Ряд " + str(r))
            row_label2.setStyleSheet("color: black; font-size: 22px;")
            row_label2.setFixedSize(70, 55)
            self.row_labels2_layout.addWidget(row_label2)

            for _ in range(num_empty_left):
                empty_label = QtWidgets.QLabel()
                row_layout.addWidget(empty_label)

            for seat in row_seats:
                button = QtWidgets.QPushButton(str(seat[1]))
                button.setFixedSize(55, 55)
                num_seat = seat[1]
                id_rows = seat[0]
                status = seat[2]
                self.buttons_dict[(num_seat, id_rows)] = button
                button.clicked.connect(
                    partial(self.button_clicked, num_seat, id_rows, status)
                )
                button.setStyleSheet(self.get_button_style(status))
                row_layout.addWidget(button)

            for _ in range(num_empty_right):
                empty_label = QtWidgets.QLabel()
                row_layout.addWidget(empty_label)

            self.button_layout.addLayout(row_layout)

    ############################Додати##################################
    def info_details(self):
        connection = self.database.connection
        cursor = connection.cursor()
        query = """
        SELECT kino.name_kino, All_Halls.name_hall, 
               DATE_FORMAT(Sessions.start_s, '%%H:%%i') AS start_s, 
               DATE_FORMAT(Sessions.end_s, '%%H:%%i') AS end_s
        FROM db_findtick.Sessions
        JOIN db_findtick.kino ON Sessions.id_kino = kino.id_kino
        JOIN db_findtick.All_Halls ON Sessions.id_Hall = All_Halls.id_Hall
        WHERE Sessions.id_Hall = %s AND Sessions.nomer_S = %s;
        """
        cursor.execute(query, (self.id_Hall, self.nomer_S))
        cinema_details = cursor.fetchall()

        details_text = ""
        for detail in cinema_details:
            details_text += (
                f"Назва: «{detail[0]}»\nЗала: {detail[1]}\nЧас: {detail[2]}-{detail[3]}"
            )

        self.text_label1.setText(details_text)

    ###########################################################################

    def get_button_style(self, status, selected=False):
        if status == 1:
            if selected:
                return """
                    QPushButton { 
                        border-radius: 10px;
                        color: lightgray;
                        font-size: 18px;
                        background-color: darkblue;
                    }
                    QPushButton:pressed { 
                        background-color: darkblue; 
                        color: lightgray; 
                    }
                """
            else:
                return """
                    QPushButton { 
                        border-radius: 10px;
                        color: white;
                        font-size: 18px;
                        background-color: blue;
                    }
                    QPushButton:pressed { 
                        background-color: darkblue; 
                        color: lightgray; 
                    }
                """
        elif status == 2:
            if selected:
                return """
                    QPushButton {
                        color: lightgray;
                        border-radius: 10px;
                        font-size: 18px;
                        background-color: darkred;
                    }
                    QPushButton:pressed { 
                        background-color: darkred; 
                        color: lightgray; 
                    }
                """
            else:
                return """
                    QPushButton {
                        color: white;
                        font-size: 18px;
                        border-radius: 10px;
                        background-color: red;
                    }
                    QPushButton:pressed { 
                        background-color: darkred; 
                        color: lightgray; 
                    }
                """
        elif status == 3:
            if selected:
                return """
                    QPushButton {
                        border-radius: 10px;
                        font-size: 18px;
                        color: lightgray;
                        background-color: #484848;
                    }
                    QPushButton:pressed { 
                        background-color: #484848; 
                        color: lightgray; 
                    }
                """
            else:
                return """
                    QPushButton {
                        border-radius: 10px;
                        font-size: 18px;
                        color: white;
                        background-color: grey;
                    }
                    QPushButton:pressed { 
                        background-color: #484848; 
                        color: lightgray; 
                    }
                """
        elif status == 4:
            if selected:
                return """
                    QPushButton { 
                        border-radius: 10px;
                        color: lightgray;
                        font-size: 18px;
                        background-color: darkblue;
                    }
                    QPushButton:pressed { 
                        background-color: darkblue; 
                        color: lightgray; 
                    }
                """
            else:
                return """
                    QPushButton { 
                        border-radius: 10px;
                        color: white;
                        font-size: 18px;
                        background-color: blue;
                    }
                    QPushButton:pressed { 
                        background-color: darkblue; 
                        color: lightgray; 
                    }
                """

    def update_seat_info_dialog(self):
        ticket_images = []
        for index, seat_info in enumerate(self.selected_seats_info):
            ticket_image = QPixmap("./hall/tiket.png")
            ticket_image = ticket_image.scaled(333, 100)
            painter = QPainter(ticket_image)
            painter.setPen(QColor("black"))
            painter.setFont(QFont("Arial", 14))

            info_text = f"Ряд: {seat_info[1]}, Місце: {seat_info[2]}, Ціна: {seat_info[6]} {seat_info[7]}"

            font_metrics = painter.fontMetrics()
            text_rect = font_metrics.boundingRect(info_text)

            x = (ticket_image.width() - 7 - text_rect.width()) / 2
            y = (ticket_image.height() + 35 - text_rect.height()) / 2

            painter.drawText(x, y, info_text)

            painter.end()

            ticket_images.append(ticket_image)

        self.seat_info_dialog.update_seat_info_dialog(ticket_images)

    def update_total_price_label(self):
        currency = self.selected_seats_info[0][7] if self.selected_seats_info else ""
        total_price_text = f"Не має вибраних місць!"
        self.total_price_label.setText(total_price_text)
        self.total_price_label.setStyleSheet("color: black; font-size: 22px;")

        if self.selected_seats_info:
            total_price = sum(info[6] for info in self.selected_seats_info)
            total_price_text = f"Загальна ціна: {total_price} {currency}"
        self.total_price_label.setText(total_price_text)
        self.total_price_label.setStyleSheet("color: black; font-size: 22px;")

    def button_clicked(self, num_seat, id_rows, status):
        with self.database.connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT
                        All_Halls.name_hall,
                        Seats.id_Rows,
                        Seats.num_seats,
                        kino.name_kino,
                        DATE_FORMAT(Sessions.start_s, '%%d.%%m.%%Y') AS date_s,
                        DATE_FORMAT(Sessions.end_s, '%%H:%%i') AS end_s,
                        Sessions.price,
                        Sessions.currency,
                        DATE_FORMAT(Sessions.start_s, '%%H:%%i') AS start_s
                    FROM
                        All_Halls
                    JOIN
                        Seats ON All_Halls.id_Hall = Seats.id_Hall
                    JOIN
                        Sessions ON All_Halls.id_Hall = Sessions.id_Hall AND Seats.nomer_S  = Sessions.nomer_S 
                    JOIN
                        kino ON Sessions.id_kino = kino.id_kino
                    WHERE
                        Seats.num_seats = %s AND
                        Seats.id_Rows = %s AND
                        Seats.id_Hall = %s AND
                        Seats.nomer_S = %s
                """,
                (num_seat, id_rows, self.id_Hall, self.nomer_S),
            )
            seat_info = cursor.fetchone()

        if seat_info:
            # dialog_text = f"Зала: {seat_info[0]}\n" \
            #             f"Ряд: {seat_info[1]} Місце: {seat_info[2]}\n" \
            #             f"Фільм: {seat_info[3]}\n" \
            #             f"Дата початку сеансу: {seat_info[4]}\n" \
            #             f"Початок сеансу: {seat_info[8]}\n" \
            #             f"Кінець сеансу: {seat_info[5]}\n" \
            #             f"Ціна: {seat_info[6]} {seat_info[7]}"
            seat_info_tuple = (num_seat, id_rows, status)
            button = self.buttons_dict.get((num_seat, id_rows))

            if button:
                if seat_info_tuple in self.selected_seats:
                    self.selected_seats.remove(seat_info_tuple)
                    for info in self.selected_seats_info:
                        if info[2] == num_seat and info[1] == id_rows:
                            self.selected_seats_info.remove(info)
                    button.setStyleSheet(self.get_button_style(status, selected=False))
                    self.update_seat_info_dialog()
                    self.update_total_price_label()
                elif len(self.selected_seats) < 10:
                    if status != 2:
                        self.selected_seats_info.append(seat_info)
                        self.update_seat_info_dialog()
                    self.selected_seats.add(seat_info_tuple)
                    button.setStyleSheet(self.get_button_style(status, selected=True))
                    self.update_total_price_label()
                    self.seat_info_dialog.show_from_left()
                else:
                    QMessageBox.warning(
                        self,
                        "Попередження",
                        "За один раз можно выбрать не более 10 квитков.",
                    )

            if status != 3:
                self.update_seat_info_dialog()
                self.seat_info_dialog.show_from_left()
            self.create_buy_ticket_image()
            self.create_reservation_ticket_image()

    def send_buy_tickets_email(self):
        to_email = self.seat_info_dialog.email_input.text()
        ticket_images = self.create_buy_ticket_image()
        self.send_email_b(to_email, "", ticket_images)

    def send_email_b(self, to_email, message_body, ticket_images):
        smtp_server = "smtp.ukr.net"
        smtp_port = 465
        email_sender = "findtick@ukr.net"
        email_sender_password = "zqJ3clNKidcynt7x"

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_sender, email_sender_password)

        subject = "Підтвердження покупки місця FINTICK"

        message = MIMEMultipart()
        message["From"] = email_sender
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(message_body, "html", "utf-8"))

        for index, ticket_image_base64 in enumerate(ticket_images):
            ticket_image_bytes = base64.b64decode(ticket_image_base64)
            img_attachment = MIMEImage(ticket_image_bytes, "png")
            img_attachment.add_header(
                "Content-Disposition", f"attachment; filename=buy_ticket_{index}.png"
            )
            message.attach(img_attachment)

        currency = self.selected_seats_info[0][7]
        total_price = sum(info[6] for info in self.selected_seats_info)
        total_price_text = f"Загальна ватрість склала: {total_price} {currency}"

        total_price_html = (
            f"<p style='font-weight: bold; font-size: 22px;'>{total_price_text}</p>"
            f"<p style='font-weight: bold; font-size: 22px;'>Дякуємо за відвідування нашого кінотеатру\n</p>"
        )
        message.attach(MIMEText(total_price_html, "html", "utf-8"))

        server.sendmail(email_sender, to_email, message.as_string())
        server.quit()

    def create_buy_ticket_image(self):
        ticket_images = []

        for index, seat_info in enumerate(self.selected_seats_info):

            background_image = Image.open("./hall/ticket.png").resize((400, 582))
            ticket_image = background_image.copy()

            draw = ImageDraw.Draw(ticket_image)

            font = ImageFont.truetype("arial.ttf", 19)
            font2 = ImageFont.truetype("arialbd.ttf", 19)
            text_color = "black"

            x = 45
            y = 133
            draw.text((x, y), f"{seat_info[3]}", fill=text_color, font=font)

            y += 73
            x -= 2
            draw.text((x, y), f"{seat_info[4]}", fill=text_color, font=font)

            x += 189
            draw.text(
                (x, y), f"{seat_info[8]}-{seat_info[5]}", fill=text_color, font=font
            )

            y += 50
            x -= 110
            draw.text((x, y), f"{seat_info[0]}", fill=text_color, font=font2)

            y += 36
            draw.text((x, y), f"{seat_info[1]}", fill=text_color, font=font2)

            y += 36
            draw.text((x, y), f"{seat_info[2]}", fill=text_color, font=font2)

            x -= 75
            y += 105
            draw.text(
                (x, y), f"{seat_info[6]} {seat_info[7]}", fill=text_color, font=font
            )

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=0,
            )
            ################################ЗМІНИ######################
            qr.add_data(
                "\n".join(
                    [
                        "Білет є дійсним",
                        str(seat_info[3]),
                        str(seat_info[4]),
                        f"{seat_info[8]}-{seat_info[5]}",
                        f"Зала: {seat_info[0]}",
                        f"Ряд: {seat_info[1]}",
                        f"Місце: {seat_info[2]}",
                    ]
                )
            )
            ############################################################
            qr.make(fit=True)

            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_position = (165, 302)
            ticket_image.paste(qr_image, qr_position)
            buffered = BytesIO()
            ticket_image.save(buffered, format="PNG")
            ticket_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            ticket_images.append(ticket_image_base64)

        return ticket_images

    def sendre_reservation_tickets_email(self):
        to_email = self.seat_info_dialog.email_input.text()
        ticket_images = self.create_reservation_ticket_image()
        self.send_email_r(to_email, "", ticket_images)

    def send_email_r(self, to_email, message_body, ticket_images):

        smtp_server = "smtp.ukr.net"
        smtp_port = 465
        email_sender = "findtick@ukr.net"
        email_sender_password = "zqJ3clNKidcynt7x"

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_sender, email_sender_password)

        subject = "Підтвердження бронювання місця FINTICK"

        message = MIMEMultipart()
        message["From"] = email_sender
        message["To"] = to_email
        message["Subject"] = subject

        message.attach(MIMEText(message_body, "html", "utf-8"))

        for index, ticket_image_base64 in enumerate(ticket_images):
            ticket_image_bytes = base64.b64decode(ticket_image_base64)
            img_attachment = MIMEImage(ticket_image_bytes, "png")
            img_attachment.add_header(
                "Content-Disposition",
                f"attachment; filename=reserve_ticket_{index}.png",
            )
            message.attach(img_attachment)

        currency = self.selected_seats_info[0][7]
        total_price = sum(info[6] for info in self.selected_seats_info)
        total_price_text = f"До сплати: {total_price} {currency}"

        ukrainian_months = [
            "січня",
            "лютого",
            "березня",
            "квітня",
            "травня",
            "червня",
            "липня",
            "серпня",
            "вересня",
            "жовтня",
            "листопада",
            "грудня",
        ]

        current_datetime = datetime.now()
        future_datetime = current_datetime + timedelta(minutes=15)
        month_index = future_datetime.month - 1
        month_in_words = ukrainian_months[month_index]
        end_time = future_datetime.strftime(f"%H:%M %d {month_in_words}")

        total_price_html = (
            f"<p style='font-weight: bold; font-size: 22px;'>{total_price_text}</p>"
            f"<p style='font-weight: bold; font-size: 22px;'>Час дії броні припинется в {end_time}!\n</p>"
        )
        message.attach(MIMEText(total_price_html, "html", "utf-8"))

        server.sendmail(email_sender, to_email, message.as_string())
        server.quit()

    def create_reservation_ticket_image(self):
        ticket_images = []

        for index, seat_info in enumerate(self.selected_seats_info):
            background_image = Image.open("./hall/reservation_tick.png").resize(
                (400, 582)
            )
            ticket_image = background_image.copy()
            draw = ImageDraw.Draw(ticket_image)

            font = ImageFont.truetype("arial.ttf", 16)
            font2 = ImageFont.truetype("arialbd.ttf", 19)
            font3 = ImageFont.truetype("arialbd.ttf", 24)
            text_color = "black"

            x = 44
            y = 132
            draw.text((x, y), f"{seat_info[3]}", fill=text_color, font=font)

            y += 76
            draw.text((x, y), f"{seat_info[4]}", fill=text_color, font=font)

            x += 206
            draw.text(
                (x, y), f"{seat_info[8]}-{seat_info[5]}", fill=text_color, font=font
            )

            y += 52
            x -= 140
            draw.text((x, y), f"{seat_info[0]}", fill=text_color, font=font2)

            y += 50
            draw.text((x, y), f"{seat_info[1]}", fill=text_color, font=font2)

            y += 49
            draw.text((x, y), f"{seat_info[2]}", fill=text_color, font=font2)

            x += 60
            y += 72
            draw.text(
                (x, y), f"{seat_info[6]} {seat_info[7]}", fill=text_color, font=font3
            )

            buffered = BytesIO()
            ticket_image.save(buffered, format="PNG")
            ticket_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            ticket_images.append(ticket_image_base64)

        return ticket_images

    def buy_seats(self):
        if not self.selected_seats:
            QMessageBox.information(self, "Інформація", "Немає вибраних місць.")
            return

        self.send_buy_tickets_email()

        with self.database.connection.cursor() as cursor:
            for seat_info in self.selected_seats:
                num_seat, id_rows, status = seat_info
                sql = """
                    UPDATE `db_findtick`.`Seats`
                    SET status = 2
                    WHERE (`num_seats` = %s) AND (`id_Hall` = %s) AND (`nomer_S` = %s) AND (`id_Rows` = %s);
                    """
                cursor.execute(sql, (num_seat, self.id_Hall, self.nomer_S, id_rows))
                self.database.connection.commit()

        self.update_seat_info_dialog()
        self.selected_seats = set()
        self.update_seat_container()
        QMessageBox.information(self, "Успішно", "Місця успішно продані.")

        for i in reversed(
            range(self.seat_info_dialog.ticket_label_container_layout.count())
        ):
            widget = self.seat_info_dialog.ticket_label_container_layout.itemAt(
                i
            ).widget()
            if widget is not None:
                widget.deleteLater()

        self.selected_seats_info = []
        self.update_total_price_label()

    def reservation_seats(self):
        if not self.selected_seats:
            QMessageBox.information(self, "Інформація", "Немає вибраних місць.")
            return
        self.sendre_reservation_tickets_email()

        with self.database.connection.cursor() as cursor:
            for seat_info in self.selected_seats:
                num_seat, id_rows, status = seat_info
                sql = """
                    UPDATE `db_findtick`.`Seats`
                    SET status = 3
                    WHERE (`num_seats` = %s) AND (`id_Hall` = %s) AND (`nomer_S` = %s) AND (`id_Rows` = %s);
                    """
                cursor.execute(sql, (num_seat, self.id_Hall, self.nomer_S, id_rows))
                self.database.connection.commit()

        self.update_seat_info_dialog()
        self.selected_seats = set()
        self.update_seat_container()
        QMessageBox.information(self, "Успішно", "Місця успішно заброньовані.")

        for i in reversed(
            range(self.seat_info_dialog.ticket_label_container_layout.count())
        ):
            widget = self.seat_info_dialog.ticket_label_container_layout.itemAt(
                i
            ).widget()
            if widget is not None:
                widget.deleteLater()

        self.selected_seats_info = []
        self.update_total_price_label()

    def free_seats(self):
        if not self.selected_seats:
            QMessageBox.information(self, "Інформація", "Немає вибраних місць.")
            return

        # Confirm the action with the user
        reply = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви впевнені, що хочете звільнити вибрані місця?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            with self.database.connection.cursor() as cursor:
                for seat_info in self.selected_seats:
                    num_seat, id_rows, status = seat_info
                    sql = """
                            UPDATE `db_findtick`.`Seats`
                            SET status = 4
                            WHERE (`num_seats` = %s) AND (`id_Hall` = %s) AND (`nomer_S` = %s) AND (`id_Rows` = %s);
                            """
                    cursor.execute(sql, (num_seat, self.id_Hall, self.nomer_S, id_rows))
                    self.database.connection.commit()

            self.selected_seats = set()
            self.update_seat_container()
            QMessageBox.information(self, "Успішно", "Білет упішно повернуто")

            for i in reversed(
                range(self.seat_info_dialog.ticket_label_container_layout.count())
            ):
                widget = self.seat_info_dialog.ticket_label_container_layout.itemAt(
                    i
                ).widget()
                if widget is not None:
                    widget.deleteLater()

            self.selected_seats_info = []
            self.update_total_price_label()

    def free_all_seats(self):

        reply = QMessageBox.question(
            self,
            "Підтвердження",
            "Ви впевнені, що хочете звільнити залу?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            with self.database.connection.cursor() as cursor:
                sql = """
                    UPDATE Seats
                    SET status = 1
                    WHERE id_Hall = %s AND nomer_S = %s
                    """
                cursor.execute(sql, (self.id_Hall, self.nomer_S))
                self.database.connection.commit()
            self.selected_seats = set()
            self.update_seat_container()
            self.selected_seats_info = []
            self.update_total_price_label()
            QMessageBox.information(self, "Успішно", "Зала успішно звільнена.")

    def update_seat_container(self):
        connection = self.database.connection
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id_Rows, num_seats, status FROM db_findtick.Seats WHERE id_Hall = %s and nomer_S = %s",
            (self.id_Hall, self.nomer_S),
        )
        updated_seats = cursor.fetchall()

        for i in reversed(range(self.button_layout.count())):
            item = self.button_layout.itemAt(i)
            if isinstance(item, QtWidgets.QHBoxLayout):
                while item.count():
                    item.takeAt(0).widget().deleteLater()
                self.button_layout.removeItem(item)

        for r in sorted(set(seat[0] for seat in updated_seats)):
            row_seats = [seat for seat in updated_seats if seat[0] == r]
            num_seats = len(row_seats)
            extra_seats = self.max_seats_per_row - num_seats
            num_empty_left = extra_seats // 2
            num_empty_right = extra_seats - num_empty_left

            row_layout = QtWidgets.QHBoxLayout()

            for _ in range(num_empty_left):
                empty_label = QtWidgets.QLabel()
                row_layout.addWidget(empty_label)

            for seat in row_seats:
                button = QtWidgets.QPushButton(str(seat[1]))
                button.setFixedSize(55, 55)
                num_seat = seat[1]
                id_rows = seat[0]
                status = seat[2]
                self.buttons_dict[(num_seat, id_rows)] = button
                button.clicked.connect(
                    partial(self.button_clicked, num_seat, id_rows, status)
                )
                button.setStyleSheet(self.get_button_style(status))
                row_layout.addWidget(button)

            for _ in range(num_empty_right):
                empty_label = QtWidgets.QLabel()
                row_layout.addWidget(empty_label)

            self.button_layout.addLayout(row_layout)

    def closeEvent(self, event):
        self.seat_info_dialog.close()
