from app import *
from tkinter import ttk
import sv_ttk

def main():
    app = MainApp()
    app.tk.call('tk', 'scaling', 2.0)
    sv_ttk.set_theme("dark")

    style = ttk.Style()
    style.configure("Treeview", font=(None, 12))
    style.configure("Treeview.Heading", font=(None, 14))

    app.mainloop()


if __name__ == "__main__":
    main()
