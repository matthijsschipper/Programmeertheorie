from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, sort, hillclimber as hc

from code.all_stars import get_all_results

if __name__ == "__main__":
    
    chip_number = 0
    netlist_number = 1

    printfile = f"./data/chip_{chip_number}/print_{chip_number}.csv"
    netlistfile = f"./data/chip_{chip_number}/netlist_{netlist_number}.csv"
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    # create grid object
    grid = grid.Grid(printfile, netlistfile)

    # sort netlists
    grid = sort.select_longest_nets(grid)

    # Testing random algorithm
    # r = random.Random(grid)

    # while not r.is_solution():
    #     r = random.Random(grid)
    
    # Testing steered random algorithm
    # sr = steered_random.steered_random_routes(grid)

    # Testing A* algorithm
    #a = astar.Astar(grid)
    #a.run()
    # get_all_results(f"./data/results_astar/net_test.csv", grid)

    # vis.visualise(printfile, outputfile, 'original')

    # Optimizing solution on wire length
    # optimized_length = hc.HillClimber(a).optimize_wire_length(chip_number, netlist_number)

    # Optimizing solution on costs
    # optimization = hc.HillClimber(a).optimize_costs(200, chip_number, netlist_number)

    # vis.visualise(printfile, outputfile, 'optimalizations')
