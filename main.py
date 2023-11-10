# Contains all code to generate the images in the images folder, used in the report.
# Usage: python3 main.py
# Maybe we can add CLA's to run random/hypercube/orthogonal sampling etc.? 

import argparse
import random
import matplotlib.pyplot as plt
import numpy as np
from libraries.methods import Mandelbrot, Sampling

# from libraries.hypercube_sampling import HypercubeSampling
# from libraries.orthogonal_sampling import OrthogonalSampling

def main(method, samples, iterations, simulations, plot):
    # random.seed(0)

        Mandelbrot_Functions = Mandelbrot(method, samples, iterations, simulations)
        mean_area, areas_found = Mandelbrot_Functions.simulate()
        print("Area found using {} sampling: {}".format(method,mean_area))

        if plot:
            cumulative_mean_progression = np.cumsum(areas_found) / (np.arange(len(areas_found)) + 1)
            plt.plot(range(len(areas_found)), cumulative_mean_progression)
            plt.title("Convergence of estimated area")
            plt.xlabel("simulations")
            plt.ylabel("Area")
            plt.show()

        return

# def main(method, samples, iterations, simulations, plot):
#     # random.seed(0)

#     if method == "random":
#         pass

#     elif method == 'hypercube':

#         LatinHypercubic = HypercubeSampling(samples)
#         mean_area, areas_found = LatinHypercubic.simulate(simulations, iterations)
#         print(f"Area found using hypercubic sampling: {mean_area}")

#         if plot:
#             cumulative_mean_progression = np.cumsum(areas_found) / (np.arange(len(areas_found)) + 1)
#             plt.plot(range(len(areas_found)), cumulative_mean_progression)
#             plt.title("Convergence of estimated area")
#             plt.xlabel("simulations")
#             plt.ylabel("Area")
#             plt.show()

#     elif method == "orthogonal":
#         Orthogonal = OrthogonalSampling(samples,iterations,simulations)
#         mean_area, areas_found = Orthogonal.simulate()
#         print(f"Area found using Orthogonal sampling: {mean_area}")

#         if plot:
#             cumulative_mean_progression = np.cumsum(areas_found) / (np.arange(len(areas_found)) + 1)
#             plt.plot(range(len(areas_found)), cumulative_mean_progression)
#             plt.title("Convergence of estimated area")
#             plt.xlabel("simulations")
#             plt.ylabel("Area")
#             plt.show()
    
#     else:
#         print("Error: Command must be one of the following: [random, hypercube, orthogonal]")
#         return

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="estimate mandelbrot area via sampling methods")

    # adding arguments
    parser.add_argument("method", help="sampling method to use")
    parser.add_argument("-n", help="number of samples", default=500, type=int)
    parser.add_argument("-i", "--iterations", help="number of iterations", default=10, type=int)
    parser.add_argument("-s", "--simulations", help="number of simulations", default=10, type=int)
    parser.add_argument("--plot", action="store_true", help="to show convergence of area in a plot")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.method, args.n, args.iterations, args.simulations, args.plot)