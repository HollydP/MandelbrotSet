import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
import pandas as pd
import random
import os

class Mandelbrot:
    """
    Contains all the required methods needed for calculating
    the Mandelbrot area.
    """
    def __init__(self, method, samples, iterations, simulations, x_min, x_max, y_min, y_max) -> None:
        """
        (str) method                     - Sampling method
        (int) samples                    - #samples generated, must be sqrtable
        (int) iterations                 - precision of mandlebrot calc
        (int) simulations                - number of simulations to run

        (float) total_area               - area of the entire grid
        """

        # Does the sample have an integer square root 
        assert int(np.sqrt(samples))**2==samples

        self.method = method
        self.samples = samples
        self.max_iters = iterations
        self.simulations= simulations

        self.x_min, self.x_max = (x_min, x_max)
        self.y_min, self.y_max = (y_min, y_max)
        self.total_area = abs(self.x_min - self.x_max) * abs(self.y_min - self.y_max)

    def in_mandelbrot_set(self, c: complex) -> bool: 
        """
        Returns true if complex number c in Mandelbrot set, else False.
        If z not diverged after MAX_ITERS, point lies in the set.
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
    
    def sampling_func(self):

        SamplingMethods = Sampling(self.samples,self.x_min, self.x_max,self.y_min, self.y_max)

        sampling_dict = {"random":SamplingMethods.pure_random_sampling(),
                             "hypercube":SamplingMethods.latin_hypercube_sampling(),
                             "orthogonal":SamplingMethods.orthogonal_sampling()}
        
        return sampling_dict[self.method]
    
    def simulate(self) -> float:
        """
        Returns mean area after N iterations.
        """

        # Sampling dict should call the sampling function and output the correct complex numbers based on the method (not sure this works)
        areas_found = [self.estimate_area(self.sampling_func()) for _ in range(self.simulations)]
        areas_df = pd.DataFrame(areas_found,columns=["Area"])
        areas_df.to_csv(os.path.join("data","Mandlebrot Area Simulations for {} n{} s{} i{}.csv".format(self.method,self.samples,self.simulations,self.max_iters)),index=False)

        return np.mean(areas_found), areas_found


class Sampling:
    """
    Contains the different sampling methods.
    """

    def __init__(self, samples, x_min, x_max, y_min, y_max) -> None:
        """
        (int) x_min, x_max, y_min, y_max - boundaries of the generated grid
        (int) samples                    - #samples generated, must be even
        (1D-array) x_points              - points on the x axis
        (1D-array) y_points              - points on the y-axis
        """

        self.x_min, self.x_max = (x_min, x_max)
        self.y_min, self.y_max = (y_min, y_max)

        self.samples = samples
    
    def pure_random_sampling(self) -> ndarray[complex]:
        """
        Generates a list of complex numbers via pure random sampling.
        """
        # complex_numbers = []
        # for i in range(0,self.samples):
        #     complex_numbers.append(complex(random.uniform(self.x_min, self.x_max), random.uniform(self.y_min, self.y_max)))

        # Generate Random x and y-coords
        x_samples = np.random.uniform(self.x_min, self.x_max,self.samples)
        y_samples = np.random.uniform(self.y_min, self.y_max,self.samples)
        paired_points = list(zip(x_samples, y_samples))

        # generate complex numbers
        complex_numbers = np.array([complex(a,b) for a, b in paired_points])

        return complex_numbers
    
    def latin_hypercube_sampling(self) -> ndarray[complex]:
        """
        Generate a list of complex numbers via hypercube sampling.
        """
        # # initialize the grid
        # Mandelbrot.__init__(Mandelbrot)

        x_points = list(np.linspace(self.x_min, self.x_max, self.samples))
        y_points = list(np.linspace(self.y_min, self.y_max, self.samples))

        # randomly pair up the x- and y-coords 
        self.x_samples = random.sample(x_points, k=self.samples)
        self.y_samples = random.sample(y_points, k=self.samples)
        paired_points = list(zip(self.x_samples, self.y_samples))

        # generate complex numbers from randomly paired points
        complex_numbers = np.array([complex(a,b) for a, b in paired_points])
        
        return complex_numbers

    def orthogonal_sampling(self) -> ndarray[complex]:
        """
        Generate a list of complex numbers via orthogonal sampling.

        - Seperate lattice into a number of subgrids.
        - In each subgrid randomly select a cell.
        - Make sure no cells share a common row or column with the cells selected in other subgrids.
        - Randomly select location within cell
        """
        # Size of cell
        dx = (self.x_max-self.x_min)/(self.samples-1) # width
        dy = (self.y_max-self.y_min)/(self.samples-1) # height

        # Create subgrids by index
        subspaces = int(np.sqrt(self.samples))
        blocks = {(i,j):[(a,b) for a in range(i*subspaces,i*subspaces+subspaces) for b in range(j*subspaces,j*subspaces+subspaces)] 
                for i in range(subspaces) for j in range(subspaces)}

        # Initilize arrays to keep track of which rows and cells have been selected
        selected_row=[]
        selected_col=[]

        # Loop through each subgrid so all subgrids have 1 sample
        for i in range(subspaces):
            for j in range(subspaces):
                # print(i,j)
                n=m=np.nan
                match = False

                # Randomly select a cell within subgrid
                while match == False:
                    (n,m) = random.sample(blocks[(i,j)], k=1)[0]
                    # check row and column of cell is different from previously selected cells
                    if n not in selected_row:
                        if m not in selected_col:
                            selected_row.append(n)
                            selected_col.append(m)
                            match = True

        # Convert index to location on the plane
        # each point describes the centre of a cell
        x_pos = self.x_min + np.array(selected_row)*dx
        y_pos = self.y_min +  np.array(selected_col)*dy

        # # randomize to a point within cell
        # random_x_pos =  x_pos + np.random.uniform(-1,1,self.samples)*dx/2
        # random_y_pos = y_pos  + np.random.uniform(-1,1,self.samples)*dy/2

        paired_points = list(zip(x_pos,y_pos))

        complex_numbers = np.array([complex(a,b) for a, b in paired_points])

        return complex_numbers
    

