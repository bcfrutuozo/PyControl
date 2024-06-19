import customtkinter as ctk
from gui.inner_frame_base import InnerFrameBase
from functools import partial

class ControlFrame(InnerFrameBase):

    def __init__(self, master, width, height, modules):
        self.modules = modules
        super().__init__(master, width, height)

    def setup_frame(self):

        for module in self.modules:
            btn = ctk.CTkButton(master=self, width=150, height=40, text=module, command=partial(self.master.open_frame, module))
            btn.pack(padx=10, pady=10)

        btn = ctk.CTkButton(master=self, width=150, height=40, text='Sair', command=self.quit)
        btn.pack(padx=10, pady=10, side='bottom')

    def quit(self):
        self.master.quit()
