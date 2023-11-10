import matplotlib.pyplot as plt
import numpy as np
from numpy import ndarray
import random

class Mandelbrot:
    """
    Contains all the required methods needed for calculating
    the Mandelbrot area.
    """

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


class Sampling:
    """
    Contains the different sampling methods.
    """

    def pure_random_sampling(self) -> ndarray[complex]:
        """
        Generates a list of complex numbers via pure random sampling.
        """
        complex_numbers = []
        for i in range(0,500):
            complex_numbers.append(complex(random.uniform(Mandelbrot.x_min, Mandelbrot.x_max), random.uniform(Mandelbrot.y_min, Mandelbrot.y_max)))

        return complex_numbers
    

    def __init_hypercube__(self, samples=500) -> None:
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


    def latin_hypercube_sampling(self) -> ndarray[complex]:
        """
        Generate a list of complex numbers via hypercube sampling.
        """

        # initialize the grid
        Mandelbrot.__init__(Mandelbrot)

        # randomly pair up the x- and y-coords 
        self.x_samples = random.sample(Mandelbrot.x_points, k=Mandelbrot.samples)
        self.y_samples = random.sample(Mandelbrot.y_points, k=Mandelbrot.samples)
        paired_points = list(zip(self.x_samples, self.y_samples))

        # generate complex numbers from randomly paired points
        complex_numbers = np.array([complex(a,b) for a, b in paired_points])
        
        return complex_numbers
    

    def __init_orthogonal__(self, samples=1000) -> None:
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
   

    def orthogonal_sampling(self) -> ndarray[complex]:
        """
        Generate a list of complex numbers via orthogonal sampling.
        """
        dx = (self.x_max-self.x_min)/(self.samples-1)
        dy = (self.y_max-self.y_min)/(self.samples-1)

        subspaces = int(np.sqrt(self.samples))
        blocks = {(i,j):[(a,b) for a in range(i*subspaces,i*subspaces+subspaces) for b in range(j*subspaces,j*subspaces+subspaces)] 
                for i in range(subspaces) for j in range(subspaces)}

        selected_row=[]
        selected_col=[]
        for i in range(subspaces):
            for j in range(subspaces):
                # print(i,j)
                n=m=np.nan
                match = False

                while match == False:
                    (n,m) = random.sample(blocks[(i,j)], k=1)[0]
                    if n not in selected_row:
                        if m not in selected_col:
                            print(n,m)
                            selected_row.append(n)
                            selected_col.append(m)
                            match = True

        selected_row = self.x_min + np.array(selected_row)*dx
        selected_col = self.y_min +  np.array(selected_col)*dy
        paired_points = list(zip(selected_row,selected_col))

        complex_numbers = np.array([complex(a,b) for a, b in paired_points])

        return complex_numbers
    

