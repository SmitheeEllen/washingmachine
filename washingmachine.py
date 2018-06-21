import numpy as np
import pprint
np.set_printoptions(suppress=True)
import csv
from prettytable import PrettyTable

## set here the prices for current and water:
current_huf_per_kWh = 35.31
water_huf_per_m3 = 218.95


column_labels = ['Programme', 'Temperature (C)', 'Max weight (kg)', 'Runtime (min)', 'Water (l)', 'Current (kWh)']
row_labels = \
    ['Pamut 90',
     'Előmosás-Pamut 60',
     'Pamut 40',
     'Pamut Hideg',
     'Pamut Eco 60 5kg',
     'Pamut Eco 60 2.5kg',
     'Pamut Eco 40',
     'Szintetikus 60',
     'Szintetikus 40',
     'Szintetikus Hideg',
     'Kényes ruhadarabok',
     'Gyapjú',
     'Kézi mosás',
     'Mini 30',
     ]


washmachine = np.array([[1, 90, 5, 130, 53, 1.63],
                        [2, 60, 5, 115, 64, 1.10],
                        [3, 40, 5, 120, 50, 0.97],
                        [4, 0, 5, 120, 52, 0.10],
                        [15.1, 60, 5, 145, 45, 0.80],
                        [15.2, 60, 2.5, 145, 38, 0.75],
                        [14, 40, 2.5, 116, 38, 0.65],
                        [13, 60, 2.5, 113, 55, 1.02],
                        [12, 40, 2.5, 105, 54, 0.50],
                        [11, 0, 2.5, 66, 52, 0.10],
                        [9, 30, 2.0, 61, 47, 0.26],
                        [10, 40, 1.5, 54, 50, 0.35],
                        [6, 20, 1.0, 41, 34, 0.20],
                        [5, 30, 2.5, 29, 72, 0.21]])

washmachine_params = washmachine[0:14,1:6]

prog_label_pairs = []
for i in range(len(washmachine)):
    prog_label_pairs.append((washmachine[i][0], row_labels[i]))

wm_total_cost = [[round(w * 2 * water_huf_per_m3 * (10**-3) + c * current_huf_per_kWh, 1)] for w, c in list(zip(washmachine[:,4], washmachine[:,5]))]

washmachine_with_cost = np.append(washmachine, wm_total_cost, axis=1)

def sort_by_cost(washmachine_with_cost, mintemp=30, maxtemp=65, minkg=2, mintime=20, maxtime=150):
    sorted_array = sorted(washmachine_with_cost, key=lambda row: row[-1])
    list_by_cost = [list(row) for row in sorted_array if not(row[1] < mintemp or row[1] > maxtemp or row[2] < minkg or row[3] < mintime or row[3] > maxtime)]
    for i in range(len(list_by_cost)):
        for tuple in prog_label_pairs:
            if tuple[0] == list_by_cost[i][0]:
                list_by_cost[i] = [tuple[1]] + list_by_cost[i]
    list_by_cost = [['Programme name'] + column_labels + ['Total cost (HUF)']] + list_by_cost
    return list_by_cost

list_by_cost_default = sort_by_cost(washmachine_with_cost)

def export_to_csv(list_by_cost):
    with open('washingm_programs_sorted.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(list_by_cost)

def print_table_with_header(list_by_cost):
    x = PrettyTable()
    x.field_names = list_by_cost[0]
    for row in list_by_cost[1:]:
        x.add_row(row)
    print(x)