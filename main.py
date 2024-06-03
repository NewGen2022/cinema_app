import sys
from PyQt5.QtWidgets import QApplication
from main_window import moviesWindow
from login_window import login
from db_connection import DataBase


def run_application():
    app = QApplication(sys.argv)

    database = DataBase()

    # Run the login window
    login_window = login.Login(database)
    login_successful = login_window.run_login_process()

    if login_successful:
        main_window = moviesWindow.MainWindow(app, database)
        main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
