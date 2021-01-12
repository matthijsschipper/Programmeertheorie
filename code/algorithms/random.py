import copy
import random

class Random():
    def  __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()
        # self.current_location = None
        # self.current_crossing = None
        self.directions = None
        self.random_routes(self.netlist)
    
    def random_routes(self, netlist):
        for net in netlist:

            self.grid.choose_net(net)
            print(net)

            self.steps = 0
            start_gate, end_gate = net.start, net.end
            self.current_location = start_gate.location
            self.end_location = end_gate.location
            self.dead_end = False

            # Randomly walk over grid until current Crossing object is end_gate
            while not self.grid.net_is_finished():
                # Wss niet nodig
                # x, y, z = self.current_location[0], self.current_location[1], self.current_location[2]
                # self.current_crossing = self.grid.grid[z][y][x]

                # If no directions are available anymore, the random route has failed to reach the end gate
                # if self.current_crossing.get_possible_directions() == []:
                #     print(f'The random route got stuck (no options left to choose from)!')
                #     self.dead_end = True
                #     break
                
                if self.grid.get_directions() == []:
                    print(f'Dead end')
                    self.dead_end = True
                    self.grid.delete_net(net, -1)
                    break

                # self.directions = self.current_crossing.get_possible_directions()
                self.directions = self.grid.get_directions()
                random_direction = random.choice(self.directions)

                # Remove selected direction from available directions
                # Moet nog aangepast worden
                # self.current_crossing.add_blockade(random_direction)

                # # Mark current crossing as visited
                # self.current_crossing.set_visited()

                # # Add current crossing to routelist
                # connection.routelist.append(self.current_crossing)

                self.grid.add_to_net(random_direction)

                # Count steps
                self.steps += 1

                # Continue kan eruit
                # if random_direction == 'N':
                #     self.current_location[1] -= 1
                #     continue
                # elif random_direction == 'E':
                #     self.current_location[0] += 1
                #     continue
                # elif random_direction == 'S':
                #     self.current_location[1] += 1
                #     continue
                # elif random_direction == 'W':
                #     self.current_location[0] -= 1
                #     continue
                # elif random_direction == 'U':
                #     self.current_location[2] += 1
                #     continue
                # elif random_direction == 'D':
                #     self.current_location[2] -= 1
                #     continue
            
            # Print statement is not applicable to routes with a dead end
            if self.dead_end:
                continue

            print(f'Amount of steps to get from {start_gate} to {end_gate} with random assigning directions is: {self.steps}.')
        
        self.grid.get_output()
    
    def __str__(self):
        return f'{self.netlist}'