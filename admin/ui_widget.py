from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QDialog,
)


class Ui_admin_widget(object):
    def setupUi(self, admin_widget):
        if not admin_widget.objectName():
            admin_widget.setObjectName("admin_widget")
        admin_widget.resize(1920, 1080)
        font = QFont()
        font.setFamilies(["Arial, Helvetica, sans - serif"])
        font.setPointSize(16)
        font.setBold(True)
        admin_widget.setFont(font)
        self.admin_qwidget = QWidget(admin_widget)
        self.admin_qwidget.setObjectName("admin_qwidget")
        self.layoutWidget = QWidget(self.admin_qwidget)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setFixedSize(1880, 980)
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.verticalSpacer_7 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_11 = QVBoxLayout()

        self.add_object_button = QPushButton(self.layoutWidget)
        self.add_object_button.setObjectName("add_object_button")
        self.add_object_button.setMinimumSize(QSize(250, 70))
        self.add_object_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: green; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: darkgreen; 
                            color: lightgray; 
                        }
                        """
        )

        self.verticalLayout_10.insertWidget(0, self.add_object_button)

        self.go_to_zvit_button = QPushButton(self.layoutWidget)
        self.go_to_zvit_button.setObjectName("go_to_zvit_button")
        self.go_to_zvit_button.setMinimumSize(QSize(0, 70))
        self.go_to_zvit_button.setFont(font)
        self.go_to_zvit_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: grey; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: lightgrey
                            color: lightgray; 
                        }
                        """
        )

        self.verticalLayout_10.insertWidget(1, self.go_to_zvit_button)

        self.horizontalLayout_3.addLayout(self.verticalLayout_9)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.hall_button = QPushButton(self.layoutWidget)
        self.hall_button.setObjectName("hall_button")
        self.hall_button.setMinimumSize(QSize(0, 70))
        self.hall_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: orange; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: lightgrey; 
                            color: orange; 
                        }
                        """
        )

        self.film_button = QPushButton(self.layoutWidget)
        self.film_button.setObjectName("film_button")
        self.film_button.setMinimumSize(QSize(0, 70))
        self.film_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: orange; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: lightgrey; 
                            color: orange; 
                        }
                        """
        )

        self.session_button = QPushButton(self.layoutWidget)
        self.session_button.setObjectName("session_button")
        self.session_button.setMinimumSize(QSize(0, 70))
        self.session_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: orange; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                        }
                        QPushButton:pressed { 
                            background-color: lightgrey; 
                            color: orange; 
                        }
                        """
        )

        self.user_button = QPushButton(self.layoutWidget)
        self.user_button.setObjectName("user_button")
        self.user_button.setMinimumSize(QSize(0, 70))
        self.user_button.setStyleSheet(
            """
                        QPushButton {
                            background-color: orange; 
                            color: white; 
                            font-size: 30px; 
                            border-radius: 20px;
                            font-weight: bold;
                            font-family: Arial, Helvetica, sans-serif; 
                            
                        }
                        QPushButton:pressed { 
                            background-color: lightgrey; 
                            color: orange; 
                        }
                        """
        )

        self.verticalLayout_11.insertItem(0, self.verticalSpacer_7)
        self.verticalLayout_11.insertWidget(1, self.session_button)

        self.verticalLayout_11.insertWidget(2, self.film_button)
        self.verticalLayout_11.insertItem(3, self.verticalSpacer_6)
        self.verticalLayout_11.insertWidget(4, self.user_button)
        self.verticalLayout_11.insertWidget(5, self.hall_button)

        self.verticalLayout_9.insertLayout(0, self.verticalLayout_11)
        self.verticalLayout_9.insertItem(1, self.verticalSpacer_2)
        self.verticalLayout_9.insertLayout(2, self.verticalLayout_10)

        self.tableWidget_label = QLabel("Таблиця сеансів", self.layoutWidget)
        self.tableWidget_label.setFont(QFont("Arial", 20, QFont.Bold))  # Шрифт
        self.tableWidget_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tableWidget = QTableWidget(self.layoutWidget)
        self.tableWidget.setMinimumSize(QSize(1000, 0))
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.verticalLayout_7.insertWidget(0, self.tableWidget_label)
        self.verticalLayout_7.insertWidget(1, self.tableWidget)

        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.retranslateUi(admin_widget)

        QMetaObject.connectSlotsByName(admin_widget)

    # setupUi

    def retranslateUi(self, admin_widget):
        admin_widget.setWindowTitle(
            QCoreApplication.translate("admin_widget", "MainWindow", None)
        )
        self.add_object_button.setText(
            QCoreApplication.translate(
                "admin_widget", "\u0414\u043e\u0434\u0430\u0442\u0438", None
            )
        )
        self.go_to_zvit_button.setText(
            QCoreApplication.translate(
                "admin_widget",
                "\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u0434\u043e \u0437\u0432\u0456\u0442\u043d\u043e\u0441\u0442\u0435\u0439",
                None,
            )
        )
        self.hall_button.setText(
            QCoreApplication.translate("admin_widget", "\u0417\u0430\u043b\u0438", None)
        )
        self.film_button.setText(
            QCoreApplication.translate(
                "admin_widget", "\u0424\u0456\u043b\u044c\u043c\u0438", None
            )
        )
        self.session_button.setText(
            QCoreApplication.translate(
                "admin_widget", "\u0421\u0435\u0430\u043d\u0441\u0438", None
            )
        )
        self.user_button.setText(
            QCoreApplication.translate(
                "admin_widget",
                "\u041a\u043e\u0440\u0438\u0441\u0442\u0443\u0432\u0430\u0447\u0456",
                None,
            )
        )
