from genetic_algorithm import *


def save_score(filename, name, iterations, score):
    with open(filename, mode="w+", newline="", encoding="utf-8") as file:
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
PACKAGES_FILE = "../data/packages50_graph20.csv"

# population
CREATE_POPULATION = True
POPULATION_FILE = "../data/simple6_population.csv"
POPULATION_SIZE = 5
ALIVE_NUMBER = 0

# DO NOT TOUCH
GENERATED_CHROMOSOME_MAX_LENGTH = 4
ADDITION_CHANCE = 0.3

# params
config = {
    "population_size": POPULATION_SIZE,
    "total_iterations": 100000,
    "stagnation_iterations": 300,
    "parent_percent": 0.3,
    "mutation_chance": 0.1,
    "selection_type": "ranking",
    "crossing_types": ["random_selection", "random_cuts"],
    "mutation_types": ["city", "date", "transit_mode", "new_gene", "delete_gene"]
}
extra_data = {}
EXTRA_DATA_PATH = "../results/extra_data0.csv"
HISTORY_PATH = "../results/history.csv"
NAME = "test1"

# algorithm
tpo = TransportProblemObject(GRAPH_FILE, PACKAGES_FILE)
if CREATE_POPULATION:
    population = generate_population(tpo, POPULATION_SIZE, ALIVE_NUMBER, GENERATED_CHROMOSOME_MAX_LENGTH,
                                     ADDITION_CHANCE)
else:
    population = Population(PACKAGES_FILE)

best = genetic_algorithm(tpo, config, None, extra_data, population, None)
print(best)

save_extra_data(extra_data, EXTRA_DATA_PATH)
save_score(HISTORY_PATH, NAME, extra_data["iterations"], best.cost())
