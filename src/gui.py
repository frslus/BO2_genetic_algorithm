# libraries
import tkinter as tk
from json import dumps, dump, load, loads
from tkinter import messagebox
from ast import literal_eval

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure

# project files
import file_handling
import generate_graphs
import organisms_and_population
import problem_description
from genetic_algorithm import *
from gui_config import *


class GUI:
    """
    Represent the main GUI window
    """

    def __init__(self):
        """
        Initialize all atributes related to GUI
        """
        # init text
        self.font = FONT
        self.font_size1 = FONT_SIZE
        self.font_size2_memory = FONT_SIZE * 0.75
        self.font_size2 = ceil(self.font_size2_memory)

        # algo input
        self.config = {}
        self.TPO = problem_description.TransportProblemObject()
        self.population = organisms_and_population.Population([])

        # algo output
        self.extra_data = {}
        self.extra_data_lock = threading.Lock()
        self.best = None

        # init window
        self.root = tk.Tk()

        # menubar
        self.menu_bar = tk.Menu(self.root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)

        # background
        self.rectangles = [tk.Canvas(self.root, bg=color) for color in BG_COLORS]

        # text fields
        textbox_count = len(TEXTBOX_LABELS)
        self.textvars = [tk.StringVar() for _ in range(textbox_count)]
        self.textboxes = [tk.Entry() for _ in range(textbox_count)]
        self.textbox_labels = [tk.Label() for _ in range(textbox_count)]
        self.textbox_grid = tk.Frame(self.root)

        # checkboxes
        self.checklabels = {name: tk.Label() for name in CHECKBOX_LABELS}
        self.checktype = {name: tk.IntVar(value=1) for name in CHECKBOX_LABELS}
        self.checktype['mutation'] = [tk.IntVar(value=1) for _ in range(5)]
        self.checklists = {name: tk.Frame(self.root) for name in CHECKBOX_LABELS}

        # generate solution
        self.main_label = tk.Label()
        self.button = tk.Button()
        self.stopbutton = tk.Button()
        self.is_running = False

        # backend connections
        self.genetic_thread = None
        self.control_thread = None
        self.fig_cost = None
        self.fig_time = None
        self.fig_population = None

        # graphs
        self.canvas = {name: FigureCanvasTkAgg() for name in FIGURE_LAYERS}
        self.graphbuttons = [tk.Button() for _ in GRAPHBUTTON_LABELS]
        self.leftarrow = tk.Button(self.root, text="<--", font=(self.font, self.font_size2),
                                   command=self.show_prev_package)
        self.rightarrow = tk.Button(self.root, text="-->", font=(self.font, self.font_size2),
                                    command=self.show_next_package)
        self.cur_package_id = 0

        # print results
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)  # close window handling
        self.starting_screen()
        self.root.mainloop()

    # fundamental screen management
    def place_backgrounds(self) -> None:
        """
        Place backgrounds on the homescreen according to constants
        :return: None
        """
        self.rectangles[0].place(**SELECTOR_BG_POS)
        self.rectangles[1].place(**GRAPH_BG_POS)

    def place_everything(self) -> None:
        """
        Places every element of the GUI
        :return: None
        """
        self.update_window_params()
        self.create_full_menu()
        self.place_backgrounds()
        self.root.config(menu=self.menu_bar)
        self.update_text_elements()
        self.place_all_selectors()
        self.update_graphs()

    def clear_everything(self) -> None:
        """
        DEBUG FUNCTION. Remove every single element of GUI.
        :return: None
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
        self.button = tk.Button(self.root, text="START", command=self.place_everything, cursor="sizing")
        self.button.place(**STARTSCREEN_BUTTON_POS)

    def close_window(self) -> None:
        """
        Handle closing via top right corner X
        :return: None
        """
        if messagebox.askyesno(title="Zamknij",
                               message="Czy na pewno chcesz wyjść z aplikacji?\nZmiany mogą być niezapisane!"):
            # TODO: if algorithm is working, we have to close it here
            self.root.destroy()

    # text operations
    def reset_font_size(self) -> None:
        """
        Reset the font size back to default
        :return: None
        """
        self.font = FONT
        self.font_size1 = FONT_SIZE
        self.font_size2_memory = FONT_SIZE * 0.75
        self.font_size2 = ceil(self.font_size2_memory)
        self.update_text_elements()

    def increase_font(self) -> None:
        """
        Increase font size and update menu
        :return: None
        """
        self.font_size1 += 2
        self.font_size2_memory += 1.5
        self.font_size2 = ceil(self.font_size2_memory)

        self.update_text_elements()

    def decrease_font(self) -> None:
        """
        Decrease font size and update menu
        :return: None
        """
        self.font_size1 -= 2 if self.font_size2 > 2 else 0
        self.font_size2_memory -= 1.5 if self.font_size2_memory > 1.5 else 0
        self.font_size2 = ceil(self.font_size2_memory)

        self.update_text_elements()

    # general updates
    def update_window_params(self) -> None:
        """
        Update window parameters
        :return: None
        """
        self.root.title("Problem transportowy PSFŚ")
        self.root.geometry("1000x750")
        self.root.iconbitmap("../GEIcon.ico")
        self.root.configure(bg='lightblue')

    def update_text_elements(self) -> None:
        """
        Update all text elements of gui with current font and fontsize
        :return: None
        """
        # label
        self.main_label.place_forget()
        self.main_label = tk.Label(self.root, text="Algorytm Genetyczny", font=(self.font, self.font_size1))
        self.main_label.place(**MAIN_LABEL_POS)

        # textbox
        for i in range(5):
            textbox = self.textboxes[i]
            textbox.grid_forget()
            # textbox = tk.Text(self.textbox_grid, height=1, width=5, font=(self.font, self.font_size1))
            textbox = tk.Entry(self.textbox_grid, textvariable=self.textvars[i], font=(self.font, self.font_size1))
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
                                command=self.generate_solution, cursor="sizing", bg="lightgreen")
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

    # menu handling
    def create_full_menu(self) -> None:
        """
        Create the full menu
        :return: None
        """
        self.create_file_menu()
        self.create_view_menu()

    def create_file_menu(self) -> None:
        """
        Create the file menu in the upper taskbar
        :return: None
        """
        # load from file
        self.file_menu.add_command(label="Wczytaj miasta", command=self.load_graph)
        self.file_menu.add_command(label="Wczytaj przesyłki", command=self.load_packages)
        self.file_menu.add_command(label="Wczytaj populację", command=self.load_population)
        self.file_menu.add_command(label="Wczytaj konfigurację", command=self.load_config)
        self.file_menu.add_separator()

        # randomize
        self.file_menu.add_command(label="Wylosuj miasta", command=self.generate_graph)
        self.file_menu.add_command(label="Wylosuj przesyłki", command=self.generate_packages)
        # self.file_menu.add_command(label="Wylosuj populację", command=self.generate_population)
        self.file_menu.add_command(label="Wylosuj przesyłki", command=self.generate_packages)
        self.file_menu.add_separator()

        # save loaded
        self.file_menu.add_command(label="Zapisz miasta", command=self.save_graph)
        self.file_menu.add_command(label="Zapisz przesyłki", command=self.save_packages)
        self.file_menu.add_command(label="Zapisz populację", command=self.save_population)
        self.file_menu.add_command(label="Zapisz konfigurację", command=self.save_config)

        self.menu_bar.add_cascade(menu=self.file_menu, label="Pliki")

    def create_view_menu(self) -> None:
        """
        Create the visual settings menu in the upper taskbar
        :return: None
        """
        # adjust config
        self.view_menu.add_command(label="Czcionka +", command=self.increase_font)
        self.view_menu.add_command(label="Czcionka -", command=self.decrease_font)
        self.view_menu.add_command(label="Wyrównaj okno", command=self.update_window_params)
        self.view_menu.add_separator()

        self.view_menu.add_command(label="Przywróć rozmiar tekstu", command=self.reset_font_size)
        # self.view_menu.add_command(label="TEST1", command=self.update_config)
        # self.view_menu.add_command(label="TEST2", command=self.select_mutation_type)

        self.menu_bar.add_cascade(menu=self.view_menu, label="Widok")

    # file handling
    def load_graph(self) -> None:
        """
        Handle loading graph from .csv
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Załaduj miasta",
                                   message="Czy na pewno chcesz załadować graf z pliku?\nAktualnie wczytany zostanie nadpisany!"):
            return

        # filewindow
        path = tk.filedialog.askopenfile(mode='r', title="Wybierz graf miast",
                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        try:
            self.TPO.reload_graph(path.name)
        except(AttributeError):
            return

    def load_packages(self) -> None:
        """
        handle loading package list from .csv
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Załaduj przesyłki",
                                   message="Czy na pewno chcesz załadować listę przesyłek z pliku?\nAktualnie wczytana zostanie nadpisana!"):
            return

        # filewindow
        path = tk.filedialog.askopenfile(mode='r', title="Wybierz listę przesyłek",
                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        try:
            self.TPO.reload_list(path.name)
        except(AttributeError):
            return

    def load_population(self) -> None:
        """
        Handle loading initiaL population from  .csv
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Załaduj populację",
                                   message="Czy na pewno chcesz załadować populację z pliku?\nAktualnie wczytana zostanie nadpisana!"):
            return

        # filewindow
        path = tk.filedialog.askopenfile(mode='r', title="Wybierz populację",
                                         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        try:
            self.population = organisms_and_population.load_population_from_file(path.name)
        except(AttributeError):
            return

    def load_config(self) -> None:
        """
        Load view settings config from .json
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Załaduj",
                                   message="Czy na pewno chcesz załadować konfigurację z pliku?\nAktualne ustawienia zostaną nadpisane!"):
            return

        # filewindow
        path = tk.filedialog.askopenfile(mode='r', title="Wybierz konfigurację",
                                         filetypes=[("json files", "*.json"), ("All files", "*.*")])

        # .json to dict
        try:
            with open(path.name, mode="r", newline="", encoding="utf-8") as file:
                self.config = load(file)
                print(type(self.config))
                #self.config["mutation_types"] = load(self.config["mutation_types"])
        except(AttributeError):
            return

        self.update_gui_config()
        return

    def generate_graph(self) -> None:
        """
        Handle generating random graph from generate_graph.create_complete_graph
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Wylosuj miasta",
                                   message="Czy na pewno chcesz wylosować graf?\nAktualnie wczytany zostanie nadpisany!"):
            return

        # genration
        self.TPO.reload_graph(generate_graphs.create_complete_graph())

    def generate_packages(self) -> None:
        """
        handle generating random package list from generate_graph.py
        :return" None
        """
        # popup
        if not messagebox.askyesno(title="Wylosuj przesylki",
                                   message="Czy na pewno chcesz wylosować listę przesyłek?\nAktualnie wczytana zostanie nadpisana!"):
            return

        # generation
        self.TPO.reload_list(generate_graphs.generate_package_list(self.TPO.__cities_graph))

    # def generate_population(self) -> None:
    #     """
    #     Handle generating random population
    #     :return: None
    #     """
    #     # popup
    #     if not messagebox.askyesno(title="Wylosuj populację",
    #                                message="Czy na pewno chcesz wylosować populację?\nAktualnie wczytana zostanie nadpisana!"):
    #         return
    #
    #     # TODO: implement me!
    #     # TODO: assess if function is redundant
    #     raise (NotImplementedError)

    def generate_packages(self) -> None:
        """
        Handle generating random packages
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Wylosuj przesyłki",
                                   message="Czy na pewno chcesz wylosować listę przesylek?\nAktualnie wczytana zostanie nadpisana!"):
            return

        # generation
        self.TPO.reload_list(generate_graphs.generate_package_list(self.TPO.graph))

    def save_graph(self) -> None:
        """
        Save currently loaded graph to .csv
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Zapisz graf", message="Czy na pewno chcesz zapisać graf do pliku"):
            return

        # filewindow
        path = tk.filedialog.asksaveasfile(initialfile='graph.csv', defaultextension=".csv",
                                           filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv")])
        try:
            file_handling.save_graph_to_file(self.TPO.__cities_graph, path.name)
        except(AttributeError):
            return

    def save_packages(self) -> None:
        """
        handle saving currently loaded package list
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Zapisz przesyłki",
                                   message="Czy na pewno chcesz zapisać listę przyesyłek do pliku"):
            return

        # filewindow
        path = tk.filedialog.asksaveasfile(initialfile='packages.csv', defaultextension=".csv",
                                           filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv")])
        try:
            file_handling.save_list_to_file(self.TPO.__packages_list, path.name)
        except(AttributeError):
            return

        return

    def save_population(self) -> None:
        """
        save currently loaded population to .csv
        :return: None
        """
        if not messagebox.askyesno(title="Zapisz populację",
                                   message="Czy na pewno chcesz zapisać aktualną populację do pliku"):
            return

        path = tk.filedialog.asksaveasfile(initialfile='population.csv', defaultextension=".csv",
                                           filetypes=[("All Files", "*.*"), ("CSV Files", "*.csv")])
        try:
            organisms_and_population.save_population_to_file(self.population, path.name)
        except(AttributeError):
            return

    def save_config(self) -> None:
        """
        Save view settings config to .json
        :return: None
        """
        # popup
        if not messagebox.askyesno(title="Zapisz ustawienia",
                                   message="Czy na pewno chcesz zapisać aktualne ustawienia do pliku"):
            return

        # filewindow
        path = tk.filedialog.asksaveasfile(initialfile='config.json', defaultextension=".json",
                                           filetypes=[("All Files", "*.*"), ("Json Files", "*.json")])

        # dict to .json
        self.update_config()
        config = dumps(self.config)
        try:
            with open(path.name, mode="w") as file:
                dump(config, file)
        except(AttributeError):
            return


    # algorithm parameters selection
    def place_all_selectors(self) -> None:
        """
        Places all selectors inside the GUI
        :return: None
        """
        self.create_mutation_selector()
        self.create_selection_selector()
        self.create_crossing_selector()

    def create_crossing_selector(self) -> None:
        """
        Create the crossing checklist with single answer
        :return: None
        """
        # init frame
        self.checklists['crossing'].columnconfigure(0, weight=1)
        self.checklabels['crossing'] = tk.Label(self.checklists['crossing'], text="Typ krzyżowania",
                                                font=(self.font, self.font_size2))
        self.checklabels['crossing'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # fill out with selectors
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

    def create_selection_selector(self) -> None:
        """
        Create the selection checklist with single answer
        :return: None
        """
        # init frame
        self.checklists['selection'].columnconfigure(0, weight=1)
        self.checklabels['selection'] = tk.Label(self.checklists['selection'], text="Typ selekcji",
                                                 font=(self.font, self.font_size2))
        self.checklabels['selection'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # fill out with selectors
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

    def create_mutation_selector(self) -> None:
        """
        Create the mutation multi-answered checklist
        :return: None
        """
        # init frame
        self.checklists['crossing'].columnconfigure(0, weight=1)
        self.checklabels['mutation'] = tk.Label(self.checklists['mutation'], text="Typy mutacji",
                                                font=(self.font, self.font_size2))
        self.checklabels['mutation'].grid(row=0, column=0, sticky=tk.W + tk.E)

        # fill out with selectors
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

    def update_config(self) -> None:
        """
        Update self.config with data pulled from gui
        :return: None
        """
        config = self.config

        # #textbox data
        config["population_size"] = int(self.textvars[0].get())
        config["parent_percent"] = float(self.textvars[1].get()) / 100
        config["mutation_chance"] = float(self.textvars[2].get()) / 100
        config["stagnation_iterations"] = int(self.textvars[3].get())
        config["total_iterations"] = int(self.textvars[4].get())
        # config["population_size"] = int(self.textboxes[0].get('1.0', tk.END).strip())
        # config["parent_percent"] = float(self.textboxes[1].get('1.0', tk.END).strip()) / 100
        # config["mutation_chance"] = float(self.textboxes[2].get('1.0', tk.END).strip()) / 100
        # config["stagnation_iterations"] = int(self.textboxes[3].get('1.0', tk.END).strip())
        # config["total_iterations"] = int(self.textboxes[4].get('1.0', tk.END).strip())

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

        return

    def update_gui_config(self) -> None:
        """
        Update the gui representation of the config from data from self.config
        """
        config = self.config

        # set textfields
        self.textvars[0].set(config["population_size"])
        self.textvars[1].set(str(float(config["parent_percent"]*100)))
        self.textvars[2].set(str(float(config["mutation_chance"]*100)))
        self.textvars[3].set(config["stagnation_iterations"])
        self.textvars[4].set(config["total_iterations"])

        # selection checkbox
        self.checktype['selection'].set(1 if config["selection_type"] == "tournament" else (2 if config["selection_type"] == "ranking" else 3))

        # crossing checkbox
        self.checktype['crossing'].set(1 if config["crossing_types"] == "one cut" else (2 if config["crossing_types"] == "random_cuts" else 3))

        #mutation checkbox
        mutations = config["mutation_types"]
        mutations[0].set(True if "city" in mutations[0] else False)
        mutations[1].set(True if "date" in mutations[1] else False)
        mutations[2].set(True if "transit_mode" in mutations[2] else False)
        mutations[3].set(True if "new_gene" in mutations[3] else False)
        mutations[4].set(True if "delete_gene" in mutations[4] else False)

        return

    # algorithm runtime
    def generate_solution(self) -> None:
        """
        Generate a random solution with loaded problem and initial population (.py).
        :return: None
        """
        # popup
        if self.is_running or not messagebox.askyesno(title="Wygeneruj rozwiązanie",
                                                      message="Czy na pewno wygenerować rozwiązanie?"):
            return

        # GUI running indicators
        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                command=self.generate_solution, cursor="watch", bg="darkgrey")
        self.button.place(**GENERATE_SOLUTION_POS)

        self.stopbutton.place_forget()
        self.stopbutton = tk.Button(self.root, text="STOP", font=(self.font, self.font_size2),
                                    command=self.stop_algorithm, cursor="pirate", bg="red")
        self.stopbutton.place(**STOP_SOLUTION_POS)

        for i,entrybox in enumerate(self.textboxes):
            entrybox.grid_forget()
            entrybox = tk.Entry(self.textbox_grid,textvariable= self.textvars[i],font=(self.font, self.font_size2),state=tk.DISABLED)
            entrybox.grid(row=i, column=1, sticky=tk.W + tk.E)
            self.textboxes[i] = entrybox

        # pre running prep
        self.is_running = True
        if not self.config:
            self.update_config()

        # start algorithm
        self.control_thread = threading.Thread(target=genetic_algorithm_controller, args=[self])
        self.control_thread.start()

    def do_when_finished(self) -> None:
        # post algo entrybox reset
        for i,entrybox in enumerate(self.textboxes):
            entrybox.grid_forget()
            entrybox = tk.Entry(self.textbox_grid,textvariable= self.textvars[i],font=(self.font, self.font_size2))
            entrybox.grid(row=i, column=1, sticky=tk.W + tk.E)
            self.textboxes[i] = entrybox
        # buttons reset
        self.stopbutton.place_forget()

        self.button.place_forget()
        self.button = tk.Button(self.root, text="Wygeneruj rozwiązanie", font=(self.font, self.font_size2),
                                    command=self.generate_solution, cursor="sizing", bg="lightgreen")
        self.button.place(**GENERATE_SOLUTION_POS)

    def stop_algorithm(self) -> None:
        """
        Stop the algorithm from running. Does nothing if the algorithm does not run
        :return: None
        """
        if not self.is_running or not messagebox.askyesno(title="STOP", message="Czy na pewno zatrzymać rozwiązanie?"):
            return

        self.is_running = False

    # graph handling
    def update_cost_graph(self) -> None:
        """
        Plot given figure object as cost graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if self.fig_cost is None else self.fig_cost

        self.canvas['cost'].get_tk_widget().place_forget()
        self.canvas['cost'] = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas['cost'].get_tk_widget().place(**COST_GRAPH_POS)

    def update_population_graph(self) -> None:
        """
        Plot given figure object as population graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if self.fig_population is None else self.fig_population

        self.canvas['population'].get_tk_widget().place_forget()
        self.canvas['population'] = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas['population'].get_tk_widget().place(**POPULATION_GRAPH_POS)

    def update_time_graph(self) -> None:
        """
        Plot given figure object as time graph
        :param fig: matplotlib figure containing graph
        :return: None
        """
        fig = self.create_test_figure() if self.fig_time is None else self.fig_time

        self.canvas['time'].get_tk_widget().place_forget()
        self.canvas['time'] = FigureCanvasTkAgg(fig, master=self.root)
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

    def draw_graphs(self) -> None:
        """
        Draw figures from self.extra_data. Create Cost figure, Population figure, Time figure, store them in right GUI attributes.
        :return: None
        """
        # self.extra data required
        # variables
        vx = [elem for elem in range(self.extra_data["iterations"])]

        # cost graph
        fig_cost, ax_cost = plt.subplots()
        vy1 = self.extra_data["best_overall"][:]
        vy2 = self.extra_data["mean_in_iter"][:]
        ax_cost.plot(vx, vy1)
        ax_cost.plot(vx, vy2)

        # time margins graph
        fig_time, ax_time = plt.subplots()
        vy1 = self.extra_data["time_margin"][:]
        ax_time.plot(vx, vy1)

        # alive percent of new generation graph
        fig_population, ax_population = plt.subplots()
        vy1 = [100 * elem for elem in self.extra_data["alive_percent"]]
        ax_population.plot(vx, vy1)

        self.fig_cost = fig_cost
        self.fig_time = fig_time
        self.fig_population = fig_population

    def update_graphs(self) -> None:
        """
        Update graphs in GUI with given figures
        :param fig_cost: new cost graph
        :param fig_population: new population graph
        :param fig_time: new time graph
        :return: None
        """
        self.update_cost_graph()
        self.update_time_graph()
        self.update_population_graph()

    # view selection
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
        :return: None
        """
        self.leftarrow.place(**LEFTARROW_POS)
        self.rightarrow.place(**RIGHTARROW_POS)
        self.clear_graphs()
        self.update_city_graph()

    def show_graphs(self) -> None:
        """
        Choose solution graphs as the one shown in the GUI
        :return: None
        """
        self.leftarrow.place_forget()
        self.rightarrow.place_forget()
        self.clear_city_graph()
        self.update_graphs()

    def show_prev_package(self) -> None:
        """
        Show the previous package in an iteration from self.extra_data
        :return: None
        """
        self.cur_package_id -= 1
        self.update_city_graph(self.extra_data["package_routes"][self.cur_package_id])

    def show_next_package(self) -> None:
        """
        Show the next package in an iteration from self.extra_data
        :return: None
        """
        self.cur_package_id += 1
        self.update_city_graph(self.extra_data["package_routes"][self.cur_package_id])


if __name__ == '__main__':
    GUI()
