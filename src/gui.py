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
        label = tk.Label(self.root, text="Algorytm Genetyczny", font=("Helvetica", 20))

        label.pack()

        # menubar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.create_file_menu()
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.create_view_menu()

        self.root.config(menu=self.menu_bar)

        # button
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=("Helvetica", 16),
                                command=self.generate_solution)
        self.button.pack(pady=10)

        # checkbox
        self.has_iter_limit = tk.IntVar(value=1)
        self.checkbox = tk.Checkbutton(self.root, text="Limit iteracji", font=("Helvetica", 16),variable=self.has_iter_limit)
        self.checkbox.pack(pady=10)


        # close window handling
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.root.mainloop()

    def create_file_menu(self):
        """
        Create the file menu in the upper taskbar
        :return: None
        """
        self.file_menu.add_command(label="Wczytaj miasta", command=self.load_graph)
        self.file_menu.add_command(label="Wczytaj populację", command=self.load_population)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Wylosuj miasta", command=self.generate_graph)
        self.file_menu.add_command(label="Wylosuj populację", command=self.generate_population)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Zapisz miasta", command=self.save_graph)
        self.file_menu.add_command(label="Zapisz populację", command=self.save_population)
        self.menu_bar.add_cascade(menu=self.file_menu, label="Pliki")

    def create_view_menu(self):
        """
        Create the visual settings menu in the upper taskbar
        :return:
        """
        self.view_menu.add_command(label="Czcionka +", command=self.increase_font)
        self.view_menu.add_command(label="Czcionka -", command=self.decrease_font)
        self.view_menu.add_command(label="Wyrównaj okno", command=self.normalize_window_size)
        self.menu_bar.add_cascade(menu=self.view_menu, label="Widok")

    def close_window(self):
        """
        Handle closing via top right corner X
        :return: None
        """
        if messagebox.askyesno(title="Zamknij",
                               message="Czy na pewno chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            self.root.destroy()

    def generate_solution(self):
        """
        Generate a random solution with loaded problem and initial population.
        :return:
        """
        if self.has_iter_limit.get() == 0:
            print("INF")
        else:
            print(9999)

    def load_graph(self):
        """
        Handle loading graph from  .csv
        :return:
        """
        pass

    def load_population(self):
        """
        Handle loading initiaL population from  .csv
        :return:
        """
        pass

    def generate_graph(self):
        """
        Handle generating random graph from generate_graph.create_complete_graph
        :return:
        """
        pass

    def generate_population(self):
        """
        Handle generating random population
        :return:
        """
        pass

    def save_graph(self):
        """
        Save currently loaded graph to .csv
        :return:
        """
        pass

    def save_population(self):
        """
        save currently loaded population to .csv
        :return:
        """
        pass



    # TODO: turn into lambdas
    def increase_font(self):
        pass

    def decrease_font(self):
        pass

    def normalize_window_size(self):
        pass


if __name__ == '__main__':
    GUI()
