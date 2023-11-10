import numpy as np
from numpy import ndarray
import random 
import pandas as pd

MAX_ITERS = 1000

class OrthogonalSampling:
    """
    Samples complex numbers via Latin Hypercube Sampling, in order to
    estimate area of the Mandelbrot Set.
    """

    def __init__(self, samples=1000, iterations = 500,simulations = 100) -> None:
        """
        (int) x_min, x_max, y_min, y_max - boundaries of the generated grid
        (float) total_area               - area of the entire grid
        (int) samples                    - #samples generated, must be even
        (1D-array) x_points              - points on the x axis
        (1D-array) y_points              - points on the y-axis
        """
        # Does the sample have an integer square root 
        assert int(np.sqrt(samples))**2==samples

        self.x_min, self.x_max = (-2, 1)
        self.y_min, self.y_max = (-1, 1)
        self.total_area = abs(self.x_min - self.x_max) * abs(self.y_min - self.y_max)

        self.samples = samples
        self.max_iters = iterations
        self.simulations= simulations

    def create_samples(self) -> ndarray[complex]:
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

        paired_points = list(zip(x_pos,random_y_pos))

        complex_numbers = np.array([complex(a,b) for a, b in paired_points])

        return complex_numbers
    
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

    def simulate(self) -> float:
        """
        Returns mean area after N iterations.
        """
        areas_found = [self.estimate_area(self.create_samples()) for _ in range(self.simulations)]
        areas_df = pd.DataFrame(areas_found,columns=["Area"])
        areas_df.to_csv("Mandlebrot Area Simulations for s{} i{}.csv".format(self.simulations,self.max_iters),index=False)

        return np.mean(areas_found), areas_found
    