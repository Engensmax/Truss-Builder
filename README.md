# Truss-Builder
Generate small truss structures for bone tissue engineering with the software ABAQUS and then calculate the compliance matrix of the metamaterial. The goal is to automate an optimization for physical target values such as Young's Modulus.
The code is written in python.
This code is in a early state.

First step: Fill out the wanted inputs and options that are given in truss_builder.py

Second step: Run truss_builder.py

There are three possible methods to run: (See # METHOD in # OPTIONS)

'single_run': Starts a single evaluation depending on the given inputs and options

'loop': Loops over up to two different values for an input variable. See the # LOOP section in the # METHOD section of # OPTIONS.

'optimization': Starts a deterministic optimization with the input values as starting point. See # OPTIMIZATION in # METHOD for the optimization options. The optimization uses the scipy optimization toolbox.

To add new topologies, define a new cell in library_cell.py and then define the new truss in library_truss.py. After that add the amount of variables and ratios in the dictionaries in truss_builder.py at the top of the User Input section.
