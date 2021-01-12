from .crossing import Crossing
from .net import Net
from csv import reader, writer

class Grid():
    def __init__(self, printfile, netlistfile):
        """
        Takes standard-formatted print and netlist files for the the chip as input
        Initializes the grid through other functions
        """

        self.grid = []
        self.size = [0, 0, 0]
        self.gate_coordinates = {}
        self.netlist = []
        self.amount_of_intersections = 0

        self.current_crossing = None
        self.current_net = None

        # reads the input file, saves gate coordinates and size of grid in self
        self.read_chip_data(printfile)

        # create and initialize the nested lists, the actual grid
        self.make_grid()

        # loads the requested netlist into the grid
        self.set_netlist(netlistfile)

    def read_chip_data(self, infile):
        """
        Takes standard-formatted print file for the the chip as input
        Reads in all relevant data
        """

        with open(infile) as file:

            # read through file
            file_reader = reader(file)

            # skip the header
            next(file_reader, None)

            # save coordinates and numbers of gates into dictionary, retrieve max_x and max_y
            data = [line.rstrip() for line in file]
            x_max, y_max = 0, 0
            for element in data:
                coordinates = element[2:].split(",")

                # check for maximum values of x and y
                x, y = int(coordinates[0]), int(coordinates[1])
                if x > x_max:
                    x_max = x
                if y > y_max:
                    y_max = y

                # save gate coordinates to dictionary
                self.gate_coordinates[element[0]] = [x, y, 0]

        # +2, because there is supposed to be a row and column clean of gates around the chip
        self.size = [x_max + 2, y_max + 2, 2]

    def make_grid(self):
        """
        Creates the 3d array that hold all crossings
        """

        # save x, y, z values of the size of the grid
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
        
        # mark gates
        for gate_nr in self.gate_coordinates:
            x_coordinate, y_coordinate, z_coordinate = self.gate_coordinates[gate_nr][0], self.gate_coordinates[gate_nr][1], self.gate_coordinates[gate_nr][2]

            # reverse order of coordinates for indexing grid
            gate = self.grid[z_coordinate][y_coordinate][x_coordinate]
            gate.place_gate(f"{gate_nr}")

    def set_netlist(self, infile):
        """
        Takes standard-formatted netlist file as input
        Saves the routes that should be placed as net objects
        Sets the current_crossing and current_net to the start of the first net
        """

        with open(infile) as file:

            # read through file
            file_reader = reader(file)

            # skip the header
            next(file_reader, None)

            # save nets into dictionary
            data = [line.rstrip() for line in file]
            for element in data:
                start = element[0]
                end = element[2]
                start_location = self.gate_coordinates[start]
                end_location = self.gate_coordinates[end]

                # index the grid with [z][y][x]
                start_crossing = self.grid[start_location[2]][start_location[1]][start_location[0]]
                end_crossing = self.grid[end_location[2]][end_location[1]][end_location[0]]

                # create net object and save it to grid
                self.netlist.append(Net(start_crossing, end_crossing))
        ###
        ### SHOULD PROBABLY BE CHANGED FOR ALGORTHMS
        ###
        self.current_net = self.netlist[0]
        self.current_crossing = self.current_net.get_start()

    def add_to_net(self, direction):
        """
        Takes a letter to represent the direction as variable
        Adds the new location to the net, add blockades to involved crossings
        Returns false if invalid direction is passed, else true
        """

        if direction in self.current_crossing.get_possible_directions():
            self.current_crossing.add_blockade(direction)
            if not self.current_crossing.set_visited():
                self.amount_of_intersections += 1

            # retrieve new crossing object at right location
            current_coordinates = self.current_crossing.get_coordinates()

            # if direction if north, y coordinate goes down by one (may seem weird, has to do with indexing)
            if direction == 'N':
                new_y_coordinate = current_coordinates[1] - 1

                new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]
                new_crossing.add_blockade('S')

            # if direction if east, x coordinate goes up by one
            elif direction == 'E':
                new_x_coordinate = current_coordinates[1] + 1

                new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]
                new_crossing.add_blockade('W')

            # if direction if north, y coordinate goes up by one (may seem weird, has to do with indexing)
            elif direction == 'S':
                new_y_coordinate = current_coordinates[1] + 1

                new_crossing = self.grid[current_coordinates[2]][new_y_coordinate][current_coordinates[0]]
                new_crossing.add_blockade('N')
                
            # if direction if west, x coordinate goes down by one
            elif direction == 'W':
                new_x_coordinate = current_coordinates[1] - 1

                new_crossing = self.grid[current_coordinates[2]][current_coordinates[1]][new_x_coordinate]
                new_crossing.add_blockade('E')
                
            # if direction is up, z coordinate goes up by one
            elif direction == 'U':
                new_z_coordinate = current_coordinates[1] + 1

                new_crossing = self.grid[new_z_coordinate][current_coordinates[1]][current_coordinates[0]]
                new_crossing.add_blockade('D')
                
            # if direction is down, z coordinate goes down by one
            elif direction == 'D':
                new_z_coordinate = current_coordinates[1] - 1

                new_crossing = self.grid[new_z_coordinate][current_coordinates[1]][current_coordinates[0]]
                new_crossing.add_blockade('U')

            self.current_net.add_crossing(new_crossing)
            self.current_crossing = new_crossing

            # react accordingly if crossing is the end of the net
            if self.current_net.is_finished():
                
                # get to next net object
                ###
                ### SHOULD PROBABLY BE CHANGED FOR DIFFERENT ALGORITHMS
                ###
                index = self.netlist.index(self.current_net)
                if index < len(self.netlist):
                    self.current_net = self.netlist[index + 1]
                
                # if all connections are made, set current net and current crossing to None
                else:
                    self.current_net = None
                    self.current_crossing = None

            return True

        # if a non-valid direction is passed, return false
        return False

    def get_directions(self):
        """
        Returns possible directions from current crossing as list
        """

        return self.current_crossing.get_possible_directions()

    def get_directions_to_end(self):
        """
        Returns a list of directions to the end of the current net, order: x, y, z
        """

        literal_directions = self.current_net.get_route_to_end()
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

    def netlist_filled(self):
        """
        Returns true of all requested connections have been made, else false
        """

        # current_crossing is only set to None if all nets are marked finished
        if self.current_crossing == None:

            checklist = []
            # double check
            for net in self.netlist:
                checklist.append(net.is_finished())
            
            if False in checklist:
                return False
            return True
        
        return False
    
    def get_output(self):
        """
        Hier zijn nog een aantal variabelen voor nodig, namelijk een lijst met nets, de chip en de netlist
        """
        with open("output.csv", 'w') as file:
            output = writer(file)
            output.writerow(["net", "wires"])

            for net in self.netlist:
                routelist = net.show_route_coordinates()
                output.writerow([net, f'"{routelist}"'])
            
            # writer.writerow([f"chip_{chip_id}_net_{net_id},{total_cost}"])