from scipy import optimize
from matplotlib import pyplot
from evaluation import objective_function
import pickle
import os
import subprocess
pyplot.ion()


# STARTS OBJECTIVE FUNCTION DEPENDING ON THE VARIABLES TO OPTIMIZE
def optimizer(x, input1, input2):
    # Apparently the optimization toolbox from scipy turns scalar x inputs into lists with 1 element.
    if len(x) == 1:
        input1[options['optimization_variables']] = x[0]
    else:
        input1[options['optimization_variables']] = x
    return objective_function(input1, input2)


# PLOTS x VS y AND SAVES THE PLOT AS A PICTURE
def plot_output(pickle_file_path, x, y, saving_path):
    p_output = pickle.load(open(pickle_file_path, 'rb'))
    x_axis = list()
    y_axis = list()
    for results in p_output:
        x_axis.append(results[str(x)])
        y_axis.append(results[str(y)])
    pyplot.plot(x_axis, y_axis)
    pyplot.xlabel(x)
    pyplot.ylabel(y)
    pyplot.title(saving_path)
    pyplot.grid(True)
    pyplot.savefig(saving_path)
    subprocess.Popen(saving_path, shell=True)


# OPENS THE CSV
def open_csv(output_file_path):
    subprocess.Popen(str(output_file_path), shell=True)

inputs = dict()
bounds = dict()
options = dict()
########################################################################################################################
########################################################################################################################
#  #######################                          INPUT  FROM  USER                          ######################  #
########################################################################################################################
########################################################################################################################

# SMALL LIBRARIES
# Contains the number of different thicknesses on each cell:
truss_thicknesses_library = dict(cubes=3, body_centered_cubes=7, truncated_cubes=9, varying_truncated_cubes=9,
                                 face_diagonal_cubes=6, face_diagonal_cubes_alt=6, octetrahedrons=6, octahedrons=6,
                                 void_octetrahedrons=6, diamonds=4, templar_crosses=1, templar_alt_crosses=1,
                                 templar_alt2_crosses=1, pyramids=3, file_super_truss=1, tetroctas=20,
                                 truncated_octahedrons=6)
# Contains the number of different ratios on each cell (for topology optimization):
truss_ratio_library = dict(cubes=0, body_centered_cubes=0, truncated_cubes=0, varying_truncated_cubes=1,
                           face_diagonal_cubes=0, face_diagonal_cubes_alt=0, octetrahedrons=0, octahedrons=0,
                           void_octetrahedrons=0, diamonds=0, templar_crosses=3, templar_alt_crosses=3,
                           templar_alt2_crosses=3, pyramids=1, file_super_truss=0, tetroctas=0, truncated_octahedrons=1)
# Dictionary of materials: E_Modulus: [N/mm^2] = [MPa]
material_library = dict(MED610=dict(name='MED610', E_Modulus=2.5e3, poisson_ratio=0.33),        # Med-grade Polymer
                        PLA=dict(name='PLA', E_Modulus=2.5e3, poisson_ratio=0.33),              # Poly-lactic acid
                        TCP=dict(name='TCP', E_Modulus=22e3, poisson_ratio=0.33),               # Tricalcium Phosphate
                        HA=dict(name='HA', E_Modulus=6e3, poisson_ratio=0.33),                  # Hydroxyapatite
                        Titanium=dict(name='Titanium', E_Modulus=116e3, poisson_ratio=0.32),
                        Relative=dict(name='Relative', E_Modulus=100, poisson_ratio=0.33)
                        )

########################################################################################################################
# INPUTS
# Directory where abaqus loads and saves files. The directory will be created if it doesn't exist already.
# This generated data is rather large:
inputs['calculating_directory'] =  "C://abaqus_temp/"
# Directory where outputs such as csv and pickle get saved. The directory will be created if it doesn't exist already.
# This generated data is very small:
inputs['output_directory'] =       'C://Users/maxe/Dropbox/Master_Thesis/outputs/final/Titanium_bone/'
# Affix to every file in the calculating directory:
inputs['job_name'] =               "temp_output"
# Name (and therefore topology) of the truss. Multiple names can be put in to iterate through all.
# For a single input, put it in brackets. For example: ['cubes']
# inputs['truss_names'] =             ['cubes']  # , 'diamonds', 'truncated_cubes']
# inputs['truss_names'] =             ['truncated_cubes', 'face_diagonal_cubes_alt',
#                                      'octetrahedrons', 'octahedrons', 'void_octetrahedrons', 'diamonds', 'pyramids',
#                                      'truncated_octahedrons']
inputs['truss_names'] =             ['cubes', 'body_centered_cubes', 'truncated_cubes', 'face_diagonal_cubes_alt',
                                     'octetrahedrons', 'octahedrons', 'void_octetrahedrons', 'diamonds', 'pyramids',
                                     'truncated_octahedrons']

# Material. See material_library to add or see materials.
inputs['material'] =                                material_library['Titanium']

# Cell topology
# Number of cells in one direction (Total number of cells is number_of_cells ** 2):
inputs['number_of_cells'] =                         3
# Length of one cell (Total size is cell_size * number_of_cells):
inputs['cell_size'] =                               1.5  # [mm]
# Minimal Thickness that can be used:
inputs['strut_min_thickness'] =                     0.1  # [mm]
# A list will be created inputs['strut_thickness_multiplicator'] that has the needed length depending on cell topoology
# This lists elements will all be inputs['strut_min_thickness'] * inputs['strut_thickness_multiplier']
inputs['strut_thickness_multiplier'] =              5
inputs['cell_ratio_multiplier'] =                   0.5

########################################################################################################################
########################################################################################################################
# OPTIONS

# Creates the loading steps for the wireframe evaluation:
options['create_steps'] =                           True
# Submits the job and evaluates the created steps:
options['submit_job'] =                             True
# Generates the solid model of the truss and exports it into an stl-file. Needed to calculate volumetric outputs:
options['stl_generate'] =                           False
# Cuts the borders of the truss off:
options['cutoff'] =                                 True
# Runs the program with the GUI (Generated User Interface). This blocks submitting of the job:
options['gui'] =                                    False
# Overwrites the csv result_file instead of appending the new results
# The result gets saved in the output_directory
# If there hasn't been an output file yet, this needs to be True:
options['overwrite_csv'] =                          True
# Overwrites the pickled result file instead of appending the new results
# (The result gets saved in the output_directory
# If there hasn't been an output file yet, this needs to be True:
options['overwrite_pickle'] =                       True

# Viewers
# Opens the stl (STereoLithography) after completion:
options['stl_view'] =                               False
# Opens the odb (Output DataBase) after completion:
options['odb_view'] =                               False
# Opens the csv (Comma Separated Values) of the output after completion:
options['csv_view'] =                               False

# Cross Section Input
# Cross Section of the Struts for the Solid and Stl Model. Can be "square", "hexagon", "octagon" or "dodecagon":
options['strut_cross_section'] =                    'octagon'
# Version Input
# To determine Version: use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)"
# If the student version is used add SE in the end. F.e. '6.14-2SE'
# This is used for defining the path of where to find the abaqus_plugin stlExport. See class Script : __init__()
options['abaqus_version'] =                         '6.14-1'

# File Path
# This is usually C:/SIMULIA/Abaqus
options['abaqus_path'] =                            "C:/Program Files/Abaqus/"
########################################################################################################################
# METHOD to run the engine. Possible entries are 'single_run', 'loop' or 'optimization'
options['method'] =                                 'optimization'

# LOOP specific (applies for options['method'] == 'loop')
# Loop over first variable:
options['loop1_variable'] =                          'strut_min_thickness'
# List of all the values to evaluate
options['loop1_values'] =                            [0.05 * a for a in range(1, 21)]


# Optional loop over second variable:
# Use 'None' if there is to be no loop
options['loop2_variable'] =                         'None'
# Use [0] if there is to be no loop
options['loop2_values'] =                           [0]

# OPTIMIZATION specific
#  Decides what to optimize for:
options['optimization_variables'] =                 'strut_thickness_multiplicator'
# Bounds of the optimization variables. This only applies to some algorithms.
options['bounds'] =                                 (1, 10)
# Define Fitness variables, their target value, their norming and their weighting.
# options['fitness_variables'] =                      {'Sigma_z': [30e3, 1e-2, 1]}
options['fitness_variables'] =                      {'Sigma_x': [12e3, 1e-2, 1],
                                                     'Sigma_y': [12e3, 1e-2, 1],
                                                     'Sigma_z': [15e3, 1e-2, 1]}
# Plot the fitness while optimizing:
options['plot_fitness'] =                           True
# Defines the algorithm used for the optimization:
options['algorithm'] =                              'L-BFGS-B'
# Possible algorithms:
# 'Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'dogleg', 'trust-ncg'
# Options for the optimization. See scipy optimization toolbox for further info:
options['options'] =                                {'disp': True, 'eps': 0.01, 'ftol': 0.05}
# Reruns the results with generating stl and writing all results into one csv:
options['run_results'] =                            True
########################################################################################################################
# OUTPUT

# Decide what to save in the csv
options['output'] = dict()
# General:
options['output']['Step'] =                         True
options['output']['Truss_Name'] =                   True
options['output']['Fitness'] =                      True
# Geometric properties:
options['output']['Cell_size'] =                    True
options['output']['Strut_Thickness'] =              True  # =Strut_Thicknesses[0]
options['output']['Pore_size'] =                    True
# Mechanic properties:
options['output']["Young's Modulus"] =              True
options['output']['Shearing Modulus'] =             True
options['output']["Poisson's Ratio"] =              True
# Volumetric properties: (will only be calculated if the STL is generated)
options['output']['Volume'] =                       True
options['output']['Porosity'] =                     True
options['output']['Void_ratio'] =                   True
options['output']['Surface_Area'] =                 True
# Optimization properties:
options['output']['X'] =                            True  # Strut_Thickness_Multiplicator

########################################################################################################################
########################################################################################################################
#  #####################                            NO MORE INPUT                            ########################  #
########################################################################################################################
########################################################################################################################
if options['gui']:
    options['submit_job'] = False
    print("Job will not be submitted if the Script is run with the GUI.")
if not options['stl_generate']:
    options['stl_view'] = False
    print("Stl cannot be viewed if it is not generated")
if not options['submit_job']:
    options['odb_view'] = False
    print("Odb cannot be viewed if the job is not submitted")

options['read_output'] = options['submit_job']

# Create folders if they don't exist yet.
if not os.path.exists(inputs['calculating_directory']):
    os.mkdir(inputs['calculating_directory'])

if not os.path.exists(inputs['output_directory']):
    os.mkdir(inputs['output_directory'])

if options['method'] == 'optimization':
    # Initialize csv
    file = open(inputs['output_directory'] + "optimization_results.csv", 'w')
    file.write("x, fun, nit, success, nfev\n")
    file.close()
    # Initialize pickle file
    pickle.dump(list(), open(inputs['output_directory'] + "pickled_results", 'wb'))

# Loop over the different truss topologies:
for name in inputs['truss_names']:
    inputs['truss_name'] = name

    bounds[options['optimization_variables']] = [options['bounds']]

    inputs['strut_thickness_multiplicator'] =         list()
    # Multiplied by strut_min_thickness results in the actual thickness of the struts
    bounds['strut_thickness_multiplicator'] =         list()
    # Multiplied by strut_min_thickness results in the actual thickness of the struts bounds
    for i in range(0, truss_thicknesses_library[name]):
        inputs['strut_thickness_multiplicator'].append(inputs['strut_thickness_multiplier'])
        bounds['strut_thickness_multiplicator'].append(options['bounds'])
    # Best thicknesses for titanium (1.5mm cell_size)(0.1mm strut_min_thickness) (3x3x3)
    # inputs['strut_thickness_multiplicator'] =         [4.71177218, 4.14965115, 4.80241845]

    inputs['cell_ratio'] =                            list()
    bounds['cell_ratio'] =                            list()
    for j in range(0, truss_ratio_library[name]):
        inputs['cell_ratio'].append(inputs['cell_ratio_multiplier'])
        bounds['cell_ratio'].append(options['bounds'])
    # Best ratio for templar_alt2_crosses:
    # inputs['cell_ratio'] =                              [0.3, 0.8, 0.2]

    inputs['output_file'] = inputs['output_directory'] + 'optim_output_' + str(name)

    if options['overwrite_csv']:
        result_file = open(str(inputs['output_file']) + '.csv', 'w')
        if options['output']['Step']:
            result_file.write('Step, ')
        if options['output']['Truss_Name']:
            result_file.write('Truss Name, ')
        if options['output']['Fitness']:
            result_file.write('Fitness, ')
        if options['output']['Cell_size']:
            result_file.write('Cell Size [mm], ')
        if options['output']['Strut_Thickness']:
            result_file.write('Strut Thickness [mu-m], ')
        if options['output']['Pore_size']:
            result_file.write('Pore Size 1[mu-m], Pore Size 2[mu-m], Pore Size 3[mu-m], Pore Size 4[mu-m], ')
        if options['output']["Young's Modulus"]:
            result_file.write('Sigma_z [MPa], Sigma_y [MPa], Sigma_x [MPa], ')
        if options['output']['Shearing Modulus']:
            result_file.write('Tau_yz [MPa], Tau_xz [MPa], Tau_xy [MPa], ')
        if options['output']["Poisson's Ratio"]:
            result_file.write('v21 [1], v31 [1], v32 [1], ')
        if options['output']['Volume']:
            result_file.write('Volume [mm^3], ')
        if options['output']['Porosity']:
            result_file.write('Porosity [%], ')
        if options['output']['Void_ratio']:
            result_file.write('Void_ratio [1], ')
        if options['output']['Surface_Area']:
            result_file.write('Surface_Area [mm^2], ')
        if options['output']['X']:
            result_file.write('Strut_Thickness_Multiplicator [1], ')
        result_file.write('\n')
        result_file.close()

    if options['run_results']:
        result_file2 = open(inputs['output_directory'] + "best_results" + '.csv', 'w')
        if options['output']['Step']:
            result_file2.write('Step, ')
        if options['output']['Truss_Name']:
            result_file2.write('Truss Name, ')
        if options['output']['Fitness']:
            result_file2.write('Fitness, ')
        if options['output']['Cell_size']:
            result_file2.write('Cell Size [mm], ')
        if options['output']['Strut_Thickness']:
            result_file2.write('Strut Thickness [mu-m], ')
        if options['output']['Pore_size']:
            result_file2.write('Pore Size 1[mu-m], Pore Size 2[mu-m], Pore Size 3[mu-m], Pore Size 4[mu-m], ')
        if options['output']["Young's Modulus"]:
            result_file2.write('Sigma_z [MPa], Sigma_y [MPa], Sigma_x [MPa], ')
        if options['output']['Shearing Modulus']:
            result_file2.write('Tau_yz [MPa], Tau_xz [MPa], Tau_xy [MPa], ')
        if options['output']["Poisson's Ratio"]:
            result_file2.write('v21 [1], v31 [1], v32 [1], ')
        if options['output']['Volume']:
            result_file2.write('Volume [mm^3], ')
        if options['output']['Porosity']:
            result_file2.write('Porosity [%], ')
        if options['output']['Void_ratio']:
            result_file2.write('Void_ratio [1], ')
        if options['output']['Surface_Area']:
            result_file2.write('Surface_Area [mm^2], ')
        if options['output']['X']:
            result_file2.write('Strut_Thickness_Multiplicator [1], ')
        result_file2.write('\n')
        result_file2.close()

    if options['overwrite_pickle']:
        output_old = list()
        file = open(inputs['output_file'] + "_pickle", 'wb')
        pickle.dump(output_old, file)
        file.close()

    # Counts the number of function evaluations. Careful, this is global
    universal_counter = 0
    ####################################################################################################################
    # Calling the engine, depending on the chosen method
    if options['method'] == 'single_run':
        options['plot_fitness'] = False
        objective_function(inputs=inputs, options=options)

    elif options['method'] == 'loop':
        options['plot_fitness'] = False
        for loop1 in options['loop1_values']:
            for loop2 in options['loop2_values']:
                inputs[options['loop1_variable']] = loop1
                inputs[options['loop2_variable']] = loop2
                objective_function(inputs=inputs, options=options)

    elif options['method'] == 'optimization':
        print("Optimization Input:")
        print("xo= " + str(inputs[options['optimization_variables']]))
        print("inputs= " + str(inputs) + ", " + str(options))
        print("options= " + str(options))
        print("method= " + str(options['algorithm']))
        print("bounds= " + str(bounds[options['optimization_variables']]))
        print("options= " + str(options['options']))
        print("#################################################################################################\n\n\n")
        result = optimize.minimize(optimizer,
                                   x0=inputs[options['optimization_variables']],
                                   args=(inputs,
                                         options),
                                   method=options['algorithm'],
                                   bounds=bounds[options['optimization_variables']],
                                   options=options['options'])
        # Save result as CSV:
        file = open(inputs['output_directory'] + "optimization_results.csv", 'a')
        key_list = ['x', 'fun', 'nit', 'success', 'nfev']
        for key in key_list:
            file.write(str(result[key]) + ", ")
        file.write("\n")
        file.close()

        # Save result as pickled file:
        result_pickle = {'inputs': inputs, 'options': options,
                         'optimization': {'x': result['x'], 'nfev': result['nfev'],
                                          'nit': result['nit'], 'success': result['success']}}
        print(result_pickle['optimization'])
        output_old = pickle.load(open(inputs['output_directory'] + "pickled_results", 'rb'))
        output_old.append(result_pickle)
        file = open(inputs['output_directory'] + "pickled_results", 'wb')
        pickle.dump(output_old, file)
        file.close()

        print("#################################################################################################\n\n\n")
    else:
        print("options['method'] does not contain a valid keyword. possible entries are: "
              "'single_run', 'loop' or 'optimization'.")
    ####################################################################################################################

    if options['csv_view']:
        open_csv(str(inputs['output_file']) + '.csv')

if options['method'] == 'optimization' and options['run_results']:
    output = pickle.load(open(inputs['output_directory'] + "pickled_results", 'rb'))
    for i in range(0, len(output)):
        inputs = output[i]['inputs']
        options = output[i]['options']
        inputs[options['optimization_variables']] = output[i]['optimization']['x']
        inputs['output_file'] = inputs['output_directory'] + "best_results"
        options['stl_generate'] = True
        objective_function(inputs=inputs, options=options)
