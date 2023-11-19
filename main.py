import argparse
import numpy as np
from libraries.methods import Mandelbrot

def main(method, samples, iterations, simulations, symmetry, stratified, save):
    """
    Runs and saves simulations via the CLI.
    Usage:
    main.py [-h] [-n N_samples] [-i ITERATIONS] [-s SIMULATIONS] [--symmetry] [--stratified] method
    """

    # check valid argument
    if method not in ["random", "hypercube", "orthogonal"]:
        print("Mandatory argument 'method' must random, hypercube or orthogonal]")
        return 1
    
    # utilize symmetry of Mandlebrot if requested
    if symmetry == True:
        x_min, x_max = (-2, 0.6)
        y_min, y_max = (0, 1.2)
    else:
        x_min, x_max = (-2, 0.6)
        y_min, y_max = (-1.2, 1.2)

    Mandelbrot_Functions = Mandelbrot(method, samples, iterations, x_min, x_max, y_min, y_max)

    if stratified is True:
        mean_area, areas_found = Mandelbrot_Functions.stratified_estimation(simulations, save)
        print(f"Area found using stratified {method} sampling: {mean_area}")
    else:
        mean_area, areas_found = Mandelbrot_Functions.simulate(simulations, save)
        print(f"Area found using {method} sampling: {mean_area}")

    print("Variance:", np.var(areas_found, ddof=1))

    return

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="estimate mandelbrot area via sampling methods")

    # adding arguments
    parser.add_argument("method", help="sampling method to use")
    parser.add_argument("-n", help="number of samples", default=2500, type=int)
    parser.add_argument("-i", "--iterations", help="number of iterations", default=500, type=int)
    parser.add_argument("-s", "--simulations", help="number of simulations", default=10, type=int)
    parser.add_argument("--symmetry", action= "store_true",help="make use of the mandelbrot symmetry")
    parser.add_argument("--stratified", action="store_true", help="use stratified sampling to estimate area")
    parser.add_argument("--save", action="store_true", help="store results in csv")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.method, args.n, args.iterations, args.simulations, args.symmetry, args.stratified, args.save)