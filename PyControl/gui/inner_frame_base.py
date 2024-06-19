import customtkinter as ctk
from abc import ABCMeta, abstractmethod


class InnerFrameBase(ctk.CTkFrame, metaclass=ABCMeta):

    def __init__(self, master, width, height, pad_x=40, pad_y=40):
        super().__init__(master)
        self.master = master

        self.frame_width = width - pad_x
        self.frame_height = height - pad_y

        self.setup_frame()

    @abstractmethod
    def setup_frame(self):
        pass
