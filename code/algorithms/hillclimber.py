import copy
import random
from code.classes import net
from code.algorithms.random import Random
from code.algorithms import astar
import operator

class HillClimber():
    def __init__(self, solution):
        """
        Hillclimber optimializes valid solutions by removing a randomly chosen net and calling the
        A* algorithm to plot it again for the amount of provided iterations.
        """
        self.solution = copy.deepcopy(solution)
        self.old_costs = self.solution.costs
        self.old_intersections = self.solution.grid.amount_of_intersections
        self.old_length = self.solution.grid.netlist_length()
        self.convergence_count = 0

    def optimize_costs(self, chip_number, netlist_number):
        """
        Otimize a given solution on base of the total costs. Remove a randomly chosen net and let 
        the A* algorithm plot it again. If the costs of the new solution are lower than or equal to
        the old costs, remember the new solution. Else, continue with the loop.
        """
        self.costs = self.solution.costs
        # self.iterations = iterations

        # Print original costs before optimalization
        print(f'Original costs: {self.costs}')
        print('Optimizing original solution....')

        while self.convergence_count != 1500:

            # Print status of the loop on every 100th iteration
            # if i % 100 == 0:
            #     print(f'On iteration {i}/{iterations}')
            
            # Make new copy of solution
            new_solution = copy.deepcopy(self.solution)
            new_grid = new_solution.grid
            route_points = new_grid.netlist

            # Choose random net from the copy and remove it 
            net = random.choice(route_points)
            new_grid.delete_net(net, -1)

            # Let A* algorithm plot new route for removed net
            new_astar_solution = astar.Astar(new_grid)

            # Costs check
            self.check_solution(new_astar_solution)
        
        self.solution.grid.get_output(self.costs)
        # Cost optimization results for {self.iterations} tries:

        print(f'''
        Convergence of {self.convergence_count} reached!
        -------------------------------------------------------
        Optimized chip {chip_number} and netlist {netlist_number}
        Optimized costs from {self.old_costs} to {self.costs}
        Optimized intersections from {self.old_intersections} to {self.solution.grid.amount_of_intersections}
        Optimized length from {self.old_length} to {self.solution.grid.netlist_length()}
        Failed nets: {self.solution.failed_nets}
        ''')

        return self.solution
    
    def check_solution(self, new_solution):
        """
        Check if new found costs are lower than or equal to old costs. Overwrite values
        if true. Solutions with equal costs overwrite the current solution as well, because
        this creates a new solution which might prevent too early convergence.
        """
        # These costs are focussed on calculating costs of A* solution and is a temporary fix
        # Might be useful to write a function for the grid class or the algorithm to calculate the costs
        new_costs = new_solution.grid.netlist_length() + (300 * new_solution.grid.amount_of_intersections)
        old_costs = self.costs

        # Checking for convergence
        if old_costs == new_costs:
            self.convergence_count += 1
        else:
            self.convergence_count = 0

        # No new route found
        if len(new_solution.grid.available_nets()) > 0:
            return

        # If true, overwrite current solution with new solution
        if new_costs <= old_costs:
            self.solution = new_solution
            self.costs = new_costs

            print(f'Found new costs: {self.costs}')






# 
# OLD FUNCTION, NOT RELEVANT NOW
# 


# def optimize_wire_length(self, chip_number, netlist_number):
#     """
#     Optimize given solution on base of wire length for every net. NOT FINISHED + BUGGY
#     """
#     self.index = 0
#     netlist = self.random_solution.grid.netlist

#     # for net in sorted(self.random_solution.grid.netlist, key=operator.methodcaller('get_length')):
#     for net in netlist:
#         new_solution = copy.deepcopy(self.random_solution)
#         new_grid = new_solution.grid

#         self.index = self.random_solution.grid.netlist.index(net)

#         net = new_grid.netlist[self.index]

#         print(f'Optimizing net {net}....')

#         self.length = net.get_length()
#         self.old_total_length.append(self.length)

#         print(f'Original length: {self.length}')

#         distance = net.get_route_to_end()
#         distance = abs(distance[0]) + abs(distance[1]) + 1

#         # Remove net
#         new_grid.delete_net(net, -1)

#         steps = 0

#         while self.length >= distance and steps < 200:

#             new_route = Random(new_grid)

#             self.check_length(new_route)
            
#             steps += 1
        
#         print(f'Found new length of {self.random_solution.grid.netlist[self.index].get_length()}')
#         print()

#         self.new_total_length.append(self.length)
        
#         self.index += 1

#     costs = self.random_solution.costs
#     self.random_solution.grid.get_output(costs)

#     print(f'''
#     Wire length optimization results:
#     -------------------------------------------------------
#     Optimized chip {chip_number} and netlist {netlist_number}
#     Optimized costs from {self.old_costs} to {costs}
#     Optimized intersections from {self.old_intersections} to {self.random_solution.grid.amount_of_intersections}
#     Optimized total length from {sum(self.old_total_length)} to {sum(self.new_total_length)}
#     ''')

#     return self.random_solution

















# def check_length(self, new_solution):
#     """
#     If new found length is equal to or shorter than old length, update the current
#     solution with the new found solution.
#     """
#     net = new_solution.grid.netlist[self.index]
#     new_length = net.get_length()
#     old_length = self.length
#     new_costs = new_solution.calculate_costs()
#     current_costs = self.random_solution.costs

#     if new_length == 0:
#         return

#     if new_length < old_length and new_costs < current_costs:
#         # Update initializer copy with better or equal copy
#         self.random_solution = new_solution
#         self.length = new_length