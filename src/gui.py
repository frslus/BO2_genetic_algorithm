import tkinter as tk
from tkinter import messagebox
class GUI:
    """
    Represent the main GUI window
    """
    def __init__(self):
        # init window
        self.root = tk.Tk()
        self.root.title("Problem transportowy PSFŚ")
        self.root.geometry("500x500")
        label = tk.Label(self.root,text = "Algorytm Genetyczny", font=("Helvetica", 20))
        label.pack()

        # menubar
        self.menu_bar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Wczytaj miasta", command=self.load_graph)
        self.file_menu.add_separator()
        self.menu_bar.add_cascade(menu=self.file_menu, label="Pliki")

        self.root.config(menu=self.menu_bar)

        # close window handling
        self.root.protocol("WM_DELETE_WINDOW",self.close_window)



        self.root.mainloop()

    def close_window(self):
        """
        Handle closing via top right corner X
        :return: None
        """

        if messagebox.askyesno(title="Zamknij",message="Czy na pewno chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            self.root.destroy()

    def load_graph(self):
        """
        Handle loading graph from  .csv
        :return:
        """
        pass

if __name__ == '__main__':
    GUI()