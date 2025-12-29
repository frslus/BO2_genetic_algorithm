from src.file_handling import *
from src.generate_graphs import *
from src.organisms_and_population import *
from src.problem_description import *


def genetic_algorithm(problem: TransportProblemObject):
    population_size = 100
    alive_percent = 0.5
    iterations = 200
    parent_percent = 0.2
    mutation_chance = 0.5
    selection_type = "ranking"
    crossing_types = ["random_selection"]
    mutation_types = ["city", "date", "transit_mode", "new_gene", "delete_gene"]

    alive_number = ceil(population_size * alive_percent)
    alive_organisms = []
    dead_organisms = []
    while len(alive_organisms) + len(dead_organisms) < population_size:
        new_organism = problem.generate_solution(4)
        new_organism.evaluate()
        if new_organism.cost() == INF and len(dead_organisms) < population_size - alive_number:
            dead_organisms.append(new_organism)
        else:
            alive_organisms.append(new_organism)
    population = Population(alive_organisms + dead_organisms)
    for i in range(iterations):
        selection = population.selection(selection_type, parent_percent)
        population.reproduction(selection, crossing_types, mutation_types, mutation_chance)
        print(f"Iteration {i}: mean_cost: {population.mean_cost()}")
    return population.best()
