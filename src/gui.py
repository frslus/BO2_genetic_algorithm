import tkinter as tk
from json import dumps, dump, load
from math import ceil
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

import file_handling
import problem_description

# text constants
FONT_SIZE = 18
FONT = "Helvetica"

#starting screen
STARTSCREEN_BG_POS = {"relx": 0.1, "rely": 0.02, "relheight": 0.5, "relwidth": 0.8}
STARTSCREEN_LABEL_POS = {"relx": 0.2, "rely": 0.05, "relheight": 0.4, "relwidth": 0.6}
STARTSCREEN_BUTTON_POS = {"relx": 0.25, "rely": 0.6,"relwidth": 0.5, "relheight": 0.3}

#backgrounds
BG_COLORS = ["lightgrey", "lightgreen", "lightgrey"]
GRAPH_BG_POS = {"relx": 0, "rely": 0.055, "relheight": 0.87, "relwidth": 0.76}
SELECTOR_BG_POS = {"relx": 0.76, "rely": 0, "relheight": 1, "relwidth": 0.3}
VIEW_BUTTONS_BG_POS = {"relx": 0.02, "rely": 0, "relheight": 0, "relwidth": 0}

# graphs positions
COST_GRAPH_POS = {"relx": 0.01, "rely": 0.065, "relheight": 0.6, "relwidth": 0.74}
POPULATION_GRAPH_POS = {"relx": 0.02, "rely": 0.68, "relheight": 0.23, "relwidth": 0.35}
TIME_GRAPH_POS = {"relx": 0.4, "rely": 0.68, "relheight": 0.23, "relwidth": 0.35}

# citygraph positions
CITY_GRAPH_POS = {"relx": 0.01, "rely": 0.065, "relheight": 0.75, "relwidth": 0.74}
LEFTARROW_POS = {"relx": 0.1, "rely": 0.1} # TODO: implement me
RIGHTARROW_POS = {"relx": 0.2, "rely": 0.2} # TODO: implement me

# graph buttons
GRAPHBUTTON_LABELS = ["Wykresy", "Graf"]
CITY_BUTTON_POS = {"relx": 0.07, "rely": 0.935}
SOL_BUTTON_POS = {"relx": 0.15, "rely": 0.935}

# algorithm parameter labels
TEXTBOX_LABELS = ["Wielkość populacji", "Ilość rodziców[%]", "Szansa mutacji [%]", "Limit pokoleń (bez poprawy)",
                  "Limit pokoleń (ogólny)"]
# TEXTBOX_VALUES = [100, 25, 5, 100, 9999]
CHECKBOX_LABELS = ["crossing", "selection", "mutation"]
FIGURE_LAYERS = ["cost", "population", "time", "city_graph"]

# algorithm parameter selection positions
NUMBER_PARAMS_POS = {"relx": 0.77, "rely": 0.05, "relheight": 0.21, "relwidth": 0.22}
CROSSING_SELECT_POS = {"relx": 0.8, "rely": 0.27, "relheight": 0.19, "relwidth": 0.16}
SELECTION_SELECT_POS = {"relx": 0.8, "rely": 0.47, "relheight": 0.19, "relwidth": 0.16}
MUTATION_SELECT_POS = {"relx": 0.8, "rely": 0.67, "relheight": 0.27, "relwidth": 0.16}

#generate solution button
MAIN_LABEL_POS = {"relx": 0.15, "rely": 0.01, "relheight": 0.04, "relwidth": 0.5}
GENERATE_SOLUTION_POS = {"relx": 0.53, "rely": 0.935}

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

        # config and data
        self.config = {}
        self.TPO = problem_description.TransportProblemObject()
        # TODO: add self.TPO = TransportProblemObject()
        # TODO: add self.population = Population()
        # TODO: add self.best = Organism()
        # TODO: add self.extra_data: dict = {} with all post algorithm information

        # init window
        self.root = tk.Tk()

        # menubar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)

        #background
        self.rectangles = [tk.Canvas(self.root, bg=color) for color in BG_COLORS]

        # text fields
        textbox_count = len(TEXTBOX_LABELS)
        self.textboxes = [tk.Text() for _ in range(textbox_count)]
        self.textbox_labels = [tk.Label() for _ in range(textbox_count)]
        self.textbox_grid = tk.Frame(self.root)

        # checkboxes
        self.checklabels = {name: tk.Label() for name in CHECKBOX_LABELS}
        self.checktype = {name: tk.IntVar(value=1) for name in CHECKBOX_LABELS}
        self.checktype['mutation'] = [tk.IntVar(value=1) for _ in range(5)]
        self.checklists = {name: tk.Frame(self.root) for name in CHECKBOX_LABELS}

        # generate solution button
        self.main_label = tk.Label()
        self.button = tk.Button()

        # graphs
        # self.figures = {name: Figure() for name in FIGURE_LAYERS}
        self.canvas = {name: FigureCanvasTkAgg() for name in FIGURE_LAYERS}
        self.graphbuttons = [tk.Button() for _ in GRAPHBUTTON_LABELS]

        # print results
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)  # close window handling
        self.starting_screen()
        self.root.mainloop()

    #background management
    def place_backgrounds(self) -> None:
        """
        Place backgrounds on the homescreen according to constants
        :return: None
        """
        self.rectangles[0].place(**SELECTOR_BG_POS)
        self.rectangles[1].place(**GRAPH_BG_POS)


    # screen management
    def place_everything(self):
        """
        Places every element of the GUI
        :return:
        """
        self.update_window_params()
        self.create_full_menu()
        self.place_backgrounds()
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

    def starting_screen(self) -> None:
        """
        Boot up starting screen
        :return: None
        """
        self.update_window_params()
        self.rectangles[0].place(**STARTSCREEN_BG_POS)
        self.main_label = tk.Label(text="PROBLEM TRANSPORTOWY\nALGORYTM GENETYCZNY\nBADANIA OPERACYJNE 2",
                                   font=(self.font, self.font_size1))
        self.main_label.place(**STARTSCREEN_LABEL_POS)
        self.button = tk.Button(self.root, text="START", command=self.place_everything)
        self.button.place(**STARTSCREEN_BUTTON_POS)

    def close_window(self):
        """
        Handle closing via top right corner X
        :return: None
        """
        if messagebox.askyesno(title="Zamknij",
                               message="Czy na pewno chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            # TODO: if algorithm is working, we have to close it here
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
        self.main_label.place_forget()
        self.main_label = tk.Label(self.root, text="Algorytm Genetyczny", font=(self.font, self.font_size1))
        self.main_label.place(**MAIN_LABEL_POS)

        # textbox
        for i in range(5):
            textbox = self.textboxes[i]
            textbox.place_forget()
            textbox = tk.Text(self.textbox_grid, height=1, width=5, font=(self.font, self.font_size1))
            textbox.grid(row=i, column=1, sticky=tk.W + tk.E)
            self.textboxes[i] = textbox

            textbox_label = self.textbox_labels[i]
            textbox_label.place_forget()
            textbox_label = tk.Label(self.textbox_grid, text=TEXTBOX_LABELS[i])
            textbox_label.grid(row=i, column=0, sticky=tk.W + tk.E)
            self.textbox_labels[i] = textbox_label

        self.textbox_grid.place(**NUMBER_PARAMS_POS)

        # crossing checklist
        self.checklabels['crossing'].grid_forget()
        self.checklabels['crossing'] = tk.Label(self.checklists['crossing'], text="Typ krzyżowania",
                                                font=(self.font, self.font_size2))
        self.checklabels['crossing'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # selection checklist
        self.checklabels['selection'].grid_forget()
        self.checklabels['selection'] = tk.Label(self.checklists['selection'], text="Typ selekcji",
                                                 font=(self.font, self.font_size2))
        self.checklabels['selection'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # mutation checklist
        self.checklabels['mutation'].grid_forget()
        self.checklabels['mutation'] = tk.Label(self.checklists['mutation'], text="Typy mutacji",
                                                font=(self.font, self.font_size2))
        self.checklabels['mutation'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # solution button
        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution)
        self.button.place(**GENERATE_SOLUTION_POS)

        # graph button
        self.graphbuttons[0].place_forget()
        self.graphbuttons[1].place_forget()
        self.graphbuttons[0] = tk.Button(self.root, text=GRAPHBUTTON_LABELS[0], font=(self.font, self.font_size2),
                                         command=self.show_graphs)
        self.graphbuttons[1] = tk.Button(self.root, text=GRAPHBUTTON_LABELS[1], font=(self.font, self.font_size2),
                                         command=self.show_city_graph)
        self.graphbuttons[0].place(**SOL_BUTTON_POS)
        self.graphbuttons[1].place(**CITY_BUTTON_POS)


    # TODO: add function creating figure
    def update_cost_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as cost graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if fig is None else fig

        self.canvas['cost'].get_tk_widget().place_forget()
        self.canvas['cost'] = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas['cost'].get_tk_widget().place(**COST_GRAPH_POS)

    def update_population_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as population graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if fig is None else fig

        self.canvas['population'].get_tk_widget().place_forget()
        self.canvas['population'] = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas['population'].get_tk_widget().place(**POPULATION_GRAPH_POS)

    def update_time_graph(self, fig: Figure = None) -> None:
        """
        Plot given figure object as time graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if fig is None else fig

        self.canvas['time'].get_tk_widget().place_forget()
        self.canvas['time'] = FigureCanvasTkAgg(fig, master=self.root)
        # self.canvas_time.get_tk_widget().place(relx= 0.1, rely=0.1)
        self.canvas['time'].get_tk_widget().place(**TIME_GRAPH_POS)

        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(self.canvas_time, self.root)
        # toolbar.update()

    def create_test_figure(self, x=None, y=None) -> Figure:
        """
        DEBUG USE ONLY. Create an example graph
        :param x: x axis data as an iter
        :param y: y axis data as an iter. Must be same length as x
        :return: example graph as a plt Figure
        """
        x = [i for i in range(20)] if x is None else x
        y = [(i ** 2 - 15 * i) for i in x] if y is None else y

        fig = Figure(figsize=(10, 10), dpi=100)
        plot1 = fig.add_subplot(111)
        plot1.plot(x, y)

        return fig

    def draw_graphs(self) -> tuple[Figure, Figure, Figure]:
        """
        Draw figures from self.extra data
        :return: Cost figure, Population figure, Time figure
        """
        # self.extra data required
        # TODO: Implement me!
        pass

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

    def clear_graphs(self) -> None:
        """
        clear algorithm iteration graphs
        :return: None
        """
        for _, graph in self.canvas.items():
            graph.get_tk_widget().place_forget()

    def update_city_graph(self, fig: Figure = None) -> None:
        """
        Update the city graph (graph representation of cities with connections) in GUI with given figures
        :param fig: matplotlib figure containing city graph
        :return: None
        """
        fig = self.create_test_figure() if fig is None else fig

        self.canvas["city_graph"].get_tk_widget().place_forget()
        self.canvas["city_graph"] = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas["city_graph"].get_tk_widget().place(**CITY_GRAPH_POS)

    def clear_city_graph(self) -> None:
        """
        Clear city graph from GUI
        :return: None
        """
        self.canvas["city_graph"].get_tk_widget().place_forget()

    def show_city_graph(self) -> None:
        """
        Choose city graph as the one shown in the GUI
        :return:
        """
        self.clear_graphs()
        self.update_city_graph()

    def show_graphs(self) -> None:
        """
        Choose solution graphs as the one shown in the GUI
        :return:
        """
        self.clear_city_graph()
        self.update_graphs()

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
        self.view_menu.add_command(label="TEST1", command=self.update_config)
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
        self.checklists['crossing'].columnconfigure(0, weight=1)

        self.checklabels['crossing'] = tk.Label(self.checklists['crossing'], text="Typ krzyżowania",
                                                font=(self.font, self.font_size2))
        self.checklabels['crossing'].grid(row=0, column=0, sticky=tk.W + tk.E)

        crossing_type = self.checktype['crossing']
        check1 = tk.Radiobutton(self.checklists['crossing'], text="1 Cięcie", variable=crossing_type, value=1,
                                font=(self.font, self.font_size2))
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Radiobutton(self.checklists['crossing'], text="losowe cięcia", variable=crossing_type, value=2,
                                font=(self.font, self.font_size2))
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Radiobutton(self.checklists['crossing'], text="Losowa selekcja", variable=crossing_type, value=3,
                                font=(self.font, self.font_size2))
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.checklists['crossing'].place(**CROSSING_SELECT_POS)

    def create_selection_selector(self):
        self.checklists['selection'].columnconfigure(0, weight=1)

        self.checklabels['selection'] = tk.Label(self.checklists['selection'], text="Typ selekcji",
                                                 font=(self.font, self.font_size2))
        self.checklabels['selection'].grid(row=0, column=0, sticky=tk.W + tk.E)

        selection_type = self.checktype['selection']
        check1 = tk.Radiobutton(self.checklists['selection'], text="Turniejowa", variable=selection_type, value=1,
                                font=(self.font, self.font_size2))
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Radiobutton(self.checklists['selection'], text="Rankingowa", variable=selection_type, value=2,
                                font=(self.font, self.font_size2))
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Radiobutton(self.checklists['selection'], text="Ruletka", variable=selection_type, value=3,
                                font=(self.font, self.font_size2))
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)

        self.checklists['selection'].place(**SELECTION_SELECT_POS)

    def create_mutation_selector(self):
        self.checklists['crossing'].columnconfigure(0, weight=1)

        self.checklabels['mutation'] = tk.Label(self.checklists['mutation'], text="Typy mutacji",
                                                font=(self.font, self.font_size2))
        self.checklabels['mutation'].grid(row=0, column=0, sticky=tk.W + tk.E)

        mutation_type = self.checktype['mutation']
        check1 = tk.Checkbutton(self.checklists['mutation'], text="Miasta", font=(self.font, self.font_size2),
                                variable=mutation_type[0])
        check1.grid(row=1, column=0, sticky=tk.W + tk.E)
        check2 = tk.Checkbutton(self.checklists['mutation'], text="Terminy", font=(self.font, self.font_size2),
                                variable=mutation_type[1])
        check2.grid(row=2, column=0, sticky=tk.W + tk.E)
        check3 = tk.Checkbutton(self.checklists['mutation'], text="Ś. Transportu", font=(self.font, self.font_size2),
                                variable=mutation_type[2])
        check3.grid(row=3, column=0, sticky=tk.W + tk.E)
        check4 = tk.Checkbutton(self.checklists['mutation'], text="Dodatek genu", font=(self.font, self.font_size2),
                                variable=mutation_type[3])
        check4.grid(row=4, column=0, sticky=tk.W + tk.E)
        check5 = tk.Checkbutton(self.checklists['mutation'], text="Usunięcie genu", font=(self.font, self.font_size2),
                                variable=mutation_type[4])
        check5.grid(row=5, column=0, sticky=tk.W + tk.E)

        self.checklists['mutation'].place(**MUTATION_SELECT_POS)

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

    def update_config(self) -> None:
        """
        update self.config with data pulled from gui
        :return: None
        """
        config = self.config

        # #textbox data
        config["population_size"] = int(self.textboxes[0].get('1.0', tk.END).strip())
        config["parent_percent"] = float(self.textboxes[1].get('1.0', tk.END).strip()) / 100
        config["mutation_chance"] = float(self.textboxes[2].get('1.0', tk.END).strip()) / 100
        config["stagnation_iterations"] = int(self.textboxes[3].get('1.0', tk.END).strip())
        config["total_iterations"] = int(self.textboxes[4].get('1.0', tk.END).strip())

        # selection checkbox
        selection_type = self.checktype['selection'].get()
        config["selection_type"] = "tournament" if selection_type == 1 else (
            "ranking" if selection_type == 2 else "roulette")

        # crossing checkbox
        crossing_type = self.checktype['crossing'].get()
        config["crossing_types"] = "one_cut" if crossing_type == 1 else (
            "random_cuts" if crossing_type == 2 else "random_selection")

        # mutation checkbox
        mutations = self.checktype['mutation']
        mutations_list = []
        if mutations[0].get():
            mutations_list.append("city")
        if mutations[1].get():
            mutations_list.append("date")
        if mutations[2].get():
            mutations_list.append("transit_mode")
        if mutations[3].get():
            mutations_list.append("new_gene")
        if mutations[4].get():
            mutations_list.append("delete_gene")
        config["mutation_types"] = mutations_list

        print(self.config)
        return

    def generate_solution(self):
        """
        Generate a random solution with loaded problem and initial population (.py).
        :return:
        """
        self.update_config()

        # TODO: implement me!
        # TODO: here we have to start a thread for genetic algorithm
        print(9999)

    # file handling
    def load_graph(self, filename: str = "graph.csv"):
        """
        Handle loading graph from  .csv
        :return:
        """
        if not messagebox.askyesno(title="Załaduj miasta",
                                   message="Czy na pewno chcesz załadować graf z pliku?\nAktualnie wczytany zostanie nadpisany!"):
            return

        path = tk.filedialog.askopenfile(mode='r', title="Wybierz graf miast",
                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        try:
            self.TPO.__cities_graph = file_handling.load_graph_from_file(path.name)
        except(AttributeError):
            return

    def load_population(self):
        """
        Handle loading initiaL population from  .csv
        :return:
        """
        if not messagebox.askyesno(title="Załaduj populację",
                               message="Czy na pewno chcesz załadować populację z pliku?\nAktualnie wczytana zostanie nadpisana!"):
            return

        path = tk.filedialog.askopenfile(mode='r', title="Wybierz populację",
                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        try:
            self.TPO.__packages_list = file_handling.load_list_from_file(path.name)
        except(AttributeError):
            return

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
        if not messagebox.askyesno(title="Zapisz graf", message="Czy na pewno chcesz zapisać graf do pliku"):
            return

        path = tk.filedialog.asksaveasfile(initialfile='graph.csv', defaultextension=".csv",
                                           filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv")])
        try:
            file_handling.save_graph_to_file(self.TPO.__cities_graph,path.name)
        except(AttributeError):
            return

        return

    def save_population(self):
        """
        save currently loaded population to .csv
        :return:
        """
        if not messagebox.askyesno(title="Zapisz populację",
                               message="Czy na pewno chcesz zapisać aktualną populację do pliku"):
            return

        path = tk.filedialog.asksaveasfile(initialfile='population.csv', defaultextension=".csv",
                                           filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv")])
        try:
            file_handling.save_list_to_file(self.TPO.__packages_list, path.name)
        except(AttributeError):
            return


    def save_config(self) -> None:
        """
        Save view settings config to .json
        :return: None
        """
        if not messagebox.askyesno(title="Zapisz ustawienia",
                                   message="Czy na pewno chcesz zapisać aktualne ustawienia do pliku"):
            return
        path = tk.filedialog.asksaveasfile(initialfile='config.json',defaultextension=".json", filetypes=[("All Files", "*.*"), ("Json Files", "*.json")])

        config = dumps(self.config)
        try:
            with open(path.name, mode="w") as file:
                dump(config, file)
        except(AttributeError):
            return

        # config = dumps(self.config)
        #
        # # save to data/filename.json
        # path = f"../data/{filename}.json"
        # with open(path, mode="w") as file:
        #     dump(config, file)

    def load_config(self) -> None:
        """
        Load view settings config from .json
        :return: None
        """
        if not messagebox.askyesno(title="Załaduj",
                                   message="Czy na pewno chcesz załadować konfigurację z pliku?\nAktualne ustawienia zostaną nadpisane!"):
            return

        path = tk.filedialog.askopenfile(mode='r',title="Wybierz konfigurację", filetypes=[("json files", "*.json"), ("All files", "*.*")])

        try:
            with open(path.name, mode="r", newline="", encoding="utf-8") as file:
                self.config = load(file)
        except(AttributeError):
            return

        return
        #
        # path = f"../data/{filename}.json"
        # with open(path, mode="r", newline="", encoding="utf-8") as file:
        #     self.config = load(file)


    # def update_from_config(self) -> None:
    #     """
    #     Update checkboxes in gui from current self.config
    #     :return:
    #     """
    #     for key in CHECKBOX_LABELS:
    #         self.checktype[key].set(self.config[key])


if __name__ == '__main__':
    GUI()
