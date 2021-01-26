from csv import writer
from code.algorithms import astar

def get_all_results(output_file, grid):

    with open(output_file, 'w') as file:
        output = writer(file)
        output.writerow(["Method", "Length", "Intersections", "Costs", "Height", "Failed"])

        methods = ['default', 'reverse', 'short', 'long', 'outside', 'inside']

        for method in methods:
            a = astar.Astar(grid)
            a.run(method)
            #output.writerow([f"{method}, {a.length}, {a.intersections}, {a.costs}, {a.height}, {a.failed_nets}"])
            output.writerow([method, a.length, a.intersections, a.costs, a.height, a.failed])

