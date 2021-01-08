class Crossing():
    def __init__(self, x_coordinate, y_coordinate, z_coordinate):
        self.location = (x_coordinate, y_coordinate, z_coordinate)
        self.links = []
        self.is_gate = False
        self.name = None
        
    def place_gate(self, number):
        """
        Add gate to crossing.
        """
        self.is_gate = True
        self.name = number
    
    def create_link(self, adjacent_crossing):
        """
        Create link between current and adjacent crossing.
        """
        paths.append((adjacent_crossing))
    
    def get_links(self):
        """
        Returns list of linked crossings
        """
        return(self.links)

    def __repr__(self):
        return f'Crossing - {self.name}'

