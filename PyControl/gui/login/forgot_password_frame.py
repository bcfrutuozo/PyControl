import customtkinter as ctk
from tkinter import messagebox
from database.login import *
from functions import is_valid_email
from gui.frame_base import FrameBase


class ForgotPasswordFrame(FrameBase):
    def __init__(self, master, user_email, **kwargs):
        self.user_email = user_email
        super().__init__(master, window_title='Recuperar Senha', window_width=360, window_height=420, centralize_window=False)

    def setup_frame(self):  # Correct method name

        self.back_button = ctk.CTkButton(
            master=self.frame,
            width=15,
            height=30,
            text="◀️",  # Use the left arrow character as the text
            corner_radius=6,
            fg_color="#3498db",
            text_color="#ffffff",
            hover_color="#2980b9",
            command=self.back_button_click
        )
        self.back_button.place(x=10, y=10)

        self.text = ctk.CTkLabel(master=self.frame, text="Entre com o seu E-Mail", font=('Century Gothic', 25))
        self.text.place(x=self.frame_width/2, y=75, anchor=ctk.CENTER)
        # Email entry block
        self.email_block = ctk.CTkEntry(master=self.frame, width=220, placeholder_text="E-Mail")

        if not self.user_email is None:
            self.email_block.insert(0, self.user_email)

        self.email_block.place(x=self.frame_width/2, y=140, anchor=ctk.CENTER)
        # Submit button
        self.submit_button = ctk.CTkButton(master=self.frame, width=100, text="Submit", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.handle_reset_password)
        self.submit_button.place(x=self.frame_width/2, y=190, anchor=ctk.CENTER)

    def back_button_click(self):
        self.master.destroy_all_frames()
        self.master.open_login_frame()

    def handle_reset_password(self):
        # Get the user's email address from the entry field
        user_email = self.email_block.get()
        check_exists = DATABASE_LOGIN.email_exists(user_email)
        security_question = DATABASE_LOGIN.get_security_question(user_email)
        if not is_valid_email(user_email):
            print("Invalid email address")
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        if check_exists:
            self.master.destroy_all_frames()
            self.master.open_forgot_password_inner_frame(user_email)
        else:
            messagebox.showerror("Error", "E-Mail doesn't exists!")