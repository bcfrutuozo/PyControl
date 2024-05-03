import customtkinter as ctk
from abc import ABCMeta, abstractmethod
from typing import Union, Callable, Any


class FrameBase(ctk.CTkFrame, metaclass=ABCMeta):

    def __init__(self, master, window_width, window_height, pad_x=40, pad_y=40, window_title=None, centralize_window=False):
        super().__init__(master)
        self.master = master

        if (window_width - pad_x < 0) or (window_height - pad_y < 0):
            raise AssertionError("Não é possível construir um Frame fora da base da janela")

        if window_title is not None:
            self.master.change_title(window_title)

        self.master.change_geometry(window_width, window_height, centralize_window)
        self.frame = ctk.CTkFrame(master=self, width=window_width - pad_x, height=window_height - pad_y)
        self.frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.window_width = window_width
        self.window_height = window_height
        self.frame_width = window_width - pad_x
        self.frame_height = window_height - pad_y

        self.setup_frame()

    @abstractmethod
    def setup_frame(self):
        pass