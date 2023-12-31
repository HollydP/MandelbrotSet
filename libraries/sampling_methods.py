import numpy as np
from numpy import ndarray
import random

def pure_random_sampling(x_range, y_range, samples) -> ndarray[complex]:
    """
    Generates a list of complex numbers via pure random sampling.
    x_range (tuple) - (x_min, x_max) values of grid
    y_range (tuple) - (y_min, y_max) values of grid
    samples (int)   - number of samples to draw
    """
    # generate random x and y-coords
    x_samples = np.random.uniform(x_range[0], x_range[1], samples)
    y_samples = np.random.uniform(y_range[0], y_range[1], samples)
    paired_points = list(zip(x_samples, y_samples))

    # generate complex numbers
    complex_numbers = np.array([complex(a,b) for a, b in paired_points])

    return complex_numbers

def latin_hypercube_sampling(x_range: tuple, y_range: tuple, samples: int) -> ndarray[complex]:
    """
    Generate a list of complex numbers via hypercube sampling.
    x_range (tuple) - (x_min, x_max) values of grid
    y_range (tuple) - (y_min, y_max) values of grid
    samples (int)   - number of samples to draw
    """
    # generate grid
    x_points = list(np.linspace(x_range[0], x_range[1], samples))
    y_points = list(np.linspace(y_range[0], y_range[1], samples))

    # randomly pair up the x- and y-coords 
    x_samples = random.sample(x_points, k=samples)
    y_samples = random.sample(y_points, k=samples)
    paired_points = list(zip(x_samples, y_samples))

    # generate complex numbers from randomly paired points
    complex_numbers = np.array([complex(a,b) for a, b in paired_points])
    
    return complex_numbers

def orthogonal_sampling(x_range, y_range, samples) -> ndarray[complex]:
    """
    Generate a list of complex numbers via orthogonal sampling.

    - Seperate lattice into a number of subgrids.
    - In each subgrid randomly select a cell.
    - Make sure no cells share a common row or column with the cells selected in other subgrids.
    - Randomly select location within cell
    """
    # size of cell
    x_min, x_max = x_range
    y_min, y_max = y_range
    dx = (x_max-x_min)/(samples-1) # width
    dy = (y_max-y_min)/(samples-1) # height

    # create subgrids by index
    subspaces = int(np.sqrt(samples))

    # initilize list of selected points
    selected_x=[]
    selected_y=[]

    # loop through each subgrid and randomly choose a location from the remaining cells and columns
    for i in range(subspaces):
        for j in range(subspaces):

            options_x = range(i*subspaces,i*subspaces+subspaces)
            options_x = list(set(options_x).difference(set(selected_x)))
            selected_x.append(random.sample(options_x, k=1)[0])

            options_y = range(j*subspaces,j*subspaces+subspaces)
            options_y = list(set(options_y).difference(set(selected_y)))
            selected_y.append(random.sample(options_y, k=1)[0])

    # change lattice position to location in plane
    x_pos = x_min + np.array(selected_x)*dx
    y_pos = y_min +  np.array(selected_y)*dy
    paired_points = list(zip(x_pos,y_pos))

    complex_numbers = np.array([complex(a,b) for a, b in paired_points])

    return complex_numbers
