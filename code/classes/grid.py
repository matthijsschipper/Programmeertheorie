from .crossing import Crossing
from .route import Route
import numpy as np
import csv

class Grid():
    """
    Grid class makes an object of a 3D matrix, which is filled with Crossing objects.
    """
    def __init__(self, infile):
        # from file, retrieve size of grid and locations of gates
        # create and initialize array
        self.grid = []
        self.coordinates = {}
        self.x_coordinates = []
        self.y_coordinates = []
        self.read_data(infile)

    def read_data(self, infile):
        """
        Read data and call make_grid function.
        """
        # Read gate coordinate data
        with open(infile, 'r') as new_file:
            data = [line.rstrip() for line in new_file]
            # Remove title
            data.pop(0)
        
        self.make_grid(data)

    def make_grid(self, data):
        """
        Determine Grid size via max x and y values of gate coordinates.
        """
        for coordinate in data:

            # Add x and y coordinates to separate lists
            self.x_coordinates.append(int(coordinate[2]))
            self.y_coordinates.append(int(coordinate[4]))

            # Add gate nr as key and gate coordinates (as tuple) to dictionary
            self.coordinates[int(coordinate[0])] = tuple(int(i) for i in coordinate[2:].split(','))
        
        # Determine maximum values
        max_x = max(self.x_coordinates) + 1
        max_y = max(self.y_coordinates) + 1

        # Create 3D matrix with found size
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
        """
        Retrieve Crossing objects from 3D matrix at coordinates of gates and edit name.
        """
        for gate in self.coordinates.values():
            row_number = gate[1]
            col_number = gate[0]

            crossing = self.grid[0][row_number][col_number]
            crossing.place_gate('Gate')
        
        self.plot_route()
    
    def plot_route(self):
        """
        Plot route with given start and end coordinates (might prove to be not necessary later?).
        """
        start = self.coordinates[1]
        end = self.coordinates[3]

        Route(start, end)

        