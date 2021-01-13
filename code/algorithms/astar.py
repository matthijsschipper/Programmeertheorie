'''
import copy


class Astar():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        self.netlist = self.grid.available_nets()

        self.get_routes(self.netlist)
    
    def get_routes(self):
        for net in netlist:

            open_list = []
            closed_list = []

            self.grid.choose_net(net)

            open_list.append(self.grid.current_net.start)
            
            while len(open_list) != 0:

                index = 0
                lowest_f = get_f(open_list[0])

                for i in range(len(open_list)):

                    f = get_f(open_list[i])

                    if f < lowest_f:
                        lowest_f = f
                        index = i
                
                current = open_list.pop(index)
                closed_list.append(current)

                # path is found
                if current == self.grid.current_net.end:
                    return True
                
                directions = self.grid.get_directions()

                for direction in directions:
                    neighbour = self.grid.add_to_net(direction)

                    if neighbour not in open_list:
                        open_list.append(neighbour)
                    
                    self.grid.delete_last_crossing(self, net)



    def get_f(self, crossing):
        return get_g(crossing) + get_h(crossing)

    def get_g(self, crossing):
        # aantal afgelegde stappen
        pass
    
    def get_h(self):
        # minimale aantal stappen te gaan
        pass
    
    def set_parent(self, crossing, parent):
        pass

'''
