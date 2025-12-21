import tkinter as tk
from tkinter import messagebox
class GUI:
    """
    Represent the main GUI window
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Algorytm Genetyczny PSFŚ")
        self.root.protocol("WM_DELETE_WINDOW",self.close_window)


        self.root.mainloop()

    def close_window(self):
        """
        Handle closing via top right corner X
        :return: None
        """
        if messagebox.askyesno(title="Zamknij",message="Czy chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            self.root.destroy()

if __name__ == '__main__':
    GUI()