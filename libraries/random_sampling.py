import matplotlib.pyplot as plt
import numpy as np
import random

MAX_ITERATIONS = 100
SAMPLES = 10000

# A suitable amount of simulations in order to achieve a 5% standard deviation
SIMULATIONS = 100


def in_mandelbrot_set(complex_constant):
    """Check if complex_constant is in the Mandelbrot set."""

    z = complex(0,0)

    # Compute the quadratic map up to iteration_number iterations.
    for i in range(0, MAX_ITERATIONS):
        z = pow(z,2) + complex_constant
        # Check if the new sequence element z blows up.
        if abs(z) > 2:
            return False
    return True


def random_sampling_area():
        """Calculate the Mandelbrot set area with
        the pure random sampling method.
        """

        mandelbrot_set_size = 0

        # Calculate the amount of samples inside the Mandelbrot set.
        for i in range(0, SAMPLES):
            c = complex(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
            if in_mandelbrot_set(c):
                mandelbrot_set_size += 1
        
        # Calculate the area
        # The ratio between the inner and total samples must be multiplied
        # by the number of squares of area 1 we sampled on.
        area = 16 * (mandelbrot_set_size / SAMPLES)

        return area


def sample_standard_deviation(samples_values):
    """Calculate the sample standard deviation S."""

    # Calculate the sample variance (S^2).
    sample_variance = 0
    for i in range(0, len(samples_values)):
        sample_variance += pow(samples_values[i] - np.mean(samples_values), 2)
    sample_variance = sample_variance / (len(samples_values)-1)
    
    # The sample standard deviation is the square root of the sample variance.
    return np.sqrt(sample_variance)


def init_area_estimate():
     """Set the area estimate with a 5% standard deviation."""

     # Initialize the array containing the results A_i,s of all simulations.
     area_values = []
     for i in range(0, SIMULATIONS):
         area_values.append(random_sampling_area())
     return np.mean(area_values)
