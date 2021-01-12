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

    def get_latest_crossings(self):
        """
        Returns the last two crossing objects in the routelist as a list, order: last, second-to-last
        """

        return [self.routelist[-1], self.routelist[-2]]
    
    def delete_last_crossing(self):
        """
        Deletes the last crossing from the route
        """

        self.routelist = del(self.routelist[-1])

    def show_route(self):
        """
        Returns all crossing objects, in order, that have been added to the net
        """

        return self.routelist

    def show_route_coordinates(self):
        """"
        Returns the coordinates of all the loactions in the net as a list of tuples
        """

        coordinate_list= []
        for crossing in self.routelist:
            coordinates = crossing.get_coordinates()
            coordinate_list.append(tuple(coordinates))
        return coordinate_list
            

    def get_end(self):
        """
        Returns the crossing object of the end of the net
        """

        return self.end

    def get_start(self):
        """
        Returns the crossing object at the start of the net
        """

        return self.start
    
    def get_route_to_end(self):
        """
        Returns the amount of steps still needed in a certain direction as a list, order: x, y, z
        If net is finished, returns None
        """

        if self.finished == True:
            return None

        # save the coordinates of all relevant crossings
        current_crossing = self.routelist[-1]
        current_location = current_crossing.get_coordinates()
        destination = self.end.get_coordinates()

        # calculate the distance in each direction
        # y direction is times minus one to account for indexing
        x_distance = destination[0] - current_location[0]
        y_distance = (destination[1] - current_location[1]) * (-1)
        z_distance = destination[2] - current_location[2]

        return [x_distance, y_distance, z_distance]

    def is_finished(self):
        """
        Returns true if path is finished, else false
        """

        return self.finished

    def get_length(self):
        """
        Returns an int of the length of the route so far
        """

        return len(self.routelist)

    # def add_step(self):
    #     """
    #     Connect start and end points, store all steps taken in routelist.
    #     If the difference is negative, it means the x/y value should increase.
    #     Example:
        
    #     start = (1,5)
    #     end = (4,4)
    #     x_difference = 1 - 4 = -3

    #     x needs to increase with all values in range(3 + 1)

    #     Example necessary?
    #     """
    #     # Calculate width difference
    #     x_difference = self.start[0] - self.end[0]

    #     # Loops runs with length of found difference + 1
    #     for x in range(abs(x_difference) + 1):
    #         # Negative difference requires addition
    #         if x_difference < 0:
    #             self.routelist.append((self.start[0] + x, self.start[1]))
    #             continue

    #         # Else difference is positive, requires subtraction
    #         self.routelist.append((self.start[0] - x, self.start[1]))
        
    #     # Same steps apply for y route
    #     y_difference = self.start[1] - self.end[1]

    #     for y in range(1, abs(y_difference) + 1):
    #         if y_difference < 0:
    #             self.routelist.append((self.end[0], self.start[1] + y))
    #             continue

    #         self.routelist.append((self.end[0], self.start[1] - y))

    #     print(self.routelist)