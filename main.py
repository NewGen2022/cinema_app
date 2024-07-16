import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from main_window import moviesWindow
from login_window import login
from db_connection import DataBase
from choice import Choice
from admin.widget import Widget


def run_application():
    app = QApplication(sys.argv)
    database = DataBase(app)

    login_window = login.Login(database)
    try:
        login_successful, access_right, login_name = login_window.run_login_process()
    except Exception as e:
        show_error_message(str(e))
        sys.exit(1)

    if login_successful:
        if access_right == 1:
            type_of_window = Choice(app, database)
            type_of_window.choice_made.connect(
                lambda choice: handle_choice(choice, app, database, login_name)
            )
            type_of_window.show()
        else:
            handle_choice("касир", app, database, login_name)

        sys.exit(app.exec())


def handle_choice(choice, app, database, login_name):
    if choice == "адмін":
        helpWindow = Widget(database, login_name)
        helpWindow.show()
    else:
        main_window = moviesWindow.MainWindow(app, database)
        main_window.show()


def show_error_message(message):
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText("Помилка з підключенням під час запуску програми")
    msg_box.setWindowTitle("Error")
    msg_box.exec()


if __name__ == "__main__":
    run_application()
