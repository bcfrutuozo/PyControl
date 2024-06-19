import customtkinter as ctk
from gui.inner_frame_base import InnerFrameBase
from tkcalendar import DateEntry
from CTkTable import CTkTable
from database.cliente_db import DATABASE_CLIENTE
import io
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk


class ClientesFrame(InnerFrameBase):

    def __init__(self, master, width, height):
        super().__init__(master, width, height)

    def setup_frame(self):

        # Load data
        self.data_source = []
        rawQuery = DATABASE_CLIENTE.selecionar_todos()
        rawImgs = DATABASE_CLIENTE.selecionar_todas_fotos()

        i = 0
        for record in rawQuery:
            img = Image.open(io.BytesIO(rawImgs[i]))
            img.thumbnail((75, 75))  # resize the image to desired size
            img = ImageTk.PhotoImage(img)
            i += 1
            self.data_source.append((img, record[0], record[1], record[2], record[3], record[4]))

        # Header
        self.header = ctk.CTkFrame(self, height=120)
        self.header.pack(padx=10, pady=10, side='top', fill='x')

        #start_date = DateEntry(self.header, width=80, height=100, placeholder="De")
        #start_date.pack(padx=10, pady=10, anchor='ne', side='right')
#
        #end_date = DateEntry(self.header, width=80, height=100, placeholder="Até")
        #end_date.pack(padx=10, pady=10, anchor='ne', side='right')
#
        #btnAtualizar = ctk.CTkButton(self.header, width=100, height=40, text="Atualizar")
        #btnAtualizar.pack(padx=10, pady=10, anchor='ne', side='right')
#
        btnCadastrar = ctk.CTkButton(self.header, width=100, height=40, text="Cadastrar")
        btnCadastrar.pack(padx=10, pady=10, anchor='nw', side='left')

        btnEditar = ctk.CTkButton(self.header, width=100, height=40, text="Editar", command=self.editar_cliente)
        btnEditar.pack(padx=10, pady=10, side='left')

        # Content
        grid = ctk.CTkFrame(self, width=100, height=100)
        grid.pack(padx=10, pady=10, side='bottom', expand=True, fill='both')

        # Create Treeview
        self.tree = ttk.Treeview(grid, columns=("IDCliente", "Nome", "E-Mail", "DDD", "Telefone"), selectmode='browse')
        self.tree.pack(padx=10, pady=10, side='bottom', expand=True, fill='both')

        # Setup column heading
        #self.tree.heading('Photo', text='photo', anchor='center')
        self.tree.heading('IDCliente', text='ID', anchor='center')
        self.tree.heading('Nome', text='Nome', anchor='center')
        self.tree.heading('E-Mail', text='E-Mail', anchor='center')
        self.tree.heading('DDD', text='DDD', anchor='center')
        self.tree.heading('Telefone', text='Telefone', anchor='center')

        # Setup column
        #self.tree.column('Photo', anchor='center', width=100)
        self.tree.column('IDCliente', anchor='center', width=80)
        self.tree.column('Nome', anchor='center', width=100)
        self.tree.column('E-Mail', anchor='center', width=100)
        self.tree.column('DDD', anchor='center', width=100)
        self.tree.column('Telefone', anchor='center', width=100)

        s = ttk.Style()
        s.configure('Treeview', rowheight=80)  # repace 40 with whatever you need
        s.layout('Treeview.Heading',
                     [('Treeheading.cell', {'sticky': 'nswe'}),
                      ('Treeheading.border', {'sticky': 'nswe', 'children': [
                          ('Treeheading.padding', {'sticky': 'nswe', 'children': [
                              ('Treeheading.image', {'side': 'top', 'sticky': '', 'expand': True}),
                              ('Treeheading.text', {'sticky': 'we'})
                          ]})
                      ]})
                      ])

        for entry in self.data_source:
            self.tree.insert('', 'end', image=entry[0], value=(entry[1], entry[2], entry[3], entry[4], entry[5]))
        pass

    def editar_cliente(self):
        print(self.tree.focus())
        pass
