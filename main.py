from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import greedy as gr, random

if __name__ == "__main__":
    
    # create grid object
    grid = grid.Grid("./data/example/print_0.csv", "./data/example/netlist_1.csv")

    # Testing random algorithm
    r = random.Random(grid)