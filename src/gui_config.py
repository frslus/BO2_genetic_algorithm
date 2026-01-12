# text constants
FONT_SIZE = 18
FONT = "Helvetica"

# starting screen
STARTSCREEN_BG_POS = {"relx": 0.1, "rely": 0.02, "relheight": 0.5, "relwidth": 0.8}
STARTSCREEN_LABEL_POS = {"relx": 0.2, "rely": 0.05, "relheight": 0.4, "relwidth": 0.6}
STARTSCREEN_BUTTON_POS = {"relx": 0.25, "rely": 0.6, "relwidth": 0.5, "relheight": 0.3}

# backgrounds
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
LEFTARROW_POS = {"relx": 0.05, "rely": 0.84}
RIGHTARROW_POS = {"relx": 0.1, "rely": 0.84}

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

# generate solution button
MAIN_LABEL_POS = {"relx": 0.15, "rely": 0.01, "relheight": 0.04, "relwidth": 0.5}
GENERATE_SOLUTION_POS = {"relx": 0.53, "rely": 0.935}
STOP_SOLUTION_POS = {"relx": 0.45, "rely": 0.935}