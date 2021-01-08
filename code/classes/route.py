class Route:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.routelist = []

        self.add_step()

    def add_step(self):
        for x in range(abs(int(self.start[0]) - int(self.end[0])) + 1):
            self.routelist.append((x, int(self.start[1])))
        
        difference = int(self.start[1]) - int(self.end[1]) + 1

        if difference < 0:
            for y in range(abs(difference)):
                self.routelist.append((int(self.end[0]), int(self.start[1]) - y))
        
        print(self.routelist)