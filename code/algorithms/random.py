import copy
import random

class Random():
    def  __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()
        self.directions = None
        self.random_routes(self.netlist)
    
    def random_routes(self, netlist):
        for net in netlist:
            self.grid.choose_net(net)

            self.steps = 0
            start_gate, end_gate = net.start, net.end
            self.current_location = start_gate.location
            self.end_location = end_gate.location
            self.dead_end = False

            # Randomly walk over grid until current Crossing object is end_gate

            """
            Wat er fout ging: self.grid.net_is_finished() aangeroepen -> roept current_net.is_finished() aan
            -> returned boolean -> loop luistert niet als boolean is -> response te sloom?
            """
            while not net.finished:

                if self.grid.get_directions() == []:
                    print(f'Dead end from {start_gate} to {end_gate} ({self.steps} steps taken)')
                    self.dead_end = True
                    # self.grid.delete_net(net, -1)
                    break

                self.directions = self.grid.get_directions()
                random_direction = random.choice(self.directions)

                self.grid.add_to_net(random_direction)

                # Count steps
                self.steps += 1

            # Print statement is not applicable to routes with a dead end
            if self.dead_end:
                continue

            print(f'Amount of steps to get from {start_gate} to {end_gate} with random assigning directions is: {self.steps}.')
        
        self.grid.get_output()