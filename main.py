from src.file_handling import *
from src.generate_graphs import *
from src.organisms_and_population import *


def main():
    graph = create_complete_graph(extended_output=False)
    # print(graph[0])
    # print(graph[1])
    # print(graph[2])
    # print(graph[3])
    print(graph.nodes(data=True), type(graph.nodes(data=True)))  # TODO save graph and recover it from file || DONE :)
    save_to_file(graph, "data/test1.csv")
    new_graph = load_from_file("data/test1.csv")
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



if __name__ == '__main__':
    main()
