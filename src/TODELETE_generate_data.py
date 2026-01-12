import file_handling
from generate_graphs import *

# README: follow the numbered comments IN ORDER to generate your own graph
# (auto) points require no user input

# 1. generate cities
# cities = generate_random_cities(count=15, names=False)
# print(cities)
cities = [(0, 717, 97, 0), (1, 371, 856, 4), (2, 445, 202, 8), (3, 300, 936, 2), (4, 515, 890, 4), (5, 521, 459, 2),
          (6, 514, 121, 9), (7, 434, 772, 8), (8, 503, 582, 0), (9, 300, 752, 0), (10, 315, 119, 6), (11, 634, 374, 3),
          (12, 966, 166, 4), (13, 401, 927, 7), (14, 812, 859, 6)]

# 2. create graph (auto)
graph = create_multigraph(cities)
assign_cartesian_distances(graph)

# 3. generate airports
# airports = assign_airports(graph)
# print(airports)
airports = {0: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True,
            11: False, 12: True, 13: False, 14: False}

# 4. generate railways
# railways = assign_train_costs(graph, train_mult=0.75, train_noise=0.15, railway_chance=0.6)
# print(railways)

railways = {(0, 1): 525.6817328516271, (0, 2): 213.44220436389932, (0, 3): 746.1641861721623, (0, 4): 691.7591322289862,
            (0, 5): 345.89854137776297, (0, 6): 143.880884215791, (0, 7): 610.8568833506771, (0, 8): 362.0653516211639,
            (0, 9): 482.59618646905466, (0, 10): 294.51714792154206, (0, 11): 247.74109213608457,
            (0, 12): 190.91097794758568, (0, 13): 620.7107152425043, (0, 14): 647.1774234345304,
            (1, 2): 437.7688253569157, (1, 3): 71.20790216667412, (1, 4): 127.8753233099083, (1, 5): 293.1946314908685,
            (1, 6): 540.0470138115389, (1, 7): 89.89888195539869, (1, 8): 200.64341765055144, (1, 9): 96.18728277170379,
            (1, 10): 515.596606630299, (1, 11): 345.99441900021947, (1, 12): 616.2108127359681,
            (1, 13): 48.80259876695101, (1, 14): 335.8220345375387, (2, 3): 593.0683153995075,
            (2, 4): 441.2460420996679, (2, 5): 183.90555103366654, (2, 6): 76.79226184165897, (2, 7): 422.1513460330963,
            (2, 8): 327.7999716184494, (2, 9): 343.4689480860258, (2, 10): 136.51148076346186,
            (2, 11): 196.7814608648195, (2, 12): 367.4257658981231, (2, 13): 608.1470856626543,
            (2, 14): 597.3409580378626, (3, 4): 191.25393719621945, (3, 5): 438.4433705975808,
            (3, 6): 564.3057368428753, (3, 7): 170.55622517768558, (3, 8): 274.3525313365157,
            (3, 9): 123.56927230594131, (3, 10): 528.189882997628, (3, 11): 496.8118369817263,
            (3, 12): 635.7183812013615, (3, 13): 64.45760303342145, (3, 14): 403.02603655406864,
            (4, 5): 296.93258786704416, (4, 6): 656.3409791458769, (4, 7): 101.08101221562889,
            (4, 8): 211.95735976256597, (4, 9): 167.79335593610585, (4, 10): 478.97144081718426,
            (4, 11): 434.64084451796276, (4, 12): 544.4218719387264, (4, 13): 88.02900691027345,
            (4, 14): 226.7511258869325, (5, 6): 286.30709648426597, (5, 7): 210.69162126258786,
            (5, 8): 104.09520537690135, (5, 9): 234.76672514295933, (5, 10): 292.35697381748133,
            (5, 11): 88.45109386718889, (5, 12): 455.33938467488167, (5, 13): 392.70508588367017,
            (5, 14): 443.0624079792102, (6, 7): 518.5914684133148, (6, 8): 290.3832344756258, (6, 9): 537.3689356516164,
            (6, 10): 159.04497078029559, (6, 11): 205.99190702262746, (6, 12): 382.30583248424546,
            (6, 13): 503.1406720665292, (6, 14): 540.0750388067023, (7, 8): 129.71298883095344,
            (7, 9): 106.66767502759564, (7, 10): 580.9962556657687, (7, 11): 362.2283977459542,
            (7, 12): 712.768890892018, (7, 13): 110.7562439959392, (7, 14): 291.0707216873211, (8, 9): 159.590794629019,
            (8, 10): 441.65362486400005, (8, 11): 161.82221939193533, (8, 12): 389.6142153594503,
            (8, 13): 265.02761913212703, (8, 14): 265.29278394332863, (9, 10): 528.9180091059637,
            (9, 11): 441.32575362893516, (9, 12): 709.3635119116939, (9, 13): 142.3024835641287,
            (9, 14): 386.1142496497733, (10, 11): 361.8779289046067, (10, 12): 431.55643696737536,
            (10, 13): 549.627872577111, (10, 14): 712.5795737031302, (11, 12): 290.78263135751007,
            (11, 13): 534.6968989965729, (11, 14): 421.36264323545817, (12, 13): 820.8245754196399,
            (12, 14): 600.7836251602025, (13, 14): 275.45590662579804}

# 5. choose randomness constants
kwargs = {"plane_mult": 2, "plane_noise": 0, "car_mult": 1.3, "car_noise": 0.2}

# 6. assign all costs (auto)
assign_train_costs(graph, railways)
assign_airports(graph, airports)
assign_plane_costs(graph, **kwargs)
assign_car_costs(graph, **kwargs)

# 7. decide on velocities
velocities = {"plane": 600, "car": 100, "train": 60}

# 8. assign times (auto)
modes_of_transit = ("plane", "car", "train")

for layer in modes_of_transit:
    assign_times(graph, layer, velocities[layer])

# 9. generate package list
kwargs = {"length": 50, "weight": (3, 7), "timespan": 16, "min_time": 3}
package_list = generate_package_list(graph, **kwargs)
print(package_list)

# package_list = [{'city_from': 11, 'city_to': 3, 'date_ready': 13, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 9, 'city_to': 14, 'date_ready': 4, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 7, 'city_to': 13, 'date_ready': 4, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 4, 'city_to': 6, 'date_ready': 10, 'date_delivery': 13, 'weight': 3},
#                 {'city_from': 0, 'city_to': 11, 'date_ready': 6, 'date_delivery': 13, 'weight': 7},
#                 {'city_from': 4, 'city_to': 12, 'date_ready': 13, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 13, 'city_to': 5, 'date_ready': 0, 'date_delivery': 10, 'weight': 6},
#                 {'city_from': 5, 'city_to': 7, 'date_ready': 2, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 6, 'city_to': 7, 'date_ready': 0, 'date_delivery': 9, 'weight': 3},
#                 {'city_from': 6, 'city_to': 2, 'date_ready': 2, 'date_delivery': 8, 'weight': 6},
#                 {'city_from': 3, 'city_to': 9, 'date_ready': 7, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 11, 'city_to': 1, 'date_ready': 7, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 8, 'city_to': 9, 'date_ready': 5, 'date_delivery': 11, 'weight': 7},
#                 {'city_from': 2, 'city_to': 7, 'date_ready': 4, 'date_delivery': 14, 'weight': 5},
#                 {'city_from': 14, 'city_to': 3, 'date_ready': 10, 'date_delivery': 13, 'weight': 4},
#                 {'city_from': 12, 'city_to': 0, 'date_ready': 7, 'date_delivery': 14, 'weight': 5},
#                 {'city_from': 10, 'city_to': 3, 'date_ready': 4, 'date_delivery': 9, 'weight': 6},
#                 {'city_from': 11, 'city_to': 8, 'date_ready': 7, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 6, 'city_to': 13, 'date_ready': 6, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 6, 'city_to': 2, 'date_ready': 10, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 8, 'city_to': 9, 'date_ready': 2, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 1, 'city_to': 11, 'date_ready': 13, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 1, 'city_to': 0, 'date_ready': 3, 'date_delivery': 10, 'weight': 4},
#                 {'city_from': 13, 'city_to': 1, 'date_ready': 10, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 9, 'city_to': 6, 'date_ready': 7, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 11, 'city_to': 13, 'date_ready': 3, 'date_delivery': 10, 'weight': 6},
#                 {'city_from': 14, 'city_to': 13, 'date_ready': 6, 'date_delivery': 10, 'weight': 7},
#                 {'city_from': 11, 'city_to': 9, 'date_ready': 7, 'date_delivery': 13, 'weight': 3},
#                 {'city_from': 6, 'city_to': 2, 'date_ready': 3, 'date_delivery': 8, 'weight': 4},
#                 {'city_from': 5, 'city_to': 10, 'date_ready': 4, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 4, 'city_to': 11, 'date_ready': 9, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 7, 'city_to': 14, 'date_ready': 12, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 2, 'city_to': 12, 'date_ready': 7, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 4, 'city_to': 0, 'date_ready': 6, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 10, 'city_to': 4, 'date_ready': 7, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 1, 'city_to': 13, 'date_ready': 9, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 1, 'city_to': 3, 'date_ready': 3, 'date_delivery': 9, 'weight': 3},
#                 {'city_from': 4, 'city_to': 3, 'date_ready': 12, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 10, 'city_to': 13, 'date_ready': 4, 'date_delivery': 7, 'weight': 3},
#                 {'city_from': 2, 'city_to': 1, 'date_ready': 10, 'date_delivery': 13, 'weight': 7},
#                 {'city_from': 9, 'city_to': 8, 'date_ready': 7, 'date_delivery': 13, 'weight': 3},
#                 {'city_from': 3, 'city_to': 8, 'date_ready': 2, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 6, 'city_to': 13, 'date_ready': 3, 'date_delivery': 10, 'weight': 3},
#                 {'city_from': 14, 'city_to': 1, 'date_ready': 4, 'date_delivery': 8, 'weight': 3},
#                 {'city_from': 6, 'city_to': 9, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 12, 'city_to': 10, 'date_ready': 4, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 0, 'city_to': 10, 'date_ready': 11, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 6, 'city_to': 10, 'date_ready': 7, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 9, 'city_to': 13, 'date_ready': 5, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 2, 'city_to': 1, 'date_ready': 0, 'date_delivery': 12, 'weight': 7},
#                 {'city_from': 7, 'city_to': 13, 'date_ready': 4, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 0, 'city_to': 11, 'date_ready': 5, 'date_delivery': 14, 'weight': 5},
#                 {'city_from': 8, 'city_to': 2, 'date_ready': 4, 'date_delivery': 7, 'weight': 7},
#                 {'city_from': 11, 'city_to': 6, 'date_ready': 7, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 8, 'city_to': 7, 'date_ready': 5, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 11, 'city_to': 12, 'date_ready': 9, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 1, 'city_to': 0, 'date_ready': 10, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 1, 'city_to': 11, 'date_ready': 0, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 11, 'city_to': 2, 'date_ready': 9, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 7, 'city_to': 13, 'date_ready': 8, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 6, 'city_to': 10, 'date_ready': 0, 'date_delivery': 7, 'weight': 6},
#                 {'city_from': 11, 'city_to': 8, 'date_ready': 11, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 10, 'city_to': 8, 'date_ready': 3, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 7, 'city_to': 2, 'date_ready': 1, 'date_delivery': 5, 'weight': 3},
#                 {'city_from': 11, 'city_to': 2, 'date_ready': 1, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 2, 'city_to': 12, 'date_ready': 12, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 7, 'city_to': 12, 'date_ready': 2, 'date_delivery': 6, 'weight': 4},
#                 {'city_from': 0, 'city_to': 3, 'date_ready': 9, 'date_delivery': 12, 'weight': 5},
#                 {'city_from': 10, 'city_to': 2, 'date_ready': 4, 'date_delivery': 11, 'weight': 7},
#                 {'city_from': 5, 'city_to': 0, 'date_ready': 4, 'date_delivery': 11, 'weight': 6},
#                 {'city_from': 7, 'city_to': 4, 'date_ready': 4, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 11, 'city_to': 8, 'date_ready': 6, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 0, 'city_to': 3, 'date_ready': 0, 'date_delivery': 6, 'weight': 3},
#                 {'city_from': 12, 'city_to': 14, 'date_ready': 8, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 2, 'city_to': 11, 'date_ready': 0, 'date_delivery': 9, 'weight': 3},
#                 {'city_from': 14, 'city_to': 4, 'date_ready': 3, 'date_delivery': 14, 'weight': 6},
#                 {'city_from': 14, 'city_to': 5, 'date_ready': 8, 'date_delivery': 13, 'weight': 3},
#                 {'city_from': 11, 'city_to': 7, 'date_ready': 2, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 1, 'city_to': 3, 'date_ready': 11, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 13, 'city_to': 5, 'date_ready': 1, 'date_delivery': 5, 'weight': 5},
#                 {'city_from': 13, 'city_to': 12, 'date_ready': 0, 'date_delivery': 4, 'weight': 4},
#                 {'city_from': 9, 'city_to': 6, 'date_ready': 1, 'date_delivery': 6, 'weight': 7},
#                 {'city_from': 4, 'city_to': 7, 'date_ready': 13, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 2, 'city_to': 12, 'date_ready': 4, 'date_delivery': 13, 'weight': 4},
#                 {'city_from': 6, 'city_to': 13, 'date_ready': 9, 'date_delivery': 14, 'weight': 5},
#                 {'city_from': 1, 'city_to': 8, 'date_ready': 1, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 0, 'city_to': 7, 'date_ready': 13, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 0, 'city_to': 5, 'date_ready': 4, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 14, 'city_to': 9, 'date_ready': 2, 'date_delivery': 12, 'weight': 3},
#                 {'city_from': 7, 'city_to': 8, 'date_ready': 0, 'date_delivery': 12, 'weight': 5},
#                 {'city_from': 13, 'city_to': 14, 'date_ready': 1, 'date_delivery': 9, 'weight': 5},
#                 {'city_from': 13, 'city_to': 3, 'date_ready': 12, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 11, 'city_to': 5, 'date_ready': 13, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 9, 'city_to': 1, 'date_ready': 9, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 14, 'city_to': 1, 'date_ready': 4, 'date_delivery': 13, 'weight': 4},
#                 {'city_from': 8, 'city_to': 6, 'date_ready': 12, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 6, 'city_to': 11, 'date_ready': 10, 'date_delivery': 15, 'weight': 7},
#                 {'city_from': 6, 'city_to': 8, 'date_ready': 2, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 1, 'city_to': 2, 'date_ready': 9, 'date_delivery': 13, 'weight': 7},
#                 {'city_from': 5, 'city_to': 0, 'date_ready': 5, 'date_delivery': 10, 'weight': 4},
#                 {'city_from': 10, 'city_to': 11, 'date_ready': 3, 'date_delivery': 13, 'weight': 5},
#                 {'city_from': 11, 'city_to': 8, 'date_ready': 2, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 2, 'city_to': 7, 'date_ready': 11, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 4, 'city_to': 5, 'date_ready': 9, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 8, 'city_to': 3, 'date_ready': 11, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 10, 'city_to': 13, 'date_ready': 9, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 6, 'city_to': 14, 'date_ready': 11, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 14, 'city_to': 13, 'date_ready': 6, 'date_delivery': 10, 'weight': 6},
#                 {'city_from': 8, 'city_to': 9, 'date_ready': 5, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 12, 'city_to': 14, 'date_ready': 6, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 3, 'city_to': 13, 'date_ready': 12, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 10, 'city_to': 5, 'date_ready': 0, 'date_delivery': 6, 'weight': 4},
#                 {'city_from': 5, 'city_to': 14, 'date_ready': 0, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 7, 'city_to': 5, 'date_ready': 9, 'date_delivery': 13, 'weight': 3},
#                 {'city_from': 4, 'city_to': 9, 'date_ready': 3, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 13, 'city_to': 0, 'date_ready': 1, 'date_delivery': 8, 'weight': 7},
#                 {'city_from': 3, 'city_to': 12, 'date_ready': 0, 'date_delivery': 15, 'weight': 7},
#                 {'city_from': 9, 'city_to': 10, 'date_ready': 10, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 1, 'city_to': 14, 'date_ready': 12, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 1, 'city_to': 4, 'date_ready': 8, 'date_delivery': 13, 'weight': 4},
#                 {'city_from': 9, 'city_to': 14, 'date_ready': 13, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 5, 'city_to': 4, 'date_ready': 6, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 0, 'city_to': 9, 'date_ready': 4, 'date_delivery': 9, 'weight': 7},
#                 {'city_from': 5, 'city_to': 11, 'date_ready': 8, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 3, 'city_to': 5, 'date_ready': 13, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 6, 'city_to': 10, 'date_ready': 6, 'date_delivery': 11, 'weight': 4},
#                 {'city_from': 3, 'city_to': 11, 'date_ready': 3, 'date_delivery': 8, 'weight': 6},
#                 {'city_from': 7, 'city_to': 14, 'date_ready': 4, 'date_delivery': 8, 'weight': 7},
#                 {'city_from': 1, 'city_to': 5, 'date_ready': 12, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 1, 'city_to': 7, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 3, 'city_to': 11, 'date_ready': 12, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 5, 'city_to': 6, 'date_ready': 10, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 7, 'city_to': 9, 'date_ready': 13, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 6, 'city_to': 11, 'date_ready': 0, 'date_delivery': 10, 'weight': 3},
#                 {'city_from': 8, 'city_to': 0, 'date_ready': 4, 'date_delivery': 10, 'weight': 4},
#                 {'city_from': 8, 'city_to': 10, 'date_ready': 6, 'date_delivery': 10, 'weight': 5},
#                 {'city_from': 3, 'city_to': 4, 'date_ready': 1, 'date_delivery': 15, 'weight': 6},
#                 {'city_from': 8, 'city_to': 3, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 12, 'city_to': 9, 'date_ready': 11, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 10, 'city_to': 2, 'date_ready': 8, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 2, 'city_to': 3, 'date_ready': 12, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 6, 'city_to': 13, 'date_ready': 7, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 8, 'city_to': 10, 'date_ready': 7, 'date_delivery': 13, 'weight': 5},
#                 {'city_from': 2, 'city_to': 4, 'date_ready': 4, 'date_delivery': 10, 'weight': 5},
#                 {'city_from': 0, 'city_to': 7, 'date_ready': 4, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 14, 'city_to': 0, 'date_ready': 1, 'date_delivery': 12, 'weight': 3},
#                 {'city_from': 10, 'city_to': 6, 'date_ready': 0, 'date_delivery': 10, 'weight': 6},
#                 {'city_from': 10, 'city_to': 14, 'date_ready': 0, 'date_delivery': 4, 'weight': 6},
#                 {'city_from': 0, 'city_to': 6, 'date_ready': 4, 'date_delivery': 14, 'weight': 6},
#                 {'city_from': 14, 'city_to': 2, 'date_ready': 13, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 4, 'city_to': 5, 'date_ready': 10, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 3, 'city_to': 7, 'date_ready': 10, 'date_delivery': 15, 'weight': 3},
#                 {'city_from': 1, 'city_to': 14, 'date_ready': 13, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 6, 'city_to': 7, 'date_ready': 8, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 5, 'city_to': 8, 'date_ready': 13, 'date_delivery': 16, 'weight': 6},
#                 {'city_from': 2, 'city_to': 12, 'date_ready': 9, 'date_delivery': 14, 'weight': 5},
#                 {'city_from': 1, 'city_to': 11, 'date_ready': 9, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 9, 'city_to': 12, 'date_ready': 5, 'date_delivery': 8, 'weight': 6},
#                 {'city_from': 12, 'city_to': 9, 'date_ready': 13, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 12, 'city_to': 8, 'date_ready': 4, 'date_delivery': 11, 'weight': 5},
#                 {'city_from': 11, 'city_to': 12, 'date_ready': 9, 'date_delivery': 16, 'weight': 7},
#                 {'city_from': 2, 'city_to': 1, 'date_ready': 2, 'date_delivery': 8, 'weight': 4},
#                 {'city_from': 11, 'city_to': 13, 'date_ready': 3, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 13, 'city_to': 2, 'date_ready': 7, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 0, 'city_to': 8, 'date_ready': 6, 'date_delivery': 11, 'weight': 7},
#                 {'city_from': 10, 'city_to': 5, 'date_ready': 3, 'date_delivery': 14, 'weight': 4},
#                 {'city_from': 3, 'city_to': 0, 'date_ready': 9, 'date_delivery': 12, 'weight': 5},
#                 {'city_from': 6, 'city_to': 9, 'date_ready': 1, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 7, 'city_to': 3, 'date_ready': 12, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 3, 'city_to': 12, 'date_ready': 13, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 12, 'city_to': 11, 'date_ready': 5, 'date_delivery': 10, 'weight': 4},
#                 {'city_from': 9, 'city_to': 6, 'date_ready': 9, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 1, 'city_to': 8, 'date_ready': 5, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 3, 'city_to': 10, 'date_ready': 8, 'date_delivery': 15, 'weight': 7},
#                 {'city_from': 10, 'city_to': 6, 'date_ready': 0, 'date_delivery': 6, 'weight': 6},
#                 {'city_from': 5, 'city_to': 10, 'date_ready': 3, 'date_delivery': 6, 'weight': 4},
#                 {'city_from': 3, 'city_to': 1, 'date_ready': 9, 'date_delivery': 12, 'weight': 6},
#                 {'city_from': 7, 'city_to': 3, 'date_ready': 3, 'date_delivery': 12, 'weight': 3},
#                 {'city_from': 8, 'city_to': 5, 'date_ready': 3, 'date_delivery': 10, 'weight': 7},
#                 {'city_from': 12, 'city_to': 14, 'date_ready': 13, 'date_delivery': 16, 'weight': 3},
#                 {'city_from': 7, 'city_to': 11, 'date_ready': 1, 'date_delivery': 5, 'weight': 4},
#                 {'city_from': 7, 'city_to': 1, 'date_ready': 4, 'date_delivery': 7, 'weight': 4},
#                 {'city_from': 8, 'city_to': 2, 'date_ready': 8, 'date_delivery': 14, 'weight': 3},
#                 {'city_from': 9, 'city_to': 2, 'date_ready': 1, 'date_delivery': 9, 'weight': 4},
#                 {'city_from': 3, 'city_to': 2, 'date_ready': 12, 'date_delivery': 15, 'weight': 4},
#                 {'city_from': 7, 'city_to': 4, 'date_ready': 3, 'date_delivery': 10, 'weight': 3},
#                 {'city_from': 5, 'city_to': 10, 'date_ready': 2, 'date_delivery': 10, 'weight': 5},
#                 {'city_from': 14, 'city_to': 1, 'date_ready': 0, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 8, 'city_to': 5, 'date_ready': 3, 'date_delivery': 7, 'weight': 3},
#                 {'city_from': 1, 'city_to': 10, 'date_ready': 2, 'date_delivery': 8, 'weight': 3},
#                 {'city_from': 12, 'city_to': 5, 'date_ready': 8, 'date_delivery': 11, 'weight': 7},
#                 {'city_from': 7, 'city_to': 8, 'date_ready': 3, 'date_delivery': 13, 'weight': 6},
#                 {'city_from': 10, 'city_to': 9, 'date_ready': 3, 'date_delivery': 7, 'weight': 3},
#                 {'city_from': 0, 'city_to': 10, 'date_ready': 5, 'date_delivery': 11, 'weight': 3},
#                 {'city_from': 10, 'city_to': 5, 'date_ready': 12, 'date_delivery': 15, 'weight': 5},
#                 {'city_from': 5, 'city_to': 11, 'date_ready': 11, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 9, 'city_to': 0, 'date_ready': 13, 'date_delivery': 16, 'weight': 5},
#                 {'city_from': 8, 'city_to': 9, 'date_ready': 9, 'date_delivery': 13, 'weight': 7},
#                 {'city_from': 11, 'city_to': 10, 'date_ready': 11, 'date_delivery': 16, 'weight': 4},
#                 {'city_from': 9, 'city_to': 5, 'date_ready': 10, 'date_delivery': 15, 'weight': 5}]

# 10. select filenames
# FORMAT:
# graphCITY_COUNTEXTRA_INFO
# packagesPACKAGE_COUNTEXTRA_INFO_graphCITY_COUNTEXTRA_INFO
graph_filename = "graph15"
packages_filename = "packages50_graph15"

# 11. save to files (auto)
# file_handling.save_graph_to_file(graph, f"../data/{graph_filename}.csv")
file_handling.save_list_to_file(package_list, f"../data/{packages_filename}.csv")
file_handling.save_graph()
