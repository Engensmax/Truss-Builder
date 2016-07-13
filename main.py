"""
main.py, First of June, 2016
Max Engensperger, maxe@alumni.ethz.ch
The goal of this program is to generate hierarchical trusses for bone tissue engineering.
This program can generate the stl-file of a given truss and evaluate the mechanical properties.
This file contains the main steps of the program such as initiation of evaluation values and generation of the stl.
All files are created with a column size of 180 instead of the PEP 8: 120.
"""

from evaluation import objective_function
import subprocess
import pickle


# OPENS THE CSV
def open_csv(output_file_path):
    subprocess.Popen(str(output_file_path), shell=True)


inputs = dict()
options = dict()

########################################################################################################################
########################################################################################################################
#  #######################                          INPUT  FROM  USER                          ######################  #
########################################################################################################################
########################################################################################################################

# SMALL LIBRARIES
# Contains the number of different thicknesses on each cell
truss_thicknesses_library = dict(cubes=3, body_centered_cubes=7, truncated_cubes=9, varying_truncated_cubes=15,
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
# Directory where abaqus loads and saves files:
inputs['calculating_directory'] =  "C://abaqus_temp2/"
# Directory where outputs such as csv and pickle get saved:
inputs['output_directory'] =       'C://Users/maxe/Dropbox/Master_Thesis/outputs/thickness_scaling21June2016/'
# Affix to every file in the calculating directory:
inputs['job_name'] =               "temp_output"
# Name (and therefore topology) of the truss. Multiple names can be put in to iterate through all
inputs['truss_names'] =             ['cubes', 'body_centered_cubes', 'face_diagonal_cubes_alt', 'octetrahedrons',
                                    'void_octetrahedrons', 'octahedrons', 'pyramids', 'truncated_cubes']
# [ 'octetrahedrons', 'octahedrons',
#                                                   'void_octetrahedrons', 'diamonds']
# i didnt do 'pyramids' 'body_centered_cubes', 'truncated_cubes'

# Material
inputs['material'] =                                material_library['MED610']

# Cell Topology
# Number of cells in one direction (Total number of cells is number_of_cells ** 2):
inputs['number_of_cells'] =                         3
# Length of one cell (Total size is cell_size * number_of_cells):
inputs['cell_size'] =                               1.5  # [mm]
# Minimal Thickness that can be used:
inputs['strut_min_thickness'] =                     0.1  # [mm]

strut_thickness_multiplier =                        1

# Multiplied by strut_min_thickness results in the actual thickness of the struts
# inputs['strut_thickness_multiplicator'] =         list()
# for i in range(0, truss_thicknesses_library[inputs['truss_name']]):
#     inputs['strut_thickness_multiplicator'].append(strut_thickness_multiplier)
# Best thicknesses for titanium and cubes:
# inputs['strut_thickness_multiplicator'] =         [4.71177218, 4.14965115, 4.80241845]
# inputs['strut_thickness_multiplicator'] =         [ 4.18 , 4.12 , 4.77]

# Used in the topology of the cells pyramids, templar_crosses, varying_truncated_cubes
# cell_ratio_multiplier =                             0.5
# inputs['cell_ratio'] =                            list()
# for i in range(0, truss_ratio_library[inputs['truss_name']]):
#     inputs['cell_ratio'].append(cell_ratio_multiplier)
# Best ratio for templar_alt2_crosses:  #good values: cell_size= 10 * strut_thickness
# inputs['cell_ratio'] =                              [0.4, 0.8, 0.2]


########################################################################################################################
# OPTIONS
# 0 == False
# 1 == True
# You can also directly write True and False instead of 1 and 0 if you prefer that.

# Creates the Loading Steps for the Wireframe Evaluation:
options['create_steps'] =                           1
# Submits the Job and evaluates the created steps:
options['submit_job'] =                             1
# Generates the Solid Model of the Truss and exports it into an stl-file. Needed to calculate volumetric outputs:
options['stl_generate'] =                           1
# Cuts the borders of the truss off:
options['cutoff'] =                                 1
# Runs the program with the GUI (Generated User Interface). This blocks submitting of the job:
options['gui'] =                                    0
# Overwrites the csv result_file instead of appending the new results
# The result gets saved in the output_directory
# If there hasn't been an output file yet, this needs to be True (1):
options['overwrite_csv'] =                          1
# Overwrites the pickled result file instead of appending the new results
# (The result gets saved in the output_directory
# If there hasn't been an output file yet, this needs to be True (1):
options['overwrite_pickle'] =                       1

# Viewers
# Opens the stl (STereoLithography) after completion:
options['stl_view'] =                               0
# Opens the odb (Output DataBase) after completion:
options['odb_view'] =                               0
# Opens the csv (Comma Separated Values) of the output after completion:
options['csv_view'] =                               0

# Cross Section Input
# Cross Section of the Struts for the Solid and Stl Model. Can be "square", "hexagon", "octagon" or "dodecagon":
options['strut_cross_section'] =                    "dodecagon"
# Version Input
# Use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)":
options['abaqus_version'] =                         "6.14-1"

########################################################################################################################
########################################################################################################################
#  #####################                            NO MORE INPUT                            ########################  #
########################################################################################################################
########################################################################################################################
if options['create_steps'] == 0:
    options['submit_job'] = 0
    print("Job will not be submitted if the steps are not created.")
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
options['plot_fitness'] = 0




universal_counter = 0  # Careful, this is global
for name in inputs['truss_names']:
    inputs['truss_name'] = name
    for strut_thickness_multiplier in range(1,10):
        inputs['strut_thickness_multiplicator'] =         list()
        for i in range(0, truss_thicknesses_library[inputs['truss_name']]):
            inputs['strut_thickness_multiplicator'].append(strut_thickness_multiplier)

        cell_ratio_multiplier =                             0.5
        inputs['cell_ratio'] =                            list()
        for j in range(0, truss_ratio_library[inputs['truss_name']]):
            inputs['cell_ratio'].append(cell_ratio_multiplier)
        inputs['output_file'] = inputs['output_directory'] + 'output_' + str(inputs['truss_name'])
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
        ############################################################################################################
        # CALLING THE ENGINE                                                                                       #
        objective_function(inputs=inputs,                                                                          #
                           options=options)                                                                        #
        ############################################################################################################

if options['csv_view']:
    open_csv(str(inputs['output_file']) + '.csv')