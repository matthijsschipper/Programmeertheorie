from csv import reader
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def visualise(printfile, outputfile, folder):
    """
    Takes in the standard-formatted output.csv file
    Outputs a visual representation of that file in the form of a graph
    Saves that file in the data/visualisations/ folder
    """

    with open(printfile) as file:

        # read through file
        file_reader = reader(file)

        # skip the header
        next(file_reader, None)

        # save coordinates and numbers of gates into dictionary
        data = [line.rstrip() for line in file]
        gates = {}
        for row in data:
            information = row.split(",")
            x, y = int(information[1]), int(information[2])

            # save gate coordinates to dictionary
            gates[information[0]] = [x, y, 0]

    with open(outputfile) as file:

        # read through file
        file_reader = reader(file)

        # skip the header
        next(file_reader, None)
        
        # save information in variables
        net_coordinates = []
        for row in file_reader:

            # seperate footer row
            if row[0][0:4] == 'chip':
                gen_info = row[0][0:12]
            
            else:

                # save path as list of x, y and z coordinates
                x_coordinates, y_coordinates, z_coordinates = [], [], []
                path = row[1].strip("[]()").split("),(")

                for element in path:
                    coordinates = element.split(",")
                    x_coordinates.append(int(coordinates[0]))
                    y_coordinates.append(int(coordinates[1]))
                    if len(coordinates) == 3:
                        z_coordinates.append(int(coordinates[2]))
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
    plt.savefig(f"./data/visualisations/{folder}/3d_{gen_info}_{folder}.png")