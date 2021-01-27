from code.classes import grid, crossing, net
from code.visualisation import visualise as vis
from code.algorithms import random, steered_random, astar, sort, hillclimber as hc

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

    # also save the name of the outputfile
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    # create grid
    grid = grid.Grid(printfile, netlistfile)

    # make user choose an algorithm
    options = {"A": "Random", "B": "Steered Random", "C": "A*"}
    
    print("\nChoose an algorithm")
    for key, value in options.items():
        print(f"{key}: {value}")
    
    while True:
        algorithm = input()
        if algorithm in options:
            break
        else:
            print("Please respond with the letter of your choice")

    # ask user if they want to use an sorting method
    print("Would you like to sort the netlists before running an algorithm?\n Y/N")
    while True:
        sort_answer = input()
        if sort_answer != 'Y' and sort_answer != 'N':
            print("Invalid answer, please respond with either Y or N")
        else:
            break

    if sort_answer == 'Y':
        sort_options = {"A": "Shortest nets first", "B": "Longest nets first", "C": "Outer nets first", "D": "Inner nets first"}

        print("Which sorting method would you like to use?")
        for key, value in sort_options.items():
            print(f"{key}: {value}")

        while True:
            sorting_method = input()
            if sorting_method in sort_options:
                break
            else:
                print("Please respond with the letter of your choice")
        
        # use correct sorting on the grid
        if sorting_method == "A":
            grid = sort.select_shortest_nets(grid)
        elif sorting_method == "B":
            grid = sort.select_longest_nets(grid)
        elif sorting_method == "C":
            grid = sort.select_outer_nets(grid)
        else:
            grid = sort.select_inner_nets(grid)

    # value to keep track if a solution is found with chosen algorithm
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
            if hillclimber_answer != 'Y' and hillclimber_answer != 'N':
                print("Invalid answer, please respond with either Y or N")
            else:
                break
    else:
        hillclimber_answer = False

    # --------------------------- Hill Climber ---------------------------------
    if hillclimber_answer == 'Y':
        hillclimber_object = hc.HillClimber(solution)

        print(f"Original costs: {hillclimber_object.old_costs}\n"
              f"Optimizing original solution....")

        hillclimber_object.optimize_costs()

        print(f"Convergence reached! (found {hillclimber_object.cost_occurence} consecutive times the same costs). Results:\n"
            "-------------------------------------------------------\n"
            f"Optimized netlist {netlist_number} from chip {chip_number}\n"
            f"Optimized costs from {hillclimber_object.old_costs} to {hillclimber_object.costs}\n"
            f"Optimized intersections from {hillclimber_object.old_intersections} to {hillclimber_object.solution.grid.amount_of_intersections}\n"
            f"Optimized length from {hillclimber_object.old_length} to {hillclimber_object.solution.grid.netlist_length()}")


    # --------------------------- Visualisation AFTER Hillclimber has run --------------------------------
    # This visualisation command should only be used if the Hillclimber algorithm has run!
    # Allows visual comparison between solution before and after Hillclimber optimization
    if hillclimber_answer == 'Y':
        vis.visualise(printfile, outputfile, 'optimizations')
