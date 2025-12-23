import tkinter as tk
from math import ceil
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

# text constants
FONT_SIZE = 18
FONT = "Helvetica"

# graph positions
COST_GRAPH_POS = {"relx": 0.05, "rely": 0.05}
POPULATION_GRAPH_POS = {"relx": 0.05, "rely": 0.5}
TIME_GRAPH_POS = {"relx": 0.25, "rely": 0.5}

# algorithm parameter selection positions
CROSSING_SELECT_POS = {"relx": 0.85, "rely": 0.3}
SELECTION_SELECT_POS = {"relx": 0.85, "rely": 0.5}
MUTATION_SELECT_POS = {"relx": 0.85, "rely": 0.7}

GENERATE_SOLUTION_POS = {"relx": 0.6, "rely": 0.7}
CHECKBOX_POS = {"relx": 0.60, "rely": 0.77}


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

        # text fields
        self.textbox = tk.Text(self.root)

        # crossing type
        self.label_crossing = tk.Label()
        self.crossing_type = tk.IntVar(value=1)
        self.checklist_crossing = tk.Frame(self.root)

        # selection type
        self.label_selection = tk.Label()
        self.selection_type = tk.IntVar(value=1)
        self.checklist_selection = tk.Frame(self.root)

        # mutation type
        self.label_mutation = tk.Label()
        self.is_mutation_type = [tk.IntVar(value=1) for _ in range(3)]
        self.checklist_mutation = tk.Frame(self.root)

        # generate solution button
        self.main_label = tk.Label()
        self.button = tk.Button()
        self.has_iter_limit = tk.IntVar(value=1)
        self.checkbox = tk.Checkbutton()

        # graphs
        self.fig_cost = Figure()
        self.canvas_cost = FigureCanvasTkAgg()
        self.fig_population = Figure()
        self.canvas_population = FigureCanvasTkAgg()
        self.fig_time = Figure()
        self.canvas_time = FigureCanvasTkAgg()

        # print results
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)  # close window handling
        self.starting_screen()
        self.root.mainloop()

    # screen management
    def place_everything(self):
        """
        Places every element of the GUI
        :return:
        """
        self.update_window_params()
        self.create_full_menu()
        self.root.config(menu=self.menu_bar)
        self.update_text_elements()
        self.place_all_selectors()
        self.update_graphs()

    def clear_everything(self):
        """
        DEBUG FUNCTION. Remove every single element of GUI.
        :return:
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def starting_screen(self):
        self.update_window_params()
        self.main_label = tk.Label(text="PROBLEM TRANSPORTOWY\nALGORYTM GENETYCZNY\nBADANIA OPERACYJNE 2",
                                   font=(self.font, self.font_size1))
        self.main_label.pack()
        self.button = tk.Button(self.root, text="START", command=self.place_everything)
        self.button.place(relx=0.45, rely=0.15)

    def close_window(self):
        """
        Handle closing via top right corner X
        :return: None
        """
        if messagebox.askyesno(title="Zamknij",
                               message="Czy na pewno chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            self.root.destroy()

    # general updates
    def update_window_params(self):
        """
        Update window parameters
        :return:
        """
        self.root.title("Problem transportowy PSFŚ")
        self.root.geometry("1000x750")
        self.root.iconbitmap("../GEIcon.ico")
        self.root.configure(bg='lightblue')

    def update_text_elements(self):
        """
        Update all text elements of gui with current font and fontsize
        :return:
        """
        # label
        self.main_label.pack_forget()
        self.main_label = tk.Label(self.root, text="Algorytm Genetyczny", font=(self.font, self.font_size1))
        self.main_label.pack()

        # textbox
        self.textbox.place_forget()
        self.textbox = tk.Text(self.root,height=1,width=5,font=(self.font, self.font_size1))
        self.textbox.place(relx=0.5, rely=0.5)

        # crossing checklist
        self.label_crossing.grid_forget()
        self.label_crossing = tk.Label(self.checklist_crossing, text="Typy krzyżowania",
                                       font=(self.font, self.font_size2))
        self.label_crossing.grid(row=0, column=0, sticky=tk.W + tk.E)

        # selection checklist
        self.label_selection.grid_forget()
        self.label_selection = tk.Label(self.checklist_selection, text="Typy selekcji",
                                        font=(self.font, self.font_size2))
        self.label_selection.grid(row=0, column=0, sticky=tk.W + tk.E)

        # mutation checklist
        self.label_mutation.grid_forget()
        self.label_mutation = tk.Label(self.checklist_mutation, text="Typ mutacji",
                                       font=(self.font, self.font_size2))
        self.label_mutation.grid(row=0, column=0, sticky=tk.W + tk.E)

        # button
        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution)
        self.button.place(**GENERATE_SOLUTION_POS)

        # checkbox
        self.checkbox.place_forget()
        self.checkbox = tk.Checkbutton(self.root, text="Limit iteracji", font=(self.font, self.font_size2),
                                       variable=self.has_iter_limit)
        self.checkbox.place(**CHECKBOX_POS)

    def update_cost_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as cost graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_graph() if fig is None else fig

        self.canvas_cost = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas_cost.get_tk_widget().place(**COST_GRAPH_POS)

    def update_population_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as population graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_graph() if fig is None else fig

        self.canvas_population = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas_population.get_tk_widget().place(**POPULATION_GRAPH_POS)

    def update_time_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as time graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_graph() if fig is None else fig

        self.canvas_time = FigureCanvasTkAgg(fig, master=self.root)
        # self.canvas_time.get_tk_widget().place(relx= 0.1, rely=0.1)
        self.canvas_time.get_tk_widget().place(**TIME_GRAPH_POS)

        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(self.canvas_time, self.root)
        # toolbar.update()

    def create_test_graph(self, x=None, y=None) -> Figure:
        """
        DEBUG USE ONLY. Create an example graph
        :param x: x axis data as an iter
        :param y: y axis data as an iter. Must be same length as x
        :return: example graph as a plt Figure
        """
        x = [i for i in range(20)] if x is None else x
        y = [(i ** 2 - 15 * i) for i in x] if y is None else y

        fig = Figure(figsize=(3, 3), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.plot(x, y)

        return fig

    def update_graphs(self, fig_cost: Figure = None, fig_population: Figure = None, fig_time: Figure = None) -> None:
        """
        Update graphs in GUI with given figures
        :param fig_cost: new cost graph
        :param fig_population: new population graph
        :param fig_time: new time graph
        :return: None
        """
        self.update_cost_graph(fig_cost)
        self.update_time_graph(fig_time)
        self.update_population_graph(fig_population)

    # menu handling
    def create_full_menu(self):
        """
        Create the full menu
        :return:
        """
        # TODO: assess if function is redundant (= if menu will not be expanded)
        self.create_file_menu()
        self.create_view_menu()

    def create_file_menu(self):
        """
        Create the file menu in the upper taskbar
        :return: None
        """
        # load from file
        self.file_menu.add_command(label="Wczytaj miasta", command=self.load_graph)
        self.file_menu.add_command(label="Wczytaj populację", command=self.load_population)
        self.file_menu.add_command(label="Wczytaj konfigurację", command=self.load_config)
        self.file_menu.add_separator()

        # randomize
        self.file_menu.add_command(label="Wylosuj miasta", command=self.generate_graph)
        self.file_menu.add_command(label="Wylosuj populację", command=self.generate_population)
        self.file_menu.add_separator()

        # save loaded
        self.file_menu.add_command(label="Zapisz miasta", command=self.save_graph)
        self.file_menu.add_command(label="Zapisz populację", command=self.save_population)
        self.file_menu.add_command(label="Zapisz konfigurację", command=self.save_config)
        # self.view_menu.add_separator()

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

        self.view_menu.add_command(label="Przywróć rozmiar tekstu", command=self.reset_font_size)
        self.view_menu.add_command(label="TEST1", command=self.clear_everything)
        self.view_menu.add_command(label="TEST2", command=self.select_mutation_type)

        self.menu_bar.add_cascade(menu=self.view_menu, label="Widok")

    # algorithm parameters selection
    def place_all_selectors(self) -> None:
        """
        Places all selectors inside the GUI
        :return: None
        """
        self.create_mutation_selector()
        self.create_selection_selector()
        self.create_crossing_selector()

    def create_crossing_selector(self):
        """
        create the checklist with single answer
        :return:
        """
        self.checklist_crossing.columnconfigure(0, weight=1)

        self.label_crossing = tk.Label(self.checklist_crossing, text="Typ krzyżowania",
                                       font=(self.font, self.font_size2))
        self.label_crossing.grid(row=0, column=0, sticky=tk.W + tk.E)
        check1 = tk.Radiobutton(self.checklist_crossing, text="typ 1", variable=self.crossing_type, value=1,
                                font=(self.font, self.font_size2))
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Radiobutton(self.checklist_crossing, text="typ 2", variable=self.crossing_type, value=2,
                                font=(self.font, self.font_size2))
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Radiobutton(self.checklist_crossing, text="typ 3", variable=self.crossing_type, value=3,
                                font=(self.font, self.font_size2))
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.checklist_crossing.place(**CROSSING_SELECT_POS)

    def create_selection_selector(self):
        self.checklist_selection.columnconfigure(0, weight=1)

        self.label_selection = tk.Label(self.checklist_selection, text="Typ selekcji",
                                        font=(self.font, self.font_size2))
        self.label_selection.grid(row=0, column=0, sticky=tk.W + tk.E)

        check1 = tk.Radiobutton(self.checklist_selection, text="typ 1", variable=self.selection_type, value=1,
                                font=(self.font, self.font_size2))
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Radiobutton(self.checklist_selection, text="typ 2", variable=self.selection_type, value=2,
                                font=(self.font, self.font_size2))
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Radiobutton(self.checklist_selection, text="typ 3", variable=self.selection_type, value=3,
                                font=(self.font, self.font_size2))
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.checklist_selection.place(**SELECTION_SELECT_POS)

    def create_mutation_selector(self):
        self.checklist_crossing.columnconfigure(0, weight=1)

        self.label_mutation = tk.Label(self.checklist_mutation, text="Typ mutacji",
                                       font=(self.font, self.font_size2))
        self.label_mutation.grid(row=0, column=0, sticky=tk.W + tk.E)

        check1 = tk.Checkbutton(self.checklist_mutation, text="typ 1", font=(self.font, self.font_size2),
                                variable=self.is_mutation_type[0])
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Checkbutton(self.checklist_mutation, text="typ 2", font=(self.font, self.font_size2),
                                variable=self.is_mutation_type[1])
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Checkbutton(self.checklist_mutation, text="typ 3", font=(self.font, self.font_size2),
                                variable=self.is_mutation_type[2])
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.checklist_mutation.place(**MUTATION_SELECT_POS)

    def select_mutation_type(self):
        """
        TEST METHOD ONLY
        Select the type of mutation
        :return:
        """
        mutation_type = self.crossing_type.get()

        # TODO: implement me
        if mutation_type == 1:
            print(1)
        elif mutation_type == 2:
            print(2)
        elif mutation_type == 3:
            print(3)

    # text operations
    def reset_font_size(self):
        """
        Reset the font size back to default
        :return:
        """
        self.font = FONT
        self.font_size1 = FONT_SIZE
        self.font_size2_memory = FONT_SIZE * 0.75
        self.font_size2 = ceil(self.font_size2_memory)
        self.update_text_elements()

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

    # file handling
    def load_graph(self):
        """
        Handle loading graph from  .csv
        :return:
        """
        if messagebox.askyesno(title="Załaduj miasta",
                               message="Czy na pewno chcesz załadować graf z pliku?\nAktualnie wczytany zostanie nadpisany!"):
            # TODO: implement me!
            pass

    def load_population(self):
        """
        Handle loading initiaL population from  .csv
        :return:
        """
        if messagebox.askyesno(title="Załaduj populację",
                               message="Czy na pewno chcesz załadować populację z pliku?\nAktualnie wczytana zostanie nadpisana!"):
            # TODO: implement me!
            pass

    def generate_graph(self):
        """
        Handle generating random graph from generate_graph.create_complete_graph
        :return:
        """
        if messagebox.askyesno(title="Wylosuj miasta",
                               message="Czy na pewno chcesz wylosować graf?\nAktualnie wczytany zostanie nadpisany!"):
            # TODO: implement me!
            pass

    def generate_population(self):
        """
        Handle generating random population
        :return:
        """
        if messagebox.askyesno(title="Wylosuj populację",
                               message="Czy na pewno chcesz wylosować populację?\nAktualnie wczytana zostanie nadpisana!"):
            # TODO: implement me!
            pass

    def save_graph(self):
        """
        Save currently loaded graph to .csv
        :return:
        """
        if messagebox.askyesno(title="Zapisz graf", message="Czy na pewno chcesz zapisać graf do pliku"):
            # TODO: implement me!
            pass

    def save_population(self):
        """
        save currently loaded population to .csv
        :return:
        """
        if messagebox.askyesno(title="Zapisz populację",
                               message="Czy na pewno chcesz zapisać aktualną populację do pliku"):
            # TODO: implement me!
            pass

    def save_config(self):
        """
        Save view settings config to .json
        :return:
        """
        if messagebox.askyesno(title="Zapisz ustawienia",
                               message="Czy na pewno chcesz zapisać aktualne ustawienia do pliku"):
            # TODO: implement me!
            pass

    def load_config(self):
        """
        Load view settings config from .json
        :return:
        """
        if messagebox.askyesno(title="Załaduj",
                               message="Czy na pewno chcesz załadować konfigurację z pliku?\nAktualne ustawienia zostaną nadpisane!"):
            # TODO: implement me!
            pass


if __name__ == '__main__':
    GUI()
