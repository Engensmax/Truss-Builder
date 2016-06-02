"""
evaluation.py
This file contains the main steps of the program such as initiation of optimization values, initiation of
optimization and generation of the stl for the final solution.
Each solution is an object with the following properties:
Nodal points, start and finish of every strut, strut thickness of each strut, pore size, porosity, surface area
Each solution might have the following properties:
Material constants, Cell types (which are repeated through the truss), cell size, thickness of each strut of a cell
"""
import os
import subprocess
import time
import pickle
from library_truss import generate_truss
from Class_Script import Script
import statistics
from matplotlib import pyplot
import warnings
import matplotlib.cbook
import numpy

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


########################################################################################################################
# HEADER


# RUN THE ABAQUS SCRIPT VIA COMMAND LINE
def run(script, gui):
    print("Running Abaqus Script")
    t0 = time.time()
    os.chdir(str(script.filename[0]))

    if gui:
        subprocess.run('abaqus cae script=' + "".join(script.filename), shell=True)
    # This program has a bug, if running with gui. To run with gui, go to Class_Script.py and disable the marked
    # line in the function def submit(filename, job_name). It is recommended to also disable the line
    # Model_Script.evaluate() in evaluation.py. If you want to see the simulation output,
    # it is recommended to run without gui and then open the odb with odb_viewer(Model_Script)
    else:
        subprocess.run('abaqus cae noGUI=' + "".join(script.filename), shell=True)
    t1 = time.time()
    print("Time elapsed: " + str(t1 - t0) + " seconds\n")


# OPENS THE ABAQUS ODB VIEWER VIA COMMAND LINE
def odb_viewer(script):
    print("Starting Abaqus Viewer")
    subprocess.Popen('abaqus viewer database=' + script.filename[0] + script.filename[1], shell=True)


# OPENS THE STL FILE WITH SELECTED DEFAULT PROGRAM VIA COMMAND LINE
def stl_viewer(script):
    print("Starting STL Viewer")
    subprocess.Popen(script.filename[0] + script.filename[1] + ".stl", shell=True)


# READS IN THE DISPLACEMENTS OF THE SIDES OF THE CUBES FOR EACH STEP/LOADING CONDITION AND CALCULATES COMPLIANCE FROM IT
def read_results(script):
    def read_stress(result, name, plane, direction):
        list_of_coordinates = list()
        for point in result[name][plane]:
            list_of_coordinates.append(float(point[direction]))
        displacement = statistics.median(list_of_coordinates)
        # print("Average displacement " + name + ": " + str(round(displacement * 1e6, 6)) + " μm")
        young = abs(applied_force / ((script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0]) * displacement))
        # print("Elastic Modulus in " + name + " step into " + plane + " direction: " + str(round(young / 1e6, 3)) + " MPa")
        return young

    def read_shearing(result, name, plane, direction):
        list_of_coordinates = list()
        for point in result[name][plane]:
            list_of_coordinates.append(float(point[direction]))
        displacement = statistics.median(list_of_coordinates)
        # print("Average displacement " + name + ": " + str(round(displacement * 1e6, 3)) + " μm")
        shear = abs(applied_force / ((script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0]) * displacement))
        return shear

    def read_displacement(result, step, plane, direction):
        list_of_coordinates = list()
        for point in result[step][plane]:
            list_of_coordinates.append(float(point[direction]))
        displacement = statistics.median(list_of_coordinates)
        # print("Average displacement " + step + ": " + str(round(displacement * 1e6, 6)) + " μm")
        return displacement

    # IMPORT SOLUTION
    with open(str(script.filename[0]) + str(script.filename[1]) + '_results', 'rb') as f:
        u = pickle._Unpickler(f)
        u.encoding = 'latin1'
        results = u.load()
    applied_force = 1

    output = dict()
    output['Cell_Size'] = script.truss.cell_size
    output['Strut_Thickness'] = script.truss.cells[0].strut_thicknesses[0]
    output['Pore_size'] = list()
    for cell in script.truss.cells:
        output['Pore_size'].append(cell.pore_size)

    try:  # This outputs volumetrics such as porosity, which is only possible when the solid is generated in abaqus.
        porosity = 1 - (results['Volume'] / ((script.truss.number_of_cells * script.truss.cell_size) ** 3))
        print("Porosity: " + str(round(porosity * 1e2, 1)) + "%")
        print("Void Ratio: " + str(round(porosity / (1 - porosity), 1)))
        print("Pore Sizes: ")
        for cells in script.truss.cells:
            for pore in cells.pore_size:
                print(str(round(pore * 1e6, 3)) + " μm, ")
        output['Volume'] = results['Volume']
        output['Porosity'] = porosity
        output['Void_ratio'] = porosity / (1 - porosity)
        output['Surface_Area'] = results['Surface_Area']
    except KeyError:
        print("This Evaluation is done without calculating Porosity or Volume")
    # Calculate Compliance Matrix
    length_cube = (script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0])

    # First Quarter:
    output['Sigma_x'] = read_stress(results, 'SIGMA_X', 'SIGMA_X_1', 0)
    output['Sigma_y'] = read_stress(results, 'SIGMA_Y', 'SIGMA_Y_1', 1)
    output['Sigma_z'] = read_stress(results, 'SIGMA_Z', 'SIGMA_Z_1', 2)
    print("Elastic Modulus in X direction: " + str(round(output['Sigma_x'] / 1e6, 3)) + " MPa")
    print("Elastic Modulus in Y direction: " + str(round(output['Sigma_y'] / 1e6, 3)) + " MPa")
    print("Elastic Modulus in Z direction: " + str(round(output['Sigma_z'] / 1e6, 3)) + " MPa")

    compliance_sigma = numpy.zeros([3, 3])
    compliance_sigma[0, 0] = 1 / output['Sigma_x']
    compliance_sigma[1, 0] = -(read_displacement(results, 'SIGMA_X', 'SIGMA_Y_1', 1) - read_displacement(results, 'SIGMA_X', 'SIGMA_Y_2_Y', 1)) * length_cube / applied_force
    compliance_sigma[2, 0] = -(read_displacement(results, 'SIGMA_X', 'SIGMA_Z_1', 2) - read_displacement(results, 'SIGMA_X', 'SIGMA_Z_2_Z', 2)) * length_cube / applied_force
    compliance_sigma[0, 1] = -(read_displacement(results, 'SIGMA_Y', 'SIGMA_X_1', 0) - read_displacement(results, 'SIGMA_Y', 'SIGMA_X_2_X', 0)) * length_cube / applied_force
    compliance_sigma[1, 1] = 1 / output['Sigma_y']
    compliance_sigma[2, 1] = -(read_displacement(results, 'SIGMA_Y', 'SIGMA_Z_1', 2) - read_displacement(results, 'SIGMA_Y', 'SIGMA_Z_2_Z', 2)) * length_cube / applied_force
    compliance_sigma[0, 2] = -(read_displacement(results, 'SIGMA_Z', 'SIGMA_X_1', 0) - read_displacement(results, 'SIGMA_X', 'SIGMA_X_2_X', 0)) * length_cube / applied_force
    compliance_sigma[1, 2] = -(read_displacement(results, 'SIGMA_Z', 'SIGMA_Y_1', 1) - read_displacement(results, 'SIGMA_X', 'SIGMA_Y_2_Y', 1)) * length_cube / applied_force
    compliance_sigma[2, 2] = 1 / output['Sigma_z']

    # Second Quarter:
    compliance_coupling2 = numpy.zeros([3, 3])
    compliance_coupling2[0, 0] = (read_displacement(results, 'TAU_YZ', 'SIGMA_X_1', 0) - read_displacement(results, 'TAU_YZ', 'SIGMA_X_2_X', 0)) * length_cube / applied_force
    compliance_coupling2[1, 0] = (read_displacement(results, 'TAU_YZ', 'SIGMA_Y_1', 1) - read_displacement(results, 'TAU_YZ', 'SIGMA_Y_2_Y', 1)) * length_cube / applied_force
    compliance_coupling2[2, 0] = (read_displacement(results, 'TAU_YZ', 'SIGMA_Z_1', 2) - read_displacement(results, 'TAU_YZ', 'SIGMA_Z_2_Z', 2)) * length_cube / applied_force
    compliance_coupling2[0, 1] = (read_displacement(results, 'TAU_XZ', 'SIGMA_X_1', 0) - read_displacement(results, 'TAU_XZ', 'SIGMA_X_2_X', 0)) * length_cube / applied_force
    compliance_coupling2[1, 1] = (read_displacement(results, 'TAU_XZ', 'SIGMA_Y_1', 1) - read_displacement(results, 'TAU_XZ', 'SIGMA_Y_2_Y', 1)) * length_cube / applied_force
    compliance_coupling2[2, 1] = (read_displacement(results, 'TAU_XZ', 'SIGMA_Z_1', 2) - read_displacement(results, 'TAU_XZ', 'SIGMA_Z_2_Z', 2)) * length_cube / applied_force
    compliance_coupling2[0, 2] = (read_displacement(results, 'TAU_XY', 'SIGMA_X_1', 0) - read_displacement(results, 'TAU_XY', 'SIGMA_X_2_X', 0)) * length_cube / applied_force
    compliance_coupling2[1, 2] = (read_displacement(results, 'TAU_XY', 'SIGMA_Y_1', 1) - read_displacement(results, 'TAU_XY', 'SIGMA_Y_2_Y', 1)) * length_cube / applied_force
    compliance_coupling2[2, 2] = (read_displacement(results, 'TAU_XY', 'SIGMA_Z_1', 2) - read_displacement(results, 'TAU_XY', 'SIGMA_Z_2_Z', 2)) * length_cube / applied_force

    # Third Quarter:
    compliance_coupling3 = numpy.zeros([3, 3])
    compliance_coupling3[0, 0] = (read_displacement(results, 'SIGMA_X', 'SIGMA_Z_1', 1) - read_displacement(results, 'SIGMA_X', 'SIGMA_Z_2_Z', 1)) * length_cube / applied_force
    compliance_coupling3[1, 0] = (read_displacement(results, 'SIGMA_X', 'SIGMA_X_1', 2) - read_displacement(results, 'SIGMA_X', 'SIGMA_X_2_X', 2)) * length_cube / applied_force
    compliance_coupling3[2, 0] = (read_displacement(results, 'SIGMA_X', 'SIGMA_Y_1', 0) - read_displacement(results, 'SIGMA_X', 'SIGMA_Y_2_Y', 0)) * length_cube / applied_force
    compliance_coupling3[0, 1] = (read_displacement(results, 'SIGMA_Y', 'SIGMA_Z_1', 1) - read_displacement(results, 'SIGMA_Y', 'SIGMA_Z_2_Z', 1)) * length_cube / applied_force
    compliance_coupling3[1, 1] = (read_displacement(results, 'SIGMA_Y', 'SIGMA_X_1', 2) - read_displacement(results, 'SIGMA_Y', 'SIGMA_X_2_X', 2)) * length_cube / applied_force
    compliance_coupling3[2, 1] = (read_displacement(results, 'SIGMA_Y', 'SIGMA_Y_1', 0) - read_displacement(results, 'SIGMA_Y', 'SIGMA_Y_2_Y', 0)) * length_cube / applied_force
    compliance_coupling3[0, 2] = (read_displacement(results, 'SIGMA_Z', 'SIGMA_Z_1', 1) - read_displacement(results, 'SIGMA_Z', 'SIGMA_Z_2_Z', 1)) * length_cube / applied_force
    compliance_coupling3[1, 2] = (read_displacement(results, 'SIGMA_Z', 'SIGMA_X_1', 2) - read_displacement(results, 'SIGMA_Z', 'SIGMA_X_2_X', 2)) * length_cube / applied_force
    compliance_coupling3[2, 2] = (read_displacement(results, 'SIGMA_Z', 'SIGMA_Y_1', 0) - read_displacement(results, 'SIGMA_Z', 'SIGMA_Y_2_Y', 0)) * length_cube / applied_force

    # Fourth Quarter:
    output['Tau_yz'] = (read_shearing(results, 'TAU_YZ', 'SIGMA_Z_1', 1) + read_shearing(results, 'TAU_YZ', 'SIGMA_Y_1', 2)) / 2
    output['Tau_xz'] = (read_shearing(results, 'TAU_XZ', 'SIGMA_X_1', 2) + read_shearing(results, 'TAU_XZ', 'SIGMA_Z_1', 0)) / 2
    output['Tau_xy'] = (read_shearing(results, 'TAU_XY', 'SIGMA_Y_1', 0) + read_shearing(results, 'TAU_XY', 'SIGMA_X_1', 1)) / 2
    print("Shearing Modulus in yz direction: " + str(round(output['Tau_yz'] / 1e6, 3)) + " MPa")
    print("Shearing Modulus in xz direction: " + str(round(output['Tau_xz'] / 1e6, 3)) + " MPa")
    print("Shearing Modulus in xy direction: " + str(round(output['Tau_xy'] / 1e6, 3)) + " MPa")

    output['Bending_yz'] = 12 / (script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0]) ** 3 * output['Tau_yz']
    output['Bending_xz'] = 12 / (script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0]) ** 3 * output['Tau_xz']
    output['Bending_xy'] = 12 / (script.truss.cell_size * script.truss.number_of_cells + script.truss.cells[0].strut_thicknesses[0]) ** 3 * output['Tau_xy']
    # print("Bending Modulus in yz direction: " + str(round(output['Bending_yz'] / 1e12, 3)) + " Pa/mm^3")
    # print("Bending Modulus in xz direction: " + str(round(output['Bending_xz'] / 1e12, 3)) + " Pa/mm^3")
    # print("Bending Modulus in xy direction: " + str(round(output['Bending_xy'] / 1e12, 3)) + " Pa/mm^3")

    compliance_tau = numpy.zeros([3, 3])
    compliance_tau[0, 0] = 1 / output['Tau_yz']
    compliance_tau[1, 0] = (read_displacement(results, 'TAU_YZ', 'SIGMA_Z_1', 0) - read_displacement(results, 'TAU_YZ', 'SIGMA_Z_2_Z', 0)) * length_cube / applied_force
    compliance_tau[2, 0] = (read_displacement(results, 'TAU_YZ', 'SIGMA_Y_1', 0) - read_displacement(results, 'TAU_YZ', 'SIGMA_Y_2_Y', 0)) * length_cube / applied_force
    compliance_tau[0, 1] = (read_displacement(results, 'TAU_XZ', 'SIGMA_Z_1', 1) - read_displacement(results, 'TAU_XZ', 'SIGMA_Z_2_Z', 1)) * length_cube / applied_force
    compliance_tau[1, 1] = 1 / output['Tau_xz']
    compliance_tau[2, 1] = (read_displacement(results, 'TAU_XZ', 'SIGMA_X_1', 1) - read_displacement(results, 'TAU_XZ', 'SIGMA_X_2_X', 1)) * length_cube / applied_force
    compliance_tau[0, 2] = (read_displacement(results, 'TAU_XY', 'SIGMA_Y_1', 2) - read_displacement(results, 'TAU_XY', 'SIGMA_Y_2_Y', 2)) * length_cube / applied_force
    compliance_tau[1, 2] = (read_displacement(results, 'TAU_XY', 'SIGMA_X_1', 2) - read_displacement(results, 'TAU_XY', 'SIGMA_X_2_X', 2)) * length_cube / applied_force
    compliance_tau[2, 2] = 1 / output['Tau_xy']

    output['Compliance'] = numpy.zeros([6, 6])
    output['Compliance'][0:3, 0:3] = compliance_sigma
    output['Compliance'][0:3, 3:7] = compliance_coupling2
    output['Compliance'][3:7, 0:3] = compliance_coupling3
    output['Compliance'][3:7, 3:7] = compliance_tau

    # POISSON'S RATIO
    output['v21'] = -output['Compliance'][1, 0] / output['Compliance'][0, 0]
    output['v31'] = -output['Compliance'][2, 0] / output['Compliance'][0, 0]
    output['v32'] = -output['Compliance'][1, 2] / output['Compliance'][2, 2]
    print("Poisson's ratio v21: " + str(round(output['v21'], 3)))
    print("Poisson's ratio v31: " + str(round(output['v31'], 3)))
    print("Poisson's ratio v32: " + str(round(output['v32'], 3)))

    print("Compliance Matrix [1/GPa]: ")
    numpy.set_printoptions(precision=2, suppress=True)
    print(numpy.multiply(output['Compliance'], 1e9))
    print("#############################################################################################")
    return output


# APPENDS RESULTS TO A CSV FILE AND A SERIALIZED PICKLE FILE
def append_output_to_file(output, output_file):
    result_file = open(output_file, 'a')
    result_file.write(str(round(output['Step'])) + ", " +
                      str(round(output['Fitness'], 3)) + ", " +
                      str(round(output['Cell_Size'] * 1e3, 3)) + ", " +
                      str(round(output['Strut_Thickness'] * 1e6, 3)) + ", ")
    counter = 0
    for cells in output['Pore_size']:
        for pore in cells:
            result_file.write(str(round(pore * 1e6, 3)) + ", ")
            counter += 1
    for i in range(0, 4 - counter):
        result_file.write(", ")
    result_file.write(str(round(output['Sigma_z'] * 1e-6, 3)) + ", " +
                      str(round(output['Sigma_y'] * 1e-6, 3)) + ", " +
                      str(round(output['Sigma_x'] * 1e-6, 3)) + ", " +
                      str(round(output['Tau_yz'] * 1e-6, 3)) + ", " +
                      str(round(output['Tau_xz'] * 1e-6, 3)) + ", " +
                      str(round(output['Tau_xy'] * 1e-6, 3)) + ", " +
                      str(round(output['Bending_yz'] * 1e-12, 3)) + ", " +
                      str(round(output['Bending_xz'] * 1e-12, 3)) + ", " +
                      str(round(output['Bending_xy'] * 1e-12, 3)) + ", " +
                      str(round(output['v21'], 3)) + ", " +
                      str(round(output['v31'], 3)) + ", " +
                      str(round(output['v32'], 3)) + ", ")
    # str(round(output['Torsion_z'] * 1e-6, 3)) + ", " +
    # str(round(output['Torsion_y'] * 1e-6, 3)) + ", " +
    # str(round(output['Torsion_x'] * 1e-6, 3)) + ", ")

    try:
        result_file.write(str(round(output['Volume'] * 1e9, 3)) + ", " +
                          str(round(output['Porosity'] * 100, 3)) + ", " +
                          str(round(output['Void_ratio'] * 1, 3)) + ", " +
                          str(round(output['Surface_Area'] * 1e6, 3)) + ", "
                          )
    except KeyError:
        pass

    result_file.write("\n")
    result_file.close()

    # APPENDS OUTPUT TO THE PICKLED OUTPUT
    unpickle = pickle._Unpickler(open(str(output_file[:len(output_file) - 4]) + "_pickle", 'rb'))
    unpickle.encoding = 'latin1'
    output_old = unpickle.load()
    output_old.append(output)
    file = open(str(output_file[:len(output_file) - 4]) + "_pickle", 'wb')
    pickle.dump(output_old, file)
    file.close()


# SAFES THE INPUT IN A SERIALIZED PICKLE FILE
def pickle_input(x, truss_name, input_file):
    pickle_dump = list()
    pickle_dump.append(x)
    pickle_dump.append(truss_name)
    file = open(str(input_file), 'wb')
    pickle.dump(pickle_dump, file)
    file.close()


universal_counter = 0


####################################################################################################################################################################################
# BEGIN OF PROGRAM


def objective_function(x, number_of_cells, cell_size, min_thickness, truss_name, directory, job_name, output_file, options):
    global universal_counter
    universal_counter += 1  # Careful this is global

    # PRINT INFO FROM INPUT
    print("Counter: " + str(universal_counter))
    print("Truss: " + str(truss_name))
    print("X: " + str(x))
    print("Number of Cells: " + str(number_of_cells))
    print("Cell Size: " + str(round(cell_size * 1e3, 3)) + " mm")
    print("Total Size: " + str(round(number_of_cells * cell_size * 1e3, 3)) + " mm\n\n\n")

    # MULTIPLY X WITH min_thickness
    thicknesses = list()
    fitness = 0
    for multiplicator in x:
        if multiplicator > 0:
            thicknesses.append(min_thickness * multiplicator)
        else:    # Blocks negative values for strut thicknesses
            thicknesses.append(abs(min_thickness * multiplicator))
            fitness += 1e9 * abs(multiplicator)
    filename = list()
    filename.append(directory)
    filename.append(job_name + str(universal_counter))
    filename.append(".py")
    # GENERATE TRUSS
    truss = generate_truss(truss_name=truss_name, affix="",
                           cell_size=cell_size, strut_thicknesses=thicknesses, number_of_cells=number_of_cells)

    # GENERATE SCRIPT

    # initialize.
    model_script = Script(filename=filename, truss=truss, material=options['material'], abaqus_version=options['abaqus_version'])
    # generate wireframe and evaluate.
    model_script.evaluate(create_steps=options['create_steps'], submit_job=options['submit_job'],
                          read_output=options['read_output'], number_of_cells=number_of_cells)
    # generate solid and export to stl.
    if options['stl_generate']:
        model_script.generate_solid(strut_name=options['strut_cross_section'], cutoff=options['cutoff'], number_of_cells=number_of_cells)
        model_script.export_stl()

    # saves the results from the simulation in a serialized pickle file.
    model_script.pickle_dump()

    # RUN SCRIPT
    run(script=model_script, gui=options['gui'])

    # OPEN VIEWERS TO SEE RESULT
    if options['stl_view']:
        stl_viewer(model_script)
    if options['odb_view']:
        odb_viewer(model_script)

    # CALCULATE COMPLIANCE FROM DISPLACEMENTS FROM THE SIMULATION
    if options['read_output']:
        output = read_results(model_script)
    else:
        output = dict()

    # CALCULATE FITNESS
    try:
        fitness += ( abs(output['Sigma_z'] - 15e9) / 100e6 + abs(output['Sigma_y'] - 11.5e9) / 100e6 + abs(output['Sigma_x'] - 11.5e9) / 100e6)
    except KeyError:
        print("No Fitness")
        fitness = 1e9
    try:
        fitness += (output['Porosity'] - 0.4)
    except KeyError:
        print("Fitness is without porosity")
    for values in x:
        fitness += abs(1 / abs(values - 0.00050) * 1e-10)  # To encourage bigger struts and kill strut solutions equal 0

    # SAFE OUTPUT INTO CSV FILE
    if options['read_output']:
        output['Step'] = universal_counter
        output['Fitness'] = fitness
        append_output_to_file(output, output_file)

    # SAFE INPUT VALUES AS A SERIALIZED PICKLE FILE
    pickle_input(x, truss_name, str(directory) + str(job_name) + str(universal_counter) + "_input")

    # PLOT FITNESS
    if options['plot_fitness']:
        pyplot.xlabel('Step')
        pyplot.ylabel('Fitness')
        pyplot.scatter(universal_counter, fitness)
        pyplot.legend()
        pyplot.show()
        pyplot.pause(0.00001)
    return fitness
