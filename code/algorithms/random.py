import copy
import random

class Random():
    """
    Randomly choose one of the available connections at the current crossing, starting
    at self.start_gate, ending at self.end_gate. A chosen direction gets removed from
    the available options, as well as the opposite direction from the new location.
    """
    def  __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()
        self.directions = None
        self.start_gate = None
        self.end_gate = None
        self.total_wires_length = 0
        self.total_costs = 0
        
        self.random_routes(self.netlist)
    
    def random_routes(self, netlist):
        """
        Iterate over every Net object and start plotting a route from the start Crossing object.
        """
        for net in netlist:
            self.grid.choose_net(net)

            self.steps = 0
            self.start_gate = net.start
            self.end_gate = net.end
            self.dead_end = False

            """
            Wat er fout ging: self.grid.net_is_finished() aangeroepen -> roept current_net.is_finished() aan
            -> returned boolean -> loop luistert niet als boolean is -> response te sloom?
            """
            # Net finished variables return True if crossing added to routelist is the destination
            while not net.finished:

                # Empty directions list means a dead end
                if self.grid.get_directions() == []:
                    print(f'Dead end from {start_gate} to {end_gate} ({self.steps} steps taken)')
                    self.dead_end = True
                    
                    # Delete dead end nets
                    self.grid.delete_net(net, -1)
                    break

                # Choose random direction ('N', 'E', 'S', 'W', 'U', 'D')
                self.directions = self.grid.get_directions()
                random_direction = random.choice(self.directions)

                # Call add_to_net function
                self.grid.add_to_net(random_direction)

                # Count steps
                self.steps += 1

            # Print statement is not applicable to routes with a dead end
            if self.dead_end:
                continue

            print(f'Amount of steps to get from {start_gate} to {end_gate} with random assigning directions is: {self.steps}.')
        
        self.check_netlist_implementation()
        
    def check_netlist_implementation(self):
        """
        Check if any net is not finished. If true, stop. Else, move on to cost calculation.
        """
        for net in self.grid.netlist:
            if not net.finished:
                return False
              
        self.calculate_costs()
        return True

    
    def calculate_costs(self):
        """
        Costs are calculated by multiplying the total length of wires with 300 * the amount of intersections.
        An intersection is where lines use the same crossing object, but have a different direction.
        """

        for net in self.grid.netlist:
            self.total_wires_length += (net.get_length() - 1)
        
        self.total_costs += self.total_wires_length
        self.total_costs += (self.grid.amount_of_intersections * 300)

        self.grid.get_output(self.total_costs)

        print(f'Total amount of costs for this ciruit: {self.total_costs}.')

        return True