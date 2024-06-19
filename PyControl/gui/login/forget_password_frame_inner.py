from gui.frame_base import FrameBase
import customtkinter as ctk
from database.login_db import *
from functions import generate_temporary_password, send_password_reset_email
from tkinter import messagebox


class ForgotPasswordInnerFrame(FrameBase):
    def __init__(self, master, user_email):
        self.user_email = user_email
        super().__init__(master, window_title='Recuperar Senha - 2º Passo', window_width=360, window_height=420, centralize_window=False)

    def setup_frame(self):

        self.back_button = ctk.CTkButton(
            master=self,
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

        self.text = ctk.CTkLabel(master=self, text="Step 2", font=('Century Gothic', 25))
        self.text.place(x=70, y=75)

        # Security Question entry block
        security_question = DATABASE_LOGIN.get_security_question(self.user_email)  # You can pass user_email here or retrieve it from somewhere
        self.security_question_label = ctk.CTkLabel(master=self, text=security_question, font=('Century Gothic', 14))
        self.security_question_label.place(x=70, y=140)

        # Security Answer entry block
        self.security_answer_block = ctk.CTkEntry(master=self, width=220, placeholder_text="Security Answer")
        self.security_answer_block.place(x=70, y=190)

        # Submit button for step 2
        self.submit_button2 = ctk.CTkButton(master=self, width=100, text="Reset Password", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.handle_reset_password)
        self.submit_button2.place(x=130, y=260)

    def back_button_click(self):
        self.master.destroy_all_frames()
        self.master.open_forgot_password_frame(self.user_email)

    def handle_reset_password(self):
        # Get the user's security answer
        user_answer = self.security_answer_block.get()

        # Check if the security answer is correct
        if DATABASE_LOGIN.check_security_answer(self.user_email, user_answer):  # Pass user_email here or retrieve it from somewhere
            # Generate a temporary password (or token)
            temporary_password = generate_temporary_password()
            DATABASE_LOGIN.update_password(self.user_email, temporary_password)  # Pass user_email here or retrieve it from somewhere
            # Send the password reset email
            send_password_reset_email(self.user_email, temporary_password)  # Pass user_email here or retrieve it from somewhere
            # Inform the user (you can customize this part)
            messagebox.showinfo("Password Reset", "An email with instructions has been sent to your email address.")

            # Remove the ForgotPassword2Frame and show the login frame again
            self.master.destroy_all_frames()
            self.master.open_main_frame()
        else:
            messagebox.showerror("Error", "Security answer does not match.")