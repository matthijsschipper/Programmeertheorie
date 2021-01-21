from copy import deepcopy
from random import choice

class Random():
    """
    Randomly choose one of the available connections at the current crossing, starting
    at self.start_gate, ending at self.end_gate. A chosen direction gets removed from
    the available options, as well as the opposite direction from the new location.
    """
    def  __init__(self, grid):
        self.grid = deepcopy(grid)
        self.netlist = self.grid.available_nets()
        self.directions = None
        self.start_gate = None
        self.end_gate = None
        self.solved = False
        self.costs = None
        
        self.random_routes(self.netlist)
    
    def random_routes(self, netlist):
        """
        Iterate over every Net object and start plotting a route from the start Crossing object.
        """

        # counts the amount of tries has passed, aborts if failure is almost certainly garanteed
        attemps = 0

        while netlist != [] and attemps < 200:
            for net in netlist:
                self.grid.choose_net(net)

                self.steps = 0
                self.start_gate = net.start
                self.end_gate = net.end
                self.dead_end = False

                # Net finished variables return True if crossing added to routelist is the destination
                while not net.finished:

                    # Empty directions list means a dead end
                    if self.grid.get_directions() == []:

                        # print(f'Dead end from {self.start_gate} to {self.end_gate} ({self.steps} steps taken)')
                        self.dead_end = True

                        # Delete dead end nets
                        self.grid.delete_net(net, -1)
                        break

                    # Choose random direction ('N', 'E', 'S', 'W', 'U', 'D')
                    self.directions = self.grid.get_directions()
                    random_direction = choice(self.directions)

                    # Call add_to_net function
                    self.grid.add_to_net(random_direction)

                    # Count steps
                    self.steps += 1

                netlist = self.grid.available_nets()

                attemps += 1

                # Print statement is not applicable to routes with a dead end
                if self.dead_end:
                    continue

                # print(f'Amount of steps to get from {self.start_gate} to {self.end_gate} with random assigning directions is: {self.steps}.')
                
        if not self.check_netlist_implementation():
            print("Netlist implementation failed.")
        
        return netlist
        
    def check_netlist_implementation(self):
        """
        Check if any net is not finished. If true, stop. Else, move on to cost calculation.
        """

        for net in self.grid.netlist:
            if not net.finished:
                return False
              
        self.calculate_costs()
        self.solved = True
        return True
 
    def calculate_costs(self):
        """
        Costs are calculated by multiplying the total length of wires with 300 * the amount of intersections.
        An intersection is where lines use the same crossing object, but have a different direction.
        """

        total_wires_length = 0
        for net in self.grid.netlist:
            total_wires_length += net.get_length()
        
        self.costs = total_wires_length
        self.costs += (self.grid.amount_of_intersections * 300)

        self.grid.get_output(self.costs)

        # print(f'Total amount of costs for this ciruit: {total_costs}.')

        return self.costs
    
    def is_solution(self):
        """
        Check if a solution exists. Is useful if random algorithm is used in other algoritms.
        """
        if self.solved:
            return True
        
        return False
