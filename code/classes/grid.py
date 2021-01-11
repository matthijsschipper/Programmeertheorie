from .crossing import Crossing
from .route import Route
import numpy as np
import csv

class Grid():
    def __init__(self, infile):
        # from file, retrieve size of grid and locations of gates
        # create and initialize array
        self.read_data(infile)

    def read_data(self, infile):
        """
        Read data and call make_grid function
        """
        # Read gate coordinate data
        with open(infile, 'r') as new_file:
            data = [line.rstrip() for line in new_file]
            # Remove title
            data.pop(0)
        
        self.make_grid(data)

    def make_grid(self, data):
        """
        Determine max X and Y coordinates and store coordinates in list
        """
        x_coordinates = []
        y_coordinates = []
        self.coordinates = {}
        self.grid = []

        for coordinate in data:
            x_coordinates.append(int(coordinate[2]))
            y_coordinates.append(int(coordinate[4]))
            self.coordinates[int(coordinate[0])] = tuple(int(i) for i in coordinate[2:].split(','))
        
        max_x = max(x_coordinates) + 1
        max_y = max(y_coordinates) + 1

        for layer in range(8):
            layer_list = []
            self.grid.append(layer_list)
            for row in range(max_y + 1):
                row_list = []
                layer_list.append(row_list)
                for i in range(max_x + 1):
                    row_list.append(Crossing(i, row, layer))
        
        self.make_gates()
        
    def make_gates(self):
        for gate in self.coordinates.values():
            row_number = gate[1]
            col_number = gate[0]

            crossing = self.grid[0][row_number][col_number]
            crossing.place_gate('Gate')
        
        self.plot_route()
    
    def plot_route(self):
        start = self.coordinates[1]
        end = self.coordinates[3]

        Route(start, end)

        