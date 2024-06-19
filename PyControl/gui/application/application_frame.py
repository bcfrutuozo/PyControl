import customtkinter as ctk
from gui.application import control_frame
from gui.application.control_frame import ControlFrame
from gui.application.cliente_frame import ClientesFrame
from gui.frame_base import FrameBase


class ApplicationFrame(FrameBase):

    def __init__(self, master, width, height, authenticated_user):

        if authenticated_user is None:
            raise RuntimeError("É necessário um usuário válido para autenticar na aplicação")

        self.authenticated_user = authenticated_user

        super().__init__(master, window_title=f'PyControl - Bem-vindo {self.authenticated_user}', window_width=width, window_height=height,
                         centralize_window=True)

        # Set min size to properly handle control bar options and base GUI operations
        self.master.minsize(width=width, height=height)
        self.inner_frame = None

    def load_modules(self):
        return ['Clientes',2,3,4,5,6,7,8,9,10]

    def setup_frame(self):

        modules = self.load_modules()

        if not modules:
            raise RuntimeError("Lista de módulos da aplicação está vazia.")

        # Allow resize for main window after log in
        self.master.enable_resize()

        self.control_frame = ControlFrame(self, 200, 200, modules)
        self.control_frame.pack(padx=10, pady=10, side='left', anchor='nw', fill='y', expand=False)

        #cb = ctk.CTkOptionMenu(master=self, values=['option 1', 'option 2'])
        #cb.pack(padx=10, pady=20, anchor="nw")

        #tabs = ctk.CTkTabview(self.frame)
        #tabs.pack(padx=20, pady=20)
#
        ##for module in modules:
#
        #tabs.add("Empresa")
        #tabs.add("Tabs 2")
        #tabs.add("Tabs 3")

        pass

    def open_frame(self, frame_name):

        if self.inner_frame is not None:
            self.inner_frame.destroy()

        match frame_name:
            case 'Clientes':
                self.inner_frame = ClientesFrame(self, width=200, height=200)
                self.inner_frame.pack(padx=(0, 10), pady=10, side='right', anchor='ne', fill='both', expand=True)

    def quit(self):
        self.master.quit()