# Estimates area of the mandelbrot set using latin hypercube sampling

import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt 
import random 

# ESTIMATING AREA VIA MONTE CARLO INTEGRATION WITH HYPERCUBE SAMPLING

# generate complex numbers from x and y coordinates via 2-D hypercube sampling 
#   - generate a [i x j] image/array of complex numbers between -2 - i and 1 + i (x coords between -2 and 1, y coords between -1 an 1)
#   - divide x_coords and y_coords into ... sections
#   - select a random x and y point in each of the sections
#   - pair up the selected x and y points randomly to create a set of complex numbers
# calculate the area of the set using these points using monte carlo 
#    - A_(i,s) = (points in set)/(total_points) * A_of_entire_grid 
# compare results and find convergence speed to the exact area

MAX_ITERS = 1000

class HypercubeSampling:
    """
    Samples complex numbers via Latin Hypercube Sampling in order to
    estimate area of the Mandelbrot Set.
    """

    def __init__(self, samples=500) -> None:
        """
        (int) x_min, x_max, y_min, y_max - boundaries of the generated grid
        (float) total_area               - area of the entire grid
        (int) samples                    - #samples generated, must be even
        (1D-array) x_points              - points on the x axis
        (1D-array) y_points              - points on the y-axis
        """
        self.x_min, self.x_max = (-2, 1)
        self.y_min, self.y_max = (-1, 1)
        self.total_area = abs(self.x_min - self.x_max) * abs(self.y_min - self.y_max)

        self.samples = samples

        self.x_points = list(np.linspace(self.x_min, self.x_max, samples))
        self.y_points = list(np.linspace(self.y_min, self.y_max, samples))

    def create_samples(self) -> ndarray[complex]:
        """
        Generate a list of complex numbers via hypercube sampling.
        """
        # randomly pair up the x- and y-samples 
        self.x_samples = random.sample(self.x_points, k=self.samples)
        self.y_samples = random.sample(self.y_points, k=self.samples)
        paired_points = list(zip(self.x_samples, self.y_samples))

        # generate complex numbers from randomly paired points
        complex_numbers = np.array([complex(a,b) for a, b in paired_points])
        
        return complex_numbers
    
    def in_mandelbrot_set(self, c: complex) -> bool: 
        """
        Returns true if complex number c in Mandelbrot set, else False.
        If z not diverged after MAX_ITERS, point lies in the set.
        """
        z = 0 
        iters = 0
        while iters < MAX_ITERS and abs(z) <= 2:
            z = z**2 + c 
            iters += 1
        return iters == MAX_ITERS

    def estimate_area(self, point_set: ndarray[complex]) -> float:
        """
        Estimates area of Mandelbrot set via Monte Carlo integration method.
        """
        boolean_arr = [self.in_mandelbrot_set(c) for c in point_set]
        points_in_set = np.sum(boolean_arr)
        return self.total_area * points_in_set / len(point_set)

    def iterate(self, iterations: int = 20) -> float:
        """
        Returns mean area after N iterations.
        """
        areas_found = [self.estimate_area(self.create_samples()) for _ in range(iterations)]
        return np.mean(areas_found)
    
    def simulate(self, simulations: int = 50) -> float:
        """
        Returns mean area after N simulations
        """
        areas_found = [self.iterate() for _ in range(simulations)]
        return np.mean(areas_found), areas_found
    
LHS = HypercubeSampling()
mean_area, areas_found = LHS.simulate()
print(mean_area)

cumulative_mean_progression = np.cumsum(areas_found) / (np.arange(len(areas_found)) + 1)
plt.plot(range(len(areas_found)), cumulative_mean_progression)
plt.show()
