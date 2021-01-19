from .crossing import Crossing

class Net:
    def __init__(self, start, end):
        """
        Takes the crossing-objects of the startgate and endgate of a route as input
        Creates a route object
        """

        self.start = start
        self.end = end
        self.routelist = [self.start]
        self.finished = False

    def __repr__(self):
        return f"{self.start},{self.end}"

    def add_crossing(self, crossing):
        """
        Takes a crossing object as input
        Adds crossing to net
        """

        self.routelist.append(crossing)

        # check if this is the end of the route
        if crossing == self.end:
            self.finished = True

    def get_latest_crossing(self):
        """
        Returns the last crossing object in the routelist
        """

        return self.routelist[-1]

    def get_latest_two_crossings(self):
        """
        Returns the last two crossing objects in the routelist as a list, order: last, second-to-last
        """

        return [self.routelist[-1], self.routelist[-2]]
    
    def delete_last_crossing(self):
        """
        Deletes the last crossing from the route
        """

        self.routelist.pop()

    def show_route_coordinates(self):
        """"
        Returns the coordinates of all the loactions in the net as a list of tuples
        """

        coordinate_list= []
        for crossing in self.routelist:
            coordinates = crossing.location
            coordinate_list.append(tuple(coordinates))
        return coordinate_list
             
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

        # calculate the distance in each direction
        # y direction is times minus one to account for indexing
        x_distance = destination[0] - current_location[0]
        y_distance = (destination[1] - current_location[1]) * (-1)
        z_distance = destination[2] - current_location[2]

        return [x_distance, y_distance, z_distance]

    def mark_unfinished(self):
        """
        Marks net unfinished
        """

        self.finished = False

    def get_length(self):

        """
        Returns an int of the length of the route so far
        """

        return len(self.routelist) - 1

    def reverse(self):
        """
        Reverses the start and the end of a net
        """

        start = self.start
        self.start = self.end
        self.end = start
        self.routelist  = [self.start]