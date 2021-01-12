class Crossing():
    def __init__(self, x_coordinate, y_coordinate, z_coordinate, grid_size):
        """
        Takes the coordinates of the crossing as input, all int, order: x, y, z, and the size of the grid as list [x, y, z]
        Creates a crossing object
        """

        self.name = None
        self.is_gate = False
        # Temporarily change self.location to list instead of tuple
        self.location = [x_coordinate, y_coordinate, z_coordinate]
        # self.location = (x_coordinate, y_coordinate, z_coordinate)
        self.directions = ['N', 'S', 'E', 'W', 'U', 'D']
        self.visited = False
        self.intersection = False

        self.set_directions(grid_size)

    def set_directions(self, grid_size):
        """
        Takes the grid_size as list as input ([x, y, z])
        At initialization, checks if crossing is at an edge and adjusts possible directions
        """
        
        # restrict possible directions in the x-directions (east and west)
        if self.location[0] == 0:
            self.directions.remove('W')
        elif self.location[0] == (grid_size[0] - 1):
            self.directions.remove('E')

        # rescrict possible directions in the y-directions (north and south)
        if self.location[1] == 0:
            self.directions.remove('N')
        elif self.location[1] == (grid_size[1] - 1):
            self.directions.remove('S')

        # rescrict possible directions in the z-directions (up and down)
        if self.location[2] == 0:
            self.directions.remove('D')
        elif self.location[2] == (grid_size[2] - 1):
            self.directions.remove('U')

    def __repr__(self):
        if self.name:
            return f"Gate-{self.name}"
        else:
            return "Nope"

    def place_gate(self, number):
        """
        Takes the number of the gate as string input
        Sets crossing to gate
        """

        self.is_gate = True
        self.name = number
    
    def add_blockade(self, direction):
        """
        Takes a letter that represents a direction (N,S,E,W,U or D)
        Removes that letter from the list of directions
        Returns false if location wasn't an option anyway
        """

        if direction in self.directions:
            self.directions.remove(direction)
            return True
        return False

    def remove_blockade(self, direction):
        """
        Takes a letter that represents a direction (N,S,E,W,U or D)
        Adds that latter back to the list
        """

        if direction no in self.directions:
            self.directions.append(direction)

    def set_visited(self):
        """
        Sets visited variable of crossing to true, if crossing was already visited, sets intersection to true
        Returns true if no intersection is created, else returns false (gates don't count as intersection)
        """

        if self.visited and not self.is_gate:
            self.intersection = True
            return False
        else:
            self.visited = True
            return True

    def get_coordinates(self):
        """
        Returns a list of crossings location
        """

        return self.location
    
    def get_possible_directions(self):
        """
        Returns a list of all possible direction you can go to from this crossing
        """
        
        return self.directions

    def get_name(self):
        """
        Returns the name of the crossing object
        """

        return self.name

