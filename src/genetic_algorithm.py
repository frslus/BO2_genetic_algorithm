from src.file_handling import *
from src.generate_graphs import *
from src.organisms_and_population import *
from src.problem_description import *
import json

# default constant parameters
DEFAULT_ALIVE_PERCENT = 0.5
DEFAULT_GENERATED_CHROMOSOME_MAX_LENGTH = 4
DEFAULT_ADDITION_CHANCE = 0.3


def genetic_algorithm(problem: TransportProblemObject, config_file: str,
                      extra_data: dict | None = None) -> Organism:
    with open(config_file, mode="r", encoding="utf-8") as file:
        params = json.load(file)

    # parameters from configuration file
    population_size = params["population_size"]
    total_iterations = params["total_iterations"]
    stagnation_iterations = params["stagnation_iterations"]
    parent_percent = params["parent_percent"]
    mutation_chance = params["mutation_chance"]
    selection_type = params["selection_type"]
    crossing_types = params["crossing_types"]
    mutation_types = params["mutation_types"]

    # hardcoded parameters
    alive_percent = DEFAULT_ALIVE_PERCENT
    generated_chromosome_max_length = DEFAULT_GENERATED_CHROMOSOME_MAX_LENGTH
    addition_chance = DEFAULT_ADDITION_CHANCE

    # variables
    alive_number = ceil(population_size * alive_percent)
    alive_organisms = []
    dead_organisms = []
    if extra_data is not None:
        extra_data["best_overall"] = []
        extra_data["mean_in_iter"] = []

    # initial population generation
    while len(alive_organisms) + len(dead_organisms) < population_size:
        new_organism = problem.generate_solution(generated_chromosome_max_length, addition_chance)
        new_organism.evaluate()
        if new_organism.cost() == INF:
            if len(dead_organisms) < population_size - alive_number:
                dead_organisms.append(new_organism)
        else:
            alive_organisms.append(new_organism)
    population = Population(alive_organisms + dead_organisms)

    # main algorithm
    best_score = population.best().cost()
    best_score_iter = 0
    for i in range(total_iterations):
        selection = population.selection(selection_type, parent_percent)
        population.reproduction(selection, crossing_types, mutation_types, mutation_chance)
        if population.best().cost() < best_score:
            best_score = population.best().cost()
            best_score_iter = i
        if extra_data is not None:
            extra_data["best_overall"].append(best_score)
            extra_data["mean_in_iter"].append(population.mean_cost())
        if i - best_score_iter >= stagnation_iterations:
            print(f"Algorithm stopped - too many iterations without improvement")
            break
        print(
            f"Iteration {i}: mean_cost: {population.mean_cost()}, best: {population.best().cost()}, best_iter: {best_score_iter}")
    else:
        print(f"Algorithm stopped - iteration limit reached")
    return population.best()
