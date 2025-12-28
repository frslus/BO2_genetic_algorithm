from src.file_handling import *
from src.generate_graphs import *
from src.organisms_and_population import *


def main():
    graph, adj_list, _, _ = create_complete_graph(extended_output=True)
    # print(graph[0])
    print(adj_list["train"]["cost"])
    print(adj_list["train"]["johnson"])
    # print(graph[2])
    # print(graph[3])
    # TODO save graph and recover it from file || DONE :)
    j1 = johnson(graph, "train", "cost")
    print()
    for elem, d in j1.items(): print(elem, d[0], d[1])
    print()
    save_graph_to_file(graph, "data/test1.csv")
    new_graph = load_graph_from_file("data/test1.csv")
    #j1 = johnson(new_graph, "train", "cost")
    #print()
    #for elem, d in j1.items(): print(elem, d[0], d[1])
    #print()
    print(new_graph.nodes(data=True))
    print(str(graph.nodes(data=True)) == str(new_graph.nodes(data=True)))
    print(str(graph.edges(data=True)) == str(new_graph.edges(data=True)))
    g1 = Gene("xD1", 10, "car")
    g2 = Gene("xD2", 20, "car")
    g3 = Gene("xD3", 30, "train")
    g4 = Gene("xD4", 11, "train")
    g5 = Gene("xD5", 21, "train")
    g6 = Gene("xD6", 31, "train")
    g7 = Gene("xD5", 22, "train")
    gx = g1
    g1.mode_of_transit = "plane"
    # print(g1.mode_of_transit)
    ch1 = Chromosome([g1, g2, g3])
    # for elem in ch1:
    # print(elem)
    # print(ch1[0])
    # ch1[0] = g2
    # print(ch1)
    ch1[0] = g4
    # print(ch1)
    ch1.insert(0, g1)
    # print(ch1)
    ch1.append(g6)
    # print(ch1)
    ch1.pop(1)
    # print(ch1)
    ch1[0].date = 50
    # print(ch1)
    gen1 = Genotype([deepcopy(ch1), deepcopy(ch1)])
    org1 = Organism(gen1, graph)
    print(org1)
    org1.mutate(MutationType.TRANSIT_MODE)
    print(org1)
    package_list = [{"city_from": "xD1", "city_to": "xD2", "date_ready": 1, "date_delivery": 2, "weight": 10},
                    {"city_from": "xD3", "city_to": "xD4", "date_ready": 3, "date_delivery": 4, "weight": 20}]
    save_list_to_file(package_list, "data/test2.csv")
    new_list = load_list_from_file("data/test2.csv")
    print(package_list)
    print(new_list)


if __name__ == '__main__':
    main()
