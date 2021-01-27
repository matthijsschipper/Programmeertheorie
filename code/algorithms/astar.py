import copy
from queue import PriorityQueue


class Astar():
    """
    Algorithm that finds the best path for each net based on a heuristic function.
    The heuristic function considers the costs to get from the starting gate to a certain point in the grid
    and the minimal costs to get from that point to the end gate.
    """
    
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.netlist

        self.length = 0
        self.intersections = 0
        self.costs = 0
        self.failed = 0
    
    def set_scores_to_infinity(self):
        """
        Creates a dictionary with a score of infinity for every crossing.
        """
        return {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
    
    def get_h_score(self, crossing):
        """
        Calculates the h-score of a given crossing.
        """
        return len(self.grid.get_directions_to_end(crossing))
    
    def end_gate_reached(self, crossing, net):
        """
        Checks if the end of a net is reached.
        """
        if crossing == net.end:
            return True

        return False

    def reconstruct(self, current, previous, start):
        """
        Reconstructs the path (of crossings) between the start and end crossing of a net
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

    def place_net(self, previous, net):
        """
        Places a net and updates self.length.
        """
        path = self.reconstruct(net.end, previous, net.start)
        directions_to_end = self.get_directions_to_end(path)
        self.length += len(directions_to_end)
        self.add_net(directions_to_end, net)

    def get_neighbours(self, crossing, net):
        """
        Returns a list of all neighbours reachable from a certain crossing.
        """
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
        """
        Returns the temporary g_score of a crossing based on the score of the previous crossing.
        """
        temp_g_score = score + 1
        if (crossing.initial_amount_of_directions - len(crossing.directions)) > 1:
            temp_g_score += 300

        return temp_g_score

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

            # initialise open set and insert start crossing
            open_set = PriorityQueue()
            count = 0
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
                    break
                
                neighbours = self.get_neighbours(current, net)
                
                # consider all available neighbouring crossings
                for neighbour in neighbours:

                    # get g_score of neighbour based on score of current crossing
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
        self.costs = self.length + 300 * self.intersections
        
        self.grid.get_output(self.costs)