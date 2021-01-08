import csv
from matplotlib import pyplot as plt

def visualise(infile):
    with open(infile) as file:

        # read through file
        reader = csv.reader(file)
        data = list(reader)
    
    print(data)
    return None