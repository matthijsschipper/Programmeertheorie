from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, hillclimber as hc

if __name__ == "__main__":
    
    chip_number = 0
    netlist_number = 3

    printfile = f"./data/chip_{chip_number}/print_{chip_number}.csv"
    netlistfile = f"./data/chip_{chip_number}/netlist_{netlist_number}.csv"
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    # create grid object
    grid = grid.Grid(printfile, netlistfile)

    # Testing random algorithm
    # r = random.Random(grid)

    # Testing steered random algorithm
    # steered_random_object = steered_random.steered_random_routes(grid)
    # steered_random = steered_random_object.run(50)

    # Testing A* algorithm
    # a = astar.Astar(grid)

    vis.visualise(printfile, outputfile, 'original')

    # Testing hillclimber algorithm
    # h = hc.HillClimber(steered_random)

    # Optimizing solution on wire length
    # optimized_length = h.optimize_wire_length(chip_number, netlist_number)

    # Optimizing optimized length solution on costs
    # optimization = hc.HillClimber(steered_random).optimize_costs(500, chip_number, netlist_number)

    # vis.visualise(printfile, outputfile, 'optimalizations')
    # vis.visualise(printfile, outputfile)
