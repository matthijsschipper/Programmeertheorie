from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random

if __name__ == "__main__":
    
    # create grid object
    grid = grid.Grid("./data/example/print_0.csv", "./data/example/netlist_1.csv")

    # Testing random algorithm
    r = random.Random(grid)

    # testing deleting routes
    # for height in r.grid.grid:
    #     for column in height:
    #         for some_crossing in column:
    #             directions = some_crossing.get_possible_directions()
    #             amount_of_directions = len(directions)
                
    #             if amount_of_directions != 5:
    #                 location = some_crossing.get_coordinates()
    #                 if location[0] != 0 and location[0] != 7 and location[1] != 0 and location[1] != 6:
    #                     print(location, amount_of_directions)

    vis.visualise("./data/example/print_0.csv", "./data/example/our_output.csv")