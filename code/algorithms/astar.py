import copy
from queue import PriorityQueue


class Astar():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.run()
    
    def run(self):
        c = 1

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
            g_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            g_score[start] = 0

            f_score = {crossing: float("inf") for layer in self.grid.grid for row in layer for crossing in row}
            f_score[start] = self.h_score(start)
            #print(f"f_score start: {f_score[start]}")

            # items in PriorityQueue
            items = {start}

            while not open_set.empty():
                current = open_set.get()[2]
                print(f"current location: {current.location}")
                items.remove(current)

                if current == end:
                    path = self.reconstruct(current, previous, start)
                    #self.net(path)
                    
                    # print(path) als je .location gebruikt in reconstruct
                    directions_to_end = self.get_directions_to_end(path)
                    print(f"directions to end: {directions_to_end}")
                    self.add_net(directions_to_end, net)
                    
                    print("jeej eind bereikt")
                    break
                
                neighbors = []

                # aanpassen -> zonder current crossing

                self.grid.current_crossing = current

                directions = self.grid.get_directions()

                '''
                # weghalen bij 3d en korter schrijven
                if 'U' in directions:
                    directions.remove('U')
                '''
                
                print(f"directions: {directions}")

                for direction in directions:
                    neighbors.append(self.grid.crossing_at_direction(direction))
                
                # later weghalen
                #for neighbor in neighbors:
                #    print(f"neighbor: {neighbor.location}")
                
                temp_g_score = g_score[current] + 1

                for neighbor in neighbors:
                    
                    if temp_g_score < g_score[neighbor]:
                        previous[neighbor] = current
                        g_score[neighbor] = temp_g_score
                        f_score[neighbor] = temp_g_score + self.h_score(neighbor)
                        
                        if neighbor not in items:
                            count += 1
                            open_set.put((f_score[neighbor], count, neighbor))
                            items.add(neighbor)
                print("")
            print("")
            #break
        
        total_costs = 300 * self.grid.amount_of_intersections + 200
        self.grid.get_output(total_costs)

    def h_score(self, crossing):
        self.grid.current_crossing = crossing
        #print(f"directions to end from {crossing.location}: {self.grid.current_net.get_route_to_end(crossing)}")
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
            print(f"current: {current}")
            next = path[i + 1].location
            print(f"next: {next}")

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
            
            print(directions)
            
        return directions
    
    #weghalen
    def net(self, path):
        for step in path:
            self.grid.current_net.add_crossing(step)

    
    def add_net(self, directions, net):
        self.grid.current_crossing = net.start
        for direction in directions:
            self.grid.add_to_net(direction)


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