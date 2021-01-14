from copy import deepcopy
from random import choice

class steered_random_routes:
    """
    The steered_random_routes class is an algorithm that tries to improve upon just randomly laying the nets
    Takes a grid object as input
    First selects which nets should be layed down first
    For each net, tries to walk towards to end point
    """

    def __init__(self, grid):
        self.grid = deepcopy(grid)
        self.total_wires_length = 0

    def select_shortest_nets(self, netlist):
        """
        Takes the netlist of a grid as input
        Determines which nets should be the shortest to lay down
        Returns an ordered list where the first nets are the shortest and they grow in size
        """

        nets_with_length = []
        for net in netlist:
            amount_of_steps = sum([abs(i) for i in net.get_route_to_end()])
            nets_with_length.append((amount_of_steps, net))
        nets_with_length.sort(key = lambda x : x[0])
        
        return [i[1] for i in nets_with_length]

    def run(self):
        """
        Algorithm that takes in a grid object as input
        First selects which nets should be layed down first
        For each net, tries to walk towards to end point
        Returns a grid object with solutions if succesful, else None
        """

        # order the nets by expected size
        ordered_nets = self.select_shortest_nets(self.grid.netlist)

        # solve puzzle net by net
        for net in ordered_nets:

            # select this net as current net in the grid
            self.grid.choose_net(net)
            
            # run until net is finished
            while not net.finished:
                directions_to_end = self.grid.get_directions_to_end()

                possible_directions = self.grid.get_directions()

                # if net is stuck, delete net and break
                if not possible_directions:
                    self.grid.delete_net(net, -1)
                    print("{net} failed")
                    break
                
                # make a list of overlap between possible directions and directions in the right direction
                optimal_options = [direction for direction in directions_to_end if direction in self.grid.get_directions()]

                # if going in the right direction is not possible, prioritize going up, else pick random possible direction
                if not optimal_options:
                    if 'U' in possible_directions:
                        self.grid.add_to_net('U')
                    else:
                        self.grid.add_to_net(choice(possible_directions))

                # prioritize staying as low as possible in the grid
                elif 'D' not in optimal_options:
                    self.grid.add_to_net(choice(optimal_options))
                else:
                    self.grid.add_to_net('D')
            
            self.total_wires_length += net.get_length()

        total_costs = 300 * self.grid.amount_of_intersections + self.total_wires_length
        self.grid.get_output(total_costs)