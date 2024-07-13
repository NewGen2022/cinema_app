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
        self.setWindowIcon(QIcon("./assets/help-black.png"))
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout(self)

        header_label = QLabel("Як продати білет", self)
        header_font = QFont("Century Gothic", 20)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)

        text = "Для того, щоб <b>продати/забронювати білети</b> потрібно натиснути лівою кнопкою миші на <b>потрібний клієнту фільм</b>, "

        # Create QLabel with word wrap enabled
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.RichText)
        self.label.setText(text)
        font = QFont("Century Gothic", 16)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        main_layout.addWidget(self.label)

        main_layout.addStretch(1)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setMaximumWidth(50)
        self.ok_button.setMinimumWidth(50)

        button_layout.addWidget(self.ok_button)
        button_layout.addStretch(1)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
