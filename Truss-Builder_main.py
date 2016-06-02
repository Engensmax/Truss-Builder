"""
main.py, First of June, 2016
Max Engensperger, maxe@alumni.ethz.ch
The goal of this program is to generate hierarchical trusses for bone tissue engineering.
This program can generate the stl-file of a given truss and evaluate the mechanical properties.
This file contains the main steps of the program such as initiation of evaluation values and generation of the stl.
"""

from evaluation import objective_function
import subprocess
import pickle


# OPENS THE CSV
def open_csv(output_file_path):
    subprocess.Popen(str(output_file_path), shell=True)


options = dict()
options['material'] = dict()
truss_thicknesses_library = dict()
truss_thicknesses_library['cubes'] = 3
truss_thicknesses_library['body_centered_cubes'] = 7
truss_thicknesses_library['truncated_cubes'] = 15
truss_thicknesses_library['varying_truncated_cubes'] = 15
truss_thicknesses_library['face_diagonal_cubes'] = 6
truss_thicknesses_library['face_diagonal_cubes_alt'] = 6
truss_thicknesses_library['octetrahedrons'] = 24
truss_thicknesses_library['octahedrons'] = 12
truss_thicknesses_library['void_octetrahedrons'] = 12
truss_thicknesses_library['diamonds'] = 4
truss_thicknesses_library['templar_crosses'] = 1
truss_thicknesses_library['templar_alt_crosses'] = 1
truss_thicknesses_library['templar_alt2_crosses'] = 1
truss_thicknesses_library['pyramids'] = 3
truss_thicknesses_library['file_super_truss'] = 1
####################################################################################################################################################################################
####################################################################################################################################################################################
######################################################                          INPUT  FROM  USER                          #########################################################
####################################################################################################################################################################################
####################################################################################################################################################################################

# DIRECTORY INPUT
calculating_directory = "C://abaqus_temp2/"
output_directory = 'C://Users/maxe/Dropbox/Master_Thesis/outputs/dump/'

# TRUSS INPUT
# Possible inputs for truss_name followed by the number of thicknesses that are different from each other (which defines the length needed of strut_thickness_multiplicator):
#
# |'cubes' 3 | 'body_centered_cubes' 7 | 'truncated_cubes' 15 | 'varying_truncated_cubes' 15 | 'face_diagonal_cubes' 6 | 'face_diagonal_cubes_alt' 6 |
# |'octetrahedrons' 24 | 'octahedrons' 12 | 'void_octetrahedrons' 12 | 'diamonds' 4 | 'templar_crosses' 1 | 'pyramids' 3 | 'file_super_truss' 1 |
truss_name =                            'templar_alt2_crosses'
number_of_cells =                       2  # Number of cells in one direction (Total number of cells is number_of_cells ** 2)
cell_size =                             0.005  # Length of one cell (Total size is cell_size * number_of_cells)
strut_min_thickness =                   0.0001  # Minimal Thickness that can be used
strut_thickness_multiplier =            5

strut_thickness_multiplicator =         list()  # Multiplied by strut_min_thickness results in the actual thickness of the struts
for i in range(0, truss_thicknesses_library[truss_name]):
    strut_thickness_multiplicator.append(strut_thickness_multiplier)

# OPTIONS
# 0 == False
# 1 == True
# You can also directly write True and False instead of 1 and 0 if you prefer that.

options['create_steps'] =               1  # Creates the Loading Steps for the Wireframe Evaluation
options['submit_job'] =                 1  # Submits the Job and evaluates the created steps
options['stl_generate'] =               1  # Generates the Solid Model of the Truss and exports it into an stl-file
options['cutoff'] =                     1  # Cuts the borders of the truss off

options['gui'] =                        0  # Runs the program with the GUI (Generated User Interface). This blocks submitting of the job
options['overwrite_csv'] =              1  # Overwrites the csv result_file instead of appending the new results (The result gets saved in the output_directory)
#                                          # If there hasn't been an output file yet, this needs to be True (1)
options['overwrite_pickle'] =           1  # Overwrites the pickled result_file instead of appending the new results (The result gets saved in the output_directory
#                                          # If there hasn't been an output file yet, this needs to be True (1)

# Viewers
options['stl_view'] =                   1  # Opens the stl (STereoLithography) after completion
options['odb_view'] =                   1  # Opens the odb (Output DataBase) after completion
options['csv_view'] =                   0  # Opens the csv (Comma Separated Values) of the output after completion

# MATERIAL INPUT
options['material']['name'] =           "MED610"  # Name of the material
options['material']['E_Modulus'] =      2.5e9  # Young's modulus of the material
options['material']['poisson_ratio'] =  0.33  # Poisson's ratio of the material

# Cross Section Input
options['strut_cross_section'] =        "dodecagon"  # Cross Section of the Struts for the Solid and Stl Model. Can be "square", "hexagon", "octagon" or "dodecagon"

# Version Input
options['abaqus_version'] =             "6.14-1"  # Use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)"

####################################################################################################################################################################################
####################################################################################################################################################################################
######################################################                            NO MORE INPUT                            #########################################################
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
options['plot_fitness'] = 0
output_file = output_directory + 'output_' + str(truss_name)

if options['overwrite_csv']:
    result_file = open(str(output_file) + '.csv', 'w')
    result_file.write("Step, Fitness, Cell Size [mm], Strut_Thickness [µm], "
                      "Pore Size 1[µm], Pore Size 2[µm], Pore Size 3[µm], Pore Size 4[µm], Sigma_z [MPa], "
                      "Sigma_y [MPa], Sigma_x [MPa], Tau_yz [MPa], Tau_xz [MPa], Tau_xy [MPa], "
                      "Bending_yz [Pa/m^2], Bending_xz [Pa/m^2], Bending_xy [Pa/m^2], "
                      "v21 [1], v31 [1], v32 [1], Volume [mm^3], Porosity [%], "
                      "Void_ratio [1], Surface_Area [mm^2]\n")
    result_file.close()

if options['overwrite_pickle']:
    output_old = list()
    file = open(output_file + "_pickle", 'wb')
    pickle.dump(output_old, file)
    file.close()

universal_counter = 0  # Careful, this is global
##########################################################################
# CALLING THE ENGINE                                                     #
objective_function(x=strut_thickness_multiplicator,                      #
                   number_of_cells=number_of_cells,                      #
                   cell_size=cell_size,                                  #
                   min_thickness=strut_min_thickness,                    #
                   truss_name=truss_name,                                #
                   directory=calculating_directory,                      #
                   job_name="temp_output",                               #
                   output_file=str(output_file) + '.csv',                #
                   options=options)                                      #
##########################################################################

if options['csv_view']:
    open_csv(str(output_file) + '.csv')
