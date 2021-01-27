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

    #VOORSTEL VOOR MAIN.PY

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

    # VOLGENSMIJ DOEN WE HIER NU NIETS MEE!! Voorstel: of verwijderen of meegeven aan grid
    outputfile = f"./data/outputfiles/chip_{chip_number}_net_{netlist_number}.csv"

    options = {"A": "Random", "B": "Steered Random", "C": "A*", "D": "Hillclimber"}
    
    print()
    print("Choose an algorithm")
    for key, value in options.items():
        print(f"{key}: {value}")
    
    algorithm = input()

    # create grid
    grid = grid.Grid(printfile, netlistfile)

    # --------------------------- Random ---------------------------------------
    r = random.Random(grid)

    if r.solved:
        print(f"Costs: {r.costs}")
    else:
        print("No solution found") #IN RANDOM ZELF STAAT OOK PRINTSTATEMENT MAAR HET LIJKT MIJ LOGISCHER OM NIKS IN DE CLASSES UIT TE PRINTEN

    # --------------------------- Steered Random -------------------------------
    sr = steered_random.steered_random_routes(grid)

    while True:
        try:
            tries = int(input("Enter amount of tries: "))
            if tries > 0:
                break
            else:
                print("Input needs to be positive")
        except ValueError:
            print("Input needs to be an integer")
    
    sr.run(tries)
    print(f"Costs: {sr.costs}") #MISS EEN MANIER TOEVOEGEN OM TE CHECKEN VOOR GELDIGE OPLOSSING?

    # --------------------------- A* -------------------------------------------
    a = astar.Astar(grid)
    a.run()
    print(f"Costs: {a.costs}")

    # --------------------------- Hill Climber ---------------------------------
    h = hc.HillClimber(a)
    h..optimize_wire_length(chip_number, netlist_number)s


    # --------------------------- Visualisation --------------------------------
    #vis.visualise(printfile, outputfile) #WELKE FOLDER???
