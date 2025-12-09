import csv
import networkx as nx


def save_to_file(graph: nx.MultiGraph, filename: str) -> None:
    """
    Save graph to CSV file.
    :param graph: The graph to save.
    :param filename: The path to the file the graph will be saved to.
    :return: None
    """
    cities_labels = list(graph.nodes())
    cities_number = len(cities_labels)
    nodes_data = dict(graph.nodes(data=True))
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        # save number of cities in the case (to use by load_from_file())
        w0 = csv.DictWriter(file, fieldnames=["cities_number"], delimiter=";")
        w0.writeheader()
        w0.writerow({"cities_number": cities_number})

        # save cities parameters
        w1 = csv.DictWriter(file, fieldnames=["cities"], delimiter=";")
        w1.writeheader()
        w2 = csv.DictWriter(file, fieldnames=["city", "x", "y", "capacity", "has_airport"], delimiter=";")
        w2.writeheader()

        # save distances and travel costs and times between all cities
        for city in cities_labels:
            row = {"city": city}
            for param in ["x", "y", "capacity", "has_airport"]:
                row[param] = nodes_data[city][param]
            w2.writerow(row)
        for layer, param_list in [("distance", ["cost"]), ("plane", ["cost", "time"]),
                                  ("train", ["cost", "time"]), ("car", ["cost", "time"])]:
            w3 = csv.DictWriter(file, fieldnames=[layer], delimiter=";")
            w3.writeheader()
            for param in param_list:
                w4 = csv.DictWriter(file, fieldnames=[param], delimiter=";")
                w4.writeheader()
                w5 = csv.DictWriter(file, fieldnames=["city"] + cities_labels, delimiter=";")
                w5.writeheader()
                for i in range(cities_number):
                    row = {"city": cities_labels[i]}
                    for j in range(i + 1):
                        row[cities_labels[j]] = ""
                    for j in range(i + 1, cities_number):
                        if (cities_labels[i], cities_labels[j]) in graph.edges():
                            row[cities_labels[j]] = graph[cities_labels[i]][cities_labels[j]][layer][param]
                        else:
                            row[cities_labels[j]] = graph[cities_labels[i]][cities_labels[j]][layer][param]
                    w5.writerow(row)


def load_from_file(filename: str) -> nx.MultiGraph:
    """
    Load graph from CSV file.
    :param filename: The path to the file where the graph is saved.
    :return graph: A reconstructed graph.
    """
    graph = nx.MultiGraph()
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader) # skip header "cities_number"
        cities_number = int(next(reader)[0])
        next(reader) # skip header "cities"
        next(reader) # skip header with city parameters
        cities_labels = []
        for i in range(cities_number):
            row = next(reader)
            cities_labels.append(row[0])
            graph.add_node(row[0], x=int(row[1]), y=int(row[2]), capacity=int(row[3]),
                           has_airport=True if row[4] == "True" else False)
        for layer, param_list in [("distance", [("cost", int)]), ("plane", [("cost", float), ("time", float)]),
                                  ("train", [("cost", float), ("time", float)]),
                                  ("car", [("cost", float), ("time", float)])]:
            next(reader) # skip header <layer>
            for param, p_type in param_list:
                next(reader) # skip header <param>
                next(reader) # skip cities labels
                for i, city_from in enumerate(cities_labels):
                    row = next(reader)
                    for j, city_to in enumerate(cities_labels[i + 1:], start=i + 1):
                        graph.add_edge(city_from, city_to, key=layer)
                        graph[city_from][city_to][layer][param] = p_type(row[j + 1])
    return graph
