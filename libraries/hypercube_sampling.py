# Estimates area of the mandelbrot set using latin hypercube sampling

import numpy as np

MAX_ITERS = 1000

def in_mandelbrot_set(c : complex) -> bool: 
    """
    Checks if complex number c is in Mandelbrot set.
    If z not diverged after MAX_ITERS, point lies in the set.
    Returns:
        (bool) - True if c in set, False otherwise
    """
    z = 0 
    iters = 0
    while iters < MAX_ITERS and abs(z) <= 2:
        z = z**2 + c 
        iters += 1
    return iters == MAX_ITERS


# ESTIMATING AREA VIA MONTE CARLO INTEGRATION

# Generate x amount of samples IN the MANDELBROT set via hypercube sampling?
#   - generate a [i, j] image/array of complex numbers between -2 - i and 1 + i (x coords between -2 and 1, y coords between -1 an 1)
#   - divide into an amount of regions
#   - generate a random point in each of the regions 
# calculate the area of the set using these points using monte carlo (A_(i,s) = (points in set)/(total_points) * A_of_image_or_array) 
# compare results and find convergence speed to the exact area (pixel counting?)


# generate a [i, j] image/array of complex numbers between -2 - i and 1 + i 
# (x coords between -2 and 1, y coords between -1 an 1)

HEIGHT = 10000
WIDTH = int(HEIGHT * (3/2))
POINTS = HEIGHT * WIDTH

x_min, x_max = (-2, 1)
y_min, y_max = (-1, 1)

x_points = np.linspace(x_min, x_max, WIDTH)
y_points = np.linspace(y_min, y_max, HEIGHT)

# generate complex numbers from x and y coordinates via 2-D hypercube sampling 

# divide x_points and y_points into 500 regions
regions = 500
x_points = x_points.reshape(regions, -1)
y_points = y_points.reshape(regions, -1)

# select random x_point and y_points from each region
points_per_region = x_points.shape[1]
random_x_indices = np.random.choice(np.arange(points_per_region), size=regions)
points_per_region = y_points.shape[1]
random_y_indices = np.random.choice(np.arange(points_per_region), size=regions)


random_x_points = x_points[np.arange(regions), random_x_indices]
random_y_points = y_points[np.arange(regions), random_y_indices]

# pair up the x_points and y_points randomly to generate random complex numbers 
np.random.shuffle(random_x_points)
np.random.shuffle(random_y_points)
paired_points = list(zip(random_x_points, random_y_points))

# generate complex numbers from the paired points
complex_numbers = np.array([complex(a,b) for a, b in paired_points])

# calculate the area of the set using these points using monte carlo 
# (A_(i,s) = (points in set)/(total_points) * A_of_image_or_array) 

# 1. count number of points in the set
boolean_arr = [in_mandelbrot_set(c) for c in complex_numbers]
points_in_set = np.sum(boolean_arr)

# 2. calculate approximated area
total_area = abs(x_min - x_max) * abs(y_min - y_max)
exact_area_mandelbrot = 1.50659
approximated_area_mandelbrot = total_area * points_in_set / len(boolean_arr)

print(approximated_area_mandelbrot)