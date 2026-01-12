import file_handling
from generate_graphs import *

# README: follow the numbered comments IN ORDER to generate your own graph
# (auto) points require no user input

# 1. generate cities
city_count = 20
# cities = generate_random_cities(count=city_count, bounds_cap=(10, 15), names=False)
# print(cities)
cities = [(0, 959, 717, 10), (1, 162, 751, 14), (2, 792, 73, 11), (3, 424, 911, 14), (4, 273, 271, 13),
          (5, 419, 153, 15), (6, 244, 529, 12), (7, 128, 336, 11), (8, 939, 296, 15), (9, 851, 928, 13),
          (10, 696, 469, 11), (11, 173, 674, 15), (12, 520, 358, 12), (13, 992, 767, 14), (14, 240, 958, 15),
          (15, 89, 12, 11), (16, 299, 973, 10), (17, 654, 981, 15), (18, 407, 913, 12), (19, 876, 670, 15)]

# 2. create graph (auto)
graph = create_multigraph(cities)
assign_cartesian_distances(graph)

# 3. generate airports
# airports = assign_airports(graph)
# print(airports)
airports = {0: True, 1: False, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: False, 9: False, 10: True,
            11: True, 12: True, 13: True, 14: True, 15: True, 16: False, 17: True, 18: False, 19: True}

# 4. generate railways
# railways = assign_train_costs(graph, train_mult=0.75, train_noise=0.15, railway_chance=0.8)
# print(railways)

railways = {(0, 1): 690.3958830185151, (0, 2): 524.771698835505, (0, 3): 500.83041426654336, (0, 4): 578.4425162765648,
            (0, 5): 675.154870421771, (0, 6): 450.95004432875055, (0, 7): 742.5915917788992, (0, 8): 267.35026931654613,
            (0, 9): 181.1389676666654, (0, 10): 266.26814485243875, (0, 11): 503.49092122816114,
            (0, 12): 510.22516501340135, (0, 13): 46.649212123063506, (0, 14): 540.3646450006946,
            (0, 15): 774.6753533185121, (0, 16): 457.7661623101749, (0, 17): 337.7718809958809,
            (0, 18): 510.9668103567459, (0, 19): 81.26881707083662, (1, 2): 741.6883962511051,
            (1, 3): 220.97210057081128, (1, 4): 435.77555621465154, (1, 5): 508.5719381119679,
            (1, 6): 165.56631638620158, (1, 7): 319.06301470044576, (1, 8): 680.5842125607815,
            (1, 9): 552.1602950910486, (1, 10): 389.8456148610664, (1, 11): 48.52949734247455,
            (1, 12): 375.91302896915556, (1, 13): 577.3323645460589, (1, 14): 175.92081388030653,
            (1, 15): 470.5736119669257, (1, 16): 232.18932775409652, (1, 17): 467.791391217238,
            (1, 18): 189.99199416504445, (1, 19): 608.7022284236284, (2, 3): 684.7696419625192,
            (2, 4): 358.7094812784315, (2, 5): 295.1494723650879, (2, 6): 549.3144584476723, (2, 7): 503.31386618208916,
            (2, 8): 200.75639778676603, (2, 9): 762.9320520640576, (2, 10): 246.26237126705155,
            (2, 11): 619.7485758391464, (2, 12): 269.6432084472144, (2, 13): 531.8284327251425,
            (2, 14): 835.7490295005119, (2, 15): 569.6851993345196, (2, 16): 724.6221209444508,
            (2, 17): 628.5843806403685, (2, 18): 707.3354427661044, (2, 19): 489.97637239547817,
            (3, 4): 551.9767668811998, (3, 5): 550.3566715888746, (3, 6): 265.3493839952733, (3, 7): 504.45890724002663,
            (3, 8): 587.0796692895182, (3, 9): 298.48085883535384, (3, 10): 369.1144815534943,
            (3, 11): 243.75962862111496, (3, 12): 340.8048788859096, (3, 13): 364.6594152235162,
            (3, 14): 118.39814393243398, (3, 15): 617.4114306259746, (3, 16): 100.72661788501001,
            (3, 17): 144.0432847603295, (3, 18): 11.164453702595992, (3, 19): 326.48727815793956,
            (4, 5): 142.4420791646625, (4, 6): 183.70078291516475, (4, 7): 103.4836814887936, (4, 8): 458.8613493397132,
            (4, 9): 574.8378893764964, (4, 10): 280.87832056351175, (4, 11): 261.2800016772663,
            (4, 12): 229.287290678197, (4, 13): 652.3994947701053, (4, 14): 544.5714121369947,
            (4, 15): 250.90980792556712, (4, 16): 472.4709247873152, (4, 17): 553.386265220423,
            (4, 18): 574.4936802140609, (4, 19): 435.75846611199836, (5, 6): 303.60694932039235,
            (5, 7): 258.8556930084984, (5, 8): 437.1392040389329, (5, 9): 701.1808752958884,
            (5, 10): 353.69949371141803, (5, 11): 447.7862081310147, (5, 12): 168.30520206669047,
            (5, 13): 535.4351300086756, (5, 14): 693.0339233768877, (5, 15): 237.51603943048195,
            (5, 16): 600.0019542196601, (5, 17): 622.4136598603163, (5, 18): 460.18840576972786,
            (5, 19): 440.2557662863687, (6, 7): 168.65699919587797, (6, 8): 492.287843709174, (6, 9): 521.2076441651443,
            (6, 10): 323.1171138417611, (6, 11): 121.57558655328299, (6, 12): 229.11159418149435,
            (6, 13): 504.8047173150054, (6, 14): 260.55466857828605, (6, 15): 401.62366328183333,
            (6, 16): 269.04795158588547, (6, 17): 546.4032283555915, (6, 18): 254.5581370311163,
            (6, 19): 582.2983036305911, (7, 8): 716.2452696753749, (7, 9): 623.0049102591912,
            (7, 10): 497.87323754445674, (7, 11): 246.55654867868648, (7, 12): 276.54717094839265,
            (7, 13): 768.2801096520751, (7, 14): 474.792006484461, (7, 15): 221.56675545496756,
            (7, 16): 446.24526271097636, (7, 17): 593.6772739417303, (7, 18): 525.0837310384153,
            (7, 19): 579.4602744593567, (8, 9): 418.12017801390334, (8, 10): 210.71252567462648,
            (8, 11): 713.9751167660654, (8, 12): 280.89724309801636, (8, 13): 318.47050839687313,
            (8, 14): 680.0229333809169, (8, 15): 690.0485236017436, (8, 16): 824.5206784639371,
            (8, 17): 512.2914998688798, (8, 18): 689.8228432269167, (8, 19): 309.53338685243705,
            (9, 10): 291.45030758678405, (9, 11): 651.020035893519, (9, 12): 422.2696726949119,
            (9, 13): 186.9192701507408, (9, 14): 509.7756154902445, (9, 15): 806.5133686229415,
            (9, 16): 372.80832478866995, (9, 17): 131.53141520355032, (9, 18): 303.740917254251,
            (9, 19): 214.05859863369693, (10, 11): 339.9539979669826, (10, 12): 157.95569062808778,
            (10, 13): 271.5706124011297, (10, 14): 554.5446829947763, (10, 15): 486.61997033424154,
            (10, 16): 485.3685120756731, (10, 17): 454.68520690690036, (10, 18): 342.28290816912147,
            (10, 19): 184.37037086846775, (11, 12): 353.2532688470047, (11, 13): 575.838822121288,
            (11, 14): 203.56570001092348, (11, 15): 412.614868421882, (11, 16): 261.49509315371955,
            (11, 17): 396.27289486128404, (11, 18): 268.8545086862966, (11, 19): 547.3694277041081,
            (12, 13): 459.36126390368884, (12, 14): 576.1367643417698, (12, 15): 344.5920062099652,
            (12, 16): 403.6690897645195, (12, 17): 400.6560085421385, (12, 18): 368.2538359194988,
            (12, 19): 344.56081040301314, (13, 14): 599.3510066252787, (13, 15): 861.1252538061179,
            (13, 16): 497.2901172416972, (13, 17): 257.27249448403995, (13, 18): 401.3497036462644,
            (13, 19): 124.08209014470958, (14, 15): 722.3712266200904, (14, 16): 53.79393121503595,
            (14, 17): 286.0339365898298, (14, 18): 114.5422750302273, (14, 19): 454.49173478063994,
            (15, 16): 768.9423340639644, (15, 17): 690.7998697262796, (15, 18): 642.5936550415943,
            (15, 19): 789.3464026583241, (16, 17): 283.3226218296412, (16, 18): 78.77273946734627,
            (16, 19): 505.97882843100814, (17, 18): 184.87926878817927, (17, 19): 320.15278797771964,
            (18, 19): 362.7470171991416}

# 5. choose randomness constants
kwargs = {"plane_mult": 2, "plane_noise": 0, "car_mult": 1.3, "car_noise": 0.2}

# 6. assign all costs (auto)
assign_train_costs(graph, railways)
assign_airports(graph, airports)
assign_plane_costs(graph, **kwargs)
assign_car_costs(graph, **kwargs)

# 7. decide on velocities
# velocities = {"plane": 600, "car": 100, "train": 60}
velocities = {"plane": 1500, "car": 250, "train": 100}

# 8. assign times (auto)
modes_of_transit = ("plane", "car", "train")

for layer in modes_of_transit:
    assign_times(graph, layer, velocities[layer])

# 9. generate package list
length = 10
kwargs = {"length": length, "weight": (3, 7), "timespan": 16, "min_time": 3}
package_list = generate_package_list(graph, **kwargs)
print(package_list)

# package_list = [{'city_from': 3, 'city_to': 5, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 5, 'city_to': 7, 'date_ready': 7, 'date_delivery': 10, 'weight': 7},
#                 {'city_from': 14, 'city_to': 0, 'date_ready': 2, 'date_delivery': 10, 'weight': 5},
#                 {'city_from': 10, 'city_to': 5, 'date_ready': 4, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 1, 'city_to': 9, 'date_ready': 0, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 13, 'city_to': 12, 'date_ready': 11, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 5, 'city_to': 14, 'date_ready': 1, 'date_delivery': 8, 'weight': 7},
#                 {'city_from': 2, 'city_to': 8, 'date_ready': 7, 'date_delivery': 12, 'weight': 4},
#                 {'city_from': 0, 'city_to': 3, 'date_ready': 12, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 2, 'city_to': 3, 'date_ready': 0, 'date_delivery': 3, 'weight': 6},
#                 {'city_from': 5, 'city_to': 1, 'date_ready': 4, 'date_delivery': 10, 'weight': 7},
#                 {'city_from': 1, 'city_to': 14, 'date_ready': 7, 'date_delivery': 10, 'weight': 7},
#                 {'city_from': 7, 'city_to': 13, 'date_ready': 10, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 14, 'city_to': 5, 'date_ready': 8, 'date_delivery': 12, 'weight': 3},
#                 {'city_from': 7, 'city_to': 14, 'date_ready': 6, 'date_delivery': 11, 'weight': 7},
#                 {'city_from': 6, 'city_to': 12, 'date_ready': 3, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 8, 'city_to': 6, 'date_ready': 6, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 5, 'city_to': 2, 'date_ready': 1, 'date_delivery': 8, 'weight': 3},
#                 {'city_from': 7, 'city_to': 9, 'date_ready': 7, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 2, 'city_to': 7, 'date_ready': 8, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 6, 'city_to': 0, 'date_ready': 9, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 7, 'city_to': 5, 'date_ready': 12, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 14, 'city_to': 3, 'date_ready': 0, 'date_delivery': 6, 'weight': 4},
#                 {'city_from': 8, 'city_to': 6, 'date_ready': 0, 'date_delivery': 9, 'weight': 6},
#                 {'city_from': 3, 'city_to': 14, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 8, 'city_to': 9, 'date_ready': 8, 'date_delivery': 12, 'weight': 5},
#                 {'city_from': 14, 'city_to': 5, 'date_ready': 0, 'date_delivery': 14, 'weight': 6},
#                 {'city_from': 14, 'city_to': 3, 'date_ready': 5, 'date_delivery': 9, 'weight': 4},
#                 {'city_from': 12, 'city_to': 1, 'date_ready': 9, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 0, 'city_to': 12, 'date_ready': 4, 'date_delivery': 9, 'weight': 5},
#                 {'city_from': 7, 'city_to': 10, 'date_ready': 0, 'date_delivery': 3, 'weight': 5},
#                 {'city_from': 13, 'city_to': 7, 'date_ready': 2, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 11, 'city_to': 0, 'date_ready': 3, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 11, 'city_to': 5, 'date_ready': 11, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 4, 'city_to': 12, 'date_ready': 7, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 1, 'city_to': 9, 'date_ready': 10, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 5, 'city_to': 11, 'date_ready': 7, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 9, 'city_to': 10, 'date_ready': 12, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 7, 'city_to': 5, 'date_ready': 5, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 1, 'city_to': 10, 'date_ready': 8, 'date_delivery': 13, 'weight': 7},
#                 {'city_from': 6, 'city_to': 14, 'date_ready': 2, 'date_delivery': 14, 'weight': 6},
#                 {'city_from': 13, 'city_to': 6, 'date_ready': 11, 'date_delivery': 15, 'weight': 7},
#                 {'city_from': 5, 'city_to': 8, 'date_ready': 9, 'date_delivery': 13, 'weight': 5},
#                 {'city_from': 7, 'city_to': 1, 'date_ready': 7, 'date_delivery': 12, 'weight': 5},
#                 {'city_from': 12, 'city_to': 6, 'date_ready': 10, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 7, 'city_to': 4, 'date_ready': 11, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 11, 'city_to': 14, 'date_ready': 12, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 8, 'city_to': 6, 'date_ready': 8, 'date_delivery': 14, 'weight': 6},
#                 {'city_from': 3, 'city_to': 0, 'date_ready': 7, 'date_delivery': 10, 'weight': 4},
#                 {'city_from': 1, 'city_to': 11, 'date_ready': 5, 'date_delivery': 12, 'weight': 4}]

# 10. select filenames
# FORMAT:
# graphCITY_COUNTEXTRA_INFO
# packagesPACKAGE_COUNTEXTRA_INFO_graphCITY_COUNTEXTRA_INFO
graph_filename = f"graph{city_count}"
packages_filename = f"packages{length}_graph{city_count}"

# 11. save to files (auto)
file_handling.save_graph_to_file(graph, f"../data/{graph_filename}.csv")
file_handling.save_list_to_file(package_list, f"../data/{packages_filename}.csv")
file_handling.save_graph()
