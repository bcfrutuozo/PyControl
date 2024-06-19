import customtkinter as ctk
from gui.frame_base import FrameBase
from database.login_db import *
from functions import toggle_password


class MainFrame(FrameBase):

    def __init__(self, master, first_time):
        super().__init__(master, window_title='PyControl - Login', window_width=360, window_height=420, centralize_window=first_time)

    def setup_frame(self):

        # Disable resize for login and its inner frames
        self.master.disable_resize()

        #TOP text
        self.text = ctk.CTkLabel(master=self, text="Autenticação", font=('Century Gothic', 25))
        self.text.place(x=self.window_width/2, y=75, anchor=ctk.CENTER)

        self.error_label = ctk.CTkLabel(master=self, text="", font=('Century Gothic', 12), text_color="red")
        self.error_label.place(x=self.window_width/2, y=110, anchor=ctk.CENTER)

        #Username entry block
        self.u_block = ctk.CTkEntry(master=self, width=220, placeholder_text="Usuário")
        self.u_block.place(x=self.window_width/2, y=140, anchor=ctk.CENTER)

        #Password entry block
        self.show_password_var = ctk.BooleanVar()
        self.p_block = ctk.CTkEntry(master=self, width=220, placeholder_text="Senha", show="*")
        self.p_block.place(x=self.window_width/2, y=180, anchor=ctk.CENTER)

        #checkbox for showing password
        self.show_password = ctk.CTkCheckBox(master=self, text="Mostrar senha", font=('Century Gothic', 12), command=lambda: toggle_password(self.p_block, self.show_password_var), variable=self.show_password_var)
        self.show_password.place(x=self.window_width/2 - 54, y=220, anchor=ctk.CENTER)

        #Forgot password text
        self.label3 = ctk.CTkLabel(master=self, text="Esqueceu a senha?", font=('Century Gothic', 10))
        self.label3.place(x=190, y=206)
        self.label3.bind("<Enter>", lambda event: self.label3.configure(cursor="hand2"))
        # Change cursor back to the default arrow when mouse leaves the widget
        self.label3.bind("<Leave>", lambda event: self.label3.configure(cursor="arrow"))
        # Bind the click event to open the Forgot Password frame
        self.label3.bind("<Button-1>", lambda event: self.forgot_password_label_click())

        #Login button
        self.login_button = ctk.CTkButton(master=self, width=100, text="Logar", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.check_login_credentials)
        self.login_button.place(x=self.window_width/2, y=280, anchor=ctk.CENTER)

        #Register button
        self.register_button = ctk.CTkButton(master=self, width=100, text="Cadastrar", corner_radius=6, fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9", command=self.register_new_user_button_click)
        self.register_button.place(x=self.window_width/2, y=315, anchor=ctk.CENTER)

    def check_login_credentials(self):
        # Get the username and password from the input fields
        username = self.u_block.get()
        password = self.p_block.get()

        # Call the check_login function from functions.py
        if DATABASE_LOGIN.check_login(username, password):
            self.master.authenticated_user = username
            self.master.destroy_all_frames()
            self.master.open_application_frame()
        else:
            # Login failed, show an error message
            self.error_label.configure(text="Senha ou usuário inválido. Por favor, tente novamente")

    def forgot_password_label_click(self):
        self.master.destroy_all_frames()
        self.master.open_forgot_password_frame()

    def register_new_user_button_click(self):
        self.master.destroy_all_frames()
        self.master.open_register_user_frame()
