from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon


class Choice(QMainWindow):
    choice_made = Signal(str)

    def __init__(self, app, database):
        super().__init__()
        self.app = app
        self.database = database
        self.setWindowTitle("Вибір ролі")
        self.setFixedSize(450, 200)

        icon = QIcon("./assets/icon.ico")
        self.setWindowIcon(icon)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        central_widget.setStyleSheet("background-color: #292929; color: white;")

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)

        # Top label
        text_style = """
        QLabel {
            font-size: 18px;
            margin: 20px 0;
        }
        """

        self.label = QLabel("Виберіть роль під якою ви хочете зайти", self)
        self.label.setStyleSheet(text_style)
        self.label.setAlignment(Qt.AlignCenter)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Create buttons
        self.admin_button = QPushButton("Адмін", self)
        self.cashier_button = QPushButton("Касир", self)

        admin_button_style = """
        QPushButton {
            background-color: none;
            color: white;
            border: 1px solid #FB7A9D;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 900;
        }
        QPushButton:hover {
            background-color: #FB7A9D;
        }
        QPushButton:pressed {
            background-color: #ffffff;
            color: black;
        }
        """
        cashier_button_style = """
        QPushButton {
            background-color: none;
            color: white;
            border: 1px solid #FB7A9D;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: 900;
        }
        QPushButton:hover {
            background-color: #FB7A9D;
        }
        QPushButton:pressed {
            background-color: #ffffff;
            color: black;
        }
        """
        self.admin_button.setStyleSheet(admin_button_style)
        self.cashier_button.setStyleSheet(cashier_button_style)

        # Connect buttons to functions
        self.admin_button.clicked.connect(self.handle_admin_button)
        self.cashier_button.clicked.connect(self.handle_cashier_button)

        # Add widgets to layouts
        main_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)
        button_layout.addWidget(self.admin_button)
        button_layout.addWidget(self.cashier_button)
        button_layout.setAlignment(Qt.AlignCenter)

    def handle_admin_button(self):
        self.choice_made.emit("адмін")
        self.close()

    def handle_cashier_button(self):
        self.choice_made.emit("касир")
        self.close()

    def show(self):
        super().show()
