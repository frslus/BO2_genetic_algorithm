import tkinter as tk
from math import ceil
from tkinter import messagebox

FONT_SIZE = 20
FONT = "Helvetica"


class GUI:
    """
    Represent the main GUI window
    """

    def __init__(self):
        # init text
        self.font = FONT
        self.font_size1 = FONT_SIZE
        self.font_size2_memory = FONT_SIZE * 0.75
        self.font_size2 = ceil(self.font_size2_memory)

        # init window
        self.root = tk.Tk()
        self.label = ""
        self.update_window_params()

        self.label = tk.Label(self.root, text="Algorytm Genetyczny", font=(self.font, self.font_size1))
        self.label.pack()

        # menubar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.create_file_menu()
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.create_view_menu()

        self.root.config(menu=self.menu_bar)

        # button
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution)

        # self.button.pack(anchor="ne", padx=10, pady=10)
        self.button.place(relx=0.6, rely=0.07)

        # checkbox
        self.has_iter_limit = tk.IntVar(value=1)
        self.checkbox = tk.Checkbutton(self.root, text="Limit iteracji", font=(self.font, self.font_size2),
                                       variable=self.has_iter_limit)
        self.checkbox.place(relx=0.62, rely=0.15)
        # self.checkbox.pack(anchor="ne", padx=10, side="top")
        # self.checkbox.pack(side="right",pady=10)

        # close window handling
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        self.root.mainloop()

    def update_window_params(self):
        """
        Update window parameters
        :return:
        """
        self.root.title("Problem transportowy PSFŚ")
        self.root.geometry("1000x750")
        self.root.iconbitmap("../GEIcon.ico")

    def update_fonts(self):
        """
        Update the fonts gui with updated size
        :return:
        """
        # button
        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution)

        # self.button.pack(anchor="ne", padx=10, pady=10)
        self.button.place(relx=0.6, rely=0.07)

        # checkbox
        self.checkbox.place_forget()
        self.checkbox = tk.Checkbutton(self.root, text="Limit iteracji", font=(self.font, self.font_size2),
                                       variable=self.has_iter_limit)
        self.checkbox.place(relx=0.62, rely=0.15)

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
        self.view_menu.add_command(label="Wyrównaj okno", command=self.update_window_params)
        self.view_menu.add_separator()
        self.view_menu.add_command(label="Zapisz konfigurację", command=self.save_config)
        self.view_menu.add_command(label="Wczytaj konfigurację", command=self.load_config)
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
        # TODO: implement me!
        if self.has_iter_limit.get() == 0:
            print("INF")
        else:
            print(9999)

    def load_graph(self):
        """
        Handle loading graph from  .csv
        :return:
        """
        # TODO: implement me!
        pass

    def load_population(self):
        """
        Handle loading initiaL population from  .csv
        :return:
        """
        # TODO: implement me!
        pass

    def generate_graph(self):
        """
        Handle generating random graph from generate_graph.create_complete_graph
        :return:
        """
        # TODO: implement me!
        pass

    def generate_population(self):
        """
        Handle generating random population
        :return:
        """
        # TODO: implement me!
        pass

    def save_graph(self):
        """
        Save currently loaded graph to .csv
        :return:
        """
        # TODO: implement me!
        pass

    def save_population(self):
        """
        save currently loaded population to .csv
        :return:
        """
        # TODO: implement me!
        pass

    def save_config(self):
        """
        Save view settings config to .json
        :return:
        """
        # TODO: implement me!
        pass

    def load_config(self):
        """
        Load view settings config from .json
        :return:
        """
        # TODO: implement me!
        pass


    def increase_font(self):
        """
        Increase font size and update menu
        :return:
        """
        self.font_size1 += 2
        self.font_size2_memory += 1.5
        print(self.font_size1, self.font_size2_memory)
        self.font_size2 = ceil(self.font_size2_memory)

        self.update_fonts()

    def decrease_font(self):
        """
        Decrease font size
        :return:
        """
        self.font_size1 -= 2 if self.font_size2 > 2 else 0
        self.font_size2_memory -= 1.5 if self.font_size2_memory > 1.5 else 0

        self.font_size2 = ceil(self.font_size2_memory)
        print(self.font_size1, self.font_size2_memory, self.font_size2)

        self.update_fonts()


if __name__ == '__main__':
    GUI()
