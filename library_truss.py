"""
This file creates and returns the nodes of a truss and defines the containing cells.
"""
from Class_Truss import Truss
from library_cell import generate_cell


def generate_truss(truss_name, affix, cell_size, strut_thicknesses, number_of_cells):
    # NODES: Describe the nodes and their affiliated cells in cartesian coordinates.
    cells = list()
    nodes = list()
    if (truss_name == "cubes" or truss_name == "body_centered_cubes" or truss_name == "octahedrons" or
        truss_name == "truncated_cubes" or truss_name == "diamonds" or truss_name == "varying_truncated_cubes" or
        truss_name == "face_diagonal_cubes" or truss_name == "octetrahedrons" or truss_name == "void_octetrahedrons" or
        truss_name == "templar_crosses" or truss_name == "templar_alt_crosses"):
        cells.append(generate_cell(cell_name=truss_name[:len(truss_name) - 1], affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        for x in range(0, number_of_cells):
            for y in range(0, number_of_cells):
                for z in range(0, number_of_cells):
                    nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[0]])
    elif truss_name == "face_diagonal_cubes_alt":
        cells.append(generate_cell(cell_name="face_diagonal_cube", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        cells.append(generate_cell(cell_name="face_diagonal_cube_inv", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))

        for x in range(0, number_of_cells):
            for y in range(0, number_of_cells):
                for z in range(0, number_of_cells):
                    if (x + y + z) % 2 == 0:
                        nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[0]])
                    else:
                        nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[1]])
    elif truss_name == "templar_alt2_crosses":
        cells.append(generate_cell(cell_name="templar_alt2_cross", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        cells.append(generate_cell(cell_name="templar_alt2_cross_inv", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))

        for x in range(0, number_of_cells):
            for y in range(0, number_of_cells):
                for z in range(0, number_of_cells):
                    if (x + y + z) % 2 == 0:
                        nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[0]])
                    else:
                        nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[1]])
    elif truss_name == "pyramids":
        cells.append(generate_cell(cell_name="pyramid", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        cells.append(generate_cell(cell_name="pyramid_inv", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        cells.append(generate_cell(cell_name="pyramid_twist", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        cells.append(generate_cell(cell_name="pyramid_twist_inv", affix="",
                                   strut_thicknesses=strut_thicknesses, cell_size=cell_size))
        for x in range(0, number_of_cells):
            for y in range(0, number_of_cells):
                for z in range(0, number_of_cells):
                    if z == 0 or z == 2:
                        if (x + y) % 2 == 0 and x != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[0]])
                        elif x == 1 and y == 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[1]])
                        elif y == 1 and x != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[2]])
                        elif x == 1 and y != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[3]])
                    if z == 1:
                        if (x + y) % 2 == 0 and x != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[1]])
                        elif x == 1 and y == 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[0]])
                        elif y == 1 and x != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[3]])
                        elif x == 1 and y != 1:
                            nodes.append([x * cell_size, y * cell_size, z * cell_size, cells[2]])
    elif truss_name == "file_super_truss":
        cells.append(generate_cell(cell_name="file_super_truss", affix="",
                                   strut_thicknesses=[1], cell_size=1))
        nodes.append([0, 0, 0, cells[0]])

    else:
        print("Possible Names are: \n"
              "cubes\nbody_centered_cubes\noctahedrons\ntruncated_cubes\npyramids\ndiamonds\nvarying_truncated_cubes\n"
              "face_diagonal_cubes\nface_diagonal_cubes_alt\noctetrahedrons\nvoid_octetrahedrons\ntemplar_crosses\ntemplar_alt_crosses\nfile_super_truss")
        nodes = None
        cells = None
        exit("ERROR: truss_name specified is not defined in the library")

    truss = Truss(name=(truss_name + affix), nodes=nodes, cells=cells, cell_size=cell_size, number_of_cells=number_of_cells)
    return truss
