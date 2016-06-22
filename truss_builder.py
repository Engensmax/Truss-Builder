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
        inputs[options['optimization_variables']] = x[0]
    else:
        inputs[options['optimization_variables']] = x
    return objective_function(input1, input2)


# PLOTS x VS y AND SAVES THE PLOT AS A PICTURE
def plot_output(pickle_file_path, x, y, saving_path):
    unpickle = pickle._Unpickler(open(pickle_file_path, 'rb'))
    unpickle.encoding = 'latin1'
    output = unpickle.load()
    x_axis = list()
    y_axis = list()
    for results in output:
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
# Contains the number of different thicknesses on each cell
truss_thicknesses_library = dict(cubes=3, body_centered_cubes=7, truncated_cubes=9, varying_truncated_cubes=9,
                                 face_diagonal_cubes=6, face_diagonal_cubes_alt=6, octetrahedrons=6, octahedrons=6,
                                 void_octetrahedrons=6, diamonds=4, templar_crosses=1, templar_alt_crosses=1,
                                 templar_alt2_crosses=1, pyramids=3, file_super_truss=1, tetroctas=20)
# Contains the number of different ratios on each cell (for topology optimization)
truss_ratio_library = dict(cubes=0, body_centered_cubes=0, truncated_cubes=0, varying_truncated_cubes=1,
                           face_diagonal_cubes=0, face_diagonal_cubes_alt=0, octetrahedrons=0, octahedrons=0,
                           void_octetrahedrons=0, diamonds=0, templar_crosses=3, templar_alt_crosses=3,
                           templar_alt2_crosses=3, pyramids=1, file_super_truss=0, tetroctas=0)
# Dictionary of materials
material_library = dict(MED610=dict(name='MED610', E_Modulus=2.5e9, poisson_ratio=0.33),        # Med-grade Polymer
                        PLA=dict(name='PLA', E_Modulus=2.5e9, poisson_ratio=0.33),              # Poly-lactic acid
                        TCP=dict(name='TCP', E_Modulus=22e9, poisson_ratio=0.33),               # Tricalcium Phosphate
                        HA=dict(name='HA', E_Modulus=6e9, poisson_ratio=0.33),                  # Hydroxyapatite
                        Titanium=dict(name='Titanium', E_Modulus=116e9, poisson_ratio=0.32))

########################################################################################################################
# INPUTS
# Directory where abaqus loads and saves files. The directory will be created if it doesn't exist already:
inputs['calculating_directory'] =  "C://abaqus_temp/"
# Directory where outputs such as csv and pickle get saved. The directory will be created if it doesn't exist already:
inputs['output_directory'] =       'C://Users/maxe/Dropbox/Master_Thesis/outputs/'
# Affix to every file in the calculating directory:
inputs['job_name'] =               "temp_output"
# Name (and therefore topology) of the truss. Multiple names can be put in to iterate through all
inputs['truss_names'] =             ['cubes', 'face_diagonal_cubes_alt']
# ['diamonds']
# i didnt do 'pyramids' 'body_centered_cubes', 'truncated_cubes'

# Material. See material_library to add or see materials.
inputs['material'] =                                material_library['MED610']

# Cell topology
# Number of cells in one direction (Total number of cells is number_of_cells ** 2):
inputs['number_of_cells'] =                         3
# Length of one cell (Total size is cell_size * number_of_cells):
inputs['cell_size'] =                               1.5  # [mm]
# Minimal Thickness that can be used:
inputs['strut_min_thickness'] =                     0.3  # [mm]
#
inputs['strut_thickness_multiplier'] =              1
inputs['cell_ratio'] =                              0.5

########################################################################################################################
# OPTIONS

# Creates the loading steps for the wireframe evaluation:
options['create_steps'] =                           True
# Submits the job and evaluates the created steps:
options['submit_job'] =                             True
# Generates the solid model of the truss and exports it into an stl-file. Needed to calculate volumetric outputs:
options['stl_generate'] =                           True
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
options['strut_cross_section'] =                    'dodecagon'
# Version Input
# To determine Version: use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)"
# If the student version is used
# This is used for defining the path of where to find the abaqus_plugin stlExport.
# See class Script __init__.
options['abaqus_version'] =                         '6.14-1'

########################################################################################################################
# METHOD to run the engine. Possible entries are 'single_run', 'loop' or 'optimization'
options['method'] =                                 'optimization'

# LOOP specific
options['loop1_variable'] =                          'strut_min_thickness'
options['loop1_values'] =                            [0.1 * a for a in range(1, 11)]

options['loop2_variable'] =                         'None'
options['loop2_values'] =                           [0]

# OPTIMIZATION specific
#  Decides what to optimize for:
options['optimization_variables'] =                 'strut_min_thickness'
# Bounds of the optimization variables. This only applies to some algorithms.
options['bounds'] =                                 (0.2, 1)
# Define Fitness variables, their target value, their norming and their weighting.
options['fitness_variables'] =                      {'Porosity': [0.6, 1e3, 1], 'Sigma_z': [15e9, 1e-8, 1]}
# Plot the fitness while optimizing:
options['plot_fitness'] =                           True
# Defines the algorithm used for the optimization:
options['algorithm'] =                              'CG'
# Possible algorithms:
# 'Nelder-Mead', 'Powell', 'CG', 'BFGS', 'Newton-CG', 'L-BFGS-B', 'TNC', 'COBYLA', 'SLSQP', 'dogleg', 'trust-ncg'
# Options for the optimization. See scipy optimization toolbox for further info:
options['options'] =                                {'disp': True, 'maxiter': 10, 'eps': 0.01}

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

# Loop over the different truss topologies:
for name in inputs['truss_names']:
    inputs['truss_name'] = name

    bounds[options['optimization_variables']] = options['bounds']

    inputs['strut_thickness_multiplicator'] =         list()
    # Multiplied by strut_min_thickness results in the actual thickness of the struts
    bounds['strut_thickness_multiplicator'] =         list()
    # Multiplied by strut_min_thickness results in the actual thickness of the struts bounds
    for i in range(0, truss_thicknesses_library[name]):
        inputs['strut_thickness_multiplicator'].append(inputs['strut_thickness_multiplier'])
        bounds['strut_thickness_multiplicator'].append(options['bounds'])
    # Best thicknesses for titanium
    # inputs['strut_thickness_multiplicator'] =         [4.71177218, 4.14965115, 4.80241845]

    inputs['cell_ratio'] =                            list()
    bounds['cell_ratio'] =                            list()
    for j in range(0, truss_ratio_library[name]):
        inputs['cell_ratio'].append(inputs['cell_ratio'])
        bounds['cell_ratio'].append(options['bounds'])
    # Best ratio for templar_alt2_crosses:
    # inputs['cell_ratio'] =                              [0.3, 0.8, 0.2]

    inputs['output_file'] = inputs['output_directory'] + 'optim_output_' + str(name)

    if options['overwrite_csv']:
        result_file = open(str(inputs['output_file']) + '.csv', 'w')
        result_file.write("Step, Truss Name, Fitness, Cell Size [mm], Strut_Thickness [µm], "
                          "Pore Size 1[µm], Pore Size 2[µm], Pore Size 3[µm], Pore Size 4[µm], Sigma_z [MPa], "
                          "Sigma_y [MPa], Sigma_x [MPa], Tau_yz [MPa], Tau_xz [MPa], Tau_xy [MPa], "
                          "Bending_yz [Pa/m^2], Bending_xz [Pa/m^2], Bending_xy [Pa/m^2], "
                          "v21 [1], v31 [1], v32 [1], Volume [mm^3], Porosity [%], "
                          "Void_ratio [1], Surface_Area [mm^2], Strut_Thickness_Multiplicator [1]\n")
        result_file.close()

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
        objective_function(inputs=inputs, options=options)

    elif options['method'] == 'loop':
        for loop1 in options['loop1_values']:
            for loop2 in options['loop2_values']:
                inputs[options['loop1_variable']] = loop1
                inputs[options['loop2_variable']] = loop2
                objective_function(inputs=inputs, options=options)

    elif options['method'] == 'optimization':
        result = optimize.minimize(optimizer,
                                   x0=inputs[options['optimization_variables']],
                                   args=(inputs,
                                         options),
                                   method=options['algorithm'],
                                   bounds=bounds[options['optimization_variables']],
                                   options=options['options'])
        print(result)
    else:
        print("options['method'] does not contain a valid keyword. possible entries are: "
              "'single_run', 'loop' or 'optimization'.")
    ####################################################################################################################

    if options['csv_view']:
        open_csv(str(inputs['output_file']) + '.csv')

