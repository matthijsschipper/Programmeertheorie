from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, hillclimber as hc

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
    netlist = ['chip 0 netlist 1', 'chip 0 netlist 2', 'chip 0 netlist 3', 'chip 1 netlist 4', 'chip 1 netlist 5', 'chip 1 netlist 6', 'chip 2 netlist 7', 'chip 2 netlist 8', 'chip 2 netlist 9']
    a_star = [22, 43, 72, 3687, 8291, 19047, 15318, 18298, 36631]
    hillclimber = [20, 43, 72, 375, 1127, 1979, 938, 3960, 7083]

    plt.plot(netlist, a_star)
    plt.plot(netlist, hillclimber)

    plt.savefig(f"./data/visualisations/costs.png")