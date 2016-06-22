"""
This File initiates the abaqus script to run for the optimization.
It consists of several functions that append text to a .py -file which is then run in abaqus.

The first block of functions creates a solid model which can be exported to stl.
The second block of functions creates a wireframe model and does an analysis of its properties.
The third block reads the output database that the simulation creates and returns it in a pickled file.

"""
import sys
import math
import numpy


########################################################################################################################
# FUNCTIONS FOR THE SOLID AND STL-FILE-GENERATION
# EXTRUDES A SIMPLE STRUT. POSSIBLE SECTIONS ARE SQUARE, HEXAGON, OCTAGON, DODECAGON
def generate_strut(filename, strut_name, affix, connection):
    file = open("".join(filename), "a")
    thickness = connection[2]
    begin_vector = numpy.asarray(connection[0])
    end_vector = numpy.asarray(connection[1])
    distance = numpy.subtract(end_vector, begin_vector)
    length = numpy.linalg.norm(distance)

    # GENERATE BASE SKETCH
    file.write(
        "s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=200.0)\n"
        "g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints\n"
        "s.setPrimaryObject(option=STANDALONE)\n")

    # SQUARE
    if strut_name == "square":
        file.write(
            "s.Line(point1=(" + str(-thickness / 2) + ", " + str(-thickness / 2) + "), point2=(" + str(thickness / 2) +
            ", " + str(-thickness / 2) + "))\n"
            "s.Line(point1=(" + str(thickness / 2) + ", " + str(-thickness / 2) + "), point2=(" + str(thickness / 2) +
            ", " + str(thickness / 2) + "))\n"
            "s.Line(point1=(" + str(thickness / 2) + ", " + str(thickness / 2) + "), point2=(" + str(-thickness / 2) +
            ", " + str(thickness / 2) + "))\n"
            "s.Line(point1=(" + str(-thickness / 2) + ", " + str(thickness / 2) + "), point2=(" + str(-thickness / 2) +
            ", " + str(-thickness / 2) + "))\n")

    # OCTAGON
    elif strut_name == "octagon":
        b = math.sqrt(2) / 2 * (1 - (math.sqrt(2) / (1 + math.sqrt(2)))) * thickness
        file.write(
            "s.Line(point1=(" + str(-thickness / 2 + b) + ", " + str(-thickness / 2) + "), point2=(" +
            str(thickness / 2 - b) + ", " + str(-thickness / 2) + "))\n"
            "s.Line(point1=(" + str(thickness / 2 - b) + ", " + str(-thickness / 2) + "), point2=(" +
            str(thickness / 2) + ", " + str(-thickness / 2 + b) + "))\n"
            "s.Line(point1=(" + str(thickness / 2) + ", " + str(-thickness / 2 + b) + "), point2=(" +
            str(thickness / 2) + ", " + str(thickness / 2 - b) + "))\n"
            "s.Line(point1=(" + str(thickness / 2) + ", " + str(thickness / 2 - b) + "), point2=(" +
            str(thickness / 2 - b) + ", " + str(thickness / 2) + "))\n"
            "s.Line(point1=(" + str(thickness / 2 - b) + ", " + str(thickness / 2) + "), point2=(" +
            str(-thickness / 2 + b) + ", " + str(thickness / 2) + "))\n"
            "s.Line(point1=(" + str(-thickness / 2 + b) + ", " + str(thickness / 2) + "), point2=(" +
            str(-thickness / 2) + ", " + str(thickness / 2 - b) + "))\n"
            "s.Line(point1=(" + str(-thickness / 2) + ", " + str(thickness / 2 - b) + "), point2=(" +
            str(-thickness / 2) + ", " + str(-thickness / 2 + b) + "))\n"
            "s.Line(point1=(" + str(-thickness / 2) + ", " + str(-thickness / 2 + b) + "), point2=(" +
            str(-thickness / 2 + b) + ", " + str(-thickness / 2) + "))\n")

    # DODECAGON
    elif strut_name == "dodecagon":
        for counter in range(0, 12):
            file.write("s.Line(point1=(" +
                       str(math.cos((15 + 30 * counter) / 180 * math.pi) * thickness / 2) + ", " +
                       str(math.sin((15 + 30 * counter) / 180 * math.pi) * thickness / 2) + "), point2=(" +
                       str(math.cos((15 + 30 * (counter + 1)) / 180 * math.pi) * thickness / 2) + ", " +
                       str(math.sin((15 + 30 * (counter + 1)) / 180 * math.pi) * thickness / 2) + "))\n")

    # HEXAGON
    elif strut_name == "hexagon":
        for counter in range(0, 6):
            file.write("s.Line(point1=(" +
                       str(math.cos((30 + 60 * counter) / 180 * math.pi) * thickness / 2) + ", " +
                       str(math.sin((30 + 60 * counter) / 180 * math.pi) * thickness / 2) + "), point2=(" +
                       str(math.cos((30 + 60 * (counter + 1)) / 180 * math.pi) * thickness / 2) + ", " +
                       str(math.sin((30 + 60 * (counter + 1)) / 180 * math.pi) * thickness / 2) + "))\n")

    else:
        sys.exit("ERROR: strut_name specified is not defined in the library")

    file.write("mdb.models['Model-1'].ConstrainedSketch(name='strut_sketch-" + str(strut_name) +
               str(affix) + "', objectToCopy=s)\n")

    # EXTRUDE BASE SKETCH
    file.write(
        "p = mdb.models['Model-1'].Part(name='strut_" + str(strut_name) + str(affix) +
        "', dimensionality=THREE_D, type=DEFORMABLE_BODY)\n"
        "p = mdb.models['Model-1'].parts['strut_" + str(strut_name) + str(affix) + "']\n"
        "p.BaseSolidExtrude(sketch=s, depth=" + str(length) + ")\n"
        "s.unsetPrimaryObject()\n")

    file.close()


# ADDS A SINGLE STRUT TO THE CELL STRUCTURE. THIS IS USED IN generate_cell()
def add_strut_to_cell(filename, strut_name, instance_name, strut_counter, connections):
    file = open("".join(filename), "a")
    begin_vector = numpy.asarray(connections[0])  # Determine the rotation and translation of the strut
    end_vector = numpy.asarray(connections[1])
    distance = numpy.subtract(end_vector, begin_vector)
    length = numpy.linalg.norm(distance)
    normal = numpy.cross(distance, [0, 0, 1])
    if numpy.linalg.norm(normal) == 0:
        normal = [1, 0, 0]
    angle = -abs(math.acos(numpy.dot([0, 0, 1], distance) / length)) / math.pi * 180
    # INCLUDE INTO ASSEMBLY
    file.write(
        "a = mdb.models['Model-1'].rootAssembly\n"

        "a.DatumCsysByDefault(CARTESIAN)\n"

        "p = mdb.models['Model-1'].parts['strut_" + str(strut_name) + str(strut_counter) + "']\n"

        "a.Instance(name='instance_" + str(instance_name) + "-" + str(strut_counter) + "', part=p, dependent=ON)\n"

        "a = mdb.models['Model-1'].rootAssembly\n"

        "a.rotate(instanceList=('instance_" + str(instance_name) + "-" + str(strut_counter) +
        "', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(" + str(normal[0]) + ", " +
        str(normal[1]) + ", " + str(normal[2]) + "), angle=" + str(angle) + ")\n"

        "a.translate(instanceList=('instance_" + str(instance_name) + "-" + str(strut_counter) + "', ), vector=(" +
        str(begin_vector[0]) + ", " +
        str(begin_vector[1]) + ", " +
        str(begin_vector[2]) + "))\n"
    )

    file.close()


# ADDS A SINGLE CELL TO THE TRUSS STRUCTURE. THIS IS USED IN generate_solid()
def add_cell_to_assembly(filename, cell_name, instance_name, cell_counter, truss_node_coordinates):
    file = open("".join(filename), "a")

    # INCLUDE INTO ASSEMBLY
    file.write(
        "a = mdb.models['Model-1'].rootAssembly\n"

        "a.DatumCsysByDefault(CARTESIAN)\n"

        "p = mdb.models['Model-1'].parts['" + str(cell_name) + "']\n"

        "a.Instance(name='instance_" + str(instance_name) + "-" + str(cell_counter) + "', part=p, dependent=ON)\n"

        "a = mdb.models['Model-1'].rootAssembly\n"

        "a.translate(instanceList=('instance_" + str(instance_name) + "-" + str(cell_counter) + "', ), vector=(" +
        str(truss_node_coordinates[0]) + ", " +
        str(truss_node_coordinates[1]) + ", " +
        str(truss_node_coordinates[2]) + "))\n")
    file.close()


# MERGES ALL PARTS OF AN INSTANCE. THIS IS USED IN generate_cell() AND generate_solid()
def merge(filename, merge_name, instance_name, part_counter):
    file = open("".join(filename), "a")
    if part_counter > 1:
        file.write("a.InstanceFromBooleanMerge(name='" + str(merge_name) + "', instances=(")
        for counter in range(0, part_counter):
            file.write("a.instances['instance_" + str(instance_name) + "-" + str(counter) + "'], ")
        file.write("), originalInstances=SUPPRESS, domain=GEOMETRY)\n")
        for counter in range(0, part_counter):
            file.write("del a.features['instance_" + str(instance_name) + "-" + str(counter) + "']\n")
    else:
        file.write("mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='instance_" + str(instance_name) +
                   "-0', toName='" + str(merge_name) + "-1')\n")
    file.close()


# GENERATES THE SOLID CELL
def generate_cell(filename, cell, strut_name):
    strut_counter = 0
    for connection in cell.connections:
        generate_strut(filename, strut_name, strut_counter, connection)
        add_strut_to_cell(filename, strut_name, cell.name, strut_counter, connection)
        strut_counter += 1

    merge(filename, cell.name, cell.name, strut_counter)  # "Instance with name 'cell.name'
    delete_struts(filename, strut_name, strut_counter)


# DELETES ALL CELL INSTANCES AFTER MERGING
def delete_struts(filename, strut_name, number_of_struts):
    for strut_counter in range(0, number_of_struts):
        file = open("".join(filename), "a")
        file.write("del mdb.models['Model-1'].parts['strut_" + str(strut_name) + str(strut_counter) + "']\n")
        file.close()


def delete_instances(filename, objects):
    file = open("".join(filename), "a")
    for obj in objects:
        file.write("del a.features['" + str(obj.name) + "-1']\n")

    file.close()


# CUT OFF THE BORDERS OF THE TRUSS
def cut_off_borders(filename, cutoff_name, merge_name, truss, number_of_cells):
    file = open("".join(filename), "a")
    file.write("s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',sheetSize=200.0)\n"
               "g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints\n"
               "s.setPrimaryObject(option=STANDALONE)\n")
    file.write("s.Line(point1=(" + str(-(number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + "), point2=(" +
               str((number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + "))\n"
               "s.Line(point1=(" + str((number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + "), point2=(" +
               str((number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str((number_of_cells + 4) * truss.cell_size / 2) + "))\n"
               "s.Line(point1=(" + str((number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str((number_of_cells + 4) * truss.cell_size / 2) + "), point2=(" +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str((number_of_cells + 4) * truss.cell_size / 2) + "))\n"
               "s.Line(point1=(" + str(-(number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str((number_of_cells + 4) * truss.cell_size / 2) + "), point2=(" +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + ", " +
               str(-(number_of_cells + 4) * truss.cell_size / 2) + "))\n")
    file.write("mdb.models['Model-1'].ConstrainedSketch(name='cut_off', objectToCopy=s)\n")
    file.write(
        "p = mdb.models['Model-1'].Part(name='cut_off', dimensionality=THREE_D, type=DEFORMABLE_BODY)\n"
        "p = mdb.models['Model-1'].parts['cut_off']\n"
        "p.BaseSolidExtrude(sketch=s, depth=" + str(2 * truss.cell_size) + ")\n"
                                                                           "s.unsetPrimaryObject()\n")
    file.write(
        "a = mdb.models['Model-1'].rootAssembly\n"

        "a.DatumCsysByDefault(CARTESIAN)\n"

        "p = mdb.models['Model-1'].parts['cut_off']\n"

        "a.Instance(name='instance_cut_off1', part=p, dependent=ON)\n"
        "a.Instance(name='instance_cut_off2', part=p, dependent=ON)\n"
        "a.Instance(name='instance_cut_off3', part=p, dependent=ON)\n"
        "a.Instance(name='instance_cut_off4', part=p, dependent=ON)\n"
        "a.Instance(name='instance_cut_off5', part=p, dependent=ON)\n"
        "a.Instance(name='instance_cut_off6', part=p, dependent=ON)\n"

        "a.translate(instanceList=('instance_cut_off1', ), vector=(" +
        str(0) + ", " +
        str(0) + ", " +
        str((number_of_cells - 0.5) * truss.cell_size) + "))\n"
        "a.translate(instanceList=('instance_cut_off1', ), vector=(" + str(truss.cell_size) + "," +
        str(truss.cell_size) + ",0))\n"
        "a.rotate(instanceList=('instance_cut_off2', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0,1,0), angle=180)\n"
        "a.translate(instanceList=('instance_cut_off2', ), vector=(" +
        str(0) + ", " +
        str(0) + ", " +
        str(-0.5 * truss.cell_size) + "))\n"
                                      "a.translate(instanceList=('instance_cut_off2', ), vector=(" +
        str(truss.cell_size) + "," + str(truss.cell_size) + ",0))\n"
        "a.rotate(instanceList=('instance_cut_off3', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0,1,0), angle=-90)\n"
        "a.translate(instanceList=('instance_cut_off3', ), vector=(" +
        str(-0.5 * truss.cell_size) + ", " +
        str(0) + ", " +
        str(0) + "))\n"
                 "a.translate(instanceList=('instance_cut_off3', ), vector=(0, " + str(truss.cell_size) + "," +
        str(truss.cell_size) + "))\n"
        "a.rotate(instanceList=('instance_cut_off4', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(0,1,0), angle=90)\n"
        "a.translate(instanceList=('instance_cut_off4', ), vector=(" +
        str((number_of_cells - 0.5) * truss.cell_size) + ", " +
        str(0) + ", " +
        str(0) + "))\n"
                 "a.translate(instanceList=('instance_cut_off4', ), vector=(0, " + str(truss.cell_size) + "," +
        str(truss.cell_size) + "))\n"
        "a.rotate(instanceList=('instance_cut_off5', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1,0,0), angle=90)\n"
        "a.translate(instanceList=('instance_cut_off5', ), vector=(" +
        str(0) + ", " +
        str(-0.5 * truss.cell_size) + ", " +
        str(0) + "))\n"
        "a.translate(instanceList=('instance_cut_off5', ), vector=(" + str(truss.cell_size) + ", 0, " +
        str(truss.cell_size) + "))\n"
        "a.rotate(instanceList=('instance_cut_off6', ), axisPoint=(0.0, 0.0, 0.0), axisDirection=(1,0,0), angle=-90)\n"
        "a.translate(instanceList=('instance_cut_off6', ), vector=(" +
        str(0) + ", " +
        str((number_of_cells - 0.5) * truss.cell_size) + ", " +
        str(0) + "))\n"
        "a.translate(instanceList=('instance_cut_off6', ), vector=(" + str(truss.cell_size) + ", 0, " +
        str(truss.cell_size) + "))\n"
    )

    file.write("a.InstanceFromBooleanCut(name='" + cutoff_name + "', "
               "instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['" + merge_name + "'], "
               "cuttingInstances=(a.instances['instance_cut_off1'], a.instances['instance_cut_off2'], "
               "a.instances['instance_cut_off3'], a.instances['instance_cut_off4'], a.instances['instance_cut_off5'], "
               "a.instances['instance_cut_off6'], ), originalInstances=DELETE)\n")
    file.close()


# MEASURE THE VOLUME AND SURFACE ARE OF THE TRUSS CREATED IN ABAQUS. ONLY WORKS IF THE BORDERS ARE CUT OFF
def get_area(script, filename, cutoff):
    file = open("".join(filename), "a")
    file.write("results['Volume'] = a.getVolume()\n"
               "results['Surface_Area'] = a.getArea(a.instances['" + filename[1] +
               "-1'].faces)\n"
               "print('Results: ' + str(results['Surface_Area']))\n")
    if cutoff:
        if script.truss.name == "cubes" or script.truss.name == "body_centered_cubes" or \
                        script.truss.name == "octetrahedrons" or script.truss.name == "face_diagonal_cubes_alt" or \
                        script.truss.name == "void_octetrahedrons":
            file.write("area_error=-6 * a.getArea(a.instances['" + filename[1] +
                       "-1'].faces.findAt(((" + str(script.truss.cells[0].strut_thicknesses[0] / 32 -
                                                    script.truss.cell_size / 2) +
                       ", " + str(-script.truss.cell_size / 2) + ", " +
                       str(script.truss.cells[0].strut_thicknesses[0] / 32 - script.truss.cell_size / 2) + "),),))\n"
                       "print('Area Error: ' + str(area_error))\n"
                       "results['Surface_Area']+=area_error\n")
        elif script.truss.name == "diamonds":
            file.write("-12 * a.getArea(a.instances['" + filename[1] +
                       "-1'].faces.findAt(((" +
                       str(script.truss.cells[0].strut_thicknesses[0] / 32 - script.truss.cell_size / 2) +
                       ", " + str(-script.truss.cell_size / 2) + ", " +
                       str(script.truss.cells[0].strut_thicknesses[0] / 32 - script.truss.cell_size / 2) + "),),))"
                       )
            file.write("-6 * a.getArea(a.instances['" + filename[1] +
                       "-1'].faces.findAt(((" + str(0) +
                       ", " + str(-script.truss.cell_size / 2) + ", " + str(0) + "),),))\n"
                       )
        elif script.truss.name == "truncated_cubes":
            file.write("-6 * a.getArea(a.instances['" + filename[1] +
                       "-1'].faces.findAt(((" +
                       str(script.truss.cells[0].strut_thicknesses[0] / 32 - script.truss.cell_size / 2) +
                       ", " + str(-script.truss.cell_size / 2) + ", " + str(0) + "),),))\n"
                       )
        else:
            print("The Calculated Surface Area is too high for it does not substract the outside area of the " +
                  str(script.truss.name) + " truss")
    else:
        print("No surface area correction because there is no cutoff")

########################################################################################################################
# FUNCTIONS FOR THE FINITE ELEMENT ANALYSIS AND WIREFRAME GENERATION


# GENERATE THE WIREFRAME
def generate_wireframe(filename, truss):
    file = open("".join(filename), "a")
    file.write(
        "p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=THREE_D, type=DEFORMABLE_BODY)\n"
        "p.ReferencePoint(point=(0.0, 0.0, 0.0))\n"
        "p.WirePolyLine(points=(\n")
    for nodes in truss.nodes:
        for connections in nodes[3].connections:
            file.write("                       ((" + str(connections[0][0] + nodes[0]) +
                       ", " + str(connections[0][1] + nodes[1]) +
                       ", " + str(connections[0][2] + nodes[2]) +
                       "), (" + str(connections[1][0] + nodes[0]) +
                       ", " + str(connections[1][1] + nodes[1]) +
                       ", " + str(connections[1][2] + nodes[2]) +
                       ")), \n")

    file.write(
        "), mergeType=IMPRINT, meshable=ON)\n"
        "p = mdb.models['Model-1'].parts['Part-1']\n"
        "e = p.edges\n"
        "edges = e.getSequenceFromMask(mask=('[#7 ]', ), )\n"
        "p.Set(edges=edges, name='Wire-" + str(truss.name) + "')\n"
                                                             "a = mdb.models['Model-1'].rootAssembly\n"
                                                             "a.DatumCsysByDefault(CARTESIAN)\n")

    file.close()


# DEFINE THE MATERIAL PROPERTIES
def define_material(filename, material_name, young_modulus, poisson_ratio):
    file = open("".join(filename), "a")
    file.write("mdb.models['Model-1'].Material(name='" + str(material_name) +
               "', description='Automatically generated. See Class_Script')\n"
               "mdb.models['Model-1'].materials['" + str(material_name) + "'].Elastic(table=((" +
               str(young_modulus) + ", " + str(poisson_ratio) + "), ))\n")
    file.close()


# ASSIGNS PROFILE AND MATERIAL
def assign_material_to_wire(filename, truss, material_name):
    file = open("".join(filename), "a")

    for cell in truss.cells:
        list_of_nodes = list()

        for node in truss.nodes:
            if cell.name == node[3].name:
                list_of_nodes.append(node)

        counter = 0
        for connection in cell.connections:
            file.write("mdb.models['Model-1'].CircularProfile(name='Profile-" + str(cell.name) + "-" + str(counter) +
                       "', r=" + str(connection[2] / 2) + ")\n"
                       "mdb.models['Model-1'].BeamSection(name='Section-" + str(cell.name) + "-" + str(counter) +
                       "',integration=DURING_ANALYSIS, poissonRatio=0.0, profile='Profile-" + str(cell.name) + "-" +
                       str(counter) + "',material='" + str(material_name) + "', temperatureVar=LINEAR, "
                       "consistentMassMatrix=False)\n"
                       "r = regionToolset.Region(edges=p.edges.findAt(")
            for connection_node in list_of_nodes:
                file.write("((" + str(1 / 2 * (connection[0][0] + connection[1][0]) + connection_node[0]) + ", " +
                           str(1 / 2 * (connection[0][1] + connection[1][1]) + connection_node[1]) + ", " +
                           str(1 / 2 * (connection[0][2] + connection[1][2]) + connection_node[2]) + ", " +
                           "), ), ")
            file.write("))\n"
                       "p.SectionAssignment(region=r, sectionName='Section-" + str(cell.name) + "-" + str(counter) +
                       "', offset=0.0,"
                       "offsetType=MIDDLE_SURFACE, offsetField='',"
                       "thicknessAssignment=FROM_SECTION)\n"
                       "p.assignBeamSectionOrientation(region=r, method=N1_COSINES, n1=(1.1, 0.9, 1.0))\n")
            counter += 1
        del counter

    file.write("p.assignBeamSectionOrientation(region=r, method=N1_COSINES, n1=(1.0, 1.0, 1.0))\n")


# MESHES THE TRUSS
def mesh_part(filename, truss, mesh_size):
    file = open("".join(filename), "a")
    file.write("a = mdb.models['Model-1'].rootAssembly\n"
               "p = mdb.models['Model-1'].parts['Part-1']\n"
               "a.Instance(name='Part-1-1', part=p, dependent=ON)\n"
               "p.seedPart(size=" + str(mesh_size) + ", deviationFactor=0.1, minSizeFactor=0.1)\n"
               "p.generateMesh()\n"
               "p.setElementType(regions=regionToolset.Region(p.edges), "
               "elemTypes=(mesh.ElemType(elemCode=B32,elemLibrary=STANDARD),))\n")
    file.close()


# CREATES A STATIC STEP
def create_static_step(filename, step_name):
    file = open("".join(filename), "a")
    file.write("mdb.models['Model-1'].StaticStep(name='" + str(step_name) + "', previous='Initial')\n")
    file.close()


# DEFINES LOADINGS ON THE TRUSS
def define_loadings(filename, step_name, affix, vertices, load_type, load_type_letter, force):
    file = open("".join(filename), "a")
    file.write("loading_points = a.instances['Part-1-1'].vertices.findAt(")
    for vertex_coordinates in vertices:
        file.write("((" + str(vertex_coordinates[0]) +
                   ", " + str(vertex_coordinates[1]) +
                   ", " + str(vertex_coordinates[2]) + "), ), ")
    file.write(
        ")\n"
        "mdb.models['Model-1']." + str(load_type) + "(name='" + str(step_name + affix) + "_load', createStepName='" +
        str(step_name) + "',region=a.Set(vertices=loading_points, name='" + str(step_name) + "_1" + str(affix) +
        "'), c" + str(load_type_letter) + "1=" + str(force[0]) + ", c" + str(load_type_letter) + "2=" + str(force[1]) +
        ", c" + str(load_type_letter) + "3=" + str(force[2]) +
        ", distributionType=UNIFORM, field='', localCsys=None)\n")
    file.close()
    # ConcentratedForce     f
    # Moment                m


# DEFINES BOUNDARY CONDITIONS OF THE MODEL
def define_boundary_conditions(filename, step_name, affix, vertices, direction):
    file = open("".join(filename), "a")
    condition_type = 'Displacement'
    file.write("fixes = a.instances['Part-1-1'].vertices.findAt(")
    for vertex_coordinates in vertices:
        file.write("((" + str(vertex_coordinates[0]) +
                   ", " + str(vertex_coordinates[1]) +
                   ", " + str(vertex_coordinates[2]) + "), ), ")
    file.write(")\n"
               "mdb.models['Model-1']." + str(condition_type) + "BC(name='" + str(step_name) + str(affix) +
               "_BC', createStepName='" + str(step_name) + "', region=a.Set(vertices=fixes, name='" +
               str(step_name) + "_2" + str(affix) + "'), localCsys=None, " + str(direction) + ")\n")
    file.close()
    # condition_type:
    # Encastre
    # Pinned
    # Xsymm
    # Ysymm
    # Zsymm
    # Xasymm
    # Yasymm
    # Zasymm
    # Displacement
    # direction:
    # u1, u2, u3, ur1, ur2, ur3


# DEACTIVATES BOUNDARY CONDITIONS OF FORMER STEPS (THEY GET PROPAGATED BY ABAQUS DEFAULT)
def deactivate_boundary_conditions(filename, step_name, deactivate_step_name):
    file = open("".join(filename), "a")
    file.write("mdb.models['Model-1'].boundaryConditions['" + str(step_name) + "_BC'].deactivate('" +
               str(deactivate_step_name) + "')\n")
    file.close()


# DEACTIVATES LOADINGS OF FORMER STEPS (THEY GET PROPAGATED BY ABAQUS DEFAULT)
def deactivate_loadings(filename, step_name, deactivate_step_name):
    file = open("".join(filename), "a")
    file.write("mdb.models['Model-1'].loads['" + str(step_name) + "_load'].deactivate('" +
               str(deactivate_step_name) + "')\n")
    file.close()


# GET THE DISPLACEMENT OF REQUESTED FIELD OUTPUT
def request_field_output(filename, step_name, output_name):
    file = open("".join(filename), "a")
    file.write("mdb.models['Model-1'].FieldOutputRequest(name='" + str(output_name) + "', createStepName='" +
               str(step_name) + "', variables=('U','S', ))\n")
    file.close()


# SUBMITS THE SIMULATION
def submit(filename, job_name):
    file = open("".join(filename), "a")
    file.write("mdb.Job(name='" + str(job_name) + "', model='Model-1', description='', type=ANALYSIS, "
               "atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, "
               "memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, "
               "explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, "
               "modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB)\n"
               "mdb.jobs['" + str(job_name) + "'].submit(consistencyChecking=OFF)\n"
               "mdb.jobs['" + str(job_name) + "'].waitForCompletion()\n"
               )
    file.close()


########################################################################################################################
# FUNCTIONS FOR THE OUTPUT EVALUATION OF THE SIMULATION

# READ THE DISPLACEMENTS OF ALL SIDES OF A CERTAIN STEP AND RETURNS THEM
def read_odb_step(filename, step_name, job_name):
    file = open("".join(filename), "a")
    file.write("myOdb = odbAccess.openOdb(path='" + str(job_name) + ".odb')\n")
    # for step_name in step_name:
    file.write("Step = myOdb.steps['" + str(step_name) + "']\n"
               "displacement = Step.frames[1].fieldOutputs['U']\n"
               "list_of_sides = ['SIGMA_X_1', 'SIGMA_X_2_X', 'SIGMA_Y_1', 'SIGMA_Y_2_Y', 'SIGMA_Z_1', 'SIGMA_Z_2_Z']\n"
               "node_region=dict()\n"
               "displacements = dict()\n"
               "for sides in list_of_sides:\n"
               "    node_region[sides]=myOdb.rootAssembly.nodeSets[sides]\n"
               "    values = displacement.getSubset(region=node_region[sides]).values\n"
               "    displacements[sides]=list()\n"
               "    for value in values:\n"
               "        displacements[sides].append(value.data)\n"
               "results['" + step_name + "'] = displacements\n")
    file.close()


########################################################################################################################


class Script:
    # INITIALIZE THE SCRIPT
    def __init__(self, filename, truss, material, abaqus_version):
        self.filename = filename
        self.truss = truss
        self.material = material

        # OPEN THE SCRIPT FILE
        file = open("".join(self.filename), "w")
        # WRITE INTO FILE
        file.write("# " + "".join(self.filename) + "\n# This file is automatically generated to run in abaqus\n")
        import datetime
        file.write("# This file was generated on " + str(datetime.datetime.now()) +
                   "\n# Max Engensperger, maxe@alumni.ethz.ch\n# Truss name: " + str(truss.name) + "\n# Cell_Size: " +
                   str(truss.cell_size) + "\n# Number of Cells: " + str(truss.number_of_cells) + "\n")
        file.write(
            "from abaqus import *\n"
            "from abaqusConstants import *\n"
            "import __main__\n"
            "import section\n"
            "import regionToolset\n"
            "import displayGroupMdbToolset as dqm\n"
            "import part\n"
            "import material\n"
            "import assembly\n"
            "import step\n"
            "import interaction\n"
            "import load\n"
            "import mesh\n"
            "import optimization\n"
            "import job\n"
            "import sketch\n"
            "import visualization\n"
            "import xyPlot\n"
            "import displayGroupOdbToolset as dgo\n"
            "import connectorBehavior\n"
            "import sys\n"
            "import odb\n"
            "from odbAccess import *\n"
            "import odbAccess\n"
            "from odbMaterial import *\n"
            "from odbSection import *\n"
            "from abaqusConstants import *\n"
            "from odbMaterial import *\n"
            "from odbSection import *\n"
            "import pickle\n"
            "sys.path.insert(9, r'c:/SIMULIA/Abaqus/" + str(abaqus_version) +
            "/code/python2.7/lib/abaqus_plugins/stlExport')\n"
            "import stlExport_kernel\n"
            "Mdb()\n"
            "session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(compassPrivilegedPlane=XYPLANE)\n"
            "session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(compassPrivilegedPlane=XYPLANE)\n"
            "session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)\n"
            "results = dict()\n\n\n\n")
        file.close()

    # GENERATE STL FROM SOLID
    def generate_solid(self, strut_name, cutoff, number_of_cells):
        for cell_types in self.truss.cells:
            generate_cell(self.filename, cell_types, strut_name)
        cell_counter = 0
        for nodes in self.truss.nodes:
            add_cell_to_assembly(self.filename, nodes[3].name, self.filename[1], cell_counter, nodes)
            cell_counter += 1
        if cutoff:
            merge(self.filename, "merged", self.filename[1], cell_counter)
            cut_off_borders(self.filename, self.filename[1], "merged-1", self.truss, number_of_cells)
        else:
            merge(self.filename, self.filename[1], self.filename[1], cell_counter)
        delete_instances(self.filename, self.truss.cells)
        del cell_counter
        get_area(self, self.filename, cutoff)

    def export_stl(self):
        file = open("".join(self.filename), "a")
        file.write(
            "a = mdb.models['Model-1'].rootAssembly\n"
            "session.viewports['Viewport: 1'].setValues(displayedObject=a)\n"
            "session.viewports['Viewport: 1'].assemblyDisplay.setValues(optimizationTasks=OFF, "
            "geometricRestrictions=OFF, stopConditions=OFF)\n"
            "stlExport_kernel.STLExport(moduleName='Assembly', stlFileName='" +
            self.filename[0] + self.filename[1] + ".stl', stlFileType='BINARY')\n")
        file.close()

    # GENERATE FEA FROM WIREFRAME BEAM ELEMENTS
    def evaluate(self, create_steps, submit_job, read_output, number_of_cells):
        applied_force = 1
        generate_wireframe(self.filename, truss=self.truss)
        define_material(self.filename, material_name=self.material['name'], young_modulus=self.material['E_Modulus'],
                        poisson_ratio=self.material['poisson_ratio'])
        assign_material_to_wire(self.filename, self.truss, material_name=self.material['name'])  # "MED610"2.5e9, 0.33
        mesh_part(self.filename, self.truss, mesh_size=self.truss.cell_size / 3)
        list_of_steps = list()

        # CREATE THE DIFFERENT STEPS/LOADING CONDITIONS
        if create_steps:

            # accuracy = 0.2 * self.truss.cell_size
            accuracy = 0
            if self.truss.name == "pyramids":
                accuracy = self.truss.cell_size * 0.3
            # SIGMA_Z
            step_name = "SIGMA_Z"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="z",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, 0, -applied_force / len(vertices)])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_Z")
            list_of_steps.append(step_name)

            # SIGMA_Y

            step_name = "SIGMA_Y"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="y",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, -applied_force / len(vertices), 0])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_Y")
            list_of_steps.append(step_name)

            # SIGMA_X

            step_name = "SIGMA_X"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="x",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[-applied_force / len(vertices), 0, 0])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_X")
            list_of_steps.append(step_name)

            # TAU_XZ

            step_name = "TAU_XZ"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="z",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_Z", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[applied_force / len(vertices), 0, 0])
            vertices = self.truss.find_points_in_plane(axis="x",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_X", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, 0, applied_force / len(vertices)])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_X", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_Z", deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_XZ")
            list_of_steps.append(step_name)

            # TAU_YZ

            step_name = "TAU_YZ"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="z",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_Z", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, applied_force / len(vertices), 0])
            vertices = self.truss.find_points_in_plane(axis="y",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_Y", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, 0, applied_force / len(vertices)])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_Y", deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_YZ")
            list_of_steps.append(step_name)

            # TAU_XY

            step_name = "TAU_XY"
            create_static_step(self.filename, step_name=step_name)
            vertices = self.truss.find_points_in_plane(axis="y",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_Y", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[applied_force / len(vertices), 0, 0])
            vertices = self.truss.find_points_in_plane(axis="x",
                                                       axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
                                                       accuracy=accuracy)
            define_loadings(self.filename, step_name=step_name, affix="_X", vertices=vertices,
                            load_type="ConcentratedForce", load_type_letter="f",
                            force=[0, applied_force / len(vertices), 0])
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Y',
                                       vertices=self.truss.find_points_in_plane(axis="y",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u1=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_X',
                                       vertices=self.truss.find_points_in_plane(axis="x",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u2=0')
            define_boundary_conditions(self.filename, step_name=step_name, affix='_Z',
                                       vertices=self.truss.find_points_in_plane(axis="z",
                                                                                axis_value=-0.5 * self.truss.cell_size,
                                                                                accuracy=accuracy),
                                       direction='u3=0')
            for step in list_of_steps:
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_X", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Y", deactivate_step_name=step)
                deactivate_boundary_conditions(self.filename, step_name=step_name + "_Z", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_Y", deactivate_step_name=step)
                deactivate_loadings(self.filename, step_name=str(step_name) + "_X", deactivate_step_name=step)
            request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_XY")
            list_of_steps.append(step_name)

            # TORSION_Z

            # step_name = "TORSION_Z"
            # create_static_step(self.filename, step_name=step_name)
            # vertices = self.truss.find_points_in_plane(axis="z",
            #                                            axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
            #                                            accuracy=accuracy)
            # define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
            #                 load_type="Moment", load_type_letter="m",  force=[0, 0, applied_force / len(vertices)])
            # define_boundary_conditions(self.filename, step_name=step_name, affix='',
            #                            vertices=self.truss.find_points_in_plane(axis="z",
            #                                                                     axis_value=-0.5*self.truss.cell_size,
            #                                                                     accuracy=accuracy),
            #                            direction='u1=0, u2=0')
            # for step in list_of_steps:
            #     deactivate_boundary_conditions(self.filename, step_name=step_name, deactivate_step_name=step)
            #     deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            # request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_TZ")
            # list_of_steps.append(step_name)

            # TORSION_Y

            # step_name = "TORSION_Y"
            # create_static_step(self.filename, step_name=step_name)
            # vertices = self.truss.find_points_in_plane(axis="y",
            #                                            axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
            #                                            accuracy=accuracy)
            # define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
            #                 load_type="Moment", load_type_letter="m",  force=[0, applied_force / len(vertices), 0])
            # define_boundary_conditions(self.filename, step_name=step_name, affix='',
            #                            vertices=self.truss.find_points_in_plane(axis="y",
            #                                                                     axis_value=-0.5*self.truss.cell_size,
            #                                                                     accuracy=accuracy),
            #                            direction='u2=0, u3=0')
            # for step in list_of_steps:
            #     deactivate_boundary_conditions(self.filename, step_name=step_name, deactivate_step_name=step)
            #     deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            # request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_TY")
            # list_of_steps.append(step_name)

            # TORSION_X

            # step_name = "TORSION_X"
            # create_static_step(self.filename, step_name=step_name)
            # vertices = self.truss.find_points_in_plane(axis="x",
            #                                            axis_value=(number_of_cells - 0.5) * self.truss.cell_size,
            #                                            accuracy=accuracy)
            # define_loadings(self.filename, step_name=step_name, affix="", vertices=vertices,
            #                 load_type="Moment", load_type_letter="m",  force=[applied_force / len(vertices), 0, 0])
            # define_boundary_conditions(self.filename, step_name=step_name, affix='',
            #                            vertices=self.truss.find_points_in_plane(axis="x",
            #                                                                     axis_value=-0.5*self.truss.cell_size,
            #                                                                     accuracy=accuracy),
            #                            direction='u2=0, u3=0')
            #
            # for step in list_of_steps:
            #     deactivate_boundary_conditions(self.filename, step_name=step_name, deactivate_step_name=step)
            #     deactivate_loadings(self.filename, step_name=step_name, deactivate_step_name=step)
            # request_field_output(self.filename, step_name=step_name, output_name="OUTPUT_TX")
            # list_of_steps.append(step_name)
            #

            # HOLD ONE CORNER
            # Set BC to last step. (It gets propagated to all the other steps)
            # c = self.truss.cell_size
            # define_boundary_conditions(self.filename, step_name=step_name, affix='_CORNER',
            #                            vertices=self.truss.find_points_in_space([[-0.6 * c, 0.0 * c],
            #                                                                     [-0.6 * c, -0.4 * c],
            #                                                                     [-0.6 * c, -0.4 * c]]),
            #                            direction='u1=0, u2=0, u3=0, ur1=0, ur2=0, ur3=0')

        if submit_job:
            submit(self.filename, job_name=self.filename[1])
        if read_output:
            read_odb_step(self.filename, 'SIGMA_Z', job_name=self.filename[1])
            read_odb_step(self.filename, 'SIGMA_Y', job_name=self.filename[1])
            read_odb_step(self.filename, 'SIGMA_X', job_name=self.filename[1])
            read_odb_step(self.filename, 'TAU_YZ', job_name=self.filename[1])
            read_odb_step(self.filename, 'TAU_XZ', job_name=self.filename[1])
            read_odb_step(self.filename, 'TAU_XY', job_name=self.filename[1])
            # read_odb_step(self.filename, 'TORSION_Z', job_name=self.filename[1])
            # read_odb_step(self.filename, 'TORSION_Y', job_name=self.filename[1])
            # read_odb_step(self.filename, 'TORSION_X', job_name=self.filename[1])

            # EXTRACTS THE RESULTS AS A DIRECTORY(PYTHON STRUCTURE) IN A BINARY PICKLE FILE

    def pickle_dump(self):

        file = open("".join(self.filename), "a")
        file.write("result_file = open('" + self.filename[0] + self.filename[1] + "_results', 'wb')\n"
                                                                                  "pickle.dump(results, result_file)\n"
                                                                                  "result_file.close()\n")
        file.close()
