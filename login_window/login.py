import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk

WIDTH_WINDOW = 1000
HEIGHT_WINDOW = 600
FONT_FAMILY = 'Franklin Gothic Heavy'

class ResizedImage(ttk.Label):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_original = Image.open(image_path)
        self.image_tk = self.resize_image()
        self.configure(image=self.image_tk)

    def resize_image(self, frame_width=630, frame_height=800):
        resized_image = self.image_original.resize((frame_width, frame_height))
        return ImageTk.PhotoImage(resized_image)

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('LogIn')
        self.attributes('-topmost', True)
        self.resizable(False, False)
        ctk.set_appearance_mode('dark')

        # set window size and center it
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_center, y_center = (screen_width - WIDTH_WINDOW) // 2, (screen_height - HEIGHT_WINDOW) // 2

        self.geometry(f'{WIDTH_WINDOW}x{HEIGHT_WINDOW}+{x_center}+{y_center}')

        # set an image frame and an image itself at the left side
        frame__image = ctk.CTkFrame(self)
        frame__image.place(x=0, y=0, relwidth=0.5, relheight=1)

        rounded_label_image = ResizedImage(frame__image, image_path='./login_photo.jpg')
        rounded_label_image.place(relx=0.5, rely=0.5, anchor='center')

        # set an login frame and an login inputs/labels at the right side
        frame_login_input = ctk.CTkFrame(self)
        frame_login_input.place(relx=0.5, y=0, relwidth=0.5, relheight=1)

        # login widgets
        self.create_label(frame_login_input, 'З поверненням!', text_color='#FB7A9D', font_size=44).pack(pady=(100, 0))
        self.create_label(frame_login_input, 'Авторизуйтесь в акаунті', text_color='gray').pack(padx=(0, 120), pady=(0, 60))

        self.create_entry(frame_login_input, placeholder='Введіть логін').pack(pady=(0, 30))
        self.create_entry(frame_login_input, placeholder='Введіть пароль', show='*').pack()

        button = ctk.CTkButton(frame_login_input, text='Вхід', width=180, height=40, font=(FONT_FAMILY, 16, 'bold'), fg_color='#FB7A9D')
        button.pack(pady=(90, 0))

        # events for window manipulations
        self.bind("<Escape>", lambda event: self.quit())
        self.bind("<Control-m>", lambda event: self.iconify())

        # run app
        self.mainloop()


    def create_label(self, parent, label_text='Label', text_color='#fff', font_size=16):
        return ctk.CTkLabel(parent, text=label_text, text_color=text_color, font=(FONT_FAMILY, font_size, 'bold'))


    def create_entry(self, parent, placeholder=None, show=None, font_size=16):
        return ctk.CTkEntry(parent, placeholder_text=placeholder, width=340, height=35, show=show, font=(FONT_FAMILY, font_size, 'bold'))


Login()
