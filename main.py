# Contains all code to generate the images in the images folder, used in the report.
# Usage: python3 main.py
# Maybe we can add CLA's to run random/hypercube/orthogonal sampling etc.? 

import argparse
import matplotlib.pyplot as plt
import numpy as np
from libraries.methods import Mandelbrot

def main(method, samples, iterations, simulations, symmetry, plot, stratified):

    # Variance Reduction Technique - Reducing the area - Utilizes the fact the Mandlebrot is symmetric about the x axis
    # For the same number of simulations we should see a better convergence
    if symmetry == True:
        x_min, x_max = (-2, 1)
        y_min, y_max = (0, 1)
    else:
        x_min, x_max = (-2, 1)
        y_min, y_max = (-1, 1)

    Mandelbrot_Functions = Mandelbrot(method, samples, iterations, x_min, x_max, y_min, y_max)

    if stratified is True:
        mean_area, areas_found = Mandelbrot_Functions.stratified_estimation(simulations)
        print("Area found using stratified {} sampling: {}".format(method,mean_area))
        print(np.var(areas_found, ddof=1))
    else:
        mean_area, areas_found = Mandelbrot_Functions.simulate(simulations)
        print("Area found using {} sampling: {}".format(method,mean_area))
        print(np.var(areas_found, ddof=1))

    if plot:
        cumulative_mean_progression = np.cumsum(areas_found) / (np.arange(len(areas_found)) + 1)
        plt.plot(range(len(areas_found)), cumulative_mean_progression)
        plt.title("Convergence of estimated area")
        plt.xlabel("simulations")
        plt.ylabel("Area")
        plt.show()

    return

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="estimate mandelbrot area via sampling methods")

    # adding arguments
    parser.add_argument("method", help="sampling method to use")
    parser.add_argument("-n", help="number of samples", default=500, type=int)
    parser.add_argument("-i", "--iterations", help="number of iterations", default=10, type=int)
    parser.add_argument("-s", "--simulations", help="number of simulations", default=10, type=int)
    parser.add_argument("--symmetry", action= "store_true",help="make use of the mandelbrot symmetry")
    parser.add_argument("--plot", action="store_true", help="to show convergence of area in a plot")
    parser.add_argument("--stratified", action="store_true", help="use stratified sampling to estimate area")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.method, args.n, args.iterations, args.simulations, args.symmetry, args.plot, args.stratified)