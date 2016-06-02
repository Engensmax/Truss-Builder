"""
This file is to extract the solution manually from a result file
"""

import pickle
import statistics
import numpy

# file_path = 'C://abaqus_temp/temp_optimization2_input'
# file_path = "/abaqus_temp2/temp_optimization1_results"
# file_path = "C:/Users/Maxe-PC2/Dropbox/Master_Thesis/outputs/dump/output_optimization_cubes_pickle"
file_path = "C:/Users\maxe\Dropbox\Master_Thesis\outputs\dump/output_optimization_cubes_pickle"

with open('' + str(file_path), 'rb') as f:
    u = pickle.Unpickler(f)
    p = u.load()
    step = 'SIGMA_Z'
    plane = 'SIGMA_X_1'
    direction = 0
l = dict()
counter = 0

# for info in sorted(set(p)):
#     print(info + ": " + str(p[info]))

if False:
    for point in p[step][plane]:
        list_of_coordinates = list()
        list_of_coordinates.append(point[direction])
    displacement = statistics.median(list_of_coordinates)
    print(str(step) + "displacement :" + str(displacement))

if False:
    print(p['SIGMA_X']['SIGMA_Z_2'])

if True:
    numpy.set_printoptions(precision=2, suppress=True)
    print(numpy.multiply(p[1]['Compliance'], 1e9))
