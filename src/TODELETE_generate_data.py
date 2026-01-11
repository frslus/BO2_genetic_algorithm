from generate_graphs import *
import file_handling
# sandbox
# cities = generate_random_cities(count=12,names=False)
# print(cities)

cities = [(0, 883, 225, 3), (1, 118, 412, 0), (2, 627, 413, 1), (3, 236, 871, 8), (4, 326, 761, 2), (5, 992, 515, 9),
          (6, 857, 667, 7), (7, 395, 75, 2), (8, 190, 362, 5), (9, 198, 604, 10), (10, 483, 494, 1), (11, 86, 740, 6)]
graph = create_multigraph(cities)
assign_cartesian_distances(graph)
# airports = assign_airports(graph)
airports = {0: True, 1: False, 2: True, 3: False, 4: True, 5: False, 6: True, 7: True, 8: True, 9: True, 10: True,
            11: True}
#print(airports)
assign_airports(graph, airports)
assign_plane_costs(graph, plane_mult=2)
assign_car_costs(graph, car_mult=1.3, car_cost=0.2)
# railways = assign_train_costs(graph, train_mult=0.75, train_cost=0.15)

railways = {(0, 1): 566.1726486579831, (0, 2): 227.7798872497017, (0, 3): 696.2197358265571, (0, 4): 595.9916100638955,
            (0, 5): 219.90026299078158, (0, 6): 333.9865332720197, (0, 7): 363.2630048022153,
            (0, 8): 510.25513175184886, (0, 9): 623.2282196385733, (0, 10): 366.95272486549754,
            (0, 11): 754.404238323602, (1, 2): 404.031894664946, (1, 3): 346.0775993722252, (1, 4): 293.12110155660235,
            (1, 5): 673.6575319937183, (1, 6): 621.3807562581178, (1, 7): 335.1218066615643, (1, 8): 62.73596885732308,
            (1, 9): 158.94226972401233, (1, 10): 275.8051022510165, (1, 11): 235.58342288171895,
            (2, 3): 481.13636093731566, (2, 4): 363.49695781309555, (2, 5): 293.02428416070677,
            (2, 6): 270.7558527394893, (2, 7): 291.5523144438865, (2, 8): 348.782365779515, (2, 9): 337.08620552139774,
            (2, 10): 117.31320814605522, (2, 11): 495.91790273187183, (3, 4): 102.8586599474667,
            (3, 5): 608.3426869913719, (3, 6): 521.2038748574582, (3, 7): 590.4118247986244, (3, 8): 364.76105927478966,
            (3, 9): 193.01764650444952, (3, 10): 334.5154341741673, (3, 11): 147.54958423851187,
            (4, 5): 509.92250508062597, (4, 6): 411.9372742802684, (4, 7): 529.7345040162932, (4, 8): 317.6166886706027,
            (4, 9): 159.94546682454902, (4, 10): 246.9295863635004, (4, 11): 175.84106294143083,
            (5, 6): 147.28776210436345, (5, 7): 555.1347701351064, (5, 8): 586.2340639471818, (5, 9): 631.8240218773025,
            (5, 10): 401.51406060691227, (5, 11): 709.8323010199477, (6, 7): 529.582164561078,
            (6, 8): 532.3859329647288, (6, 9): 512.1698221528875, (6, 10): 306.9623917886402,
            (6, 11): 594.3032712455662, (7, 8): 280.88649957636176, (7, 9): 438.35141348640207,
            (7, 10): 324.6587287061987, (7, 11): 517.5798788100132, (8, 9): 178.77033219269313,
            (8, 10): 247.8582827754796, (8, 11): 305.1475480996172, (9, 10): 242.10951614403794,
            (9, 11): 133.4207924494085, (10, 11): 371.3788057611953}

assign_train_costs(graph, railways)

modes_of_transit = ("plane", "car", "train")
velocities = {"plane": 1500, "car": 250, "train": 100}
for layer in modes_of_transit:
    assign_times(graph, layer, velocities[layer])

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

file_handling.save_graph_to_file(graph, "../data/test_graph.csv")

# print(generate_package_list(graph))

#
# graph = create_complete_graph(cities=cities)
