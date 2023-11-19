import os
import pandas as pd
import numpy as np
from numpy import ndarray

from libraries.sampling_methods import pure_random_sampling, latin_hypercube_sampling, orthogonal_sampling
from libraries.strata import StrataCollection

class Mandelbrot:
    
    """
    Contains all the required methods needed for calculating
    the Mandelbrot area.
    """

    def __init__(self, method, samples, iterations, x_min, x_max, y_min, y_max) -> None:
        """  
        Input and attributes:
        (str) method                - Sampling method
        (int) samples               - #samples generated, must be sqrtable
        (int) iterations            - precision of mandlebrot calc
        (int) simulations           - number of simulations to run
        (float, float) x_min, x_max - x-boundaries of the grid
        (float, float) y_min, y_max - y-boundaries of the grid
        (float) total_area          - area of the entire grid
        (func) sampling_function    - sampling method to be used
        """

        # does the sample have an integer square root 
        assert int(np.sqrt(samples))**2==samples

        self.method = method
        self.samples = samples
        self.max_iters = iterations

        self.x_range = (x_min, x_max)
        self.y_range = (y_min, y_max)
        self.total_area = abs(x_min - x_max) * abs(y_min - y_max)
        
        # select a sampling method
        sampling_dict = {
            "random"    : pure_random_sampling, 
            "hypercube" : latin_hypercube_sampling, 
            "orthogonal": orthogonal_sampling
            }
        self.sampling_function = sampling_dict[method]

    def in_mandelbrot_set(self, c: complex) -> bool: 
        """
        Returns true if complex number c in Mandelbrot set, else False.
        If z not diverged after max_iters, point lies in the set.
        """
        z = 0 
        iters = 0
        while iters < self.max_iters and abs(z) <= 2:
            z = z**2 + c 
            iters += 1
        return iters == self.max_iters

    def estimate_area(self, point_set: ndarray[complex]) -> float:
        """
        Estimates area of Mandelbrot set via Monte Carlo integration method.
        """
        boolean_arr = [self.in_mandelbrot_set(c) for c in point_set]
        points_in_set = np.sum(boolean_arr)
        return self.total_area * points_in_set / len(point_set)
    
    def simulate(self, simulations, save=True, return_samples=False):
        """
        Returns mean area and all estimations after N simulations.
        """
        areas_found = []
        samples_matrix = []
        for _ in range(simulations):
            samples_drawn = self.sampling_function(self.x_range, self.y_range, self.samples)
            estimated_area = self.estimate_area(samples_drawn)
            areas_found.append(estimated_area)
            
            if return_samples:
                samples_matrix.append(samples_drawn)

        # save to csv
        if save:
            self.save_to_csv(areas_found, simulations)

        if return_samples == False:
            return np.mean(areas_found), areas_found
        else:
            return np.mean(areas_found), areas_found, samples_matrix
    
    def stratified_estimation(self, simulations, save=True):
        """
        Estimates area by distributing samples across strata of differing importance.
        """
        Stratas = StrataCollection()
        areas = []
        for _ in range(simulations):
            areas.append(Stratas.estimate_area(self.samples, self.sampling_function, self.max_iters))
        
        if save:
            self.save_to_csv(
                areas,
                simulations,
                title=f"stratified for {self.method}_n{self.samples}_i{self.max_iters}_s{simulations}")
        return np.mean(areas), areas
    
    def save_to_csv(self, areas_found, simulations, title=None):
        """
        Saves the area estimations to csv file.
        """
        areas_df = pd.DataFrame(areas_found, columns=["Area"])
        if title:
            areas_df.to_csv(
            os.path.join("data",f"{title}.csv"), 
                index=False
            )
        else:
            areas_df.to_csv(
                os.path.join("data",f"Mandlebrot Area Simulations for {self.method} n{self.samples} s{simulations} i{self.max_iters}.csv"), 
                    index=False
                )  