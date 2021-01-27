from .crossing import Crossing
from .net import Net
from csv import reader, writer

class Grid():
    def __init__(self, printfile, netlistfile):
        """
        Takes standard-formatted print and netlist files for the the chip as input.
        Initializes the grid through other functions.
        """
        self.grid = []
        self.size = [0, 0, 0]
        self.gate_coordinates = {}
        self.netlist = []
        self.amount_of_intersections = 0

        self.chip_id = None
        self.netlist_id = None

        self.current_crossing = None
        self.current_net = None

        # Reads the input file, saves gate coordinates and size of grid in self
        self.read_chip_data(printfile)

        # Create and initialize the nested lists, the actual grid
        self.make_grid()

        # Loads the requested netlist into the grid
        self.set_netlist(netlistfile)

    def read_chip_data(self, infile):
        """
        Takes standard-formatted print file for the the chip as input.
        Reads in all relevant data.
        """
        with open(infile) as file:

            # Read through file
            file_reader = reader(file)

            # Skip the header
            next(file_reader, None)

            # Save coordinates and numbers of gates into dictionary, retrieve max_x and max_y
            data = [line.rstrip() for line in file]
            x_max, y_max = 0, 0
            for row in data:
                information = row.split(",")

                # check for maximum values of x and y
                x, y = int(information[1]), int(information[2])
                x_max, y_max = max(x, x_max), max(y, y_max)

                # save gate coordinates to dictionary
                self.gate_coordinates[information[0]] = [x, y, 0]

        # +2, because there is supposed to be a row and column clean of gates around the chip
        self.size = [x_max + 2, y_max + 2, 8]

        # Save the number of the chip you're working with and the location of the file
        for char in infile:
            try:
                self.chip_id = int(char)
            except:
                pass

    def make_grid(self):
        """
        Creates the 3d array that holds all crossings.
        """
        # Save x, y, z values of the size of the grid
        x, y, z = self.size[0], self.size[1], self.size[2]

        # Create 3D matrix with found size
        for height in range(z):
            height_list = []
            self.grid.append(height_list)

            for column in range(y):
                column_list = []
                height_list.append(column_list)

                for row in range(x):
                    column_list.append(Crossing(row, column, height, self.size))
        
        # Mark gates
        for gate_nr in self.gate_coordinates:
            x_coordinate, y_coordinate, z_coordinate = self.gate_coordinates[gate_nr][0], self.gate_coordinates[gate_nr][1], self.gate_coordinates[gate_nr][2]

            # Reverse order of coordinates for indexing grid
            gate = self.grid[z_coordinate][y_coordinate][x_coordinate]
            gate.place_gate(f"{gate_nr}")

    def set_netlist(self, infile):
        """
        Takes standard-formatted netlist file as input.
        Saves the routes that should be placed as net objects.
        Sets the current_crossing and current_net to the start of the first net.
        """
        with open(infile) as file:

            # Read through file
            file_reader = reader(file)

            # Skip the header
            next(file_reader, None)

            # Save nets into dictionary
            data = [line.rstrip() for line in file]
            for row in data:
                if row:
                    information = row.split(",")
                    start, end = information[0], information[1]
                    start_location = self.gate_coordinates[start]
                    end_location = self.gate_coordinates[end]

                    # Index the grid with [z][y][x]
                    start_crossing = self.grid[start_location[2]][start_location[1]][start_location[0]]
                    end_crossing = self.grid[end_location[2]][end_location[1]][end_location[0]]

                    # Create net object and save it to grid
                    self.netlist.append(Net(start_crossing, end_crossing))

        # Default setting, can be changed by algorithm
        self.current_net = self.netlist[0]
        self.current_crossing = self.current_net.start

        # Save netlist id
        for char in infile:
            try:
                self.netlist_id = int(char)
            except:
                pass

    def available_nets(self):
        """
        Returns all net objects in the netlist that aren't marked as finished.
        """
        unfinished_nets = []

        comprehension = [unfinished_nets.append(net) for net in self.netlist if not net.finished]

        return unfinished_nets

    def choose_net(self, net):
        """
        After calling which nets are available, pass the net you want to work on making
        If net is an unfinished net, sets net to current net, set current crossing to latest crossing in net
        """
        if net in self.available_nets():
            self.current_net = net
            self.current_crossing = net.get_latest_crossing()
            return True
        return False

    def add_to_net(self, direction):
        """
        Takes a letter to represent the direction as variable
        Adds the new location to the net, add blockades to involved crossings
        Returns false if invalid direction is passed or crossing is a gate not in the current_net, else true
        """

        # first check if this direction is still an option from the current crossing
        if direction in self.current_crossing.directions:
            new_crossing = self.crossing_at_direction(direction)

            # block the directions from both crossings
            self.current_crossing.add_blockade(direction)
            already_intersection = new_crossing.intersection
            opposite = self.get_opposite(direction)
            new_crossing.add_blockade(opposite[0])

            # add new crossing object to the net
            self.current_net.add_crossing(new_crossing)
            self.current_crossing = new_crossing

            # count if intersection is created
            if not already_intersection:
                if self.current_crossing.intersection:
                    self.amount_of_intersections += 1

            # react accordingly if crossing is the end of the net
            if self.current_net.finished:

                # go to next unfinished net per default
                possible_nets = self.available_nets()
                if possible_nets != []:
                    self.current_net = possible_nets[0]
                    self.current_crossing = self.current_net.start
                else:
                    self.current_net = None
                    self.current_crossing = None

            return True

        # if a non-valid direction is passed, return false
        return False

    def delete_net(self, net, steps):
        """
        Takes a net object as input, and the number of steps you want to remove from the route
        Deletes the asked amount of steps from the end of the route from the net objects and crossing objects
        If amount of steps is bigger then the total steps in the route, or -1, deletes the entire route
        """

        if steps > net.get_length() or steps < 0:
            steps = net.get_length()
        
        # remove the last crossing from the net as many times as is necessary
        while steps > 0:
            self.delete_last_crossing(net)
            steps  -= 1

        # when a crossing is removed, the net can never be finished anymore
        net.mark_unfinished()

    def delete_last_crossing(self, net):
        """
        Takes a net object as input
        Removes the last added crossing from the route
        Removes the blockades in the crossing objects
        """

        # retrieve relevant crossing objects
        crossings = net.get_latest_two_crossings()
        last_crossing, second_last_crossing = crossings[0], crossings[1]

        # retrieves the direction between the crossing objects
        last_crossing_coordinates = last_crossing.location
        second_last_crossing_coordinates = second_last_crossing.location

        x_difference = last_crossing_coordinates[0] - second_last_crossing_coordinates[0]
        y_difference = last_crossing_coordinates[1] - second_last_crossing_coordinates[1]
        z_difference = last_crossing_coordinates[2] - second_last_crossing_coordinates[2]

        # check if last of second last crossing is an intersection
        check_last_crossing = last_crossing.intersection

        # removes the blockades on both crossings
        if x_difference < 0:
            last_crossing.remove_blockade('E')
            second_last_crossing.remove_blockade('W')
        elif x_difference > 0:
            last_crossing.remove_blockade('W')
            second_last_crossing.remove_blockade('E')
        elif y_difference < 0:
            last_crossing.remove_blockade('S')
            second_last_crossing.remove_blockade('N')
        elif y_difference > 0:
            last_crossing.remove_blockade('N')
            second_last_crossing.remove_blockade('S')
        elif z_difference < 0:
            last_crossing.remove_blockade('U')
            second_last_crossing.remove_blockade('D')
        elif z_difference > 0:
            last_crossing.remove_blockade('D')
            second_last_crossing.remove_blockade('U')

        # adjusts amount of intersections accordingly
        if check_last_crossing == True:
            if last_crossing.intersection == False:
                self.amount_of_intersections -= 1

        # deletes the last crossing object in the net
        net.delete_last_crossing()

    def get_crossing(self, x, y, z):
        """
        Takes the coordinates x, y and z as integers as input
        Returns the crossing object in that location
        """

        # indexing order: z, y, x
        return self.grid[z][y][x]

    def get_directions(self, crossing = ""):
        """
        Returns possible directions from crossing as list
        """
        if crossing == "":
            crossing = self.current_crossing

        return crossing.directions

    def get_directions_to_end(self, crossing = ""):
        """
        Returns a list of directions to the end of the current net, order: x, y, z
        """
        if crossing == "":
            crossing = self.current_crossing

        literal_directions = self.current_net.get_route_to_end(crossing)
        directions = []

        # translate to directions
        if literal_directions[0] >= 0:
            for i in range(literal_directions[0]):
                directions.append("E")
        elif literal_directions[0] < 0:
            for i in range(abs(literal_directions[0])):
                directions.append("W")

        if literal_directions[1] >= 0:
            for i in range(literal_directions[1]):
                directions.append("N")
        elif literal_directions[1] < 0:
            for i in range(abs(literal_directions[1])):
                directions.append("S")

        if literal_directions[2] >= 0:
            for i in range(literal_directions[2]):
                directions.append("U")
        elif literal_directions[2] < 0:
            for i in range(abs(literal_directions[2])):
                directions.append("D")

        return directions
    
    def crossing_at_direction(self, direction, crossing = ""):
        """
        Takes as input a direction and optionally a crossing object, default is the current_crossing in the grid
        Returns the crossing object a certain direction away from the crossing object, no matter if there is a blockade
        Returns None if an invalid direction was passed
        """

        if crossing == "":
            crossing = self.current_crossing

        if direction in ['N', 'S', 'E', 'W', 'U', 'D']:

            current_coordinates = crossing.location

            # if direction if north, y coordinate goes down by one (may seem weird, has to do with indexing)
            if direction == 'N':
                new_y_coordinate = current_coordinates[1] - 1

                new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]

            # if direction if south, y coordinate goes up by one (may seem weird, has to do with indexing)
            elif direction == 'S':
                new_y_coordinate = current_coordinates[1] + 1

                new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]

            # if direction if east, x coordinate goes up by one
            elif direction == 'E':
                new_x_coordinate = current_coordinates[0] + 1

                new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]

            # if direction if west, x coordinate goes down by one
            elif direction == 'W':
                new_x_coordinate = current_coordinates[0] - 1

                new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]

            # if direction is up, z coordinate goes up by one
            elif direction == 'U':
                new_z_coordinate = current_coordinates[2] + 1

                new_crossing = self.grid[new_z_coordinate][current_coordinates[1]][current_coordinates[0]]

            # if direction is down, z coordinate goes down by one
            elif direction == 'D':
                new_z_coordinate = current_coordinates[2] - 1

                new_crossing = self.grid[new_z_coordinate][current_coordinates[1]][current_coordinates[0]]

            return new_crossing
        return None

    def get_opposite(self, direction):
        """
        For each possible direction, returns the opposite
        """

        if direction in ['S', 'N']:
            return [i for i in ['S', 'N'] if i != direction]
        elif direction in ['E', 'W']:
            return [i for i in ['E', 'W'] if i != direction]
        elif direction in ['U', 'D']:
            return [i for i in ['U', 'D'] if i != direction]

    def get_output(self, total_costs):
        """
        Takes the total_costs of the chip as int as input
        Can be called on the grid to write an outputfile
        """

        with open(f"./data/outputfiles/chip_{self.chip_id}_net_{self.netlist_id}.csv", 'w') as file:
        # This other output file can be used for the check50
        # with open('./data/outputfiles/output.csv', 'w') as file:
            output = writer(file)
            output.writerow(["net", "wires"])

            for net in self.netlist:
                start_gate, end_gate = net.start.name, net.end.name
                route = tuple([int(start_gate),int(end_gate)])
                route_string = str(route).replace(" ", "")
                routelist = net.show_route_coordinates()
                routelist_string = str(routelist).replace(" ", "")
                output.writerow([route_string, f"{routelist_string}"])
            
            output.writerow([f"chip_{self.chip_id}_net_{self.netlist_id},{total_costs}"])
    
    def netlist_length(self):
        length = []

        for net in self.netlist:
            length.append(net.get_length())
        
        return sum(length)
    
    def calculate_costs(self):
        return self.netlist_length() + 300 * self.amount_of_intersections