from copy import deepcopy
from math import sqrt
from random import random, randint

import networkx as nx

# predefined types
INF = float('inf')
type city_id = str | int
type path = tuple[float, list[city_id]]
type city_params = tuple[city_id, int, int, int]
type edge = tuple[city_id, city_id]
type edge_data = dict[edge, None] | dict[edge, int] | dict[edge, float]


# helpers
def randomize_data(data: int | float, multiplier: float, noise: float) -> float:
    """
    Randomize and scale the data. Used for randomizing costs and velocities with noise
    :param data: starting cost
    :param multiplier: the basis multiplier applied to cost
    :param noise: the noise constant of the multiplier. Must no greater than the multiplier
    :return: randomized cost
    """
    # noise_cleaned = noise % multiplier # decreases efficiency, prevents negative results
    cost = data * (multiplier - noise + 2 * random() * noise)
    return cost


def randomize_bool(chance: float = 0.5) -> bool:
    """
    Roll for True with given chance.
    :param chance: Chance to roll true. Must be between 0 and 1.
    :return: Result of the roll.
    """
    # chance_cleaned = chance % 1 decreases efficiency, prevents illogical results
    return random() < chance


def generate_city_name() -> str:
    """
    Generate a random city name.in one of the following formats:
    Aa000 A000 Aa00 A00
    :return: the name of the city as string
    """
    # random capital letter
    first_char = chr(randint(65, 90))

    # random lowercase letter
    second_char = ""
    for i in range(randint(0, 1)):
        second_char = chr(randint(97, 112))

        # random numbers
    numbers = str(randint(100, 999)) if randomize_bool() else str(randint(0, 99))

    return first_char + second_char + numbers


# city generation
def generate_random_cities(count: int = 5, bounds_x: tuple[int, int] = (0, 1000), bounds_y: tuple[int, int] = (0, 1000),
                           bounds_cap: tuple[int, int] = (3, 10), *, names: bool = True) -> list[city_params]:
    """
    Generate a random list of cities, defined by their cartesian coordinates and capacities.
    :param count: Amount of cities to generate.
    :param bounds_x: Bounds within the x dimension. Needs to be a pair of integers.
    :param bounds_y: Bounds within the y dimension. Needs to be a pair of integers.
    :param bounds_cap: Bounds of storage capacity.
    :param names: If True, names will also be generated. Otherwise integer city id will be used.
    :return: List of cities and their coordinates and capacities.
    """
    cities = [
        (i, randint(bounds_x[0], bounds_x[1]), randint(bounds_y[0], bounds_y[1]), randint(bounds_cap[0], bounds_cap[1]))
        for i in range(count)]

    return cities if not names else assign_city_names(cities)


def assign_city_names(cities: list[city_params], names: list[str] = None) -> list[city_params]:
    """
    Assigns names to cities. By default, the assignment is random.
    :param cities: Cartesian coordinates of cities.
    :param names: Optional, list of names to assign. Needs to be of the same length as cities.
    :return: A list of cities as tuple (name, x, y).
    """
    # TODO: check for duplicates
    if names is None:
        return [(generate_city_name(), x, y, cap) for _, x, y, cap in cities]
    return cities


# basic graph generation
def create_multigraph(cities: list[city_params] = None) -> nx.MultiGraph:
    """
    Create a multigraph of cities. Make them accessible by names, or by numbers, if names aren't provided.
    :param cities: List of cities with city_ids and capacities.
    :return: A graph object representing the cities as a multigraph.
    """
    graph = nx.MultiGraph()
    for name, x, y, cap in cities:
        graph.add_node(name, x=x, y=y, capacity=cap)

    return graph


def assign_cartesian_distances(graph: nx.MultiGraph) -> edge_data:
    """
    Assign cartesian distances between cities. The data is assigned as edges 'distance' between every pair of different cities.
    :param graph: The multigraph representation of cities, with cartesian coordinates.
    :return: Dictionary of edge:distance
    """
    # init
    cities = list(graph.nodes())
    city_count = len(cities)
    distances = {}

    # iterate over every edge
    for i, city_from in enumerate(cities):
        for j in range(i + 1, city_count):
            # calculate distance between city_from and city_to
            city_to = cities[j]
            dx = graph.nodes[city_from]['x'] - graph.nodes[city_to]['x']
            dy = graph.nodes[city_from]['y'] - graph.nodes[city_to]['y']
            dist = round(sqrt(dx ** 2 + dy ** 2))

            # assign edges, presumed symmetric
            graph.add_edge(city_from, city_to, key="distance", cost=dist)
            distances[(city_from, city_to)] = dist

    return distances


# plane layer methods
def assign_airports(graph: nx.MultiGraph, airports: dict[city_id, bool] = None, *, airport_chance: float = 0.7,
                    **kwargs) -> dict[city_id, bool]:
    """
    Assign airports to all cities, given a dictionary of cities having one or not. If there isn't one assign airports.
     with random, but potentially specifiable chance
    :param graph: The multigraph representation of cities.
    :param airports: Dictionary of city_name:has_airport.
    :param airport_chance: Specifies the random chance of assigning an airport, should it be assigned randomly.
    Must be between 0 and 1. Keyword only.
    :return: dictionary of city_id:has_airport.
    """
    # airports given for assignment
    if airports:
        for city, has_airport in airports.items():
            graph.nodes[city]['has_airport'] = has_airport
        return airports

    # randomly generate airports
    airports = {}
    airport_chance_cleaned = airport_chance % 1

    for city in graph.nodes:
        roll = randomize_bool(airport_chance_cleaned)
        graph.nodes[city]['has_airport'] = roll
        airports[city] = roll

    return airports


def assign_plane_costs(graph: nx.MultiGraph, *, plane_mult: float = 1.5, plane_noise: float = 0,
                       **kwargs) -> edge_data:
    """
    Assign plane costs between cities. Calculates distances if they have not been calculated yet.
    :param graph: The multigraph representation of cities, with distances between them and specified having airport or not.
    :param plane_mult: The multiplier for plane costs.
    :param plane_noise: The noise constant of the multiplier. Must be no greater than the multiplier
    :return: dictionary of edge:plane_cost
    """
    # init
    cities = list(graph.nodes())
    city_count = len(cities)
    plane_costs = {}

    for i, city_from in enumerate(cities):
        if not graph.nodes[city_from]['has_airport']:

            # make city with no airport have no planes out
            for j in range(i + 1, city_count):
                city_to = cities[j]
                graph.add_edge(city_from, city_to, key="plane", cost=INF)
                plane_costs[(city_from, city_to)] = INF
            continue

        for j in range(i + 1, city_count):
            # check for airport
            city_to = cities[j]
            if not graph.nodes[city_to]['has_airport']:
                graph.add_edge(city_from, city_to, key="plane", cost=INF)
                plane_costs[(city_from, city_to)] = INF
                continue

            # calculate each edge and assign
            plane_cost = randomize_data(graph[city_from][city_to]['distance']['cost'], plane_mult, plane_noise)
            graph.add_edge(city_from, city_to, key="plane", cost=plane_cost)
            plane_costs[(city_from, city_to)] = plane_cost

    return plane_costs


# car layer methods
def assign_car_costs(graph: nx.MultiGraph, roads: edge_data = None, *, car_mult: float = 1.0, car_noise: float = 0.125,
                     **kwargs) -> edge_data:
    """
    Assign costs of going by car between every pair of cities. Randomize them with given parameters, if a list of costs was not provided.
    :param graph: The multigraph representation of cities, with distances between them required if costs are randomized.
    :param roads: Optional. List of costs of going between cities, expressed as a tuple (city_from, city_to, distance).
    :param car_mult: Optional. Multiplier for car costs, should they be randomized
    :param car_noise: Optional. Noise constant of the multiplier. Must be no greater than the multiplier.
    :return: dict of generated edge:car_cost, returns roads if roads provided
    """
    # TODO: add railway like implementation for roads

    # edges and costs provided
    if roads:
        for (city_from, city_to), cost in roads.items():
            graph.add_edge(city_from, city_to, key="car", cost=cost)
        return roads

    # init randomize
    roads = {}
    noise_cleaned = car_noise % car_mult
    cities = list(graph.nodes())
    city_count = len(cities)

    # randomize costs for all edges
    for i, city_from in enumerate(cities):
        for j in range(i + 1, city_count):
            city_to = cities[j]
            car_cost = randomize_data(graph[city_from][city_to]['distance']['cost'], car_mult, noise_cleaned)
            graph.add_edge(city_from, city_to, key="car", cost=car_cost)
            roads[(city_from, city_to)] = car_cost

    return roads


# train layer methods
def assign_train_costs(graph: nx.MultiGraph, railways: edge_data = None, *, train_mult: float = 0.75,
                       train_noise: float = 0.05, railway_chance: float = 0.75, **kwargs) -> edge_data:
    """
    Assign railways from a list of edges and costs. If not all costs are provided, random ones are assigned in their places,
    with option to give multiplier and noise. If neither edges nor costs are provided, both are assigned randomly, with option
    to give chance of a railway connection, as well as multiplier and noise of cost.
    :param graph: The multigraph representation of cities, with distances between them required if costs are randomized.
    :param railways: List of edges with optionally assigned costs.
    :param train_mult: Train transport cost multiplier. Used only when costs are randomized. Highly recommended
    positive values.
    :param train_noise: Noise for train transport costs, defined as maximal variance from average result
    railway_mult in randomizing. Used only when costs are randomized.
    :param railway_chance: Chance of creating a railway connection. Used only when edges are randomized.
    :return: dict of edge:train_costs, returns railways if complete, fills railways with costs if not complete.
    """
    if railways:

        # init given railways
        railways_keys = set(railways.keys())
        cities = list(graph.nodes())
        city_count = len(cities)
        noise_cleaned = train_noise % train_mult

        # iterate over every edge
        for i, city_from in enumerate(cities):
            for j in range(i + 1, city_count):
                city_to = cities[j]

                if (city_from, city_to) in railways_keys:
                    # assign cost if is known
                    if (train_cost := railways[(city_from, city_to)]) is not None:
                        graph.add_edge(city_from, city_to, key='train', cost=train_cost)

                    # randomize if cost is not known
                    else:
                        train_cost = randomize_data(graph[city_from][city_to]['distance']['cost'], train_mult,
                                                    noise_cleaned)
                        railways[(city_from, city_to)] = train_cost
                        graph.add_edge(city_from, city_to, key='train', cost=train_cost)

                # forbid non-specified edges from being traversed
                elif graph[city_from][city_to]['train'] != INF:
                    graph.add_edge(city_from, city_to, key="train", cost=INF)

        return railways

    # init randomize
    railways = {}
    railway_chance_cleaned = railway_chance % 1
    noise_cleaned = train_noise % train_mult
    cities = list(graph.nodes())
    city_count = len(cities)

    # assign random edges random costs
    for i, city_from in enumerate(cities):
        for j in range(i + 1, city_count):
            city_to = cities[j]

            # no rail connection
            if not randomize_bool(railway_chance_cleaned):
                railways[(city_from, city_to)] = INF
                graph.add_edge(city_from, city_to, key='train', cost=INF)

            train_noise = randomize_data(graph[city_from][city_to]['distance']['cost'], train_mult, noise_cleaned)
            graph.add_edge(city_from, city_to, key="train", cost=train_noise)
            railways[(city_from, city_to)] = train_noise

    return railways


def johnson(graph: nx.MultiGraph, layer1: str, layer2: str, path_layer: str = "path") -> dict[edge, path]:
    """
    Optimise connections on a given layer using johnson algorithm.
    :param graph: The multigraph representation of cities. The layer needs to be complete.
    :param layer1: The name of the higher layer to optimize for. Must be from ("plane","car","train")
    :param layer2: The name of the lower layer to optimize for. Must be from ("cost","time")
    :param path_layer: The name of the new layer containing calculated path
    :return: a dict of edge:optimized_path for every optimized edge in the graph
    """
    nodes_list = [node for node in graph.nodes()]
    param_dict = {}
    for i, node1 in enumerate(nodes_list[:-1]):
        d, prev = dijkstra(graph, node1, layer1, layer2)
        for node2 in nodes_list[i + 1:]:
            p = [node2]
            while prev[p[0]] != node1:
                p.insert(0, prev[p[0]])
            graph[node1][node2][layer1][layer2] = d[node2]
            graph[node1][node2][layer1][path_layer] = deepcopy(p[:-1])
            param_dict[(node1, node2)] = (d[node2], deepcopy(p[:-1]))
    return param_dict


def dijkstra(graph, node, layer1: str, layer2: str):
    nodes_list = [node for node in graph.nodes()]
    d = {node: INF for node in nodes_list}
    d[node] = 0
    q = deepcopy(nodes_list)
    prev = {node: None for node in nodes_list}
    while q:
        u = q[0]
        for i in range(1, len(q)):
            if d[u] > d[q[i]]:
                u = q[i]
        q.remove(u)
        for v in nodes_list:
            if v != u and d[v] > d[u] + graph[u][v][layer1][layer2]:
                d[v] = d[u] + graph[u][v][layer1][layer2]
                prev[v] = u
    return d, prev


# time assignment
def assign_times(graph: nx.MultiGraph, layer: str, velocity: float = 1) -> edge_data:
    """
    Assign times of travel between cities for given mode of transit.
    :param graph: The multigraph representation of cities, with all distances defined within given layer.
    :param layer: The mode of transit to assign times for. Must be provided from ("plane","car","train")
    :param velocity: The average speed of travelling by given mode of transit
    :return: None
    """
    # init
    cities = list(graph.nodes())
    city_count = len(cities)
    times = {}

    # assign all times
    for i, city_from in enumerate(cities):
        for j in range(i + 1, city_count):
            city_to = cities[j]
            time = graph[city_from][city_to][layer]['cost'] / velocity
            graph.add_edge(city_from, city_to, key=layer, time=time)
            times[(city_from, city_to)] = time

    return times


# main method
def create_complete_graph(cities: list[city_params] = None, airports: dict[city_id, bool] = None,
                          railways: edge_data = None, roads: edge_data = None, plane_velocity: float = 2,
                          car_velocity: float = 1.3, train_velocity: float = 0.8, *, city_count: int = 5,
                          extended_output=False, **kwargs) -> nx.MultiGraph:
    """
    Create a complete graph of cities, with all edges assigned.
    :param cities: Optional. List of predefined city coordinates
    :param airports: Optional. List of cities with airports. Must contain the same city_ids as cities.
    :param railways: Optional. List of all railways to create. Must contain the same city_ids as cities.
    :param roads: Optional. List of all car roads to create. Must contain the same city_ids as cities.
    :param plane_velocity: Optional. Velocity of planes.
    :param car_velocity: Optional. Velocity of cars.
    :param train_velocity: Optional. Velocity of trains.
    :param city_count: Optional. Amount of cities to create, if cities have not been provided. Ignored otherwise
    :param extended_output: Defines whether the output should contain built-in python type versions of each layer. Simplified by default
    :param kwargs: All keyword arguments. Notable ones include transport multipliers and noise, railway and airport
    chances if transit info was not provided, or city names, bounds of coordinates and capacity, if cities were not provided.
    :return: The complete graph representation of the problem, ready to be optimised. When extended, contains all layers
    in form of edge:cost/time, list of cities, and dictionary of airports.
    """
    # init
    if not cities:
        cities = generate_random_cities(city_count, **kwargs)
    graph = create_multigraph(cities)
    assign_cartesian_distances(graph)

    # calculate costs of each mode of transit
    airports = assign_airports(graph, airports, **kwargs)
    plane_costs = assign_plane_costs(graph, **kwargs)
    train_costs = assign_train_costs(graph, railways, **kwargs)
    optimized_train_costs = johnson(graph, "train", "cost")
    car_costs = assign_car_costs(graph, roads, **kwargs)

    # calculate times for each mode of transit
    modes_of_transit = ("plane", "car", "train")
    velocities = {"plane": plane_velocity, "car": car_velocity, "train": train_velocity}
    times = []
    for layer in modes_of_transit:
        times.append(assign_times(graph, layer, velocities[layer]))
    plane_times, car_times, train_times = tuple(times)

    # create extended output
    adj_list = {"plane": {"cost": plane_costs, "time": plane_times}, "car": {"cost": car_costs, "time": car_times},
                "train": {"cost": train_costs, "time": train_times, "johnson": optimized_train_costs}}

    if not extended_output:
        return graph
    return graph, adj_list, cities, airports


def generate_package_list(graph: nx.MultiGraph, length: int = 10, weight: tuple[int, int] = (3, 7),
                          timespan: int = 16, min_time: int = 3) -> list[dict]:
    """
    Generate a random package list
    :param graph: The graph to generate a package list for.
    :param length: The length of the package list.
    :param weight: The weight of the packages in the list.
    :param timespan: The amount of time windows in which packages are sent/received.
    :param min_time: The minimum time for a package to be delivered.
    :return: The generated package list as a list of dictionary-packed package info.
    """
    # init
    cities = list(graph.nodes())
    cities_number = len(cities)
    if (timespan - min_time) < 1 or cities_number < 2:
        return []
    package_list = [{} for _ in range(length)]

    # generating packages
    for package in package_list:
        from_idx = randint(0, cities_number - 1)
        package["city_from"] = cities[from_idx]
        package["city_to"] = cities[(from_idx + randint(1, cities_number - 1)) % cities_number]
        package["date_ready"] = randint(0, timespan - min_time)
        package["date_delivery"] = randint(package["date_ready"] + min_time, timespan)
        package["weight"] = randint(weight[0], weight[1])

    return package_list