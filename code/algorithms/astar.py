import copy
from queue import PriorityQueue


class Astar():
    """
    Algorithm that finds the best path for each net based on a heuristic function.
    The heuristic function considers the costs to get from the starting gate to a certain point in the grid,
    the minimal costs to get from that point to the end gate and the amount of intersections along the path.
    """
    
    def __init__(self, grid, method = 'default'):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.get_netlist(method, self.grid.available_nets())

        self.length = 0
        self.intersections = 0
        self.costs = 0
        self.failed = 0
    
    def run(self):
        """
        Runs A* algoritm until all nets are considered.
        """

        # solve problem net by net
        for net in self.netlist:
            self.grid.current_net = net

            # save start and end crossing
            start = net.start

            # set g-scores and f-scores for all crossings to infinity and update for start
            g_score = self.set_scores_to_infinity()
            f_score = self.set_scores_to_infinity()
            g_score[start] = 0
            f_score[start] = self.get_h_score(start)

            count = 0

            # initialise open set and insert start crossing
            open_set = PriorityQueue()
            open_set.put((0, count, start))

            # keep track of elements in open_set
            elements = {start}
            
            # keep track of predecessors of crossings
            previous = {}

            # keep trying while still crossings left
            while open_set:
                current = open_set.get()[2]
                elements.remove(current)

                # if end is reached place net and move to next
                if self.end_gate_reached(current, net):
                    self.place_net(previous, net)
                    # length = self.place_net(current, previous, net)
                    # self.length += length
                    break
                
                neighbours = self.get_neighbours(current, net)
                
                # consider all available neighbouring crossings
                for neighbour in neighbours:

                    # get g_score of neighbour based on current crossing
                    temp_g_score = self.get_temp_g_score(g_score[current], neighbour)

                    # check whether calculated g-score is smaller than saved g-score, if so update g-score and f-score
                    if temp_g_score < g_score[neighbour]:
                        previous[neighbour] = current
                        g_score[neighbour] = temp_g_score
                        f_score[neighbour] = temp_g_score + self.get_h_score(neighbour)
                        
                        # make sure considered crossing is in open_set
                        if neighbour not in elements:
                            count += 1
                            open_set.put((f_score[neighbour], count, neighbour))
                            elements.add(neighbour)

            # if net is not finished it failed
            if not net.finished:
                self.failed += 1
        
        self.intersections = self.grid.amount_of_intersections
        self.costs =  self.length + 300 * self.intersections

        # create output
        self.grid.get_output(self.costs)
    
    def get_neighbours(self, crossing, net):
        neighbours = []
        directions = self.grid.get_directions(crossing)
        for direction in directions:
            neighbour = self.grid.crossing_at_direction(direction, crossing)
            if neighbour.is_gate:
                if neighbour != net.end:
                    continue
            neighbours.append(neighbour)
        return neighbours

    def get_temp_g_score(self, score, crossing):
        temp_g_score = score + 1
        if (crossing.initial_amount_of_directions - len(crossing.directions)) > 1:
            temp_g_score += 300
        return temp_g_score

    def place_net(self, previous, net):
        """
        Places net and updates length
        """
        path = self.reconstruct(net.end, previous, net.start)
        directions_to_end = self.get_directions_to_end(path)
        self.length += len(directions_to_end)
        self.add_net(directions_to_end, net)

    def end_gate_reached(self, crossing, net):
        if crossing == net.end:
            return True
        return False
    
    def set_scores_to_infinity(self):
        return {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}

    def get_h_score(self, crossing):
        """
        Calculates the h-score of a given crossing.
        """
        return len(self.grid.get_directions_to_end(crossing))
    
    def reconstruct(self, current, previous, start):
        """
        Reconstructs the path between the start and end crossing of a net
        based on a dictionary with crossings and their predecessors.
        The steps are saved in a list.
        """
        path = []
        
        while current in previous:
            path.append(current)
            current = previous[current]
        
        path.append(start)
        path.reverse()

        return path
    
    def get_directions_to_end(self, path):
        """
        Takes a list of crossings from the start to the end of
        a net and converts it to a list of directions.
        """
        directions = []

        for i in range(len(path) - 1):
            current = path[i].location
            next = path[i + 1].location

            if next[0] - current[0] == 1:
                directions.append('E')
            elif next[0] - current[0] == -1:
                directions.append('W')
            elif next[1] - current[1] == 1:
                directions.append('S')
            elif next[1] - current[1] == -1:
                directions.append('N')
            elif next[2] - current[2] == 1:
                directions.append('U')
            elif next[2] - current[2] == -1:
                directions.append('D')
            
        return directions
    
    def add_net(self, directions, net):
        """
        Creates a complete net based on a list of directions.
        """
        self.grid.current_crossing = net.start
        for direction in directions:
            self.grid.add_to_net(direction)
            
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

    def get_outer(self, netlist):

        outer_nets = []
        for net in netlist:
            start = net.start.location
            end = net.end.location
            size = self.grid.size

            start_score = min(start[0], size[0]-start[0]-1, start[1], size[1]-start[1]-1)
            end_score = min(end[0], size[0]-end[0]-1, end[1], size[1]-end[1]-1)
            score = (start_score + end_score) / 2
            outer_nets.append((score, net))
        outer_nets.sort(key = lambda x : x[0])
        
        return [i[1] for i in outer_nets]
    
    def get_inner(self, netlist):
        return list(reversed(self.get_outer(netlist)))

    def select_longest_nets(self, netlist):
        return list(reversed(self.select_shortest_nets(netlist)))
    
    def get_netlist(self, method, netlist):

        if method == 'default':
            return netlist
        elif method == 'reverse':
            return list(reversed(netlist))
        elif method == 'short':
            return self.select_shortest_nets(netlist)
        elif method == 'long':
            return self.select_longest_nets(netlist)
        elif method == 'outside':
            return self.get_outer(netlist)
        elif method == 'inside':
            return self.get_inner(netlist)
        else:
            raise Exception('Invalid method')