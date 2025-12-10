from copy import deepcopy

import networkx as nx

class TransportProblemObject:
    def __init__(self, cities_graph: nx.MultiGraph, packages_list: list[dict]):
        param_list = [(cities_graph, nx.MultiGraph), (packages_list, list[dict])]
        for param, ptype in param_list:
            if not isinstance(param, ptype):
                raise TypeError(f"Parameter {param} must be of type {ptype}, not {type(param)}")
        self.__cities_graph = deepcopy(cities_graph)
        self.__packages_list = deepcopy(packages_list)
