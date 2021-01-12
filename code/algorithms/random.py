import copy
import random

class Random():
    def  __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.netlist
        self.current_location = None
        self.current_crossing = None
        self.directions = None
        self.steps = 0
        self.random_routes(self.netlist)
    
    def random_routes(self, netlist):
        for connection in netlist:
            start_gate, end_gate = connection.start, connection.end
            self.current_location = start_gate.location
            self.end_location = end_gate.location

            # Randomly walk over grid until current Crossing object is end_gate
            while self.current_location != self.end_location:
                x, y, z = self.current_location[0], self.current_location[1], self.current_location[2]
                self.current_crossing = self.grid.grid[z][y][x]

                # If no directions are available anymore, the random route has failed to reach the end gate
                if self.current_crossing.get_possible_directions() == []:
                    print(f'The random route got stuck (no options left to choose from)!')
                    break
                
                self.directions = self.current_crossing.get_possible_directions()
                random_direction = random.choice(self.directions)

                # Remove selected direction from available directions
                # Moet nog aangepast worden
                self.current_crossing.add_blockade(random_direction)

                # Mark current crossing as visited
                self.current_crossing.set_visited()

                # Add current crossing to routelist
                connection.routelist.append(self.current_crossing)

                # Count steps
                self.steps += 1

                if random_direction == 'N':
                    self.current_location[1] -= 1
                    continue
                elif random_direction == 'E':
                    self.current_location[0] += 1
                    continue
                elif random_direction == 'S':
                    self.current_location[1] += 1
                    continue
                elif random_direction == 'W':
                    self.current_location[0] -= 1
                    continue
                elif random_direction == 'U':
                    self.current_location[2] += 1
                    continue
                elif random_direction == 'D':
                    self.current_location[2] -= 1
                    continue
            
            print(f'Amount of steps to get from {start_gate} to {end_gate} with random assigning directions is: {self.steps}.')
        
        self.grid.get_output()
    
    def __str__(self):
        return f'{self.netlist}'