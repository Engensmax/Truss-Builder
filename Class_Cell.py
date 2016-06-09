"""
This class defines the cell which will be inserted into the truss.
The object contains the needed nodes and the connections in between, which are dependent of the nodes to evade errors.
"""


class Cell:
    def __init__(self, name, pore_size, nodes, connections, strut_thicknesses):
        self.name = name                        # Name of the cell. F.e. "cube"
        self.pore_size = pore_size              # Should be determined once per cell-> Maybe determine roundness of pore
        self.nodes = nodes                      # Syntax: [["node1x", "node1y", node1z"], ...]
        self.connections = connections          # Syntax: [["node1", "node2", "thickness"], ...]
        self.strut_thicknesses = strut_thicknesses
