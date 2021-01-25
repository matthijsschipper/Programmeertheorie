import copy
from queue import PriorityQueue


class Astar():
    """
    Algorithm that finds the best path for each net based on a heuristic function.
    The heuristic function considers the traveled distance from the starting gate,
    the minimal distance to the end gate and the amount of intersections along the path.
    (All distances are Manhattan distances.)
    """
    
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.failed_nets = []
        self.costs = 0

        self.height = 0

        self.run()
    
    def run(self):
        """
        Runs A* algoritm until all nets are considered.
        """

        # total wire length starts at 0
        length = 0

        # solve problem net by net
        for net in self.netlist:
            self.grid.current_net = net

            # save start and end crossing
            start = net.start
            end = net.end

            # set all g-scores and f-scores to infinity and update for start
            g_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            f_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            g_score[start] = 0
            f_score[start] = self.h_score(start)

            count = 0

            # initialise open set and insert start crossing
            open_set = PriorityQueue()
            open_set.put((0, count, start))

            # keep track of elements in open_set
            elements = {start}
            
            # keep track of previous crossing
            previous = {}

            # keep trying until no more crossings left
            while not open_set.empty():
                current = open_set.get()[2]
                elements.remove(current)

                # check if end is reached, if so reconstruct path and break
                if current == end:
                    path = self.reconstruct(current, previous, start)
                    
                     # alleen om hoogte te bepalen
                    for p in path:
                        self.height = max(self.height, p.location[2])

                    directions_to_end = self.get_directions_to_end(path)
                    length += len(directions_to_end)
                    self.add_net(directions_to_end, net)
                    break
                
                # get available directions for considered crossing
                directions = self.grid.get_directions(current)
                
                # consider all available neighbouring crossings
                for direction in directions:
                    
                    neighbour = self.grid.crossing_at_direction(direction, current)

                    # OVERGENOMEN VAN STEERED RANDOM
                    # if the crossing is a gate, only allow it if it's the endgate of the net
                    if neighbour.is_gate:
                        if neighbour != end:
                            continue
                    
                    temp_g_score = g_score[current] + 1
                    
                    # if you only want to consider distances and not the cost of interections remove the following if statement
                    # if intersection at neighbour increment temp_g_score with 300 (cost of intersection)
                    if (neighbour.initial_amount_of_directions - len(neighbour.directions)) > 1:
                        temp_g_score += 300

                    # check whether calculated g-score is smaller than saved g-score, if so update g-score and f-score
                    if temp_g_score < g_score[neighbour]:
                        previous[neighbour] = current
                        g_score[neighbour] = temp_g_score
                        f_score[neighbour] = temp_g_score + self.h_score(neighbour)
                        
                        # make sure considered crossing is in open_set
                        if neighbour not in elements:
                            count += 1
                            open_set.put((f_score[neighbour], count, neighbour))
                            elements.add(neighbour)

            # if net is not finished it failed
            if not net.finished:
                self.failed_nets.append(f"from {net.start} to {net.end}")
        
        intersections = self.grid.amount_of_intersections
        self.costs =  length + 300 * intersections

        # Optional
        print("")
        print(f"Total length: {length}")
        print(f"Amount of intersections: {intersections}")
        print(f"{len(self.failed_nets)} failed nets: {self.failed_nets}")
        print(f"Costs: {self.costs}")
        print(f"Height: {self.height}")
        print("")

        self.grid.get_output(self.costs)

    def h_score(self, crossing):
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
    '''
    # OVERGENOMEN VAN STEERED RANDOM (miss moeten we er een methode in grid.py van maken)
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
    '''