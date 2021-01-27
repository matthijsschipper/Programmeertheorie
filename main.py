from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, sort, hillclimber as hc
from code.all_stars import get_all_results

from pathlib import Path

if __name__ == "__main__":

    # get print file
    while True:
        chip_number = input("Enter chip to use: ")
        printfile = f"./data/chip_{chip_number}/print_{chip_number}.csv"
        if Path(printfile).is_file():
            break
        else:
            print("Invalid chip")
    
    # get netlist file
    while True:
        netlist_number = input("Enter netlist to use: ")
        netlistfile = f"./data/chip_{chip_number}/netlist_{netlist_number}.csv"
        if Path(netlistfile).is_file():
            break
        else:
            print("Netlist does not exist for given chip.")

    # make user choose an algorithm
    options = {"A": "Random", "B": "Steered Random", "C": "A*"}
    
    print("\nChoose an algorithm")
    for key, value in options.items():
        print(f"{key}: {value}")
    
    algorithm = input()

    # create grid
    grid = grid.Grid(printfile, netlistfile)

    # value to keep track if a solution is found
    solution = False

    # --------------------------- Random ---------------------------------------
    if options[algorithm] == "Random":
        random_object = random.Random(grid)

        if random_object.is_solution():
            print(f"Costs: {random_object.costs}")
            solution = random_object
        else:
            print("No solution found") 

    # --------------------------- Steered Random -------------------------------
    elif options[algorithm] == "Steered Random":
        steered_random_object = steered_random.steered_random_routes(grid)

        tries = 0
        while tries <= 0:
            try:
                tries = int(input("Enter amount of tries: "))
                if tries > 0:
                    break
                else:
                    print("Input needs to be positive")
            except ValueError:
                print("Input needs to be an integer")
    
        steered_random_object.run(tries)
        if steered_random_object.succeeded:
            print(f"Costs: {steered_random_object.costs}")
            solution = steered_random_object
        else:
            print(f"Unfortunately, no solution was found")

    # --------------------------- A* -------------------------------------------
    elif options[algorithm] == "A*":
        astar_object = astar.Astar(grid)
        astar_object.run()
        solution = astar_object
        print(f"Costs: {astar_object.costs}")

    # --------------------------- Visualisation BEFORE Hillclimber has run --------------------------------
    # This visualisation is for all algorithms except the Hillclimber
    vis.visualise(printfile, outputfile, 'original')

    if solution:
        print("Would you like to optimize this result with the hillclimber algorithm?\n Y/N")
        while True:
            hillclimber_answer = input()
            if hillclimber_answer != 'Y' of hillclimber_answer != 'N':
                print("Invalid answer, please respond with either Y or N")
            else:
                break
    else:
        hillclimber_answer = False

    # --------------------------- Hill Climber ---------------------------------
    if hillclimber_answer == 'Y':
        hillclimber_object = hc.HillClimber()

        print(f"""
            Original costs: {hillclimber_object.old_costs}
            Optimizing original solution....
        """)

        hillclimber_object.optimize_costs()

        print(f"""
            Convergence reached! (found {h.cost_occurence} consecutive times the same costs). Results:
            -------------------------------------------------------
            Optimized netlist {netlist_number} from chip {chip_number}
            Optimized costs from {h.old_costs} to {h.costs}
            Optimized intersections from {h.old_intersections} to {h.solution.grid.amount_of_intersections}
            Optimized length from {h.old_length} to {h.solution.grid.netlist_length()}
        """)


    # --------------------------- Visualisation AFTER Hillclimber has run --------------------------------
    # This visualisation command should only be used if the Hillclimber algorithm has run!
    # Allows visual comparison between solution before and after Hillclimber optimization
    if hillclimber_answer == 'Y':
        vis.visualise(printfile, outputfile, 'optimizations')
