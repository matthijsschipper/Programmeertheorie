def select_shortest_nets(grid):
    """
    Takes a grid object as input
    Determines which nets should be the shortest to lay down
    Returns a grid object with the ordered lists
    """

    netlist = grid.netlist
    nets_with_length = []
    for net in netlist:
        amount_of_steps = sum([abs(i) for i in net.get_route_to_end()])
        nets_with_length.append((amount_of_steps, net))
    nets_with_length.sort(key = lambda x : x[0])
        
    grid.netlist = [i[1] for i in nets_with_length]

    return grid

def select_longest_nets(grid):
    """
    Takes a grid object as input
    Inverses the order of the shortest lists results
    Returns a grid object with the ordered lists
    """

    order_shortest = select_shortest_nets(grid)
    order_shortest.netlist.reverse()

    return grid

def select_outer_nets(grid):
    """
    Takes a grid object as input
    Orders the netlist in a way that the netlists that should be the most to the edges of the grid are placed first
    Returns a grid object with the ordered netlists
    """

    outer_nets = []
    for net in grid.netlist:
        start = net.start.location
        end = net.end.location
        size = grid.size

        start_score = min(start[0], size[0]-start[0]-1, start[1], size[1]-start[1]-1)
        end_score = min(end[0], size[0]-end[0]-1, end[1], size[1]-end[1]-1)
        score = (start_score + end_score) / 2
        outer_nets.append((score, net))
    outer_nets.sort(key = lambda x : x[0])
        
    grid.netlist = [i[1] for i in outer_nets]

    return grid

def select_inner_nets(grid):
    """
    Takes a grid object as input
    Orders the netlist in a way that the netlists that should be the most to the center of the grid are placed first
    Returns a grid object with the ordered netlists
    """

    order_outer = select_outer_nets(grid)
    order_outer.netlist.reverse()

    return grid