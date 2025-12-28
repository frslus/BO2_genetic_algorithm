from enum import Enum
from copy import deepcopy
from random import randint

import networkx as nx


class TransitMode(Enum):
    PLANE = "plane"
    CAR = "car"
    TRAIN = "train"

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
    ONE_CUT = "cut"
    RANDOM_SELECTION = "random"


class MutationType(Enum):
    CITY = "city"
    DATE = "date"
    TRANSIT_MODE = "transit_mode"
    NEW_GENE = "new_gene"
    DELETE_GENE = "delete_gene"


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

    def crossover(self, other, crossing_type: CrossingType):
        problem_size = len(self)
        match crossing_type:
            case CrossingType.ONE_CUT:
                cut = randint(0, problem_size)
                new_genotype = deepcopy(self.__genotype)[:cut] + deepcopy(other.__genotype)[cut:]
            case CrossingType.RANDOM_SELECTION:
                pattern = [randint(0, 1) for _ in range(problem_size)]
                new_genotype = []
                for i in range(problem_size):
                    if pattern[i] == 0:
                        new_genotype.append(deepcopy(self.__genotype[i]))
                    else:
                        new_genotype.append(deepcopy(other.__genotype[i]))
            case _:
                raise TypeError(f"'{crossing_type}' is not correct crossover type")
        return Organism(new_genotype, self.__problem)

    def mutate(self, mutation_type: MutationType):
        problem_size = len(self)
        chromosome = randint(0, problem_size - 1)
        gene = randint(0, len(self.__genotype[chromosome]) - 1)
        match mutation_type:
            case MutationType.CITY:
                if len(self.__genotype[chromosome]) == 1:
                    return
                if gene == len(self.__genotype[chromosome]) - 1:
                    gene -= 1
                cities = list(self.__problem.graph.nodes)
                cities.remove(self.__genotype[chromosome][gene].city_to)
                if gene == 0:
                    cities.remove(self.__problem.list[chromosome]["city_from"])
                else:
                    cities.remove(self.__genotype[chromosome][gene - 1].city_to)
                cities.remove(self.__genotype[chromosome][gene + 1].city_to)
                if not cities:
                    return
                city_to = cities[randint(0, len(cities) - 1)]
                self.__genotype[chromosome][gene].city_to = city_to
                return
            case MutationType.DATE:
                if randint(0, 1) == 1:
                    self.__genotype[chromosome][gene].date += randint(1, 3)
                else:
                    self.__genotype[chromosome][gene].date -= randint(1, 3)
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
                cities.remove(self.__genotype[chromosome][gene + 1].city_to)
                city_to = cities[randint(0, len(cities) - 1)]
                date = self.__genotype[chromosome][gene - 1].date + randint(1, 3)
                rand_idx = randint(0, 2)
                mode_of_transit = TransitMode.TRAIN if rand_idx == 0 else TransitMode.PLANE if rand_idx == 1 else TransitMode.CAR
                self.__genotype[chromosome].insert(gene, Gene(city_to, date, mode_of_transit))
            case MutationType.DELETE_GENE:
                if gene == len(self.__genotype[chromosome]) - 1:
                    gene -= 1
                self.__genotype[chromosome].pop(gene)
        raise ValueError(f"{mutation_type} is not correct type of mutation")
