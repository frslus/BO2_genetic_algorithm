from genetic_algorithm import *
from time import time

def save_score(filename, name, iterations, score):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        labels = ["name", "iterations", "score"]
        w0 = csv.DictWriter(file, fieldnames=labels, delimiter=";")
        # w0.writeheader()
        w0.writerow({"name": name, "iterations": iterations, "score": score})


def save_extra_data(extra_data, filename):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        labels = ["iterations", "best_overall", "mean_in_iter", "time_margin", "alive_percent"]
        w0 = csv.DictWriter(file, fieldnames=labels, delimiter=";")
        w0.writeheader()
        for i in range(extra_data["iterations"]):
            row = {label: extra_data[label][i] for label in labels[1:]}
            row["iterations"] = i
            w0.writerow(row)


# graph
GRAPH_FILE = "../data/graph20.csv"

# packages
PACKAGES_FILE = "../data/packages20_graph20.csv"

# population
CREATE_POPULATION = False
POPULATION_FILE_READ = "../data/packages20_graph20_population.csv"
POPULATION_FILE_SAVE = "../data/foo.csv"
POPULATION_SIZE = 100
ALIVE_NUMBER = 10
GENERATED_CHROMOSOME_MAX_LENGTH = 2
ADDITION_CHANCE = 0.3

# params
config = {
    "population_size": POPULATION_SIZE,
    "total_iterations": 100,
    "stagnation_iterations": 100,
    "parent_percent": 0.3,
    "mutation_chance": 0.1,
    "selection_type": "tournament",
    "crossing_types": ["random_selection"],
    "mutation_types": ["city", "date", "transit_mode", "new_gene", "delete_gene"]
    # ["city", "date", "transit_mode", "new_gene", "delete_gene"]
}
extra_data = {}
EXTRA_DATA_PATH = "../results/extra_data0.csv"
HISTORY_PATH = "../results/history.csv"
NAME = "t6_15"

# algorithm
tpo = TransportProblemObject(GRAPH_FILE, PACKAGES_FILE)
if CREATE_POPULATION:
    population = generate_population(tpo, POPULATION_SIZE, ALIVE_NUMBER, GENERATED_CHROMOSOME_MAX_LENGTH,
                                     ADDITION_CHANCE)
    save_population_to_file(population, POPULATION_FILE_SAVE)
else:
    population = Population(POPULATION_FILE_READ)
    population.link_problem(tpo)

REPEAT = 5

for _ in range(REPEAT):
    time_start = time()
    best = genetic_algorithm(tpo, config, None, extra_data, population, None)
    time_end = time()
    print(best)

    save_extra_data(extra_data, EXTRA_DATA_PATH)
    save_score(HISTORY_PATH, NAME, 20, time_end - time_start)
