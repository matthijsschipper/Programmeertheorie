from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar

if __name__ == "__main__":
    
    chip_number = 1
    netlist_number = 4

    printfile = f"./data/chip_{chip_number}/print_{chip_number}.csv"
    netlistfile = f"./data/chip_{chip_number}/netlist_{netlist_number}.csv"
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    # create grid object
    grid = grid.Grid(printfile, netlistfile)

    # Testing random algorithm
    # r = random.Random(grid)

    # Testing steered random algorithm
    steered_random_object = steered_random.steered_random_routes(grid)
    grid = steered_random_object.run(50)

    # Testing A* algorithm
    # a = astar.Astar(grid)

    # vis.visualise(printfile, outputfile)