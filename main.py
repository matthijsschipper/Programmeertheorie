from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random

if __name__ == "__main__":
    
    # create grid object
    grid = grid.Grid("./data/chip_1/print_1.csv", "./data/chip_1/netlist_4.csv")

    # Testing random algorithm
    # r = random.Random(grid)

    steered_random_object = steered_random.steered_random_routes(grid)
    steered_random_object.run()

    vis.visualise("./data/chip_1/print_1.csv", "./data/chip_1/our_output.csv")