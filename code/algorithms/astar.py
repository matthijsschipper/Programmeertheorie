import copy
from queue import PriorityQueue


class Astar():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.run()
    
    def run(self):
        for net in self.netlist:

            c = 1
            print(f"net: {c}")
            c += 1

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
            # AANPASSEN
            g_score = {crossing.location: float("inf") for row in self.grid.grid[1] for crossing in row}
            print(g_score)
            g_score[start] = 0

            f_score = {crossing: float("inf") for row in self.grid.grid[1] for crossing in row}
            f_score[start] = self.h_score(start)

            # items in PriorityQueue
            items = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                print(current.location)
                items.remove(current)

                # .location?
                if current == end:
                    reconstruct(previous)
                    return True
                
                neighbors = []

                self.grid.current_crossing = current

                print(self.grid.get_directions())

                for direction in self.grid.get_directions():
                    neighbors.append(self.grid.crossing_at_direction(direction))
                print(neighbors)
                
                for neighbor in neighbors:
                    temp_g_score = g_score[current] + 1
                    #hier ggat het mis
                    print(temp_g_score)
                    print(g_score[neighbor])

                    if temp_g_score < g_score[neighbor]:
                        previous[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + self.h_score(neighbor)
                        
                        if neighbor not in items:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            items.add(neighbor)
        
        return False
    
    def h_score(self, crossing):
        self.current_crossing = crossing
        # nog iets doen met current_net
        return len(self.grid.get_directions_to_end())
    
    def reconstruct(self, current, previous):
        path = []
        # aanpassen
        while current in previous:
            path.append(current.location)
            current = previous[current]
        
        print(path)

