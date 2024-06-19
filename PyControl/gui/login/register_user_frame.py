import customtkinter as ctk
from tkinter import messagebox
from functions import *
import io
from widgets.video_cam import *
from database.login_db import *
from gui.frame_base import FrameBase


class RegisterUserFrame(FrameBase):
    def __init__(self, master):
        super().__init__(master, window_title='Cadastro de Usuário', window_width=510, window_height=840, centralize_window=False)
        self.initialize_driver()

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

        # Entry fields for registration form
        self.name_entry = ctk.CTkEntry(master=self, width=400, placeholder_text="Nome")
        self.name_entry.place(x=50, y=55)

        self.username_entry = ctk.CTkEntry(master=self, width=400, placeholder_text="Login")
        self.username_entry.place(x=50, y=85)

        self.email_entry = ctk.CTkEntry(master=self, width=400, placeholder_text="Entre com seu e-mail")
        self.email_entry.place(x=50, y=115)

        self.p_block = ctk.CTkEntry(master=self, width=400, placeholder_text="Digite a sua senha", show="*")
        self.p_block.place(x=50, y=145)

        self.security_question_label = ctk.CTkLabel(master=self, text="Pergunta secreta", font=('Century Gothic', 10))
        self.security_question_label.place(x=50, y=175)

        self.security_questions = ["Qual o primeiro nome da sua mãe?", "Qual seu nome favorito de pet?", "Aonde você nasceu?", "Qual seu filme favorito?", "Qual o seu herói de infância?"]
        self.security_question_var = ctk.StringVar(value="Selecione a sua pergunta secreta")
        self.security_question_dropdown = ctk.CTkComboBox(master=self, variable=self.security_question_var, values=self.security_questions, width=400, state="readonly")
        self.security_question_dropdown.place(x=50, y=205)

        # Security Answer entry field
        self.security_answer_entry = ctk.CTkEntry(master=self, width=400, placeholder_text="Resposta secreta")
        self.security_answer_entry.place(x=50, y=235)

        # Webcam widget
        self.webcam = VideoStreamWidget(master=self, width=600, height=560, enable_start_stop=True, enable_snapshot=False)
        self.webcam.place(x=50, y=270)

        # Registration button
        self.register_button = ctk.CTkButton(master=self, width=150, text="Cadastrar",
                                                  corner_radius=6,
                                                  fg_color="#3498db", text_color="#ffffff", hover_color="#2980b9",
                                                  command=self.new_user_data)
        self.register_button.place(x=self.window_width/2, y=755, anchor=ctk.CENTER)

    def initialize_driver(self):
        self.webcam.initialize_driver()

    def back_button_click(self):
        self.webcam.close_driver()
        self.master.destroy_all_frames()
        self.master.open_login_frame()

    def new_user_data(self):
        # Get user inputs from the registration form
        name = self.name_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.p_block.get()
        security_question = self.security_question_var.get()  # Get the selected security question
        security_answer = self.security_answer_entry.get()

        # Photo as byte array for serialization
        stream = io.BytesIO()
        self.webcam.image.save(stream, format="JPEG")
        photo = stream.getvalue()

        if not name or not name or not username or not password:
            print("Por favor, preencha todos os campos necessários")
            messagebox.showerror("Erro", "Por favor, preencha todos os campos necessários")
            return
        # Check if fields contain only English letters and standard characters
        if not is_valid_chars(username):
            print("Campo usuário deve possuir apenas caracteres da lingua inglesa")
            messagebox.showerror("Erro", "Por favor, utilize apenas caracteres da lingua inglesa para o campo do usuário")
            return
        if security_question == "Selecione a sua pergunta secreta":
            print("Pergunta secreta inválida")
            messagebox.showerror("Erro", "A pergunta secreta não é válida")
            return
        if not is_valid_email(email):
            print("E-mail inválido")
            messagebox.showerror("Erro", "Por favor, digita um endereço de e-mail válido")
            return

        # Call the register_user function from functions.py
        if DATABASE_LOGIN.register_user(name, username, email, password, security_question, security_answer, photo):
            # Registration successful
            print("Usuário cadastrado com sucesso!")
            messagebox.showinfo("Sucesso", "Registro foi inserido com sucesso na base de dados!")
            self.webcam.close_driver()
            self.registration_frame.place_forget()
            self.registration_frame.destroy()
            self.master.open_main_frame()
        else:
            # Handle the case where the username or email is already taken
            print("Username or email is already in use.")
            messagebox.showerror("Error", "The username or e-mail already exists.")