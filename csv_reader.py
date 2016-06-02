import csv

def csv_read_mems(path, multiplicator):
    connections = [[]]
    connections.pop(0)
    i = 0
    # C:\\Users / Maxe - PC2 / Desktop / code_and_csv / mems.csv
    with open(path, newline='') as csvfile:
        conn_reader = csv.reader(csvfile, delimiter=',')
        for row in conn_reader:
            i += 1
            # row2 = [map(int, x) for x in row[2]]
            # if(i>2): connections.append([row2, row[3], row[13]])
            # row2 = [map(int, x) for x in row[2]]
            # if(i>2): connections.append([list(map(int, row[2])), row[3], row[13]])
            if i > 2:
                connections.append([int(row[2]) - 1, int(row[3]) - 1, float(row[13]) * 1e-6])
            # if(i>2): connections.append([list(map(int, row[2])), row[3], row[13]])
            # print(row[0]+"\t"+row[2]+"\t"+row[3])
    return connections


def csv_read_nodes(path, multiplicator):
    coordinates = [[]]
    coordinates.pop(0)
    i = 0
    # "C:\\Users/Maxe-PC2/Desktop/code_and_csv/nodes.csv"
    with open(path, newline='') as csvfile:
        coord_reader = csv.reader(csvfile, delimiter=',')
        for row in coord_reader:
            i += 1
            if i > 2:
                coordinates.append([float(row[3]) * 1e-3, float(row[4]) * 1e-3, float(row[5]) * 1e-3])

    return coordinates


def csv_read_list(path):

    values = [[]]
    values.pop(0)
    i = 0
    # "C:\\Users/Maxe-PC2/Desktop/code_and_csv/nodes.csv"
    with open(path, newline='') as csvfile:
        coord_reader = csv.reader(csvfile, delimiter=',')
        for row in coord_reader:
            value_row = list()
            for value in row:
                value_row.append(float(value))
            values.append(value_row)

    return values
