import sys
from PySide6.QtWidgets import QApplication
from main_window import moviesWindow
from login_window import login
from db_connection import DataBase
from choice import Choice


def run_application():
    app = QApplication(sys.argv)
    database = DataBase(app, sys.argv)

    login_window = login.Login(database)
    login_successful, access_right = login_window.run_login_process()

    if login_successful:
        if access_right == 1:
            type_of_window = Choice(app, database)
            type_of_window.choice_made.connect(
                lambda choice: handle_choice(choice, app, database)
            )
            type_of_window.show()
        else:
            handle_choice("касир", app, database)

        sys.exit(app.exec_())


def handle_choice(choice, app, database):
    if choice == "адмін":
        print("ADMIN WINDOW IMITATION")
    else:
        main_window = moviesWindow.MainWindow(app, database)
        main_window.show()


if __name__ == "__main__":
    run_application()
