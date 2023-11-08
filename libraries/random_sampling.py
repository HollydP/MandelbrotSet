import matplotlib.pyplot as plt
import numpy as np
import random


def in_mandelbrot_set(complex_constant, iteration_number):
    """Check if complex_constant is in the Mandelbrot set."""

    z = complex(0,0)

    # Compute the quadratic map up to iteration_number iterations.
    for i in range(0,iteration_number):
        z = pow(z,2) + complex_constant
        # Check if the new sequence element z blows up.
        if abs(z) > 2:
            return False
    return True


def random_sampling_area(sample_number, iteration_number):
        """Calculate the Mandelbrot set area with
        the pure random sampling method.
        """

        mandelbrot_set_size = 0

        # Calculate the amount of samples inside the Mandelbrot set.
        for i in range(0,sample_number):
            c = complex(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
            if in_mandelbrot_set(c, iteration_number):
                mandelbrot_set_size += 1
        
        # Calculate the area
        # The ratio between the inner and total samples must be multiplied
        # by the number of squares of area 1 we sampled on.
        area = 16 * (mandelbrot_set_size / sample_number)

        return area


MAX_ITERATIONS = 100
SAMPLES = 10000


print(random_sampling_area(SAMPLES, MAX_ITERATIONS))
