import customtkinter as ctk
from abc import ABCMeta, abstractmethod


class FrameBase(ctk.CTkFrame, metaclass=ABCMeta):

    def __init__(self, master, window_width, window_height, window_title=None, centralize_window=False):
        super().__init__(master, width=window_width, height=window_height)
        self.master = master

        if window_title is not None:
            self.master.change_title(window_title)

        self.master.change_geometry(window_width, window_height, centralize_window)

        self.window_width = window_width
        self.window_height = window_height

        self.setup_frame()

    @abstractmethod
    def setup_frame(self):
        pass