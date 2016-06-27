"""
This file creates and returns the nodes of a cell and defines the connections between the nodes.
"""
import math
from Class_Cell import Cell
import csv_reader


def generate_cell(cell_name, affix, strut_thicknesses, cell_size, ratio):
    # NODES: Describe the nodes in cartesian coordinates.
    # ratio = 0.8
    # ratio = list()
    # ratio.append(0.3)   # 0-1    --> 0.3
    # ratio.append(0.4)   # 0-0.5  --> 0.8
    # ratio.append(0.05)  # 0-0.33 --> 0.15
    pore_size = list()
    if cell_name == "truncated_cuboctahedron":
        sizing = 1 / (2 * (1 + 2 * math.sqrt(2)))
        a = sizing
        b = sizing * (1 + math.sqrt(2))
        c = sizing * (1 + 2 * math.sqrt(2))
        cell_node_coordinates = [
            [-a, -b, -c], [a, -b, -c], [b, -a, -c], [b, a, -c], [a, b, -c], [-a, b, -c], [-b, a, -c], [-b, -a, -c],
            [-a, -c, -b], [a, -c, -b], [c, -a, -b], [c, a, -b], [a, c, -b], [-a, c, -b], [-c, a, -b], [-c, -a, -b],
            [-b, -c, -a], [b, -c, -a], [c, -b, -a], [c, b, -a], [b, c, -a], [-b, c, -a], [-c, b, -a], [-c, -b, -a],
            [-b, -c, a], [b, -c, a], [c, -b, a], [c, b, a], [b, c, a], [-b, c, a], [-c, b, a], [-c, -b, a],
            [-a, -c, b], [a, -c, b], [c, -a, b], [c, a, b], [a, c, b], [-a, c, b], [-c, a, b], [-c, -a, b],
            [-a, -b, c], [a, -b, c], [b, -a, c], [b, a, c], [a, b, c], [-a, b, c], [-b, a, c], [-b, -a, c]]

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[0]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 4, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 0, strut_thicknesses[0]],
                            [0, 8, strut_thicknesses[0]],
                            [1, 9, strut_thicknesses[0]],
                            [2, 10, strut_thicknesses[0]],
                            [3, 11, strut_thicknesses[0]],
                            [4, 12, strut_thicknesses[0]],
                            [5, 13, strut_thicknesses[0]],
                            [6, 14, strut_thicknesses[0]],
                            [7, 15, strut_thicknesses[0]],
                            [8, 9, strut_thicknesses[0]],
                            [10, 11, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[0]],
                            [14, 15, strut_thicknesses[0]],
                            [8, 16, strut_thicknesses[0]],
                            [9, 17, strut_thicknesses[0]],
                            [10, 18, strut_thicknesses[0]],
                            [11, 19, strut_thicknesses[0]],
                            [12, 20, strut_thicknesses[0]],
                            [13, 21, strut_thicknesses[0]],
                            [14, 22, strut_thicknesses[0]],
                            [15, 23, strut_thicknesses[0]],
                            [17, 18, strut_thicknesses[0]],
                            [19, 20, strut_thicknesses[0]],
                            [21, 22, strut_thicknesses[0]],
                            [23, 16, strut_thicknesses[0]],
                            [16, 24, strut_thicknesses[0]],
                            [17, 25, strut_thicknesses[0]],
                            [18, 26, strut_thicknesses[0]],
                            [19, 27, strut_thicknesses[0]],
                            [20, 28, strut_thicknesses[0]],
                            [21, 29, strut_thicknesses[0]],
                            [22, 30, strut_thicknesses[0]],
                            [23, 31, strut_thicknesses[0]],
                            [25, 26, strut_thicknesses[0]],
                            [27, 28, strut_thicknesses[0]],
                            [29, 30, strut_thicknesses[0]],
                            [31, 24, strut_thicknesses[0]],
                            [24, 32, strut_thicknesses[0]],
                            [25, 33, strut_thicknesses[0]],
                            [26, 34, strut_thicknesses[0]],
                            [27, 35, strut_thicknesses[0]],
                            [28, 36, strut_thicknesses[0]],
                            [29, 37, strut_thicknesses[0]],
                            [30, 38, strut_thicknesses[0]],
                            [31, 39, strut_thicknesses[0]],
                            [32, 33, strut_thicknesses[0]],
                            [34, 35, strut_thicknesses[0]],
                            [36, 37, strut_thicknesses[0]],
                            [38, 39, strut_thicknesses[0]],
                            [32, 40, strut_thicknesses[0]],
                            [33, 41, strut_thicknesses[0]],
                            [34, 42, strut_thicknesses[0]],
                            [35, 43, strut_thicknesses[0]],
                            [36, 44, strut_thicknesses[0]],
                            [37, 45, strut_thicknesses[0]],
                            [38, 46, strut_thicknesses[0]],
                            [39, 47, strut_thicknesses[0]],
                            [40, 41, strut_thicknesses[0]],
                            [41, 42, strut_thicknesses[0]],
                            [42, 43, strut_thicknesses[0]],
                            [43, 44, strut_thicknesses[0]],
                            [44, 45, strut_thicknesses[0]],
                            [45, 46, strut_thicknesses[0]],
                            [46, 47, strut_thicknesses[0]],
                            [47, 40, strut_thicknesses[0]]]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(2 * a)
        pore_size.append(math.sqrt(3) / 2 * a)
        pore_size.append((math.sqrt(2) + 1) * a)

    elif cell_name == "varying_truncated_cube":
        strut_length = 1 / (1 + math.sqrt(2))
        tl = math.sqrt(2) / 2 * strut_length * ratio[0] / 2  # standing for truncated_length
        cell_node_coordinates = [[0, tl, 0], [tl, 0, 0], [1 - tl, 0, 0], [1, tl, 0], [1, 1 - tl, 0], [1 - tl, 1, 0],
                                 [tl, 1, 0], [0, 1 - tl, 0], [0, 0, tl], [1, 0, tl], [1, 1, tl], [0, 1, tl],
                                 [0, 0, 1 - tl], [1, 0, 1 - tl], [1, 1, 1 - tl], [0, 1, 1 - tl], [0, tl, 1], [tl, 0, 1],
                                 [1 - tl, 0, 1], [1, tl, 1], [1, 1 - tl, 1], [1 - tl, 1, 1], [tl, 1, 1], [0, 1 - tl, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[2]],
                            [3, 4, strut_thicknesses[3]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[2]],
                            [7, 0, strut_thicknesses[3]],
                            [0, 8, strut_thicknesses[4]],
                            [8, 1, strut_thicknesses[5]],
                            [2, 9, strut_thicknesses[6]],
                            [9, 3, strut_thicknesses[4]],
                            [4, 10, strut_thicknesses[7]],
                            [10, 5, strut_thicknesses[6]],
                            [6, 11, strut_thicknesses[5]],
                            [11, 7, strut_thicknesses[7]],
                            [8, 12, strut_thicknesses[8]],
                            [9, 13, strut_thicknesses[8]],
                            [10, 14, strut_thicknesses[8]],
                            [11, 15, strut_thicknesses[8]],
                            [12, 16, strut_thicknesses[7]],
                            [12, 17, strut_thicknesses[6]],
                            [17, 18, strut_thicknesses[1]],
                            [18, 13, strut_thicknesses[5]],
                            [13, 19, strut_thicknesses[7]],
                            [19, 20, strut_thicknesses[3]],
                            [20, 14, strut_thicknesses[4]],
                            [14, 21, strut_thicknesses[5]],
                            [21, 22, strut_thicknesses[1]],
                            [22, 15, strut_thicknesses[6]],
                            [15, 23, strut_thicknesses[4]],
                            [23, 16, strut_thicknesses[3]],
                            [16, 17, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[2]],
                            [20, 21, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[2]]]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(2 / 3 * math.sqrt(2) * tl)
        if 1 - 2 * tl >= math.sqrt(2) * tl:
            pore_size.append(1)
        else:
            pore_size.append(math.sqrt(2) / 2 * (1 - tl))

    elif cell_name == "truncated_cube":
        truncated_ratio = 1
        strut_length = 1 / (1 + math.sqrt(2))
        tl = math.sqrt(2) / 2 * strut_length * truncated_ratio  # standing for truncated_length
        cell_node_coordinates = [[0, tl, 0], [tl, 0, 0], [1 - tl, 0, 0], [1, tl, 0], [1, 1 - tl, 0], [1 - tl, 1, 0],
                                 [tl, 1, 0], [0, 1 - tl, 0], [0, 0, tl], [1, 0, tl], [1, 1, tl], [0, 1, tl],
                                 [0, 0, 1 - tl], [1, 0, 1 - tl], [1, 1, 1 - tl], [0, 1, 1 - tl], [0, tl, 1], [tl, 0, 1],
                                 [1 - tl, 0, 1], [1, tl, 1], [1, 1 - tl, 1], [1 - tl, 1, 1], [tl, 1, 1], [0, 1 - tl, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[2]],
                            [3, 4, strut_thicknesses[3]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[2]],
                            [7, 0, strut_thicknesses[3]],
                            [0, 8, strut_thicknesses[4]],
                            [8, 1, strut_thicknesses[5]],
                            [2, 9, strut_thicknesses[6]],
                            [9, 3, strut_thicknesses[4]],
                            [4, 10, strut_thicknesses[7]],
                            [10, 5, strut_thicknesses[6]],
                            [6, 11, strut_thicknesses[5]],
                            [11, 7, strut_thicknesses[7]],
                            [8, 12, strut_thicknesses[8]],
                            [9, 13, strut_thicknesses[8]],
                            [10, 14, strut_thicknesses[8]],
                            [11, 15, strut_thicknesses[8]],
                            [12, 16, strut_thicknesses[7]],
                            [12, 17, strut_thicknesses[6]],
                            [17, 18, strut_thicknesses[1]],
                            [18, 13, strut_thicknesses[5]],
                            [13, 19, strut_thicknesses[7]],
                            [19, 20, strut_thicknesses[3]],
                            [20, 14, strut_thicknesses[4]],
                            [14, 21, strut_thicknesses[5]],
                            [21, 22, strut_thicknesses[1]],
                            [22, 15, strut_thicknesses[6]],
                            [15, 23, strut_thicknesses[4]],
                            [23, 16, strut_thicknesses[3]],
                            [16, 17, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[2]],
                            [20, 21, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[2]]]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(2 / 3 * math.sqrt(2) * tl)
        pore_size.append(1)

    elif cell_name == "octetrahedron":
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [1 / 2, 1 / 2, 0],
                                 [1 / 2, 0, 1 / 2], [1, 1 / 2, 1 / 2], [1 / 2, 1, 1 / 2], [0, 1 / 2, 1 / 2],
                                 [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], [1 / 2, 1 / 2, 1], ]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 4, strut_thicknesses[0]],
                            [1, 4, strut_thicknesses[1]],
                            [2, 4, strut_thicknesses[0]],
                            [3, 4, strut_thicknesses[1]],
                            [0, 5, strut_thicknesses[2]],
                            [1, 5, strut_thicknesses[3]],
                            [1, 6, strut_thicknesses[4]],
                            [2, 6, strut_thicknesses[5]],
                            [2, 7, strut_thicknesses[3]],
                            [3, 7, strut_thicknesses[2]],
                            [3, 8, strut_thicknesses[5]],
                            [0, 8, strut_thicknesses[4]],
                            [5, 9, strut_thicknesses[3]],
                            [5, 10, strut_thicknesses[2]],
                            [6, 10, strut_thicknesses[5]],
                            [6, 11, strut_thicknesses[4]],
                            [7, 11, strut_thicknesses[2]],
                            [7, 12, strut_thicknesses[3]],
                            [8, 12, strut_thicknesses[4]],
                            [8, 9, strut_thicknesses[5]],
                            [9, 13, strut_thicknesses[0]],
                            [10, 13, strut_thicknesses[1]],
                            [11, 13, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[1]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[1]],
                            [7, 8, strut_thicknesses[0]],
                            [8, 5, strut_thicknesses[1]],
                            [4, 5, strut_thicknesses[5]],
                            [4, 6, strut_thicknesses[2]],
                            [4, 7, strut_thicknesses[4]],
                            [4, 8, strut_thicknesses[3]],
                            [5, 13, strut_thicknesses[4]],
                            [6, 13, strut_thicknesses[3]],
                            [7, 13, strut_thicknesses[5]],
                            [8, 13, strut_thicknesses[2]],
                            ]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(math.sqrt(2) / 3)

    elif cell_name == "void_octetrahedron":
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [1 / 2, 1 / 2, 0],
                                 [1 / 2, 0, 1 / 2], [1, 1 / 2, 1 / 2], [1 / 2, 1, 1 / 2], [0, 1 / 2, 1 / 2],
                                 [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1], [1 / 2, 1 / 2, 1], ]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 4, strut_thicknesses[0]],
                            [1, 4, strut_thicknesses[1]],
                            [2, 4, strut_thicknesses[0]],
                            [3, 4, strut_thicknesses[1]],
                            [0, 5, strut_thicknesses[2]],
                            [1, 5, strut_thicknesses[3]],
                            [1, 6, strut_thicknesses[4]],
                            [2, 6, strut_thicknesses[5]],
                            [2, 7, strut_thicknesses[3]],
                            [3, 7, strut_thicknesses[2]],
                            [3, 8, strut_thicknesses[5]],
                            [0, 8, strut_thicknesses[4]],
                            [5, 9, strut_thicknesses[3]],
                            [5, 10, strut_thicknesses[2]],
                            [6, 10, strut_thicknesses[5]],
                            [6, 11, strut_thicknesses[4]],
                            [7, 11, strut_thicknesses[2]],
                            [7, 12, strut_thicknesses[3]],
                            [8, 12, strut_thicknesses[4]],
                            [8, 9, strut_thicknesses[5]],
                            [9, 13, strut_thicknesses[0]],
                            [10, 13, strut_thicknesses[1]],
                            [11, 13, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[1]]]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(math.sqrt(2) / 3 * 2)

    elif cell_name == "diamond":
        cell_node_coordinates = [[0, 0, 0], [1 / 2, 1 / 2, 0], [1, 1, 0], [1 / 2, 0, 1 / 2], [1, 1 / 2, 1 / 2],
                                 [1 / 2, 1, 1 / 2], [0, 1 / 2, 1 / 2], [1, 0, 1], [1 / 2, 1 / 2, 1],
                                 [0, 1, 1], [1 / 4, 1 / 4, 1 / 4], [3 / 4, 3 / 4, 1 / 4], [3 / 4, 1 / 4, 3 / 4],
                                 [1 / 4, 3 / 4, 3 / 4], ]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
        # CONNECTIONS: Describes the connections via the nodes.
        # node_connections = [
        #                     [0, 10, strut_multiplicator[0]],
        #                     [1, 10, strut_multiplicator[1]],
        #                     [1, 11, strut_multiplicator[2]],
        #                     [2, 11, strut_multiplicator[3]],
        #                     [3, 10, strut_multiplicator[4]],
        #                     [6, 10, strut_multiplicator[5]],
        #                     [4, 11, strut_multiplicator[6]],
        #                     [5, 11, strut_multiplicator[7]],
        #                     [3, 12, strut_multiplicator[8]],
        #                     [4, 12, strut_multiplicator[9]],
        #                     [7, 12, strut_multiplicator[10]],
        #                     [8, 12, strut_multiplicator[11]],
        #                     [5, 13, strut_multiplicator[12]],
        #                     [6, 13, strut_multiplicator[13]],
        #                     [8, 13, strut_multiplicator[14]],
        #                     [9, 13, strut_multiplicator[15]],
        #                     ]
        node_connections = [
            [0, 10, strut_thicknesses[0]],
            [1, 10, strut_thicknesses[1]],
            [1, 11, strut_thicknesses[0]],
            [2, 11, strut_thicknesses[1]],
            [3, 10, strut_thicknesses[2]],
            [6, 10, strut_thicknesses[3]],
            [4, 11, strut_thicknesses[2]],
            [5, 11, strut_thicknesses[3]],
            [3, 12, strut_thicknesses[0]],
            [4, 12, strut_thicknesses[1]],
            [7, 12, strut_thicknesses[2]],
            [8, 12, strut_thicknesses[3]],
            [5, 13, strut_thicknesses[1]],
            [6, 13, strut_thicknesses[0]],
            [8, 13, strut_thicknesses[2]],
            [9, 13, strut_thicknesses[3]],
        ]
        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(3 / 8)

    elif cell_name == "cube":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(1)

    elif cell_name == "pyramid":
        # NODES: Describe the nodes in cartesian coordinates.
        p = ratio[0]
        q = (1 - p) / 2
        cell_node_coordinates = [[-q, -q, 0], [1 + q, -q, 0], [1 + q, 1 + q, 0], [-q, 1 + q, 0],
                                 [q, q, 1], [1 - q, q, 1], [1 - q, 1 - q, 1], [q, 1 - q, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        if (math.sqrt(1 / 4 + (1 - p / 2) ** 2) * math.sin(math.atan(2 / (2 - p)) - math.atan(1 / (2 - p)))) >= 1 / 2:
            pore_size.append(1)
        else:
            pore_size.append(2 * (1 - p / 2) * math.tan(math.atan(1 / (1 - p)) / 2))

    elif cell_name == "pyramid_inv":
        # NODES: Describe the nodes in cartesian coordinates.
        p = ratio[0]
        q = (1 - p) / 2
        cell_node_coordinates = [[q, q, 0], [1 - q, q, 0], [1 - q, 1 - q, 0], [q, 1 - q, 0],
                                 [-q, -q, 1], [1 + q, -q, 1], [1 + q, 1 + q, 1], [-q, 1 + q, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        if (math.sqrt(1 / 4 + (1 - p / 2) ** 2) * math.sin(math.atan(2 / (2 - p)) - math.atan(1 / (2 - p)))) >= 1 / 2:
            pore_size.append(1)
        else:
            pore_size.append(2 * (1 - p / 2) * math.tan(math.atan(1 / (1 - p)) / 2))

    elif cell_name == "pyramid_twist":
        # NODES: Describe the nodes in cartesian coordinates.
        p = ratio[0]
        q = (1 - p) / 2
        cell_node_coordinates = [[-q, q, 0], [1 + q, q, 0], [1 + q, 1 - q, 0], [-q, 1 - q, 0],
                                 [q, -q, 1], [1 - q, -q, 1], [1 - q, 1 + q, 1], [q, 1 + q, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        if (math.sqrt(1 / 4 + (1 - p / 2) ** 2) * math.sin(math.atan(2 / (2 - p)) - math.atan(1 / (2 - p)))) >= 1 / 2:
            pore_size.append(1)
        else:
            pore_size.append(2 * (1 - p / 2) * math.tan(math.atan(1 / (1 - p)) / 2))

    elif cell_name == "pyramid_twist_inv":
        # NODES: Describe the nodes in cartesian coordinates.
        p = ratio[0]
        q = (1 - p) / 2
        cell_node_coordinates = [[q, -q, 0], [1 - q, -q, 0], [1 - q, 1 + q, 0], [q, 1 + q, 0],
                                 [-q, q, 1], [1 + q, q, 1], [1 + q, 1 - q, 1], [-q, 1 - q, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        if (math.sqrt(1 / 4 + (1 - p / 2) ** 2) * math.sin(math.atan(2 / (2 - p)) - math.atan(1 / (2 - p)))) >= 1 / 2:
            pore_size.append(1)
        else:
            pore_size.append(2 * (1 - p / 2) * math.tan(math.atan(1 / (1 - p)) / 2))

    elif cell_name == "face_diagonal_cube":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
        # strut_multiplicator = 0.2   # unit meters
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [
            [0, 1, strut_thicknesses[0]],
            [1, 2, strut_thicknesses[1]],
            [2, 3, strut_thicknesses[0]],
            [3, 0, strut_thicknesses[1]],
            [0, 4, strut_thicknesses[2]],
            [4, 5, strut_thicknesses[0]],
            [5, 6, strut_thicknesses[1]],
            [6, 7, strut_thicknesses[0]],
            [7, 4, strut_thicknesses[1]],
            [1, 5, strut_thicknesses[2]],
            [2, 6, strut_thicknesses[2]],
            [3, 7, strut_thicknesses[2]],
            # [1, 3, strut_multiplicator[3]],
            # [1, 4, strut_multiplicator[4]],
            # [1, 6, strut_multiplicator[5]],
            # [3, 4, strut_multiplicator[6]],
            # [3, 6, strut_multiplicator[7]],
            # [4, 6, strut_multiplicator[8]],
            [1, 3, strut_thicknesses[3]],
            [1, 4, strut_thicknesses[4]],
            [1, 6, strut_thicknesses[5]],
            [3, 4, strut_thicknesses[5]],
            [3, 6, strut_thicknesses[4]],
            [4, 6, strut_thicknesses[3]],
        ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(math.sqrt(2) / 3)  # ONLY estimated, needs to be determined

    elif cell_name == "face_diagonal_cube_inv":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
        # strut_multiplicator = 0.2   # unit meters
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [
            [0, 1, strut_thicknesses[0]],
            [1, 2, strut_thicknesses[1]],
            [2, 3, strut_thicknesses[0]],
            [3, 0, strut_thicknesses[1]],
            [0, 4, strut_thicknesses[2]],
            [4, 5, strut_thicknesses[0]],
            [5, 6, strut_thicknesses[1]],
            [6, 7, strut_thicknesses[0]],
            [6, 7, strut_thicknesses[0]],
            [7, 4, strut_thicknesses[1]],
            [1, 5, strut_thicknesses[2]],
            [2, 6, strut_thicknesses[2]],
            [3, 7, strut_thicknesses[2]],
            # [0, 2, strut_multiplicator[3]],
            # [0, 5, strut_multiplicator[4]],
            # [0, 7, strut_multiplicator[5]],
            # [2, 5, strut_multiplicator[6]],
            # [2, 7, strut_multiplicator[7]],
            # [5, 7, strut_multiplicator[8]],
            [0, 2, strut_thicknesses[3]],
            [0, 5, strut_thicknesses[4]],
            [0, 7, strut_thicknesses[5]],
            [2, 5, strut_thicknesses[5]],
            [2, 7, strut_thicknesses[4]],
            [5, 7, strut_thicknesses[3]],
        ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(math.sqrt(2) / 3)  # ONLY estimated, needs to be determined

    elif cell_name == "body_centered_cube":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1],
                                 [1, 0, 1], [1, 1, 1], [0, 1, 1], [1 / 2, 1 / 2, 1 / 2]]
        # strut_multiplicator = 0.2   # unit meters
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[1]],
                            [0, 4, strut_thicknesses[2]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[1]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[1]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 6, strut_thicknesses[2]],
                            [3, 7, strut_thicknesses[2]],
                            [0, 8, strut_thicknesses[3]],
                            [1, 8, strut_thicknesses[4]],
                            [2, 8, strut_thicknesses[5]],
                            [3, 8, strut_thicknesses[6]],
                            [4, 8, strut_thicknesses[5]],
                            [5, 8, strut_thicknesses[6]],
                            [6, 8, strut_thicknesses[3]],
                            [7, 8, strut_thicknesses[4]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        # pore_size[0] = 2/3 * math.sqrt(2) / 2 - strut_multiplicator[0]
        #  ONLY estimated, needs to be determined

    elif cell_name == "octahedron":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2, 1 / 2, 0], [1 / 2, 0, 1 / 2], [1, 1 / 2, 1 / 2],
                                 [1 / 2, 1, 1 / 2], [0, 1 / 2, 1 / 2], [1 / 2, 1 / 2, 1]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [0, 2, strut_thicknesses[1]],
                            [0, 3, strut_thicknesses[2]],
                            [0, 4, strut_thicknesses[3]],
                            [1, 5, strut_thicknesses[2]],
                            [2, 5, strut_thicknesses[3]],
                            [3, 5, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[1]],
                            [1, 2, strut_thicknesses[4]],
                            [2, 3, strut_thicknesses[5]],
                            [3, 4, strut_thicknesses[4]],
                            [4, 1, strut_thicknesses[5]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(math.sqrt(2) / 3)

    elif cell_name == "templar_crosse":
        # p = ratio
        # p = 0.3  # 0-1
        # q = 0.4  # 0-0.5
        p = ratio[0]
        q = ratio[1] / 2
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2 - q, 1 / 2, 0], [1 / 2, 1 / 2 - q, 0], [1 / 2 + q, 1 / 2, 0],
                                 [1 / 2, 1 / 2 + q, 0],
                                 [0, 1 / 2, 1 / 2 - q], [0, 1 / 2 + q, 1 / 2], [0, 1 / 2, 1 / 2 + q],
                                 [0, 1 / 2 - q, 1 / 2],
                                 [1 / 2, 0, 1 / 2 - q], [1 / 2 - q, 0, 1 / 2], [1 / 2, 0, 1 / 2 + q],
                                 [1 / 2 + q, 0, 1 / 2],
                                 [1, 1 / 2, 1 / 2 - q], [1, 1 / 2 - q, 1 / 2], [1, 1 / 2, 1 / 2 + q],
                                 [1, 1 / 2 + q, 1 / 2],
                                 [1 / 2, 1, 1 / 2 - q], [1 / 2 + q, 1, 1 / 2], [1 / 2, 1, 1 / 2 + q],
                                 [1 / 2 - q, 1, 1 / 2],
                                 [1 / 2 - q, 1 / 2, 1], [1 / 2, 1 / 2 - q, 1], [1 / 2 + q, 1 / 2, 1],
                                 [1 / 2, 1 / 2 + q, 1],
                                 [1 / 2 * (1 - p), 1 / 2, 1 / 2 * (1 - p)], [1 / 2, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2, 1 / 2 * (1 - p)],
                                 [1 / 2, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 - p), 1 / 2, 1 / 2 * (1 + p)], [1 / 2, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2, 1 / 2 * (1 + p)],
                                 [1 / 2, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2], [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[0]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[0]],
                            [8, 9, strut_thicknesses[0]],
                            [9, 10, strut_thicknesses[0]],
                            [10, 11, strut_thicknesses[0]],
                            [11, 8, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[0]],
                            [13, 14, strut_thicknesses[0]],
                            [14, 15, strut_thicknesses[0]],
                            [15, 12, strut_thicknesses[0]],
                            [16, 17, strut_thicknesses[0]],
                            [17, 18, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[0]],
                            [19, 16, strut_thicknesses[0]],
                            [20, 21, strut_thicknesses[0]],
                            [21, 22, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[0]],
                            [23, 20, strut_thicknesses[0]],
                            [0, 24, strut_thicknesses[0]],
                            [1, 25, strut_thicknesses[0]],
                            [2, 26, strut_thicknesses[0]],
                            [3, 27, strut_thicknesses[0]],
                            [24, 4, strut_thicknesses[0]],
                            [25, 8, strut_thicknesses[0]],
                            [26, 12, strut_thicknesses[0]],
                            [27, 16, strut_thicknesses[0]],
                            [6, 28, strut_thicknesses[0]],
                            [10, 29, strut_thicknesses[0]],
                            [14, 30, strut_thicknesses[0]],
                            [18, 31, strut_thicknesses[0]],
                            [28, 20, strut_thicknesses[0]],
                            [29, 21, strut_thicknesses[0]],
                            [30, 22, strut_thicknesses[0]],
                            [31, 23, strut_thicknesses[0]],
                            [7, 32, strut_thicknesses[0]],
                            [32, 9, strut_thicknesses[0]],
                            [11, 33, strut_thicknesses[0]],
                            [33, 13, strut_thicknesses[0]],
                            [15, 34, strut_thicknesses[0]],
                            [34, 17, strut_thicknesses[0]],
                            [19, 35, strut_thicknesses[0]],
                            [35, 5, strut_thicknesses[0]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)

    elif cell_name == "templar_alt_crosse":
        # p = ratio
        # p = 0.3   # 0-1
        # q = 0.4   # 0-0.5
        # r = 0.05  # 0-0.33
        p = ratio[0]
        q = ratio[1] / 2
        r = ratio[2] / 2
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2 - q, 1 / 2, 0], [1 / 2, 1 / 2 - q, 0], [1 / 2 + q, 1 / 2, 0],
                                 [1 / 2, 1 / 2 + q, 0],  # 0-3
                                 [0, 1 / 2, 1 / 2 - q], [0, 1 / 2 + q, 1 / 2], [0, 1 / 2, 1 / 2 + q],
                                 [0, 1 / 2 - q, 1 / 2],  # 4-7
                                 [1 / 2, 0, 1 / 2 - q], [1 / 2 - q, 0, 1 / 2], [1 / 2, 0, 1 / 2 + q],
                                 [1 / 2 + q, 0, 1 / 2],  # 8-11
                                 [1, 1 / 2, 1 / 2 - q], [1, 1 / 2 - q, 1 / 2], [1, 1 / 2, 1 / 2 + q],
                                 [1, 1 / 2 + q, 1 / 2],  # 12-15
                                 [1 / 2, 1, 1 / 2 - q], [1 / 2 + q, 1, 1 / 2], [1 / 2, 1, 1 / 2 + q],
                                 [1 / 2 - q, 1, 1 / 2],  # 16-19
                                 [1 / 2 - q, 1 / 2, 1], [1 / 2, 1 / 2 - q, 1], [1 / 2 + q, 1 / 2, 1],
                                 [1 / 2, 1 / 2 + q, 1],  # 20-23
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 24-27
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 28-31
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 + r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 + r],  # 32-35
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 36-39
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 40-43
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 - r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 - r]]  # 44-47
        #                        #######################################################################################
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[0]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[0]],
                            [8, 9, strut_thicknesses[0]],
                            [9, 10, strut_thicknesses[0]],
                            [10, 11, strut_thicknesses[0]],
                            [11, 8, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[0]],
                            [13, 14, strut_thicknesses[0]],
                            [14, 15, strut_thicknesses[0]],
                            [15, 12, strut_thicknesses[0]],
                            [16, 17, strut_thicknesses[0]],
                            [17, 18, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[0]],
                            [19, 16, strut_thicknesses[0]],
                            [20, 21, strut_thicknesses[0]],
                            [21, 22, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[0]],
                            [23, 20, strut_thicknesses[0]],
                            ###############################
                            [0, 24, strut_thicknesses[0]],
                            [1, 25, strut_thicknesses[0]],
                            [2, 26, strut_thicknesses[0]],
                            [3, 27, strut_thicknesses[0]],

                            [24, 36, strut_thicknesses[0]],
                            [25, 37, strut_thicknesses[0]],
                            [26, 38, strut_thicknesses[0]],
                            [27, 39, strut_thicknesses[0]],

                            [36, 4, strut_thicknesses[0]],
                            [37, 8, strut_thicknesses[0]],
                            [38, 12, strut_thicknesses[0]],
                            [39, 16, strut_thicknesses[0]],
                            ###############################
                            [6, 40, strut_thicknesses[0]],
                            [10, 41, strut_thicknesses[0]],
                            [14, 42, strut_thicknesses[0]],
                            [18, 43, strut_thicknesses[0]],

                            [28, 40, strut_thicknesses[0]],
                            [29, 41, strut_thicknesses[0]],
                            [30, 42, strut_thicknesses[0]],
                            [31, 43, strut_thicknesses[0]],

                            [28, 20, strut_thicknesses[0]],
                            [29, 21, strut_thicknesses[0]],
                            [30, 22, strut_thicknesses[0]],
                            [31, 23, strut_thicknesses[0]],
                            ###############################
                            [7, 44, strut_thicknesses[0]],
                            [44, 32, strut_thicknesses[0]],
                            [32, 9, strut_thicknesses[0]],

                            [11, 45, strut_thicknesses[0]],
                            [45, 33, strut_thicknesses[0]],
                            [33, 13, strut_thicknesses[0]],

                            [15, 46, strut_thicknesses[0]],
                            [46, 34, strut_thicknesses[0]],
                            [34, 17, strut_thicknesses[0]],

                            [19, 47, strut_thicknesses[0]],
                            [47, 35, strut_thicknesses[0]],
                            [35, 5, strut_thicknesses[0]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)

    elif cell_name == "templar_alt2_cross":
        # p = ratio
        # p = 0.3   # 0-1
        # q = 0.4   # 0-0.5
        # r = 0.05  # 0-0.33
        p = ratio[0]
        q = ratio[1] / 2
        r = ratio[2] / 3
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2 - q, 1 / 2 - r, 0], [1 / 2 + r, 1 / 2 - q, 0],
                                 [1 / 2 + q, 1 / 2 + r, 0], [1 / 2 - r, 1 / 2 + q, 0],  # 0-3
                                 [0, 1 / 2 + r, 1 / 2 - q], [0, 1 / 2 + q, 1 / 2 + r],
                                 [0, 1 / 2 - r, 1 / 2 + q], [0, 1 / 2 - q, 1 / 2 - r],  # 4-7
                                 [1 / 2 - r, 0, 1 / 2 - q], [1 / 2 - q, 0, 1 / 2 + r],
                                 [1 / 2 + r, 0, 1 / 2 + q], [1 / 2 + q, 0, 1 / 2 - r],  # 8-11
                                 [1, 1 / 2 - r, 1 / 2 - q], [1, 1 / 2 - q, 1 / 2 + r],
                                 [1, 1 / 2 + r, 1 / 2 + q], [1, 1 / 2 + q, 1 / 2 - r],  # 12-15
                                 [1 / 2 + r, 1, 1 / 2 - q], [1 / 2 + q, 1, 1 / 2 + r],
                                 [1 / 2 - r, 1, 1 / 2 + q], [1 / 2 - q, 1, 1 / 2 - r],  # 16-19
                                 [1 / 2 - q, 1 / 2 + r, 1], [1 / 2 - r, 1 / 2 - q, 1],
                                 [1 / 2 + q, 1 / 2 - r, 1], [1 / 2 + r, 1 / 2 + q, 1],  # 20-23
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 24-27
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 28-31
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 + r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 + r],  # 32-35
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 36-39
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 40-43
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 - r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 - r]]  # 44-47
        #                        #######################################################################################
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[0]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[0]],
                            [8, 9, strut_thicknesses[0]],
                            [9, 10, strut_thicknesses[0]],
                            [10, 11, strut_thicknesses[0]],
                            [11, 8, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[0]],
                            [13, 14, strut_thicknesses[0]],
                            [14, 15, strut_thicknesses[0]],
                            [15, 12, strut_thicknesses[0]],
                            [16, 17, strut_thicknesses[0]],
                            [17, 18, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[0]],
                            [19, 16, strut_thicknesses[0]],
                            [20, 21, strut_thicknesses[0]],
                            [21, 22, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[0]],
                            [23, 20, strut_thicknesses[0]],
                            ###############################
                            [0, 24, strut_thicknesses[0]],
                            [1, 25, strut_thicknesses[0]],
                            [2, 26, strut_thicknesses[0]],
                            [3, 27, strut_thicknesses[0]],

                            [24, 36, strut_thicknesses[0]],
                            [25, 37, strut_thicknesses[0]],
                            [26, 38, strut_thicknesses[0]],
                            [27, 39, strut_thicknesses[0]],

                            [36, 4, strut_thicknesses[0]],
                            [37, 8, strut_thicknesses[0]],
                            [38, 12, strut_thicknesses[0]],
                            [39, 16, strut_thicknesses[0]],
                            ###############################
                            [6, 40, strut_thicknesses[0]],
                            [10, 41, strut_thicknesses[0]],
                            [14, 42, strut_thicknesses[0]],
                            [18, 43, strut_thicknesses[0]],

                            [28, 40, strut_thicknesses[0]],
                            [29, 41, strut_thicknesses[0]],
                            [30, 42, strut_thicknesses[0]],
                            [31, 43, strut_thicknesses[0]],

                            [28, 20, strut_thicknesses[0]],
                            [29, 21, strut_thicknesses[0]],
                            [30, 22, strut_thicknesses[0]],
                            [31, 23, strut_thicknesses[0]],
                            ###############################
                            [7, 44, strut_thicknesses[0]],
                            [44, 32, strut_thicknesses[0]],
                            [32, 9, strut_thicknesses[0]],

                            [11, 45, strut_thicknesses[0]],
                            [45, 33, strut_thicknesses[0]],
                            [33, 13, strut_thicknesses[0]],

                            [15, 46, strut_thicknesses[0]],
                            [46, 34, strut_thicknesses[0]],
                            [34, 17, strut_thicknesses[0]],

                            [19, 47, strut_thicknesses[0]],
                            [47, 35, strut_thicknesses[0]],
                            [35, 5, strut_thicknesses[0]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)

    elif cell_name == "templar_alt2_cross_inv":
        # p = ratio
        # p = 0.3   # 0-1
        # q = 0.4   # 0-0.5
        # r = 0.05  # 0-0.33
        p = ratio[0]
        q = ratio[1] / 2
        r = ratio[2] / 3
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2 - q, 1 / 2 - r, 0], [1 / 2 + r, 1 / 2 - q, 0],
                                 [1 / 2 + q, 1 / 2 + r, 0], [1 / 2 - r, 1 / 2 + q, 0],  # 0-3
                                 [0, 1 / 2 + r, 1 / 2 - q], [0, 1 / 2 + q, 1 / 2 + r],
                                 [0, 1 / 2 - r, 1 / 2 + q], [0, 1 / 2 - q, 1 / 2 - r],  # 4-7
                                 [1 / 2 - r, 0, 1 / 2 - q], [1 / 2 - q, 0, 1 / 2 + r],
                                 [1 / 2 + r, 0, 1 / 2 + q], [1 / 2 + q, 0, 1 / 2 - r],  # 8-11
                                 [1, 1 / 2 - r, 1 / 2 - q], [1, 1 / 2 - q, 1 / 2 + r],
                                 [1, 1 / 2 + r, 1 / 2 + q], [1, 1 / 2 + q, 1 / 2 - r],  # 12-15
                                 [1 / 2 + r, 1, 1 / 2 - q], [1 / 2 + q, 1, 1 / 2 + r],
                                 [1 / 2 - r, 1, 1 / 2 + q], [1 / 2 - q, 1, 1 / 2 - r],  # 16-19
                                 [1 / 2 - q, 1 / 2 + r, 1], [1 / 2 - r, 1 / 2 - q, 1],
                                 [1 / 2 + q, 1 / 2 - r, 1], [1 / 2 + r, 1 / 2 + q, 1],  # 20-23
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 24-27
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 28-31
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 + r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 + r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 + r],  # 32-35
                                 #######################################################################################
                                 [1 / 2 * (1 - p), 1 / 2 + r, 1 / 2 * (1 - p)],
                                 [1 / 2 - r, 1 / 2 * (1 - p), 1 / 2 * (1 - p)],
                                 [1 / 2 * (1 + p), 1 / 2 - r, 1 / 2 * (1 - p)],
                                 [1 / 2 + r, 1 / 2 * (1 + p), 1 / 2 * (1 - p)],  # 36-39
                                 [1 / 2 * (1 - p), 1 / 2 - r, 1 / 2 * (1 + p)],
                                 [1 / 2 + r, 1 / 2 * (1 - p), 1 / 2 * (1 + p)],
                                 [1 / 2 * (1 + p), 1 / 2 + r, 1 / 2 * (1 + p)],
                                 [1 / 2 - r, 1 / 2 * (1 + p), 1 / 2 * (1 + p)],  # 40-43
                                 [1 / 2 * (1 - p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 - p), 1 / 2 - r],
                                 [1 / 2 * (1 + p), 1 / 2 * (1 + p), 1 / 2 - r],
                                 [1 / 2 * (1 - p), 1 / 2 * (1 + p), 1 / 2 - r]]  # 44-47
        #                        #######################################################################################
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
            cell_node_coordinates[x][2] = -cell_node_coordinates[x][2]

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[0]],
                            [2, 3, strut_thicknesses[0]],
                            [3, 0, strut_thicknesses[0]],
                            [4, 5, strut_thicknesses[0]],
                            [5, 6, strut_thicknesses[0]],
                            [6, 7, strut_thicknesses[0]],
                            [7, 4, strut_thicknesses[0]],
                            [8, 9, strut_thicknesses[0]],
                            [9, 10, strut_thicknesses[0]],
                            [10, 11, strut_thicknesses[0]],
                            [11, 8, strut_thicknesses[0]],
                            [12, 13, strut_thicknesses[0]],
                            [13, 14, strut_thicknesses[0]],
                            [14, 15, strut_thicknesses[0]],
                            [15, 12, strut_thicknesses[0]],
                            [16, 17, strut_thicknesses[0]],
                            [17, 18, strut_thicknesses[0]],
                            [18, 19, strut_thicknesses[0]],
                            [19, 16, strut_thicknesses[0]],
                            [20, 21, strut_thicknesses[0]],
                            [21, 22, strut_thicknesses[0]],
                            [22, 23, strut_thicknesses[0]],
                            [23, 20, strut_thicknesses[0]],
                            ###############################
                            [0, 24, strut_thicknesses[0]],
                            [1, 25, strut_thicknesses[0]],
                            [2, 26, strut_thicknesses[0]],
                            [3, 27, strut_thicknesses[0]],

                            [24, 36, strut_thicknesses[0]],
                            [25, 37, strut_thicknesses[0]],
                            [26, 38, strut_thicknesses[0]],
                            [27, 39, strut_thicknesses[0]],

                            [36, 4, strut_thicknesses[0]],
                            [37, 8, strut_thicknesses[0]],
                            [38, 12, strut_thicknesses[0]],
                            [39, 16, strut_thicknesses[0]],
                            ###############################
                            [6, 40, strut_thicknesses[0]],
                            [10, 41, strut_thicknesses[0]],
                            [14, 42, strut_thicknesses[0]],
                            [18, 43, strut_thicknesses[0]],

                            [28, 40, strut_thicknesses[0]],
                            [29, 41, strut_thicknesses[0]],
                            [30, 42, strut_thicknesses[0]],
                            [31, 43, strut_thicknesses[0]],

                            [28, 20, strut_thicknesses[0]],
                            [29, 21, strut_thicknesses[0]],
                            [30, 22, strut_thicknesses[0]],
                            [31, 23, strut_thicknesses[0]],
                            ###############################
                            [7, 44, strut_thicknesses[0]],
                            [44, 32, strut_thicknesses[0]],
                            [32, 9, strut_thicknesses[0]],

                            [11, 45, strut_thicknesses[0]],
                            [45, 33, strut_thicknesses[0]],
                            [33, 13, strut_thicknesses[0]],

                            [15, 46, strut_thicknesses[0]],
                            [46, 34, strut_thicknesses[0]],
                            [34, 17, strut_thicknesses[0]],

                            [19, 47, strut_thicknesses[0]],
                            [47, 35, strut_thicknesses[0]],
                            [35, 5, strut_thicknesses[0]],
                            ]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)
    elif cell_name == "tetrocta":  # These are basically just octahedrons cut on a different plane
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[1 / 2, 0, 0], [1, 1 / 2, 0], [1 / 2, 1, 0], [0, 1 / 2, 0],
                                 [0, 0, 1 / 2], [1, 0, 1 / 2], [1, 1, 1 / 2], [0, 1, 1 / 2],
                                 [1 / 2, 0, 1], [1, 1 / 2, 1], [1 / 2, 1, 1], [0, 1 / 2, 1],
                                 [1 / 2, 1 / 2, 1 / 2]]
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 3):
                cell_node_coordinates[x][y] -= 1 / 2
        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1, strut_thicknesses[0]],
                            [1, 2, strut_thicknesses[1]],
                            [2, 3, strut_thicknesses[2]],
                            [3, 0, strut_thicknesses[3]],
                            [8, 9, strut_thicknesses[0]],
                            [9, 10, strut_thicknesses[1]],
                            [10, 11, strut_thicknesses[2]],
                            [11, 8, strut_thicknesses[3]],
                            [0, 5, strut_thicknesses[4]],
                            [1, 5, strut_thicknesses[5]],
                            [1, 6, strut_thicknesses[6]],
                            [2, 6, strut_thicknesses[7]],
                            [2, 7, strut_thicknesses[8]],
                            [3, 7, strut_thicknesses[9]],
                            [3, 4, strut_thicknesses[10]],
                            [0, 4, strut_thicknesses[11]],
                            [4, 8, strut_thicknesses[12]],
                            [5, 8, strut_thicknesses[13]],
                            [5, 9, strut_thicknesses[14]],
                            [6, 9, strut_thicknesses[15]],
                            [6, 10, strut_thicknesses[16]],
                            [7, 10, strut_thicknesses[17]],
                            [7, 11, strut_thicknesses[18]],
                            [4, 11, strut_thicknesses[19]]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(1)

    elif cell_name == "file_super_truss":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = csv_reader.csv_read_nodes("C:\\Users/Maxe-PC2/Desktop/code_and_csv/"
                                                          "1nC[10]tL[1]tG[1]uL[1000]di[200]/nodes.csv", 0)
        # for x in range(0, len(cell_node_coordinates)):
        #     for y in range(0, 3):
        #         cell_node_coordinates[x][y] -= 1/2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = csv_reader.csv_read_mems("C:\\Users/Maxe-PC2/Desktop/code_and_csv/"
                                                    "1nC[10]tL[1]tG[1]uL[1000]di[200]/mems.csv", 0)

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)

    elif cell_name == "square":
        # NODES: Describe the nodes in cartesian coordinates.
        cell_node_coordinates = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
        # strut_multiplicator = 0.2   # unit meters
        for x in range(0, len(cell_node_coordinates)):
            for y in range(0, 2):
                cell_node_coordinates[x][y] -= 1 / 2

        # CONNECTIONS: Describes the connections via the nodes.
        node_connections = [[0, 1],
                            [1, 2],
                            [2, 3],
                            [3, 0]]

        # PORE SIZE: Describes the pore size of the Cell in standard size 1.
        # It is described by the diameter of the biggest fitting sphere in the cell
        pore_size.append(0)

    else:
        node_connections = [None, None]
        cell_node_coordinates = None
        pore_size = None
        exit("ERROR: cell_name specified is not defined in the library")
    # DEFINE the strut thickness of each strut

    if len(node_connections[1]) < 3:
        counter = 0
        for struts in node_connections:
            struts.append(strut_thicknesses[counter])
            counter += 1
        del counter

    # SIZING change to cell size
    for x in range(0, len(cell_node_coordinates)):
        for y in range(0, 3):
            cell_node_coordinates[x][y] *= cell_size
    for counter in range(0, len(pore_size)):
        pore_size[counter] *= cell_size
        pore_size[counter] -= strut_thicknesses[0]
        if pore_size[counter] < 0:
            pore_size[counter] = 0
    # GENERATE beginning and ending coordinates of each connection in cartesian coordinates.
    cell_node_connections = list()
    for connection_points in node_connections:
        cell_node_connections.append([cell_node_coordinates[connection_points[0]],
                                      cell_node_coordinates[connection_points[1]],
                                      connection_points[2]])

    cell = Cell(name=(cell_name + affix), pore_size=pore_size,
                nodes=cell_node_coordinates, connections=cell_node_connections, strut_thicknesses=strut_thicknesses)
    return cell
