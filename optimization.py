from scipy import optimize
from matplotlib import pyplot
from evaluation import objective_function
import pickle
import subprocess


pyplot.ion()


# STARTS OBJECTIVE FUNCTION DEPENDING ON THE VARIABLES TO OPTIMIZE
def optimizer(x, inputs, options):
    inputs[options['optimization_variables']] = x
    # return objective_function(inputs['strut_thickness_multiplicator'], inputs['number_of_cells'], inputs['cell_size'], inputs['cell_ratio'], inputs['strut_min_thickness'],
    #                           inputs['truss_name'], inputs['calculating_directory'], "temp_output", inputs['output_directory'] + 'output_' + str(inputs['truss_name']) + '.csv',
    #                           options)
    return objective_function(inputs, options)


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
    # pyplot.show()
    subprocess.Popen(saving_path, shell=True)


# OPENS THE CSV
def open_csv(output_file_path):
    subprocess.Popen(str(output_file_path), shell=True)

inputs = dict()
bounds = dict()
options = dict()
####################################################################################################################################################################################
####################################################################################################################################################################################
#  #####################################################                          INPUT  FROM  USER                          ####################################################  #
####################################################################################################################################################################################
####################################################################################################################################################################################

# SMALL LIBRARIES
# Contains the number of different thicknesses on each cell
truss_thicknesses_library = dict(cubes=3, body_centered_cubes=7, truncated_cubes=15, varying_truncated_cubes=15, face_diagonal_cubes=6, face_diagonal_cubes_alt=6,
                                 octetrahedrons=24, octahedrons=12, void_octetrahedrons=12, diamonds=4, templar_crosses=1, templar_alt_crosses=1, templar_alt2_crosses=1,
                                 pyramids=3, file_super_truss=1)
# Contains the number of different ratios on each cell (for topology optimization)
truss_ratio_library = dict(cubes=0, body_centered_cubes=0, truncated_cubes=0, varying_truncated_cubes=1, face_diagonal_cubes=0, face_diagonal_cubes_alt=0, octetrahedrons=0,
                           octahedrons=0, void_octetrahedrons=0, diamonds=0, templar_crosses=3, templar_alt_crosses=3, templar_alt2_crosses=3, pyramids=1, file_super_truss=0)
# Dictionary of materials
material_library = dict(MED610=dict(name='MED610', E_Modulus=2.5e9, poisson_ratio=0.33),
                        PLA=dict(name='PLA', E_Modulus=2.5e9, poisson_ratio=0.33),
                        Titanium=dict(name='Titanium', E_Modulus=116e9, poisson_ratio=0.32))

####################################################################################################################################################################################
# INPUTS
inputs['calculating_directory'] =                   "C://abaqus_temp2/"  # Directory where abaqus loads and saves files
inputs['output_directory'] =                        'C://Users/maxe/Dropbox/Master_Thesis/outputs/dump/'  # Directory where outputs such as csv and pickle get saved
inputs['job_name'] =                                "temp_output"  # Affix to every file in the calculating directory
inputs['truss_name'] =                              'cubes'  # Name (and therefore topology) of the truss

# Material
inputs['material'] =                                material_library['MED610']

# Cell Topology
inputs['number_of_cells'] =                         3  # Number of cells in one direction (Total number of cells is number_of_cells ** 2)
inputs['cell_size'] =                               0.0015  # Length of one cell (Total size is cell_size * number_of_cells)
inputs['strut_min_thickness'] =                     0.0001  # Minimal Thickness that can be used

strut_thickness_multiplier =                        3
inputs['strut_thickness_multiplicator'] =         list()  # Multiplied by strut_min_thickness results in the actual thickness of the struts
bounds['strut_thickness_multiplicator'] =         list()  # Multiplied by strut_min_thickness results in the actual thickness of the struts
for i in range(0, truss_thicknesses_library[inputs['truss_name']]):
    inputs['strut_thickness_multiplicator'].append(strut_thickness_multiplier)
    bounds['strut_thickness_multiplicator'].append((1, 10))
# Best thicknesses for titanium
# inputs['strut_thickness_multiplicator'] =         [4.71177218, 4.14965115, 4.80241845]

cell_ratio_multiplier =                             0.5
inputs['cell_ratio'] =                            list()
bounds['cell_ratio'] =                            list()
for i in range(0, truss_ratio_library[inputs['truss_name']]):
    inputs['cell_ratio'].append(cell_ratio_multiplier)
    bounds['strut_thickness_multiplicator'].append((0.1, 1))
# Best ratio for templar_alt2_crosses:
# inputs['cell_ratio'] =                              [0.3, 0.8, 0.2]


####################################################################################################################################################################################
# OPTIONS
# 0 == False
# 1 == True
# You can also directly write True and False instead of 1 and 0 if you prefer that.

options['create_steps'] =                           1  # Creates the Loading Steps for the Wireframe Evaluation
options['submit_job'] =                             1  # Submits the Job and evaluates the created steps
options['stl_generate'] =                           1  # Generates the Solid Model of the Truss and exports it into an stl-file
options['cutoff'] =                                 1  # Cuts the borders of the truss off

options['gui'] =                                    0  # Runs the program with the GUI (Generated User Interface). This blocks submitting of the job
options['overwrite_csv'] =                          1  # Overwrites the csv result_file instead of appending the new results (The result gets saved in the output_directory)
#                                                      # If there hasn't been an output file yet, this needs to be True (1)
options['overwrite_pickle'] =                       1  # Overwrites the pickled result_file instead of appending the new results (The result gets saved in the output_directory
#                                                      # If there hasn't been an output file yet, this needs to be True (1)

# Viewers
options['stl_view'] =                               1  # Opens the stl (STereoLithography) after completion
options['odb_view'] =                               1  # Opens the odb (Output DataBase) after completion
options['csv_view'] =                               0  # Opens the csv (Comma Separated Values) of the output after completion

# Cross Section Input
options['strut_cross_section'] =                    "dodecagon"  # Cross Section of the Struts for the Solid and Stl Model. Can be "square", "hexagon", "octagon" or "dodecagon"

# Version Input
options['abaqus_version'] =                         "6.14-1"  # Use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)"

# Optimization specific
options['plot_fitness'] =                           1  # Plot the fitness while optimizing
options['algorithm'] =                              'l_bfgs_b'  # Defines the algorithm used for the optimization
options['optimization_variables'] =                 'strut_thickness_multiplicator'  # Decides what to optimize for

####################################################################################################################################################################################
####################################################################################################################################################################################
#  ###################################################                            NO MORE INPUT                            ######################################################  #
####################################################################################################################################################################################
####################################################################################################################################################################################
if options['gui']:
    options['submit_job'] = 0
    print("Job will not be submitted if the Script is run with the GUI.")
if options['stl_generate'] == 0:
    options['stl_view'] = 0
    print("Stl cannot be viewed if it is not generated")
if options['submit_job'] == 0:
    options['odb_view'] = 0
    print("Odb cannot be viewed if the job is not submitted")

options['read_output'] = options['submit_job']

for name in inputs['truss_name']:
    # try:
        inputs['output_file'] = inputs['output_directory'] + 'optim_output_' + str(name)
        universal_counter = 0  # Careful, this is global
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

        if options['algorithm'] == 'l_bfgs_b':
            result = optimize.fmin_l_bfgs_b(optimizer,
                                            x0=inputs[options['optimization_variables']],
                                            args=(inputs,
                                                  options),
                                            bounds=bounds[options['optimization_variables']],
                                            approx_grad=True,
                                            epsilon=0.05,
                                            # options={'eps': 0.5},
                                            # options={'disp': False, 'eps': 0.5},
                                            )
        elif options['algorithm'] == 'BFGS':
            result = optimize.minimize(optimizer,
                                       x0=inputs[options['optimization_variables']],
                                       args=(inputs,
                                             options),
                                       method=options['algorithm'],
                                       options={'disp': True, 'maxiter': 10, 'eps': 0.1})

        if options['csv_view']:
            open_csv(str(inputs['output_file']) + '.csv')

    # except:
    #     print(str(name) + " failed!")