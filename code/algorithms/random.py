from copy import deepcopy
from random import choice

class Random():
    def  __init__(self, grid):
        """
        Randomly choose one of the available connections at the current crossing, starting
        at self.start_gate, ending at self.end_gate. A chosen direction gets removed from
        the available options, as well as the opposite direction from the new location.
        This algorithm can only solve netlist 1 & 2.
        """
        self.grid = deepcopy(grid)
        self.netlist = self.grid.available_nets()
        self.solved = False
        self.costs = None
        
        self.run(self.netlist)
    
    def run(self, netlist):
        """
        Iterate over every Net object and start plotting a route from the start Crossing object.
        Solution is found if the 'netlist' variable is an empty list, which means that there are
        no available nets anymore. If attempts equals 200, no solution is found.
        """

        # Counts the amount of tries has passed, aborts if failure is almost certainly garanteed
        attempts = 0

        # Try to find a solution
        while netlist != [] and attempts < 200:
            for net in netlist:
                self.grid.choose_net(net)

                # Net finished variables returns true if crossing added to routelist is the destination
                while not net.finished:

                    # Empty directions list means a dead end
                    if self.grid.get_directions() == []:

                        # Delete dead end nets, can be plotted again
                        self.grid.delete_net(net, -1)
                        break

                    # Choose random direction ('N', 'E', 'S', 'W', 'U', 'D')
                    directions = self.grid.get_directions()
                    random_direction = choice(directions)

                    # Call add_to_net function
                    self.grid.add_to_net(random_direction)

                # Update netlist
                netlist = self.grid.available_nets()

                # Update amount of attempts
                attempts += 1

        return self.grid
        
    def solved_check(self):
        """
        Check if any net is not finished. If true, stop. Else, calculate costs.
        """
        for net in self.grid.netlist:
            if not net.finished:
                return False

        self.solved = True
        self.costs = self.grid.calculate_costs()

        # Let grid write output file
        self.grid.get_output((self.costs))
        
        return True
    
    def is_solution(self):
        """
        Check if a solution is found.
        """
        if self.solved:
            return True
        
        return False