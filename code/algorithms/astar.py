import copy
from queue import PriorityQueue


class Astar():
    """
    Algorithm that finds the best path for each net based on a heuristic function.
    The heuristic function is the traveled distance from the starting gate
    plus the minimal distance to the end gate. (All distances are Manhattan distances.)
    """
    
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.failed_nets = []
        self.costs = 0

        self.run()
    
    def run(self):
        length = 0

        for net in self.netlist:

            self.grid.current_net = net

            start = net.start
            end = net.end

            count = 0
            open_set = PriorityQueue()
            
            # f-score, count for breaking ties 
            open_set.put((0, count, start))
            previous = {}

            g_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            g_score[start] = 0

            f_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            f_score[start] = self.h_score(start)

            # items in PriorityQueue
            items = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                items.remove(current)

                if current == end:
                    path = self.reconstruct(current, previous, start)
                    directions_to_end = self.get_directions_to_end(path)
                    length += len(directions_to_end)
                    self.add_net(directions_to_end, net)
                    break
                
                directions = self.grid.get_directions(current)
                
                for direction in directions:
                    temp_g_score = g_score[current] + 1
                    
                    neighbor = self.grid.crossing_at_direction(direction, current)

                    # verwijder deze 2 regels om alleen de afstand de beschouwen
                    if (neighbor.initial_amount_of_directions - len(neighbor.directions)) > 1:
                        temp_g_score += 300
                        

                    if temp_g_score < g_score[neighbor]:
                        previous[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + self.h_score(neighbor)
                        
                        if neighbor not in items:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            items.add(neighbor)

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
        print("")

        self.grid.get_output(self.costs)

    def h_score(self, crossing):
        self.grid.current_crossing = crossing
        return len(self.grid.get_directions_to_end())
    
    def reconstruct(self, current, previous, start):
        path = []
        
        while current in previous:
            path.append(current)
            current = previous[current]
        
        path.append(start)
        path.reverse()

        return path
    
    def get_directions_to_end(self, path):
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
        self.grid.current_crossing = net.start
        for direction in directions:
            self.grid.add_to_net(direction)