# Contains all code to generate the images in the images folder, used in the report.
# Usage: python3 main.py
# Maybe we can add CLA's to run random/hypercube/orthogonal sampling etc.? 

import argparse
import random
import matplotlib.pyplot as plt
import numpy as np
from libraries.methods import Mandelbrot

def main(method, samples, iterations, simulations, symmetry, plot):
    # random.seed(0)

    # Variance Reduction Technique - Reducing the area - Utilizes the fact the Mandlebrot is symmetric about the x axis
    # For the same number of simulations we should see a better convergence
    if symmetry == True:
        x_min, x_max = (-2, 0.6)
        y_min, y_max = (0, 1.2)
    else:
        x_min, x_max = (-2, 0.6)
        y_min, y_max = (-1.2, 1.2)

    convergence = [[],[],[]]
    ci = [[],[],[]] # 1-sigma error bars for the data of each method
    # The convergence is computed for each sampling method
    methods_list = ['random', 'hypercube', 'orthogonal']

    Mandelbrot_Functions = Mandelbrot(method, samples, iterations, x_min, x_max, y_min, y_max)
    area_estimate = 1.5058492800000003
    area_estimate_std = np.sqrt(1.8655279476363516e-05)
    simulation_number_area_estimate = 100


    print(f'Area estimate = {area_estimate} | with method = {method}')

    if plot == 'i_convergence':
        for method in methods_list: 
            print(f'CURRENTLY USING {method} SAMPLING METHOD.')
            Mandelbrot_Functions = Mandelbrot(method, samples, iterations, x_min, x_max, y_min, y_max)
            # We save the sets of samples in a matrix. The area_estimate is our reference A_{M}
            samples_matrix = Mandelbrot_Functions.simulate(simulations)[2]

            k = 2
            x = [10]
            while k <= np.log10(iterations):
                x.append(int((10**k)/2))
                x.append(10**k)
                k += 1

            area_values = []
            error_bars = []
            # The areas are computed over the samples sets with different amount of iterations.
            for i in x:
                print(f'Iterations = {i}')
                Mandelbrot_Functions.max_iters = i
                area_sample_vector = []
                # Areas are computed for each samples sets (there are a simulations amount of samples sets)
                for j in range(0, len(samples_matrix)):
                    area_sample_vector.append(Mandelbrot_Functions.estimate_area(samples_matrix[j]))
                area_sample = np.mean(area_sample_vector) # We obtain A_{i,s}.
                print(f'Mean area for current simulation: {area_sample} ')
                area_values.append(area_sample)
                # Each computed area A_{i,s} is compared to the one obtained with the most iterations (A_{M})
                convergence[methods_list.index(method)].append(abs(area_sample - area_estimate))

                area_sample_std = Mandelbrot_Functions.sample_standard_deviation(area_sample_vector)
                error_bars.append(area_sample_std)
            
            plt.figure(1)
            plt.errorbar(x, area_values, yerr=error_bars, capsize=5, marker='.',markersize=10, label=method)

            plt.figure(2)
            plt.plot(x,convergence[methods_list.index(method)], marker='.',markersize=10, label=method)


        # Error band for the area_estimate
        ci_min = area_estimate - (1.96*np.sqrt(area_estimate_std)/np.sqrt(simulation_number_area_estimate))
        ci_max = area_estimate + (1.96*np.sqrt(area_estimate_std)/np.sqrt(simulation_number_area_estimate))

        plt.figure(1)
        plt.axhline(y = area_estimate, color = 'r', linestyle = ':', label = "$A_{i,s}$") 
        plt.axhspan(ci_min, ci_max, color = 'r', alpha=.1)
        plt.legend()
        plt.xlabel('Iterations', fontsize=12)
        plt.ylabel(r'$A_{j,s}$', fontsize=12)

        plt.figure(2)
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Iterations', fontsize=12)
        plt.ylabel(r'$A_{j,s}$', fontsize=12)

        plt.show()

  
    elif plot == 's_convergence':
        print("SAMPLES PLOT")
        for method in methods_list: 
            print(f'CURRENTLY USING {method} SAMPLING METHOD.')

            # The array x contains all the samples values that will be tested
            p = 30
            x = []
            while p**2 < samples:
                x.append(p**2)
                p += 5
            
            Mandelbrot_Functions = Mandelbrot(method, samples, iterations, x_min, x_max, y_min, y_max)
            convergence[methods_list.index(method)], ci[methods_list.index(method)] = Mandelbrot_Functions.samples_convergence(simulations, area_estimate, area_estimate_std, x)
           
           # The values needed for creating the confidence interval band are stored in ci_min and ci_max
            ci_min = []
            ci_max = []
            for i in range(0, len(x)):
                ci_min.append(convergence[methods_list.index(method)][i] - ci[methods_list.index(method)][i])
                ci_max.append(convergence[methods_list.index(method)][i] + ci[methods_list.index(method)][i])

            plt.plot(x,convergence[methods_list.index(method)],marker='.',markersize=10, label=method)
            plt.fill_between(x, ci_min, ci_max, alpha=.1)

        plt.legend()
        plt.xlabel('Samples', fontsize=12)
        plt.ylabel(r'$|A_{j,s} - A_{i,s}|$', fontsize=12)
        plt.show()
    
    return


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="estimate mandelbrot area via sampling methods")

    # adding arguments
    parser.add_argument("method", help="sampling method to use", default="orthogonal")
    parser.add_argument("-n", help="number of samples", default=2500, type=int)
    parser.add_argument("-i", "--iterations", help="number of iterations", default=1000, type=int)
    parser.add_argument("-s", "--simulations", help="number of simulations", default=20, type=int)
    parser.add_argument("--symmetry", action= "store_true",help="make use of the mandelbrot symmetry", default=False)
    parser.add_argument("--plot", action="store_true", help="which figure to plot: i_convergence, s_convergence", default="s_convergence")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.method, args.n, args.iterations, args.simulations, args.symmetry, args.plot)
