class Route:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.routelist = []

        self.add_step()

    def add_step(self):
        x_difference = self.start[0] - self.end[0]

        for x in range(abs(x_difference) + 1):
            if x_difference < 0:
                self.routelist.append((self.start[0] + x, self.start[1]))
                continue

            self.routelist.append((self.start[0] - x, self.start[1]))
        
        y_difference = self.start[1] - self.end[1]

        for y in range(1, abs(y_difference) + 1):
            if y_difference < 0:
                self.routelist.append((self.end[0], self.start[1] + y))
                continue

            self.routelist.append((self.end[0], self.start[1] - y))

        print(self.routelist)