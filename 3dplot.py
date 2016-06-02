from mpl_toolkits.mplot3d import Axes3D
import csv_reader
from matplotlib import pyplot

folder = 'C://Users/maxe/Dropbox/Master_Thesis/Calculations/'

strut_thickness = csv_reader.csv_read_list(folder + 'strut_thickness.csv')
cell_size = csv_reader.csv_read_list(folder + 'cell_size.csv')
displacement = csv_reader.csv_read_list(folder + 'displacement.csv')
e_meta = csv_reader.csv_read_list(folder + 'E_Meta.csv')

figure = pyplot.figure()
ax = figure.gca(projection='3d')
ax.plot_wireframe(strut_thickness[0], cell_size[0], displacement)


pyplot.show()
