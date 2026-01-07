from enum import Enum
from copy import deepcopy
from random import randint, uniform
from math import ceil, floor
import csv

INF = float("inf")
import networkx as nx

type reproduction_pairs = list[tuple[int, int]]


class TransitMode(Enum):
    PLANE = "plane"
    CAR = "car"
    TRAIN = "train"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if hasattr(other, "value"):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not (self == other)


class CrossingType(Enum):
    ONE_CUT = "one_cut"
    RANDOM_CUT = "random_cuts"
    RANDOM_SELECTION = "random_selection"


class MutationType(Enum):
    CITY = "city"
    DATE = "date"
    TRANSIT_MODE = "transit_mode"
    NEW_GENE = "new_gene"
    DELETE_GENE = "delete_gene"


class SelectionType(Enum):
    TOURNAMENT = "tournament"
    RANKING = "ranking"
    ROULETTE = "roulette"



type PackagesList = list[tuple[str, int, TransitMode]]


class Gene:
    """
    Represents one transit of one load.
    """

    def __init__(self, city_to: str, date: int, mode_of_transit: TransitMode | str):
        self.city_to = city_to
        self.date = date
        self.mode_of_transit = TransitMode(mode_of_transit)

    def __setattr__(self, name, value):
        match name:
            case "city_to":
                if type(value) != str:
                    raise TypeError(f"Attribute {name} must be {str}")
            case "date":
                if type(value) != int:
                    raise TypeError(f"Attribute {name} must be {int}")
                if value < 0:
                    raise ValueError(f"Attribute {name} must be >= 0")
            case "mode_of_transit":
                if type(value) != TransitMode and type(value) != str:
                    raise TypeError(f"Attribute {name} must be {TransitMode} or {str}")
                if type(value) == str:
                    value = TransitMode(value)
        object.__setattr__(self, name, value)

    def __repr__(self):
        mode_of_transit = {TransitMode.PLANE: "plane", TransitMode.CAR: "car", TransitMode.TRAIN: "train"}[
            self.mode_of_transit]
        return f"({self.city_to}, {self.date}, {mode_of_transit})"

    def __eq__(self, other):
        return self.city_to == other.city_to and self.date == other.date and self.mode_of_transit == other.mode_of_transit


class Chromosome:
    """
    Represents all transits of one load.
    """

    def __init__(self, genes: list[Gene]):
        if len(genes) == 0:
            raise Exception("Chromosome cannot be empty")
        if not all([isinstance(x, Gene) for x in genes]):
            raise TypeError(f"All genes must be of type {Gene}")
        for i in range(1, len(genes)):
            if genes[i].date <= genes[i - 1].date:
                raise ValueError(f"Transits are not in chronological order: {genes[i - 1]}, {genes[i]}")
        self.__genes = [Gene(gene.city_to, gene.date, gene.mode_of_transit) for gene in genes]

    def __iter__(self):
        return iter(self.__genes)

    def __getitem__(self, index):
        return self.__genes[index]

    def __setitem__(self, index, value):
        if not isinstance(value, Gene):
            raise TypeError(f"All genes must be of type {Gene}")
        if index < 0 or index >= len(self):
            raise KeyError(f"Index {index} out of range, length of chromosome: {len(self)}")
        if index > 0 and self.__genes[index - 1].date >= value.date:
            raise ValueError(f"New value ({value.date}) must be > {self.__genes[index - 1].date}")
        if index < len(self) - 1 and self.__genes[index + 1].date <= value.date:
            raise ValueError(f"New value ({value.date}) must be < {self.__genes[index + 1].date}")
        self.__genes[index] = value

    def __len__(self):
        return len(self.__genes)

    def __contains__(self, gene):
        return gene in self.__genes

    def __repr__(self):
        result = ""
        for gene in self.__genes:
            result += f" {gene},\n"
        return f"[{result[1:-2]}]"

    def insert(self, index, value):
        if not isinstance(value, Gene):
            raise TypeError(f"All genes must be of type {Gene}")
        if index < 0 or index > len(self):
            raise KeyError(f"Index {index} out of range, length of chromosome: {len(self)}")
        if index > 0 and self.__genes[index - 1].date >= value.date:
            raise ValueError(f"New value ({value.date}) must be > {self.__genes[index - 1].date}")
        if index < len(self) and self.__genes[index].date <= value.date:
            raise ValueError(f"New value ({value.date}) must be < {self.__genes[index].date}")
        self.__genes.insert(index, value)

    def pop(self, index):
        if len(self) == 1:
            raise Exception("Chromosome cannot be empty")
        if index < 0 or index >= len(self):
            raise KeyError(f"Index {index} out of range, length of chromosome: {len(self)}")
        self.__genes.pop(index)

    def append(self, value):
        self.__genes.insert(len(self), value)


class Genotype:
    """
    Represents all transits included in the solution.
    """

    def __init__(self, chromosomes: list[Chromosome]):
        if not all([isinstance(x, Chromosome) for x in chromosomes]):
            raise TypeError(f"All chromosomes must be of type {Chromosome}")
        self.__chromosomes = deepcopy(chromosomes)

    def __iter__(self):
        return iter(self.__chromosomes)

    def __getitem__(self, index):
        return self.__chromosomes[index]

    def __setitem__(self, index, value):
        self.__chromosomes[index] = value

    def __len__(self):
        return len(self.__chromosomes)

    def __repr__(self):
        result = "{"
        for chromosome in self.__chromosomes[:-1]:
            result += f"{chromosome},\n"
        return result + f"{self.__chromosomes[-1]}" + "}"


class Organism:
    """
    Represents one specific solution.
    """

    def __init__(self, genotype: Genotype, problem):
        if not isinstance(genotype, Genotype):
            raise TypeError(f"Genotype must be type of {Genotype}, not {type(genotype)}")
        self.__genotype = genotype
        self.__problem = problem
        self.__cost = None

    def __iter__(self):
        return iter(self.__genotype)

    def __getitem__(self, index):
        return self.__genotype[index]

    def __setitem__(self, index, value):
        self.__genotype[index] = value

    def __len__(self):
        return len(self.__genotype)

    def __repr__(self):
        return str(self.__genotype)

    def cost(self):
        if self.__cost is None:
            self.evaluate()
        return self.__cost

    def evaluate(self):
        self.__cost = self.__problem.evaluate_function(self)

    def is_evaluated(self):
        return not self.__cost is None

    def link_problem(self, problem):
        self.__problem = problem

    def crossover(self, other, crossing_type: CrossingType | str):
        if isinstance(crossing_type, str):
            crossing_type = CrossingType(crossing_type)
        problem_size = len(self)
        match crossing_type:
            case CrossingType.ONE_CUT:
                cut = randint(0, problem_size)
                new_genotype = deepcopy(self.__genotype)[:cut] + deepcopy(other.__genotype)[cut:]
            case CrossingType.RANDOM_CUT:
                pattern = [randint(0, 1) for _ in range(problem_size)]
                new_genotype = []
                for i in range(problem_size):
                    if pattern[i] == 0:
                        new_genotype.append(deepcopy(self.__genotype[i]))
                    else:
                        new_genotype.append(deepcopy(other.__genotype[i]))
            case CrossingType.RANDOM_SELECTION:
                c_pattern = [randint(0, 1) for _ in range(problem_size)]
                new_genotype = []
                for i in range(problem_size):
                    self_genes_list = [deepcopy(gene) for gene in self.__genotype[i]]
                    other_genes_list = [deepcopy(gene) for gene in other.__genotype[i]]
                    if c_pattern[i] == 0:
                        last_gene = self_genes_list.pop()
                        other_genes_list.pop()
                    else:
                        last_gene = other_genes_list.pop()
                        self_genes_list.pop()
                    all_genes_list = self_genes_list + other_genes_list
                    all_genes_list.sort(key=lambda x: x.date)
                    new_chromosome = []
                    location = self.__problem.list[i]["city_from"]
                    min_time = self.__problem.list[i]["date_ready"]
                    for j in range(len(all_genes_list)):
                        if all_genes_list[j].date < min_time or location == all_genes_list[j].city_to:
                            continue
                        if all_genes_list[j].date + self.__problem.graph[location][all_genes_list[j].city_to][
                            all_genes_list[j].mode_of_transit]["time"] > last_gene.date:
                            break
                        if randint(0, 1) == 1:
                            min_time = ceil(all_genes_list[j].date +
                                            self.__problem.graph[location][all_genes_list[j].city_to][
                                                all_genes_list[j].mode_of_transit]["time"])
                            location = all_genes_list[j].city_to
                            new_chromosome.append(deepcopy(all_genes_list[j]))
                    new_chromosome.append(deepcopy(last_gene))
                    new_genotype.append(Chromosome(deepcopy(new_chromosome)))
            case _:
                raise TypeError(f"'{crossing_type}' is not correct crossover type")
        return Organism(Genotype(new_genotype), self.__problem)

    def mutate(self, mutation_type: MutationType | str):
        if isinstance(mutation_type, str):
            mutation_type = MutationType(mutation_type)
        problem_size = len(self)
        chromosome = randint(0, problem_size - 1)
        gene = randint(0, len(self.__genotype[chromosome]) - 1)
        # DEBUGGING
        # print(chromosome, gene)
        # /DEBUGGING
        match mutation_type:
            case MutationType.CITY:
                if len(self.__genotype[chromosome]) == 1:
                    return
                if gene == len(self.__genotype[chromosome]) - 1:
                    gene -= 1
                cities = list(self.__problem.graph.nodes)
                cities.remove(self.__genotype[chromosome][gene].city_to)
                if gene == 0 and self.__problem.list[chromosome]["city_from"] in cities:
                    cities.remove(self.__problem.list[chromosome]["city_from"])
                else:
                    cities.remove(self.__genotype[chromosome][gene - 1].city_to)
                if self.__genotype[chromosome][gene + 1].city_to in cities:
                    cities.remove(self.__genotype[chromosome][gene + 1].city_to)
                if not cities:
                    return
                city_to = cities[randint(0, len(cities) - 1)]
                self.__genotype[chromosome][gene].city_to = city_to
            case MutationType.DATE:
                dt = randint(1, 2)
                if randint(0, 1) == 1:
                    self.__genotype[chromosome][gene].date += dt
                else:
                    self.__genotype[chromosome][gene].date -= dt if dt <= self.__genotype[chromosome][gene].date else \
                        self.__genotype[chromosome][gene].date
            case MutationType.TRANSIT_MODE:
                match self.__genotype[chromosome][gene].mode_of_transit:
                    case TransitMode.CAR:
                        mode_of_transit = TransitMode.TRAIN if randint(0, 1) == 0 else TransitMode.PLANE
                    case TransitMode.PLANE:
                        mode_of_transit = TransitMode.TRAIN if randint(0, 1) == 0 else TransitMode.CAR
                    case TransitMode.TRAIN:
                        mode_of_transit = TransitMode.CAR if randint(0, 1) == 0 else TransitMode.PLANE
                self.__genotype[chromosome][gene].mode_of_transit = mode_of_transit
                return
            case MutationType.NEW_GENE:
                cities = list(self.__problem.graph.nodes)
                if gene != 0:
                    cities.remove(self.__genotype[chromosome][gene - 1].city_to)
                if self.__genotype[chromosome][gene].city_to in cities:
                    cities.remove(self.__genotype[chromosome][gene].city_to)
                city_to = cities[randint(0, len(cities) - 1)]
                date = randint(1, 2) + (
                    self.__genotype[chromosome][gene - 1].date if gene != 0 else self.__problem.list[chromosome][
                        "date_ready"])
                rand_idx = randint(0, 2)
                mode_of_transit = TransitMode.TRAIN if rand_idx == 0 else TransitMode.PLANE if rand_idx == 1 else TransitMode.CAR
                try:
                    self.__genotype[chromosome].insert(gene, Gene(city_to, date, mode_of_transit))
                except ValueError:
                    # DEBUGGING
                    # print("Mutation error")
                    # /DEBUGGING
                    pass
            case MutationType.DELETE_GENE:
                if len(self.__genotype[chromosome]) == 1:
                    # DEBUGGING
                    # print("Mutation error")
                    # /DEBUGGING
                    return
                if gene == len(self.__genotype[chromosome]) - 1:
                    gene -= 1
                self.__genotype[chromosome].pop(gene)
            case _:
                raise ValueError(f"{mutation_type} is not correct type of mutation")


def save_population_to_file(filename: str, population):
    organisms_list = [deepcopy(elem) for elem in population]
    organisms_number = len(organisms_list)
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        w0 = csv.DictWriter(file, fieldnames=["population_size"], delimiter=";")
        w0.writeheader()
        w0.writerow({"population_size": organisms_number})
        w1 = csv.DictWriter(file, fieldnames=[f"organism_size"], delimiter=";")
        w1.writeheader()
        w1.writerow({"organism_size": len(organisms_list[0])})
        for i in range(organisms_number):
            w2 = csv.DictWriter(file, fieldnames=[f"organism_{i}"], delimiter=";")
            w2.writeheader()
            for j, chromosome in enumerate(organisms_list[i]):
                w3 = csv.DictWriter(file, fieldnames=[f"chromosome_{j}"], delimiter=";")
                w3.writeheader()
                w3.writerow({f"chromosome_{j}": len(chromosome)})
                w4 = csv.DictWriter(file, fieldnames=["city_to", "date", "mode_of_transit"], delimiter=";")
                w4.writeheader()
                for gene in chromosome:
                    w4.writerow({"city_to": gene.city_to, "date": gene.date,"mode_of_transit": str(gene.mode_of_transit)})

def load_population_from_file(filename: str):
    organisms_list = []
    labels = [("city_to", str), ("date", int), ("mode_of_transit", str)]
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        organisms_number = int(next(reader)[0])
        next(reader)
        organism_size = int(next(reader)[0])
        for _ in range(organisms_number):
            next(reader)
            chromosomes = []
            for _ in range(organism_size):
                next(reader)
                chromosome_length = int(next(reader)[0])
                next(reader)
                genes = []
                for _ in range(chromosome_length):
                    city_to, date, mode_of_transit = next(reader)
                    genes.append(Gene(city_to, int(date), mode_of_transit))
                chromosomes.append(Chromosome(genes))
            organisms_list.append(Organism(Genotype(chromosomes), None))
    return organisms_list

class Population:
    """
    Represents a generation of solutions.
    """

    def __init__(self, organisms_list: list[Organism] | str):
        self.__organisms = []
        if isinstance(organisms_list, str):
            organisms_list = load_population_from_file(organisms_list)
        for organism in organisms_list:
            if not isinstance(organism, Organism):
                raise TypeError(f"Organism must be type of {Organism}, not {type(organism)}")
        self.__organisms = deepcopy(organisms_list)

    def __iter__(self):
        return iter(self.__organisms)

    def __getitem__(self, index):
        return self.__organisms[index]

    def __setitem__(self, index, value):
        self.__organisms[index] = value

    def __len__(self):
        return len(self.__organisms)

    def mean_cost(self):
        sum_cost = 0.0
        organism_number = 0
        for organism in self.__organisms:
            if organism.cost() != INF:
                sum_cost += organism.cost()
                organism_number += 1
        return sum_cost / organism_number if organism_number != 0 else INF

    def best(self):
        population_copy = [elem for elem in enumerate(deepcopy(self.__organisms))]
        population_copy.sort(key=lambda x: x[1].cost())
        return deepcopy(population_copy[0][1])

    def worst(self):
        population_copy = [elem for elem in enumerate(deepcopy(self.__organisms))]
        population_copy.sort(key=lambda x: x[1].cost() if x[1].cost() != INF else 0, reverse=True)
        return deepcopy(population_copy[0][1])

    def link_problem(self, problem):
        for organism in self.__organisms:
            organism.link_problem(problem)

    def selection(self, selection_type: SelectionType | str, parent_percent: float) -> list[tuple[int, int]]:
        if isinstance(selection_type, str):
            selection_type = SelectionType(selection_type)
        parents_number = ceil(len(self) * parent_percent)
        if parents_number % 2 == 1:
            parents_number += 1
        if parents_number < 2:
            raise ValueError(f"Too few organisms to be selected")
        if parents_number > len(self):
            raise ValueError(f"Too many organisms to be selected")
        for organism in self.__organisms:
            if not organism.is_evaluated():
                organism.evaluate()
        population_copy = [elem for elem in enumerate(deepcopy(self.__organisms))]
        pairs = []
        match selection_type:
            case SelectionType.ROULETTE:
                min_cost = self.best().cost()
                max_cost = self.worst().cost()
                delta_cost = max_cost - min_cost
                pool = 0
                tickets = [0 for _ in range(len(self))]
                if population_copy[0][1].cost() == INF:
                    pool += 1
                    tickets[0] = 1
                else:
                    if delta_cost == 0:
                        tickets_number = 100
                    else:
                        tickets_number = 100 - ceil(90 * ((population_copy[0][1].cost() - min_cost) / delta_cost))
                    pool += tickets_number
                    tickets[0] = tickets_number
                for idx, elem in population_copy[1:]:
                    if elem.cost() == INF:
                        pool += 1
                        tickets[idx] = 1
                    else:
                        if delta_cost == 0:
                            tickets_number = 100
                        else:
                            tickets_number = 100 - ceil(90 * ((elem.cost() - min_cost) / delta_cost))
                        pool += tickets_number
                        tickets[idx] = tickets_number
                for _ in range(parents_number // 2):
                    ticket1 = randint(0, pool - 1)
                    organism1 = 0
                    while ticket1 > tickets[organism1]:
                        ticket1 -= tickets[organism1]
                        organism1 += 1
                    pool -= tickets[organism1]
                    tickets[organism1] = 0
                    ticket2 = randint(0, pool - 1)
                    organism2 = 0
                    while ticket2 > tickets[organism2]:
                        ticket2 -= tickets[organism2]
                        organism2 += 1
                    pool -= tickets[organism2]
                    tickets[organism2] = 0
                    pairs.append((organism1, organism2))
                # print(pairs)
            case SelectionType.RANKING:
                population_copy.sort(key=lambda x: x[1].cost())
                population_copy = population_copy[:parents_number]
                for _ in range(parents_number // 2):
                    organism1 = population_copy.pop(randint(0, len(population_copy) - 1))[0]
                    organism2 = population_copy.pop(randint(0, len(population_copy) - 1))[0]
                    pairs.append((organism1, organism2))
            case SelectionType.TOURNAMENT:
                group_max_len = floor(len(self) / parents_number)
                groups_unready = [[None for _ in range(group_max_len)] for _ in range(parents_number)]
                groups_ready = []
                for i in range(len(self) - group_max_len * parents_number):
                    groups_unready[i].append(None)
                for _ in range(len(self)):
                    elem = population_copy.pop(randint(0, len(population_copy) - 1))
                    i = randint(0, len(groups_unready) - 1)
                    groups_unready[i].insert(0, elem)
                    groups_unready[i].pop()
                    if groups_unready[i][-1] is not None:
                        full_group = groups_unready.pop(i)
                        groups_ready.append(full_group)
                for i in range(parents_number // 2):
                    organism1 = groups_ready[2 * i][0]
                    # print(organism1[0], organism1[1].cost())
                    for j in range(1, len(groups_ready[2 * i])):
                        # print(groups_ready[2 * i][j][0], groups_ready[2 * i][j][1].cost())
                        if organism1[1].cost() > groups_ready[2 * i][j][1].cost():
                            organism1 = groups_ready[2 * i][j]
                    # print(organism1[0])
                    # print()
                    organism2 = groups_ready[2 * i + 1][0]
                    # print(organism2[0], organism2[1].cost())
                    for j in range(1, len(groups_ready[2 * i + 1])):
                        # print(groups_ready[2 * i + 1][j][0], groups_ready[2 * i + 1][j][1].cost())
                        if organism2[1].cost() > groups_ready[2 * i + 1][j][1].cost():
                            organism2 = groups_ready[2 * i + 1][j]
                    pairs.append((organism1[0], organism2[0]))
                    # print(organism2[0])
                    # print()
                # print(pairs)
            case _:
                raise TypeError(f"'{selection_type}' is not correct selection type")
        return pairs

    def reproduction(self, pairs: reproduction_pairs, crossing_types: list[CrossingType | str],
                     mutation_types: list[MutationType | str], mutation_chance: float) -> None:
        new_generation = []
        for idx1, idx2 in pairs:
            for _ in range(2):
                crossing_type = crossing_types[randint(0, len(crossing_types) - 1)]
                child = self.__organisms[idx1].crossover(self.__organisms[idx2], crossing_type)
                if uniform(0, 1) < mutation_chance:
                    mutation_type = mutation_types[randint(0, len(mutation_types) - 1)]
                    child.mutate(mutation_type)
                new_generation.append(child)
        missing_elements = len(self.__organisms) - len(new_generation)
        old_generation = deepcopy(self.__organisms)
        for organism in old_generation:
            if not organism.is_evaluated():
                organism.evaluate()
        old_generation.sort(key=lambda x: x.cost())
        self.__organisms = deepcopy(new_generation + old_generation[:missing_elements])
