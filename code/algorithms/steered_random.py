from copy import deepcopy
from random import choice, shuffle

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

    def check_direction(self, net, direction):
        """
        Takes a net object and a direction as input
        Checks if that diretion doesn't result in a definitive dead end
        Also checks if that direction isn't a gate, unless it's the end of the net
        Returns true if that direction is a good option, else false
        """

        # start from the last added crossing in the list
        crossing = net.routelist[-1]

        to_be_added_crossing = self.grid.crossing_at_direction(direction, crossing)
        
        # if the crossing is a dead-end, don't go there
        if to_be_added_crossing.directions == []:
            return False

        # if the crossing is a gate, only allow it if it's the endgate of the net
        if to_be_added_crossing.is_gate:
            if to_be_added_crossing != net.end:
                return False

        # if the crossing will become an intersection, try to avoid it
        if (to_be_added_crossing.initial_amount_of_directions - len(to_be_added_crossing.directions)) > 1:
            return False

        return True

    def run(self, tries):
        """
        Algorithm that takes in a grid object as input
        First selects which nets should be layed down first
        For each net, tries to walk towards to end point
        Returns a grid object with solutions if succesful, else None
        """

        # order the nets by expected size
        ordered_nets = self.select_shortest_nets(self.grid.netlist)
        succeeded_nets = []

        # try given amount of times
        while tries > 0:

            # solve puzzle net by net
            for net in ordered_nets:

                # variable to keep track if net failed or succeeded
                succes = True
                optimal_choices = True

                # select this net as current net in the grid
                self.grid.choose_net(net)
                print(f"starting on {net}")

                # run until net is finished
                while not net.finished:
                    directions_to_end = self.grid.get_directions_to_end()
                    possible_directions = self.grid.get_directions()

                    # if net is stuck, delete net and break
                    if not possible_directions:
                        print(f"{net} failed")
                        print(net.show_route_coordinates())
                        self.grid.delete_net(net, -1)
                        succes = False
                        break
                
                    # make a list of overlap between possible directions and directions in the right direction
                    optimal_options = [direction for direction in directions_to_end if direction in possible_directions]

                    # if going in the right direction is not possible, prioritize going up, else pick random possible direction
                    if not optimal_options or optimal_choices == False:
                        if 'U' in possible_directions and self.check_direction(net, 'U'):
                            optimal_choices = True
                            self.grid.add_to_net('U')

                        else:
                            shuffle(possible_directions)
                            found_direction = False

                            # check all non-optimal directions, if one isn't a dead end, add to net
                            for direction in possible_directions:
                                if self.check_direction(net, direction) and found_direction == False:
                                    found_direction = True
                                    optimal_choices = True
                                    self.grid.add_to_net(direction)
                            
                            # if none of the directions are possible, register net as failure
                            if found_direction == False:
                                print(f"{net} failed")
                                self.grid.delete_net(net, -1)
                                succes = False
                                break

                    # prioritize staying as low as possible in the grid
                    elif 'D' in optimal_options and self.check_direction(net, 'D'):
                        optimal_choices = True
                        self.grid.add_to_net('D')

                    # if there is overlap between the right direction and the possible directions, pick a random direction out of that list
                    else:
                        shuffle(optimal_options)
                        direction_added = False
                        for direction in optimal_options:
                            if self.check_direction(net, direction) and direction_added == False:
                                direction_added = True
                                optimal_choices = True
                                self.grid.add_to_net(direction)
                        
                        # if there were optimal choices, but none were a not-deadend, make sure it doesn't endlessly loop
                        if not direction_added:
                            optimal_choices = False
                        
                # if the net is finished, save the length and exclude from running again
                if succes != False:
                    self.total_wires_length += net.get_length()
                    succeeded_nets.append(net)

            ordered_nets = [i for i in ordered_nets if i not in succeeded_nets]
            tries -= 1

        total_costs = 300 * self.grid.amount_of_intersections + self.total_wires_length
        self.grid.get_output(total_costs)
