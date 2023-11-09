import numpy as np
from numpy import ndarray
import random 

MAX_ITERS = 1000

class OrthogonalSampling:
    """
    Samples complex numbers via Latin Hypercube Sampling, in order to
    estimate area of the Mandelbrot Set.
    """

    def __init__(self, samples=1000) -> None:
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

    def create_samples(self) -> ndarray[complex]:
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