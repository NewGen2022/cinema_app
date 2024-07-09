from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt


class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon("./assets/help.png"))
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)

        # Header label
        header_label = QLabel("Як продати білет", self)
        header_font = QFont("Century Gothic", 20)  # Set font size to 20
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)  # Center align the header
        main_layout.addWidget(header_label)

        text = (
            "Для того, щоб <b>продати/забронювати білети</b> потрібно натиснути лівою кнопкою миші на <b>потрібний клієнту фільм</b>, "
            "після чого відкриється нове вікно з доступними сеансами. В вікні з вибраним фільмом <b>вибираємо потрібний "
            "клієнту сеанс</b> та натискаємо лівою кнопкою миші на нього, після чого відкриється вікно з розташуванням місць (зал). "
            "Лівою кнопкою миші обираємо,<b> потрібні клієнту місця</b>, <b>вводимо електронну пошту клієнта та чекаємо поки йому прийде повідомлення.</b> "
            "Білет(-и) продано. <br> <span style='color:#00ff15; font-weight:700;'>Гарна робота!</span> <br> <i> Потрібний фільм можна шукати вручну гортаючи горизонтально (за допомогою колеса миші) або "
            "ввівши в поле пошуку початок назви потрібного фільму. </i>"
        )

        # Create QLabel with word wrap enabled
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.RichText)
        self.label.setText(text)
        font = QFont("Century Gothic", 16)  # Set larger font
        self.label.setFont(font)
        self.label.setWordWrap(True)  # Enable word wrap for the label
        main_layout.addWidget(self.label)

        # Spacer to push OK button to the bottom
        main_layout.addStretch(1)

        # Horizontal layout for the OK button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)  # Add stretch to center align button horizontally

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setMaximumWidth(50)
        self.ok_button.setMinimumWidth(50)

        button_layout.addWidget(self.ok_button)
        button_layout.addStretch(1)  # Add stretch to center align button horizontally

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
