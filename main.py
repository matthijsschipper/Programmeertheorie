from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, hillclimber as hc

## TEMP
from matplotlib import pyplot as plt

if __name__ == "__main__":
    
    chip_number = 1
    netlist_number = 4

    printfile = f"./data/chip_{chip_number}/print_{chip_number}.csv"
    netlistfile = f"./data/chip_{chip_number}/netlist_{netlist_number}.csv"
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    # create grid object
    # grid = grid.Grid(printfile, netlistfile)

    # Testing random algorithm
    # r = random.Random(grid)

    # while not r.is_solution():
    #     r = random.Random(grid)

    # while not r.is_solution():
    #     r = random.Random(grid)
    
    # Testing steered random algorithm
    # sr = steered_random.steered_random_routes(grid)

    # Testing A* algorithm
    # a = astar.Astar(grid)

    # vis.visualise(printfile, outputfile, 'original')

    # Optimizing solution on wire length
    # optimized_length = hc.HillClimber(a).optimize_wire_length(chip_number, netlist_number)

    # Optimizing solution on costs
    # optimization = hc.HillClimber(a).optimize_costs(200, chip_number, netlist_number)

    # vis.visualise(printfile, outputfile, 'optimalizations')


    # TEMP for making a graph
    netlist = ['netlist 1', 'netlist 2', 'netlist 3', 'netlist 4', 'netlist 5', 'netlist 6', 'netlist 7', 'netlist 8', 'netlist 9']
    a_star = [22, 43, 72, 3687, 8291, 19047, 15318, 18298, 36631]
    hillclimber = [20, 43, 72, 375, 1127, 1979, 938, 3960, 7083]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(netlist, a_star, label = "A*")
    ax.plot(netlist, hillclimber, label  = "Hillclimber")

    ax.set_ylabel('Costs')
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
    ax.legend()

    fig.savefig(f"./data/visualisations/costs.png")