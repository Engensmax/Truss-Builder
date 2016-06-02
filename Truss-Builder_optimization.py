from scipy import optimize
from matplotlib import pyplot
from evaluation import objective_function
import pickle
import subprocess

pyplot.ion()


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

options = dict()
options['material'] = dict()
truss_thicknesses_library = dict(cubes=3, body_centered_cubes=7, truncated_cubes=15, varying_truncated_cubes=15, face_diagonal_cubes=6, face_diagonal_cubes_alt=6, octetrahedrons=24,
                                 octahedrons=12, void_octetrahedrons=12, diamonds=4, templar_crosses=1, pyramids=3, file_super_truss=1)
####################################################################################################################################################################################
# |'cubes' 3 | 'body_centered_cubes' 7 | 'truncated_cubes' 15 | 'varying_truncated_cubes' 15 | 'face_diagonal_cubes' 6 | 'face_diagonal_cubes_alt' 6 |
# |'octetrahedrons' 24 | 'octahedrons' 12 | 'void_octetrahedrons' 12 | 'diamonds' 4 | 'templar_crosses' 1 | 'pyramids' 3 | 'file_super_truss' 1 |

# truss_name = ['cubes', 'body_centered_cubes', 'octetrahedrons', 'void_octetrahedrons', 'face_diagonal_cubes_alt',
#               'truncated_cubes', 'pyramids', 'diamonds', 'face_diagonal_cubes_alt']
# truss_name = ['file_super_truss']
# truss_name = ['templar_crosses']
truss_name = ['cubes']
calculating_directory = "C://abaqus_temp2/"
output_directory = 'C://Users/maxe/Dropbox/Master_Thesis/outputs/optimization/BFGS/Titanium_Bone/'
#
# OPTIONS
# 0 == False
# 1 == True
# You can also directly write True and False instead of 1 and 0 if you prefer that.

options['create_steps'] =               1  # Creates the Loading Steps for the Wireframe Evaluation
options['submit_job'] =                 1  # Submits the Job and evaluates the created steps
options['stl_generate'] =               0  # Generates the Solid Model of the Truss and exports it into an stl-file
options['cutoff'] =                     1  # Cuts the borders of the truss off

options['gui'] =                        0  # Runs the program with the GUI (Generated User Interface). This blocks submitting of the job
options['overwrite_csv'] =              1  # Overwrites the csv result_file instead of appending the new results (The result gets saved in the output_directory)
#                                          # If there hasn't been an output file yet, this needs to be True (1)
options['overwrite_pickle'] =           1  # Overwrites the pickled result_file instead of appending the new results (The result gets saved in the output_directory
#                                          # If there hasn't been an output file yet, this needs to be True (1)

# Optimization specific
options['plot_fitness'] =               1  # Plot the fitness while optimizing
options['algorithm'] =                  'BFGS'  # Defines the algorithm used for the optimization

# Viewers
options['stl_view'] =                   0  # Opens the stl (STereoLithography) after completion
options['odb_view'] =                   0  # Opens the odb (Output DataBase) after completion
options['csv_view'] =                   0  # Opens the csv (Comma Separated Values) of the output after completion

# MATERIAL INPUT
# options['material']['name'] =           "MED610"  # Name of the material
# options['material']['E_Modulus'] =      2.5e9  # Young's modulus of the material
# options['material']['poisson_ratio'] =  0.33  # Poisson's ratio of the material
options['material']['name'] =           "TITANIUM_MED_GRADE"  # Name of the material
options['material']['E_Modulus'] =      110e9  # Young's modulus of the material
options['material']['poisson_ratio'] =  0.32  # Poisson's ratio of the material

# Cross Section Input
options['strut_cross_section'] =        "dodecagon"  # Cross Section of the Struts for the Solid and Stl Model. Can be "square", "hexagon", "octagon" or "dodecagon"

# Version Input
options['abaqus_version'] =             "6.14-1"  # Use windows command prompt: "abaqus cae nogui" and then ">>> version" or ">>> print(version)"
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

for name in truss_name:
    try:
        output_file = output_directory + 'optim_output_' + str(name)
        universal_counter = 0  # Careful, this is global
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

        strut_multiplicator = list()
        bounds = list()
        for i in range(0, truss_thicknesses_library[name]):
            strut_multiplicator.append(3)
            bounds.append((1, 15))

        if options['algorithm'] == 'l_bfgs_b':
            result = optimize.fmin_l_bfgs_b(objective_function,
                                            x0=strut_multiplicator,
                                            args=(3,  # Number of cells
                                                  0.0015,  # Cell_size
                                                  0.0001,  # strut_min_thickness
                                                  name,  # Truss_name
                                                  calculating_directory,  # Calculating Directory
                                                  "optim_output",  # job name
                                                  output_file + '.csv',  # Output File Path
                                                  options),
                                            bounds=bounds,
                                            approx_grad=True,
                                            epsilon=0.5
                                            # options={'eps': 0.5}
                                            # options={'disp': False, 'eps': 0.5}
                                            )
        elif options['algorithm'] == 'BFGS':
            result = optimize.minimize(objective_function,
                                       x0=strut_multiplicator,
                                       args=(3,  # Number of cells
                                             0.0015,  # Cell_size
                                             0.0001,  # strut_min_thickness
                                             name,  # Truss_name
                                             calculating_directory,  # Calculating Directory
                                             "optim_output_" + str(name),  # job name
                                             output_file + '.csv',  # Output File Path
                                             options),
                                       method=options['algorithm'],
                                       options={'disp': True, 'maxiter': 10, 'eps': 0.5})

        if options['csv_view']:
            open_csv(str(output_file) + '.csv')

    except:
        print(str(name) + " failed!")