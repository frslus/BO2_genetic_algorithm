import tkinter as tk
from math import ceil
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure

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

        # menubar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)

        # buttons, checkboxes, text elements
        self.label = tk.Label()
        self.button = tk.Button()
        self.has_iter_limit = tk.IntVar(value=1)
        self.checkbox = tk.Checkbutton()

        #checklist
        self.mutation_type = tk.IntVar()
        self.checklist = tk.Frame(self.root)
        self.create_checklist()

        # graph
        self.fig = Figure(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg()

        # print results
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)  # close window handling
        self.place_everything()
        self.root.mainloop()

    def place_everything(self):
        """
        Places every element of the GUI
        :return:
        """
        self.update_window_params()
        self.create_full_menu()
        self.root.config(menu=self.menu_bar)
        self.update_text_elements()
        self.update_graph()

    def clear_everything(self):
        """
        Remove every single element of GUI
        :return:
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_full_menu(self):
        """
        Create the full menu
        :return:
        """
        # TODO: assess if function is redundant (= if menu will not be expanded)
        self.create_file_menu()
        self.create_view_menu()

    def update_window_params(self):
        """
        Update window parameters
        :return:
        """
        self.root.title("Problem transportowy PSFŚ")
        self.root.geometry("1000x750")
        self.root.iconbitmap("../GEIcon.ico")

    def update_text_elements(self):
        """
        Update all text elements of gui with current font and fontsize
        :return:
        """
        # label
        self.label.pack_forget()
        self.label = tk.Label(self.root, text="Algorytm Genetyczny", font=(self.font, self.font_size1))
        self.label.pack()

        # button
        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution)
        self.button.place(relx=0.6, rely=0.07)

        # checkbox
        self.checkbox.place_forget()
        self.checkbox = tk.Checkbutton(self.root, text="Limit iteracji", font=(self.font, self.font_size2),
                                       variable=self.has_iter_limit)
        self.checkbox.place(relx=0.62, rely=0.15)

    def update_graph(self, x=None, y=None):
        """
        Plot the graph object with updates
        :return:
        """
        x = [i for i in range(20)] if x is None else x
        y = [(i ** 2 - 15 * i) for i in x] if y is None else y

        plot1 = self.fig.add_subplot(111)
        plot1.plot(x, y)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(relx=0.05, rely=0.1)

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()

    def create_file_menu(self):
        """
        Create the file menu in the upper taskbar
        :return: None
        """
        # load from file
        self.file_menu.add_command(label="Wczytaj miasta", command=self.load_graph)
        self.file_menu.add_command(label="Wczytaj populację", command=self.load_population)
        self.file_menu.add_separator()

        # randomize
        self.file_menu.add_command(label="Wylosuj miasta", command=self.generate_graph)
        self.file_menu.add_command(label="Wylosuj populację", command=self.generate_population)
        self.file_menu.add_separator()

        # save loaded
        self.file_menu.add_command(label="Zapisz miasta", command=self.save_graph)
        self.file_menu.add_command(label="Zapisz populację", command=self.save_population)

        self.menu_bar.add_cascade(menu=self.file_menu, label="Pliki")

    def create_view_menu(self):
        """
        Create the visual settings menu in the upper taskbar
        :return:
        """
        # adjust config
        self.view_menu.add_command(label="Czcionka +", command=self.increase_font)
        self.view_menu.add_command(label="Czcionka -", command=self.decrease_font)
        self.view_menu.add_command(label="Wyrównaj okno", command=self.update_window_params)
        self.view_menu.add_separator()

        # config.json handling
        self.view_menu.add_command(label="Zapisz konfigurację", command=self.save_config)
        self.view_menu.add_command(label="Wczytaj konfigurację", command=self.load_config)
        self.view_menu.add_command(label="TEST1", command=self.clear_everything)
        self.view_menu.add_command(label="TEST2", command=self.select_mutation_type)

        self.menu_bar.add_cascade(menu=self.view_menu, label="Widok")

    def create_checklist(self):
        """
        create the checklist with single answer
        :return:
        """
        self.checklist.columnconfigure(0, weight=1)

        check1 = tk.Radiobutton(self.checklist, text="typ 1", variable=self.mutation_type, value=1)
        check1.grid(row=0, column=0, sticky=tk.W+tk.E)
        check2 = tk.Radiobutton(self.checklist, text="typ 2", variable=self.mutation_type, value=2)
        check2.grid(row=1, column=0, sticky=tk.W + tk.E)
        check3 = tk.Radiobutton(self.checklist, text="typ 3", variable=self.mutation_type, value=3)
        check3.grid(row=2, column=0, sticky=tk.W + tk.E)

        self.checklist.place(relx=0.5, rely=0.1)

    def select_mutation_type(self):
        """
        TEST METHOD ONLY
        Select the type of mutation
        :return:
        """
        mutation_type = self.mutation_type.get()

        if mutation_type == 1:
            print(1)
        elif mutation_type == 2:
            print(2)
        elif mutation_type == 3:
            print(3)
            
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
        Generate a random solution with loaded problem and initial population (.py).
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
        # print(self.font_size1, self.font_size2_memory)
        self.font_size2 = ceil(self.font_size2_memory)

        self.update_text_elements()

    def decrease_font(self):
        """
        Decrease font size
        :return:
        """
        self.font_size1 -= 2 if self.font_size2 > 2 else 0
        self.font_size2_memory -= 1.5 if self.font_size2_memory > 1.5 else 0

        self.font_size2 = ceil(self.font_size2_memory)
        # print(self.font_size1, self.font_size2_memory, self.font_size2)

        self.update_text_elements()


if __name__ == '__main__':
    GUI()
