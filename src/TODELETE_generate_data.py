import file_handling
from generate_graphs import *

# README: follow the numbered comments IN ORDER to generate your own graph
# (auto) points require no user input

# 1. generate cities
# cities = generate_random_cities(count=12,names=False)
# print(cities)
cities = [(0, 689, 688, 9), (1, 769, 105, 7), (2, 250, 132, 1), (3, 274, 461, 7), (4, 807, 6, 6), (5, 785, 819, 1),
          (6, 507, 521, 9), (7, 785, 892, 1), (8, 642, 956, 2), (9, 935, 378, 4), (10, 477, 662, 10), (11, 212, 820, 6)]

# 2. create graph (auto)
graph = create_multigraph(cities)
assign_cartesian_distances(graph)

# 3. generate airports
# airports = assign_airports(graph)
# print(airports)
airports = {0: True, 1: False, 2: True, 3: False, 4: True, 5: False, 6: True, 7: True, 8: True, 9: True, 10: True,
            11: True}

# 4. generate railways
# railways = assign_train_costs(graph, train_mult=0.75, train_noise=0.15, railway_chance=0.75)
# print(railways)

railways = {(0, 1): 502.0685686565512, (0, 2): 485.1021633535401, (0, 3): 336.07003653262194, (0, 4): 501.0284793990241,
            (0, 5): 99.12350518222837, (0, 6): 161.60657594365145, (0, 7): 198.1887628467883,
            (0, 8): 223.26928573227963, (0, 9): 255.8360046788212, (0, 10): 163.05023875953805,
            (0, 11): 340.9648440478381, (1, 2): 401.5017413523384, (1, 3): 414.1811928870804, (1, 4): 68.46874948010087,
            (1, 5): 601.1744635837777, (1, 6): 317.9778771525043, (1, 7): 704.3720372259264, (1, 8): 770.0251275093615,
            (1, 9): 250.64348977992756, (1, 10): 447.55957660941783, (1, 11): 565.7302348381174,
            (2, 3): 285.48925557308127, (2, 4): 363.5664804153615, (2, 5): 674.1979622225945, (2, 6): 407.9953507365072,
            (2, 7): 630.3158124489912, (2, 8): 814.1206899217281, (2, 9): 636.1032421582638, (2, 10): 475.030789519051,
            (2, 11): 505.24197312005555, (3, 4): 621.6674862874377, (3, 5): 499.87236916774987,
            (3, 6): 174.10065516095102, (3, 7): 506.32712670487183, (3, 8): 483.947498645748, (3, 9): 590.0350742906236,
            (3, 10): 240.5362260002478, (3, 11): 307.7026972053082, (4, 5): 699.8120555070303,
            (4, 6): 371.6326340967447, (4, 7): 638.3618206180354, (4, 8): 650.04913467498, (4, 9): 285.6819656184814,
            (4, 10): 616.8563554608911, (4, 11): 684.7238601476538, (5, 6): 349.7530593770503,
            (5, 7): 56.56852728021082, (5, 8): 133.0328116952773, (5, 9): 413.39149289519656,
            (5, 10): 267.51136920456497, (5, 11): 414.4838896806353, (6, 7): 311.7072065079135,
            (6, 8): 286.41887825534036, (6, 9): 339.50717240635043, (6, 10): 90.085395262009,
            (6, 11): 367.55443157780667, (7, 8): 102.41649589649394, (7, 9): 421.79519001237827,
            (7, 10): 252.10241851446926, (7, 11): 462.4570429157246, (8, 9): 395.79204845935897,
            (8, 10): 269.46804491989525, (8, 11): 325.3034351837458, (9, 10): 428.8974576898797,
            (9, 11): 697.3385404440671, (10, 11): 247.40693473830459}

# 5. choose randomness constants
kwargs = {"plane_mult": 2, "plane_noise": 0, "car_mult": 1.3, "car_noise": 0.2}

# 6. assign all costs (auto)
assign_train_costs(graph, railways)
assign_airports(graph, airports)
assign_plane_costs(graph, **kwargs)
assign_car_costs(graph, **kwargs)

# 7. decide on velocities
velocities = {"plane": 1500, "car": 250, "train": 100}

# 8. assign times (auto)
modes_of_transit = ("plane", "car", "train")

for layer in modes_of_transit:
    assign_times(graph, layer, velocities[layer])

# 9. generate package list
# kwargs = {"length": 10, "weight":(3, 7),"timespan": 16,"min_time": 3}
# package_list = generate_package_list(graph,**kwargs)
# print(package_list)

package_list = [{'city_from': 9, 'city_to': 3, 'date_ready': 11, 'date_delivery': 14, 'weight': 3},
                {'city_from': 4, 'city_to': 10, 'date_ready': 2, 'date_delivery': 11, 'weight': 5},
                {'city_from': 4, 'city_to': 9, 'date_ready': 3, 'date_delivery': 7, 'weight': 5},
                {'city_from': 6, 'city_to': 7, 'date_ready': 7, 'date_delivery': 16, 'weight': 6},
                {'city_from': 2, 'city_to': 6, 'date_ready': 12, 'date_delivery': 15, 'weight': 6},
                {'city_from': 1, 'city_to': 0, 'date_ready': 0, 'date_delivery': 14, 'weight': 7},
                {'city_from': 2, 'city_to': 5, 'date_ready': 3, 'date_delivery': 8, 'weight': 7},
                {'city_from': 1, 'city_to': 5, 'date_ready': 5, 'date_delivery': 10, 'weight': 6},
                {'city_from': 7, 'city_to': 8, 'date_ready': 2, 'date_delivery': 9, 'weight': 7},
                {'city_from': 9, 'city_to': 10, 'date_ready': 5, 'date_delivery': 16, 'weight': 5}]

# 10. select filenames
graph_filename = "test_graph2"
packages_filename = "test_packages2"

# 11. save to files (auto)
file_handling.save_graph_to_file(graph, f"../data/{graph_filename}.csv")
file_handling.save_list_to_file(package_list, f"../data/{packages_filename}.csv")
