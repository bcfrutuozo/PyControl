import customtkinter as ctk
from gui.frame_base import FrameBase


class ApplicationFrame(FrameBase):

    def __init__(self, master, authenticated_user):

        if authenticated_user is None:
            raise RuntimeError("É necessário um usuário válido para autenticar na aplicação")

        self.authenticated_user = authenticated_user

        super().__init__(master, window_title=f'PyControl - Bem-vindo {self.authenticated_user}', window_width=1440, window_height=900,
                         centralize_window=True)

    def load_modules(self):
        return []

    def setup_frame(self):

        modules = self.load_modules()

        tabs = ctk.CTkTabview(self.frame)
        tabs.pack(padx=20, pady=20)

        #for module in modules:
        tabs.add("Tab2 1")
        tabs.add("Tabs 2")
        tabs.add("Tabs 3")

        pass

