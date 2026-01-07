from file_handling import *
from organisms_and_population import *
import networkx as nx


class TransportProblemObject:
    def __init__(self, cities_graph: nx.MultiGraph | str | None = None,
                 packages_list: list[dict] | str | None = None):
        self.__cities_graph = None
        self.__packages_list = None
        self.__timespan = None
        if cities_graph is not None:
            self.reload_graph(cities_graph)
        if packages_list is not None:
            self.reload_list(packages_list)

    def __getattr__(self, item):
        if item == "graph":
            return self.__cities_graph
        if item == "list":
            return self.__packages_list
        if item == "timespan":
            return self.__timespan
        raise AttributeError(f"The object do not have attribute: {item}")

    def __len__(self):
        return len(self.__packages_list)

    def reload_graph(self, cities_graph: nx.MultiGraph | str):
        if isinstance(cities_graph, str):
            cities_graph_file = cities_graph
            cities_graph = load_graph_from_file(cities_graph_file)
        self.__cities_graph = deepcopy(cities_graph)

    def reload_list(self, packages_list: list[dict] | str):
        if isinstance(packages_list, str):
            packages_list_file = packages_list
            packages_list = load_list_from_file(packages_list_file)
        self.__packages_list = deepcopy(packages_list)
        self.__timespan = max([elem["date_delivery"] for elem in self.__packages_list])

    def save_to_file(self, filename: str) -> None:
        save_graph_to_file(self.__cities_graph, filename + "/cities_graph.csv")
        save_list_to_file(self.__packages_list, filename + "/packages_list.csv")

    def evaluate_function(self, organism: Organism) -> float:
        # DEBUGGING
        RAPORT = False
        # /DEBUGGING
        cost = 0.0
        storage_matrix = [{key: 0 for key in self.__cities_graph.nodes} for _ in range(self.__timespan)]
        for i in range(len(organism)):
            location = self.__packages_list[i]["city_from"]
            is_transported = False
            transport_end = None
            j = 0
            for t in range(self.__packages_list[i]["date_ready"], self.__packages_list[i]["date_delivery"]):
                if is_transported:
                    if transport_end <= t:
                        is_transported = False
                        location = organism[i][j].city_to
                        j += 1
                if not is_transported and j < len(organism[i]):
                    if organism[i][j].date < t:
                        # DEBUGGING
                        if RAPORT:
                            print(i, j, t, organism[i][j])
                        # /DEBUGGING
                        return INF
                    if organism[i][j].date == t:
                        is_transported = True
                        if location == organism[i][j].city_to:
                            return INF
                        transport_end = organism[i][j].date + self.__cities_graph[location][organism[i][j].city_to][
                            organism[i][j].mode_of_transit]["time"]
                        cost += self.__cities_graph[location][organism[i][j].city_to][
                                    organism[i][j].mode_of_transit]["cost"] * self.__packages_list[i]["weight"]
                if not is_transported:
                    storage_matrix[t][location] += self.__packages_list[i]["weight"]
                # DEBUGGING
                if RAPORT:
                    print(f"n={i} t={t}: ", end="")
                    if is_transported:
                        print(f"{location} -> {organism[i][j].city_to}: {transport_end}")
                    else:
                        print(f"{location}")
                # /DEBUGGING
            else:
                if is_transported:
                    if transport_end <= self.__packages_list[i]["date_delivery"]:
                        is_transported = False
                        location = organism[i][j].city_to
                        j += 1
            if is_transported or j < len(organism[i]) or location != self.__packages_list[i]["city_to"]:
                # DEBUGGING
                if RAPORT:
                    print(is_transported, j, location, "!=", self.__packages_list[i]["city_to"])
                # /DEBUGGING
                return INF
        # DEBUGGING
        if RAPORT:
            for i, elem in enumerate(storage_matrix):
                print(f"{i}: {elem}")
        # /DEBUGGING
        capacities = {elem[0]: elem[1]["capacity"] for elem in self.__cities_graph.nodes(data=True)}
        for t in range(self.__timespan):
            for location in self.__cities_graph.nodes:
                if storage_matrix[t][location] > capacities[location]:
                    # DEBUGGING
                    if RAPORT:
                        print(t, location, storage_matrix[t][location], capacities[location])
                    # /DEBUGGING
                    return INF
        return cost

    def generate_solution(self, max_len: int = 3, addition_chance: float = 0.3):
        if max_len < 1:
            raise ValueError(f"Max chromosome length must be 1 or more, not: {max_len}")
        genotype = []
        modes_of_transit = ["train", "car", "plane"]
        cities = [elem for elem in self.__cities_graph.nodes()]
        for i in range(len(self)):
            chromosome = []
            for j in range(max_len - 1):
                if uniform(0, 1) < addition_chance:
                    local_cities = deepcopy(cities)
                    local_cities.remove(self.__packages_list[i]["city_to"])
                    if chromosome:
                        if chromosome[-1][0] in local_cities:
                            local_cities.remove(chromosome[-1][0])
                        date = chromosome[-1][1] + randint(0, 1)
                        if len(chromosome) > 1:
                            date += ceil(self.__cities_graph[chromosome[-1][0]][chromosome[-2][0]]
                                         [chromosome[-1][2]]["time"])
                        else:
                            date += ceil(self.__cities_graph[chromosome[-1][0]][self.__packages_list[i]["city_from"]]
                                         [chromosome[-1][2]]["time"])
                    else:
                        if self.__packages_list[i]["city_from"] in local_cities:
                            local_cities.remove(self.__packages_list[i]["city_from"])
                        date = self.__packages_list[i]["date_ready"]
                    city = local_cities[randint(0, len(local_cities) - 1)]
                    mode = modes_of_transit[randint(0, len(modes_of_transit) - 1)]
                    chromosome.append((city, date, mode))
            if chromosome:
                date = chromosome[-1][1] + randint(0, 1)
                if len(chromosome) > 1:
                    date += ceil(self.__cities_graph[chromosome[-1][0]][chromosome[-2][0]]
                                 [chromosome[-1][2]]["time"])
                else:
                    date += ceil(
                        self.__cities_graph[chromosome[-1][0]][self.__packages_list[i]["city_from"]]
                        [chromosome[-1][2]]["time"])
            else:
                date = self.__packages_list[i]["date_ready"]
            mode = modes_of_transit[randint(0, len(modes_of_transit) - 1)]
            chromosome.append((self.__packages_list[i]["city_to"], date, mode))
            processed_chromosome = Chromosome([Gene(c, d, m) for c, d, m in chromosome])
            genotype.append(processed_chromosome)
        return Organism(Genotype(genotype), self)
