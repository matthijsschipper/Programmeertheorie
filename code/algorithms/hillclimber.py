import copy
import random
from code.classes import net
from code.algorithms.random import Random

class HillClimber():
    """
    Receive a random solution, change random routes at one point at the time and check for
    improval.
    """
    def __init__(self, random_solution):
        # Check for validity
        if not random_solution.is_solution():
            raise Exception('HillClimber requires a valid solution.')

        self.random_solution = copy.deepcopy(random_solution)

        self.mutate_single_route()
    
    def mutate_single_route(self):
        """
        Pick random route, try to find new route.
        """

        '''
        FOR OPTIMIZING ON BASE OF WIRE LENGTH
        '''
        
        # self.index = 0

        # for net in self.random_solution.grid.netlist:
        #     new_solution = copy.deepcopy(self.random_solution)
        #     new_grid = new_solution.grid

        #     net = new_grid.netlist[self.index]

        #     print(f'Optimizing net {net}....')

        #     self.length = net.get_length()

        #     print(f'Original length: {self.length}')

        #     distance = net.get_route_to_end()
        #     distance = abs(distance[0]) + abs(distance[1]) + 1

        #     # Remove net
        #     new_grid.delete_net(net, -1)

        #     steps = 0

        #     while self.length >= distance and steps < 200:

        #         r = Random(new_grid)

        #         self.check_length(r)
                
        #         steps += 1
            
        #     print(f'Found new length of {self.random_solution.grid.netlist[self.index].get_length()}')
        #     print()
            
        #     self.index += 1

        # costs = self.random_solution.calculate_costs()
        # self.random_solution.grid.get_output(costs)

        '''
        FOR OPTIMIZING ON BASE OF COSTS
        '''
            
        for i in range(1000):
            # Make new copy of solution
            new_solution = copy.deepcopy(self.random_solution)
            new_grid = new_solution.grid
            route_points = new_grid.netlist
            self.costs = new_solution.calculate_costs()

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
    
    def check_solution(self, new_solution):
        """
        Check if new found costs are lower than or equal to old costs. Overwrite values
        if true.
        """
        new_costs = new_solution.calculate_costs()
        old_costs = self.costs

        if new_costs <= old_costs:
            # Update initializer copy with better or equal copy
            self.random_solution = new_solution
            self.costs = new_costs

            print(f'Found new costs: {self.costs}')
    
    def check_length(self, new_solution):
        net = new_solution.grid.netlist[self.index]
        new_length = net.get_length()
        old_length = self.length

        if new_length == 0:
            return

        if new_length < old_length:
            # Update initializer copy with better or equal copy
            self.random_solution = new_solution
            self.length = new_length