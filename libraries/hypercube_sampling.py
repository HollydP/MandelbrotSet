import numpy as np
from numpy import ndarray
import random 

MAX_ITERS = 1000

class HypercubeSampling:
    """
    Samples complex numbers via Latin Hypercube Sampling, in order to
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
        # randomly pair up the x- and y-coords 
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
    
    def simulate(self, simulations: int = 50, iterations: int = 20) -> float:
        """
        Returns mean area after N simulations
        """
        areas_found = [self.iterate(iterations) for _ in range(simulations)]
        return np.mean(areas_found), areas_found
    