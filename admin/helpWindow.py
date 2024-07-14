from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
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

        header_label = QLabel("Інструкція з користування", self)
        header_font = QFont("Century Gothic", 20)
        header_label.setFont(header_font)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        text = (
            "<span style='color: #ff0055; font-weight: bold;'>Загальна навігація</span> по вікну відбувається за допомогою лівої бокової панелі(далі меню). Обираючи пункт меню, в таблиці буде відображено всю необхідну інформацію.\n\n"
            '<br> <span style="color: #ff0055; font-weight: bold;">Для додавання нового запису</span> потрібно обрати бажаний пункт меню та нажати кнопку "додати". Буде відкрите вікно, в якому необхідно обрати та ввести всі необхідні для\n'
            "додавання об'єкту дані. При введені нових даних уважно перевіряйте коректність заповнення поля та відповідність необхідному формату.\n\n"
            "<br><span style='color: #ff0055; font-weight: bold;'>Для редагування чи видалення записів</span> потрібно нажати на запис в таблиці правою кнопкою миші та вибрати бажану дію. Перед видаленням уважно перевіряйте об'єкт, адже\n"
            "відмінити цю дію неможливо. При введені нових даних уважно перевіряйте коректність заповнення поля та відповідність необхідному формату.\n\n"
            '<br><span style="color: #ff0055; font-weight: bold;">Пункт меню "перейти до звітностей"</span> відкриває ще одне вікно, в якому відображаються дані про фінансову успішність кінотеатру. Окрім цього в даному вікні можна переглянути\n'
            "всі дії користувачів, що увійшли в програму. Інформацію в даному вікні не можна будь-яким чином редагувати."
        )

        # Create QLabel with word wrap enabled
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setText(text)
        font = QFont("Century Gothic", 16)
        self.label.setFont(font)
        self.label.setWordWrap(True)

        # Create a scroll area and set the QLabel as its widget
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(self.label)

        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        main_layout.addWidget(scroll_area)

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
