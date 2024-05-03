from gui.application_frame import ApplicationFrame
from gui.functions import *
from gui.login.login_frame import *
from gui.login.register_user_frame import *
from gui.login.forgot_password_frame import *
from gui.login.forget_password_frame_inner import *

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Variables
        self.authenticated_user = None
        self.main_frame = None
        self.frames = {}

        # Create the Main frame
        self.open_login_frame(first_time=True)

    def change_geometry(self, width, height, centralize=False):
        if not centralize:
            self.geometry(f"{width}x{height}")
        else:
            self.geometry(center_window_to_display(self, width, height, self._get_window_scaling()))

    def change_title(self, new_title):
        # Change the window geometry
        self.title(new_title)

    def open_register_user_frame(self):
        self.main_frame.destroy()
        self.main_frame = RegisterUserFrame(self)
        self.frames["register_frame"] = self.main_frame
        self.main_frame.pack(expand=True, fill="both")  # Expand to fill the main app window

    def open_forgot_password_frame(self, user_email=None):
        self.main_frame.destroy()
        self.main_frame = ForgotPasswordFrame(self, user_email)
        self.frames["forgot_password_frame"] = self.main_frame
        self.main_frame.pack(expand=True, fill="both")

    def open_forgot_password_inner_frame(self, user_email):
        self.main_frame.destroy()
        self.main_frame = ForgotPasswordInnerFrame(self, user_email)
        self.frames["forgot_password_inner_frame"] = self.main_frame
        self.main_frame.pack(expand=True, fill="both")

    def open_login_frame(self, first_time=False):

        if not self.main_frame is None:
            self.main_frame.destroy()

        self.main_frame = MainFrame(self, first_time)
        self.main_frame.pack(expand=True, fill="both")

    def open_application_frame(self):
        self.main_frame.destroy()
        self.main_frame = ApplicationFrame(self, self.authenticated_user)
        self.main_frame.pack(expand=True, fill="both")

    def destroy_all_frames(self):
        # Destroy all frames in the dictionary
        for frame_name, frame in self.frames.items():
            frame.destroy()
        self.frames = {}  # Clear the dictionary