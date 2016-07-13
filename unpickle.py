"""
This file is to extract the solution manually from a result file
"""

import pickle
import statistics
import numpy

# file_path = 'C://abaqus_temp/temp_optimization2_input'
# file_path = "/abaqus_temp2/temp_optimization1_results"
# file_path = "C:/Users/Maxe-PC2/Dropbox/Master_Thesis/outputs/dump/output_optimization_cubes_pickle"
# file_path = "C:/Users\maxe\Dropbox\Master_Thesis\outputs\optimization\BFGS\Titanium_Bone\cubes_input"
# file_path = "C://abaqus_temp/temp_output154_results"
file_path = 'C://Users/maxe/Dropbox/Master_Thesis/outputs/final/SigmaZ_Max/pickled_results'
# file_path = 'C://Users/maxe/Dropbox/Master_Thesis/outputs/final/Titanium_bone/optim_output_octahedrons_pickle'

# HOW TO WRITE TO FILE:

# result=dict({'fun': 15.208073954667745, 'jac': [19.03, 19.94, -19.94],
#                   'message': 'STOP: TOTAL NO. of ITERATIONS EXCEEDS LIMIT', 'nfev': 16, 'nit': 1, 'status': 1,
#                   'success': False, 'x': 4})
# file = open(file_path + ".csv", 'w')
# file.write(result['fun'])
# file.write(str(result.keys()) + "\n")
# for key in result.keys():
#     file.write(str(result[key]) + ", ")
# file.write("\n")
#
# file.close()



# with open('' + str(file_path), 'rb') as f:
    # u = pickle._Unpickler(f)
    # u.encoding = 'latin1'
    # p = u.load()
# unpickle = pickle._Unpickler(open(file_path, 'rb'))
# unpickle.encoding = 'latin1'
# result_pickle = {'x': 1, 'inputs': 2, 'options': True, 'optimization': [5, 2]}
# pickle.dump(result_pickle, open(file_path, 'wb'))
p = pickle.load(open(file_path, 'rb'))
# p = unpickle.load()
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
    print(p)

if False:
    numpy.set_printoptions(precision=2, suppress=True)
    print(numpy.multiply(p[1]['Compliance'], 1e9))

if True:
    # for elements in p:
        for dicts in p[0]:
            print(str(dicts) + " :")
            print(p[0][dicts])
