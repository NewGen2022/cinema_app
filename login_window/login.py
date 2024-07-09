import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from login_window.resizeImage import ResizedImage

WIDTH_WINDOW = 1000
HEIGHT_WINDOW = 600
FONT_FAMILY = "Franklin Gothic Heavy"


class Login(ctk.CTk):
    def __init__(self, database):
        super().__init__()

        self.database = database
        self.access_rights = 0

        self.isLoginSuccessful = False

        # query usernames and logins
        connection = self.database.connection
        cursor = connection.cursor()
        query_login = "SELECT * FROM db_findtick.authorization"
        cursor.execute(query_login)
        self.username_passwords = cursor.fetchall()
        # print(self.username_passwords)

        self.set_window_appearance()
        self.center_window()
        self.create_left_side()
        self.create_right_side()
        self.bind_events()

    # set window title, resizing, dark mode
    def set_window_appearance(self):
        self.title("LogIn")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

    # set an image frame and an image itself at the left side
    def create_left_side(self):
        frame_image = ctk.CTkFrame(self)
        frame_image.place(x=0, y=0, relwidth=0.5, relheight=1)

        rounded_label_image = ResizedImage(
            frame_image, image_path="./assets/login_photo.jpg"
        )
        rounded_label_image.place(relx=0.5, rely=0.5, anchor="center")

    # set an login frame and an login inputs/labels at the right side
    def create_right_side(self):
        frame_login_input = ctk.CTkFrame(self)
        frame_login_input.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

        self.error_label = self.create_label(
            frame_login_input, text_color="red", font_size=16
        )
        self.error_label.pack_forget()

        # login widgets
        self.create_label(
            frame_login_input, "З поверненням!", text_color="#FB7A9D", font_size=44
        ).pack(pady=(100, 0))
        self.create_label(
            frame_login_input, "Авторизуйтесь в акаунті", text_color="gray"
        ).pack(padx=(0, 120), pady=(0, 60))

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        entry_login = self.create_entry(
            frame_login_input, placeholder="Введіть логін", textvariable=self.username
        )
        entry_login.pack(pady=(0, 30))

        entry_password = self.create_entry(
            frame_login_input,
            placeholder="Введіть пароль",
            show="*",
            textvariable=self.password,
        )
        entry_password.pack()

        button = ctk.CTkButton(
            frame_login_input,
            text="Вхід",
            width=180,
            height=40,
            font=(FONT_FAMILY, 16, "bold"),
            fg_color="#FB7A9D",
            command=self.on_login,
        )
        button.pack(pady=(90, 0))

    # set window size and center it
    def center_window(self):
        screen_width, screen_height = (
            self.winfo_screenwidth(),
            self.winfo_screenheight(),
        )
        x_center, y_center = (screen_width - WIDTH_WINDOW) // 3, (
            screen_height - HEIGHT_WINDOW
        ) // 4

        self.geometry(f"{WIDTH_WINDOW}x{HEIGHT_WINDOW}+{x_center}+{y_center}")

    # events for window manipulations
    def bind_events(self):
        self.bind("<Escape>", lambda event: self.quit())
        self.bind("<Control-m>", lambda event: self.iconify())

    # handle button "Вхід" pressing
    def on_login(self):
        username = self.username.get()
        password = self.password.get()

        for entry in self.username_passwords:
            if username in entry:
                if password == entry[1]:
                    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    connection = self.database.connection
                    cursor = connection.cursor()
                    query = "INSERT INTO db_findtick.actions (user, actions, date_actions) VALUES (%s, %s, %s)"
                    values = (username, "ВХІД", time)
                    cursor.execute(query, values)
                    connection.commit()

                    self.isLoginSuccessful = True
                    self.access_rights = entry[2]
                    self.destroy()
                    return
                else:
                    error_message = "Invalid password"
                    break
            else:
                error_message = "Invalid login"

        # display error
        if error_message:
            self.display_error(error_message)

    # displaying error
    def display_error(self, error_message):
        self.error_label.configure(text=error_message)
        self.error_label.pack(pady=(45, 0))

    # creating label
    def create_label(self, parent, label_text="Label", text_color="#fff", font_size=16):
        return ctk.CTkLabel(
            parent,
            text=label_text,
            text_color=text_color,
            font=(FONT_FAMILY, font_size, "bold"),
        )

    # creating entry
    def create_entry(self, parent, placeholder=None, show=None, font_size=16, **kwargs):
        textvariable = kwargs.pop("textvariable", None)
        return ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=340,
            height=35,
            show=show,
            font=(FONT_FAMILY, font_size, "bold"),
            textvariable=textvariable,
            **kwargs,
        )

    # run login window
    def run_login_process(self):
        self.mainloop()
        return self.isLoginSuccessful, self.access_rights, self.username.get()
