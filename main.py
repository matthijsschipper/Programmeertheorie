from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random

### REMOVE LATER
from csv import reader

if __name__ == "__main__":
    
    # create grid object
    grid = grid.Grid("./data/example/print_0.csv", "./data/example/netlist_1.csv")

    # Testing random algorithm
    r = random.Random(grid)

    # coordinates1 = []
    # for height in r.grid.grid:
    #     for column in height:
    #         for element in column:
    #             if element.intersection == True:
    #                 coordinates1.append(element.get_coordinates())
    # print(f"coordinates are {coordinates1}, total = {len(coordinates1)}")

    vis.visualise("./data/example/print_0.csv", "./data/example/our_output.csv")

    # double checking costs calculation
    with open("./data/example/our_output.csv") as file:

        # read through file
        file_reader = reader(file)

        # skip the header
        next(file_reader, None)
        
        # save information in variables
        coordinates = []
        intersections = 0
        bla = []
        for row in file_reader:
            if row[0][0:4] != 'chip':
                path = row[1].strip("[]()").split("),(")
                for element in path:
                    if element in coordinates and element not in bla:
                        intersections += 1
                        bla.append(element)
                    else:
                        coordinates.append(element)
        print(intersections, bla)