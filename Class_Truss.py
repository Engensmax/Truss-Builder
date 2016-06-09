"""
This class defines the truss which will be generated with abaqus script.
The object contains the corner nodes for each cell, and the cell that is attached on every node.
"""


class Truss:
    def __init__(self, name, nodes, cells, cell_size, number_of_cells):
        self.name = name                    # Name of the cells. F.e. "cubetruss"
        self.nodes = nodes                  # Syntax: [["node1x", "node1y", "node1z", "self.cells[0]"], ...]
        self.cells = cells                  # Syntax: ["Cell1","Cell2",...]
        self.cell_size = cell_size          # Unit length of the smallest unit cell
        self.number_of_cells = number_of_cells

# FINDS THE POINTS IN A PLANE DEFINED BY THE NORMAL AXIS AND THE COORDINATE WHERE IT INTERSECTS WITH SAID AXIS
    def find_points_in_plane(self, axis, axis_value, accuracy):

        if axis == "x":
            array_position = 0
        if axis == "y":
            array_position = 1
        if axis == "z":
            array_position = 2

        list_of_points = list()

        for truss_nodes in self.nodes:
                for cell_nodes in truss_nodes[3].nodes:
                    node = [x + y for x, y in zip(truss_nodes, cell_nodes)]
                    if axis_value - accuracy <= node[array_position] <= \
                       axis_value + accuracy:
                        check = True
                        for point in list_of_points:
                            if abs(node[0] - point[0]) < 1e-9 and \
                               abs(node[1] - point[1]) < 1e-9 and \
                               abs(node[2] - point[2]) < 1e-9:
                                check = False
                        if check:
                            list_of_points.append(node)
        return list_of_points

# FINDS THE POINTS IN A SPACE DEFINED BY BOUNDARIES FOR EACH OF THE THREE COORDINATE DIRECTIONS
    def find_points_in_space(self, boundaries):

        list_of_points = list()

        for truss_nodes in self.nodes:
            for cell_nodes in truss_nodes[3].nodes:
                node = [x + y for x, y in zip(truss_nodes, cell_nodes)]
                if boundaries[0][0] <= node[0] <= boundaries[0][1]:
                    if boundaries[1][0] <= node[1] <= boundaries[1][1]:
                        if boundaries[2][0] <= node[2] <= boundaries[2][1]:
                            check = True
                            for point in list_of_points:
                                if abs(node[0] - point[0]) < 1e-9 and \
                                   abs(node[1] - point[1]) < 1e-9 and \
                                   abs(node[2] - point[2]) < 1e-9:
                                    check = False
                            if check:
                                list_of_points.append(node)

        return list_of_points
