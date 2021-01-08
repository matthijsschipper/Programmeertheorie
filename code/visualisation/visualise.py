import csv
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualise(infile):
    with open(infile) as file:

        # read through file
        reader = csv.reader(file)

        # skip the header
        next(reader, None)
        
        # save information in variables
        net_coordinates = []
        gates = {}
        for row in reader:

            # seperate footer row
            if row[0][0:4] == 'chip':
                gen_info = row[0][0:12]
            
            else:

                # save all gate locations
                if str(row[0][1]) not in gates:
                    gates[row[0][1]] = (int(row[1][2]), int(row[1][4]), 0)
                if str(row[0][3]) not in gates:
                    gates[row[0][3]] = (int(row[1][-7]), int(row[1][-5]), 0)

                # save path as list of x, y and z coordinates
                x_coordinates, y_coordinates, z_coordinates = [], [], []
                path = row[1].strip("[]()").split("),(")

                for element in path:
                    x_coordinates.append(int(element[0]))
                    y_coordinates.append(int(element[2]))
                    if len(element) == 5:
                        z_coordinates.append(int(element[4]))
                    else:
                        z_coordinates.append(0)

                # add coordinates to list
                net_coordinates.append((x_coordinates, y_coordinates, z_coordinates))

    # create plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # plotting all nets
    for i in range(len(net_coordinates)):
        ax.plot(net_coordinates[i][0], net_coordinates[i][1], net_coordinates[i][2], label=f"net_{i + 1}")

    # plotting all gates
    for key in gates:
        ax.scatter(gates[key][0], gates[key][1], gates[key][2], c="red")
        ax.text(gates[key][0], gates[key][1], gates[key][2], f'{key}')

    # set axes
    ax.set_xlabel('x-as')
    ax.set_ylabel('y-as')
    ax.set_zlabel('z-as')
    ax.invert_xaxis()

    # save plot
    plt.savefig(f"./data/visualisations/3d_{gen_info}.png")