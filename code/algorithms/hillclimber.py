import copy
import random
from code.classes import net
from code.algorithms.random import Random
import operator

class HillClimber():
    """
    Receive a random solution, change random routes at one point at the time and check for
    improval.
    """
    def __init__(self, random_solution):
        # Check for validity
        # if not random_solution.is_solution():
        #     raise Exception('HillClimber requires a valid solution.')

        self.random_solution = copy.deepcopy(random_solution)
        self.old_costs = random_solution.costs
        self.old_intersections = random_solution.grid.amount_of_intersections
        self.old_total_length = []
        self.new_total_length = []

    def optimize_wire_length(self, chip_number, netlist_number):
        """
        Optimize given solution on base of wire length for every net.
        """
        self.index = 0

        for net in self.random_solution.grid.netlist[:1]:
            new_solution = copy.deepcopy(self.random_solution)
            new_grid = new_solution.grid

            net = new_grid.netlist[self.index]

            print(f'Optimizing net {net}....')

            self.length = net.get_length()
            self.old_total_length.append(self.length)

            print(f'Original length: {self.length}')

            distance = net.get_route_to_end()
            distance = abs(distance[0]) + abs(distance[1]) + 1

            # Remove net
            new_grid.delete_net(net, -1)

            print(new_grid.available_nets())
            continue

            steps = 0

            while self.length >= distance and steps < 200:

                new_route = Random(new_grid)

                self.check_length(new_route)
                
                steps += 1
            
            print(f'Found new length of {self.random_solution.grid.netlist[self.index].get_length()}')
            print()

            self.new_total_length.append(self.length)
            
            self.index += 1

        costs = self.random_solution.costs
        self.random_solution.grid.get_output(costs)

        print(f'''
        Wire length optimization results:
        -------------------------------------------------------
        Optimized chip {chip_number} and netlist {netlist_number}
        Optimized costs from {self.old_costs} to {costs}
        Optimized intersections from {self.old_intersections} to {self.random_solution.grid.amount_of_intersections}
        Optimized total length from {sum(self.old_total_length)} to {sum(self.new_total_length)}
        ''')

        return self.random_solution
    
    def optimize_costs(self, iterations, chip_number, netlist_number):
        """
        Otimize a given solution on base of the total costs.
        """
        self.costs = self.random_solution.costs
        self.iterations = iterations
        for i in range(iterations):
            if i % 100 == 0:
                print(f'On iteration {i}/{iterations}')
            # Make new copy of solution
            new_solution = copy.deepcopy(self.random_solution)
            new_grid = new_solution.grid
            route_points = new_grid.netlist

            if i == 0:
                print(f'Original costs: {self.costs}')
                print('Optimizing original solution....')

            net = random.choice(route_points)

            # Remove net
            new_grid.delete_net(net, -1)

            # Make new route
            r = Random(new_grid)

            self.check_solution(r)
        
        self.random_solution.grid.get_output(self.costs)

        print(f'''
        Cost optimization results for {self.iterations} tries:
        -------------------------------------------------------
        Optimized chip {chip_number} and netlist {netlist_number}
        Optimized costs from {self.old_costs} to {self.costs}
        Optimized intersections from {self.old_intersections} to {self.random_solution.grid.amount_of_intersections}
        ''')

        return self.random_solution
    
    def short_long(self, chip_number, netlist_number):
        self.costs = self.random_solution.costs
        self.index = 0
        
        nets = self.random_solution.grid.netlist
        new = sorted(nets, key=operator.methodcaller('get_length'))

        for net in new:
            new_solution = copy.deepcopy(self.random_solution)
            new_grid = new_solution.grid

            self.index = self.random_solution.grid.netlist.index(net)

            net = new_grid.netlist[self.index]

            print(f'Optimizing net {net}....')

            self.length = net.get_length()
            self.old_total_length.append(self.length)

            print(f'Original length: {self.length}')

            distance = net.get_route_to_end()
            distance = abs(distance[0]) + abs(distance[1]) + 1

            # Remove net
            new_grid.delete_net(net, -1)

            print(new_grid.available_nets())
            continue

            steps = 0

            while self.length >= distance and steps < 200:

                new_route = Random(new_grid)

                self.check_length(new_route)
                
                steps += 1
            
            print(f'Found new length of {self.random_solution.grid.netlist[self.index].get_length()}')
            print()

            self.new_total_length.append(self.length)
            
            self.index += 1

        costs = self.random_solution.costs
        self.random_solution.grid.get_output(costs)

        print(f'''
        Wire length optimization results:
        -------------------------------------------------------
        Optimized chip {chip_number} and netlist {netlist_number}
        Optimized costs from {self.old_costs} to {costs}
        Optimized intersections from {self.old_intersections} to {self.random_solution.grid.amount_of_intersections}
        Optimized total length from {sum(self.old_total_length)} to {sum(self.new_total_length)}
        ''')

    
    def check_solution(self, new_solution):
        """
        Check if new found costs are lower than or equal to old costs. Overwrite values
        if true.
        """
        new_costs = new_solution.calculate_costs()
        old_costs = self.costs

        if len(new_solution.grid.available_nets()) > 0:
            return

        if new_costs <= old_costs:
            # Update initializer copy with better or equal copy
            self.random_solution = new_solution
            self.costs = new_costs

            print(f'Found new costs: {self.costs}')
    
    def check_length(self, new_solution):
        """
        If new found length is equal to or shorter than old length, update the current
        solution with the new found solution.
        """
        net = new_solution.grid.netlist[self.index]
        new_length = net.get_length()
        old_length = self.length
        new_costs = new_solution.calculate_costs()
        current_costs = self.random_solution.costs

        if new_length == 0:
            return

        if new_length < old_length and new_costs < current_costs:
            # Update initializer copy with better or equal copy
            self.random_solution = new_solution
            self.length = new_length