import copy
import random
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
        self.route_points = None
        self.net = None
        self.grid = None
        self.costs = random_solution.calculate_costs()

        self.mutate_single_route(self.random_solution)
    
    def mutate_single_route(self, random_solution):
        """
        Pick random route, try to find new route.
        """
        for i in range(5000):
            # Make new copy of solution
            new_solution = copy.deepcopy(random_solution)
            self.grid = new_solution.grid
            self.route_points = self.grid.netlist

            # Pick random net
            self.net = random.choice(self.route_points)

            # Remove net
            self.grid.delete_net(self.net, -1)

            # Make new route
            r = Random(self.grid)

            self.check_solution(r)
    
    def check_solution(self, new_solution):
        """
        If new costs are lower or equal to current costs, overwrite costs and solution
        with new values.
        """
        new_costs = new_solution.calculate_costs()
        old_costs = self.costs

        if new_costs <= old_costs:
            self.random_solution = new_solution
            self.costs = new_costs

            print(f'NEW COSTS: {self.costs}')

# Need to check if routes are necessary to be replotted and when to replot which route
