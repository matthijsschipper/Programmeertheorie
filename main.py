from code.classes import grid, crossing, net
from code.algorithms import random
from code.visualisation import visualise as vis

if __name__ == "__main__":
    
    # create grid object
    grid = grid.Grid("./data/example/print_0.csv", "./data/example/netlist_1.csv")

    random = random.Random(grid)