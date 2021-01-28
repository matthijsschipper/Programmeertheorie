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
        
        # Checking random algoritm solution validity
        if solution.__class__.__name__ == 'Random' and not solution.is_solution():
            raise Exception('Hillclimber requires a valid solution from the random algorithm')

        self.solution = deepcopy(solution)
        self.old_costs = self.solution.costs
        self.old_intersections = self.solution.grid.amount_of_intersections
        self.old_length = self.solution.grid.netlist_length()
        self.cost_occurence = 0
        self.costs = self.solution.costs
        self.chip_nr = self.solution.grid.chip_id
        self.netlist_nr = self.solution.grid.netlist_id

    def optimize_costs(self):
        """
        Optimize a given solution on base of the total costs. Remove a randomly chosen net and let 
        the A* algorithm plot it again. If the costs of the new solution are lower than or equal to
        the old costs, remember the new solution. Else, continue with the loop.
        """

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
            new_astar_solution.run()

            # New solution costs check
            self.check_solution(new_astar_solution)
        
        # Write final solution to output file
        self.solution.grid.get_output(self.costs)

        return self.solution
    
    def check_solution(self, new_solution):
        """
        Check if new found costs are lower than or equal to old costs. Overwrite values
        if true. Solutions with equal costs overwrite the current solution as well, because
        this creates a new solution which might prevent too early convergence.
        """

        # Retrieving costs of new found solution
        new_costs = new_solution.grid.calculate_costs()

        # Counting cost occurence
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
                print(f"Found costs of {self.costs} for {self.cost_occurence}/1500 times now")
        
            return True
        
        return False