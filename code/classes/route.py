class Route:
    """
    Route class searches for routes between start and end points
    by making the x and y values of start and end points the same
    and storing all steps taken.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.routelist = []

        self.add_step()

    def add_step(self):
        """
        Connect start and end points, store all steps taken in routelist.
        If the difference is negative, it means the x/y value should increase.
        Example:
        
        start = (1,5)
        end = (4,4)
        x_difference = 1 - 4 = -3

        x needs to increase with all values in range(3 + 1)

        Example necessary?
        """
        # Calculate width difference
        x_difference = self.start[0] - self.end[0]

        # Loops runs with length of found difference + 1
        for x in range(abs(x_difference) + 1):
            # Negative difference requires addition
            if x_difference < 0:
                self.routelist.append((self.start[0] + x, self.start[1]))
                continue

            # Else difference is positive, requires subtraction
            self.routelist.append((self.start[0] - x, self.start[1]))
        
        # Same steps apply for y route
        y_difference = self.start[1] - self.end[1]

        for y in range(1, abs(y_difference) + 1):
            if y_difference < 0:
                self.routelist.append((self.end[0], self.start[1] + y))
                continue

            self.routelist.append((self.end[0], self.start[1] - y))

        print(self.routelist)