import copy
from queue import PriorityQueue


class Astar():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.run()
    
    def run(self):
        c = 1
        print (f"netlist = {self.netlist}")

        for net in self.netlist:

            print(f"net: {c}")
            c += 1

            self.grid.current_net = net

            # miss in methode in grid
            start = net.start
            end = net.end

            print(f"start: {start.location}")
            print(f"end: {end.location}")
            print("")

            count = 0
            open_set = PriorityQueue()
            
            # f-score, count for breaking ties 
            open_set.put((0, count, start))
            previous = {}

            # AANPASSEN voor 3d
            g_score = {crossing: float("inf") for row in self.grid.grid[0] for crossing in row}
            g_score[start] = 0

            f_score = {crossing: float("inf") for row in self.grid.grid[0] for crossing in row}
            f_score[start] = self.h_score(start)
            #print(f"f_score start: {f_score[start]}")

            # items in PriorityQueue
            items = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                print(f"current location: {current.location}")
                items.remove(current)

                if current == end:
                    self.reconstruct(current, previous, start)
                    print("jeej eind bereikt")
                    break
                
                neighbors = []

                self.grid.current_crossing = current

                directions = self.grid.get_directions()
                #print(f"directions: {directions}")

                # weghalen bij 3d en korter schrijven
                if 'U' in directions:
                    directions.remove('U')
                
                print(f"directions: {directions}")

                for direction in directions:
                    neighbors.append(self.grid.crossing_at_direction(direction))
                
                # later weghalen
                for neighbor in neighbors:
                    print(f"neighbor: {neighbor.location}")
                
                temp_g_score = g_score[current] + 1
                #hier ggat het mis
                print(f"temp g_score: {temp_g_score}")

                for neighbor in neighbors:
                    
                    if temp_g_score < g_score[neighbor]:
                        previous[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + self.h_score(neighbor)

                        #print(f"g_score neighbor: {g_score[neighbor]}")
                        #print(f"f_score neighbor: {f_score[neighbor]}")
                        
                        if neighbor not in items:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            items.add(neighbor)
                    print("")
            print("")
                    
                    
            # stop na 1 net
            #break
        
        return False
    
    def h_score(self, crossing):
        self.grid.current_crossing = crossing
        #print(f"directions to end from {crossing.location}: {self.grid.current_net.get_route_to_end(crossing)}")
        return len(self.grid.get_directions_to_end())
    
    def reconstruct(self, current, previous, start):
        path = []
        
        # aanpassen
        while current in previous:
            path.append(current.location)
            current = previous[current]
        
        path.append(start.location)
        
        print(f"path: {path}")

'''
Aanpassing net class

 def get_route_to_end(self, current_crossing = ""):
        """
        Returns the amount of steps still needed in a certain direction as a list, order: x, y, z
        If net is finished, returns None
        """

        if self.finished == True:
            return None

        # save the coordinates of all relevant crossings
        if current_crossing == "":
            current_crossing = self.routelist[-1]
        current_location = current_crossing.location
        destination = self.end.location
'''