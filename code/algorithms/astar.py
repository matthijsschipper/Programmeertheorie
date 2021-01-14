import copy
from queue import PriorityQueue


class Astar():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.run()
    
    def run(self, netlist):
        for net in self.netlist:
            self.grid.current_net = net

            # miss in methode in grid
            start = net.start
            end = net.end

            count = 0
            open_set = PriorityQueue()
            
            # f-score, count for breaking ties 
            open_set.put((0, count, start))
            previous = {}

            # pakt hij hier niet de diepte? Miss self.grid[1]
            g_score = {crossing: float("inf") for row in self.grid for crossing in row}
            g_score[start] = 0

            f_score = {crossing: float("inf") for row in self.grid for crossing in row}
            f_score[start] = h_score(start)

            # items in PriorityQueue
            items = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                items.remove(current)

                if current == end:
                    reconstruct(previous)
                    return True
                
                for neighbor in current.neighbors:
                    temp_g_score = g_score[current] + 1

                    if temp_g_score < g_score[neighbor]:
                        previous[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + h_score(neighbor)
                        
                        if neighbor not in items:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            items.add(neighbor)
        
        return False
    
    def h_score(self, crossing):
        self.current_crossing = crossing
        # nog iets doen met current_net
        return len(get_directions_to_end())
    
    def reconsturct(self, current, previous):
        path = []
        # aanpassen
        while current in previous:
            path.append(current.location)
            current = previous[current]
        
        print(path)


# CHANGES TO DATASTRUCTURE

in Crossing class
self.neighbors = []

in Grid class

get_crossing(self, x, y, z):
    return self.grid[z][y][x]

set_neighbors(self, crossing):
    directions = crossing.get_possible_directions()

    for direction in crossing.get_possible_directions
        # retrieve new crossing object at right location
        current_coordinates = crossing.get_coordinates()

        # if direction is north, y coordinate goes down by one (may seem weird, has to do with indexing)
        if direction == 'N':
            new_y_coordinate = current_coordinates[1] - 1
            new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]

        # if direction is south, y coordinate goes up by one (may seem weird, has to do with indexing)
        elif direction == 'S':
            new_y_coordinate = current_coordinates[1] + 1
            new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]

        # if direction is east, x coordinate goes up by one
        elif direction == 'E':
            new_x_coordinate = current_coordinates[0] + 1
            new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]
            
        # if direction is west, x coordinate goes down by one
        elif direction == 'W':
            new_x_coordinate = current_coordinates[0] - 1
            new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]     

        crossing.neighbors.append(new_crossing)
