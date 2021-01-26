from copy import deepcopy
from random import choice
from code.algorithms import astar

class HillClimber():
    def __init__(self, solution):
        """
        Hillclimber optimizes valid solutions by removing a randomly chosen net and calling the
        A* algorithm to plot it again. This process is repeated until the same amount of costs
        is found for 1500 times.
        """
        self.solution = deepcopy(solution)
        self.old_costs = self.solution.costs
        self.old_intersections = self.solution.grid.amount_of_intersections
        self.old_length = self.solution.grid.netlist_length()
        self.cost_occurence = 0
        self.costs = self.solution.costs

    def optimize_costs(self, chip_number, netlist_number):
        """
        Optimize a given solution on base of the total costs. Remove a randomly chosen net and let 
        the A* algorithm plot it again. If the costs of the new solution are lower than or equal to
        the old costs, remember the new solution. Else, continue with the loop.
        """

        # Print original costs before optimization
        print(f"""
        Original costs: {self.old_costs}
        Optimizing original solution....
        """)

        # Loop keeps running until the same amount of costs is found 1500 times consecutively
        while self.cost_occurence != 1500:

            # Make new copy of solution
            new_solution = deepcopy(self.solution)
            new_grid = new_solution.grid
            netlist = new_grid.netlist

            # Choose random net from the copy and remove it 
            net = choice(netlist)
            new_grid.delete_net(net, -1)

            # Let A* algorithm plot new route for removed net
            new_astar_solution = astar.Astar(new_grid)

            # New solution costs check
            self.check_solution(new_astar_solution)
        
        # Write final solution to output file
        self.solution.grid.get_output(self.costs)

        print(f'''
        Convergence of {self.convergence_count} reached! The results:
        -------------------------------------------------------
        Optimized netlist {netlist_number} from chip {chip_number}
        Optimized costs from {self.old_costs} to {self.costs}
        Optimized intersections from {self.old_intersections} to {self.solution.grid.amount_of_intersections}
        Optimized length from {self.old_length} to {self.solution.grid.netlist_length()}
        ''')

        return self.solution
    
    def check_solution(self, new_solution):
        """
        Check if new found costs are lower than or equal to old costs. Overwrite values
        if true. Solutions with equal costs overwrite the current solution as well, because
        this creates a new solution which might prevent too early convergence.
        """
        # new_costs = new_solution.grid.netlist_length() + (300 * new_solution.grid.amount_of_intersections)
        
        # Retrieving costs of new found solution
        new_costs = new_solution.grid.calculate_costs()

        # Checking for convergence
        if self.costs == new_costs:
            self.cost_occurence += 1
        else:
            self.cost_occurence = 0

        # No new route found
        if len(new_solution.grid.available_nets()) > 0:
            return False

        # If true, overwrite current solution and costs with new solution and costs
        if new_costs <= self.costs:
            self.solution = new_solution
            self.costs = new_costs

            if self.cost_occurence == 0:
                print(f"Found new costs of {self.costs}")
            elif self.cost_occurence % 50 == 0:
                print(f"Found costs of {self.costs} for {self.cost_occurence} times now")
        
             return True
        
        return False