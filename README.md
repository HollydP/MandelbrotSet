# Area of the Mandelbrot Set
### Stochastic Simulations - Assignment 1
![Image](images/Mandelbrot%20zoom.png)

### Contributors
* Holly - 15055108
* Nina - 12896934
* Raphael - 14805367


## Table of Contents

* [Introduction](#introduction)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Licensing](#license)
* [Acknowledgements](#acknowledgements)

## Introduction
This project contains all code used to generate the results in the submitted report for the stochastic simulations course at UvA, assignment 1.
Finding the area of the Mandelbrot set is a challenging open problem, due to the finite precision of computers and the intricate border of the set.
The area of the Mandelbrot set is approached via three different sampling methods: random, latin hypercube and orthogonal. Convergence of the area is investigated for varying number of samples and iteration limits. In order to reduce variance, a stratified sampling method is employed. Next to being run in notebooks, simulations can be run via the CLI as well.

## Project Structure

* `/libraries/*`     -  All the classes and functions used to run simulations are in this folder.
    - `./methods.py` - contains the main area estimation class, `Mandelbrot`.
    - `./sampling_methods.py` - All the sampling functions for orthogonal, hypercube and random sampling. Used in `methods.py`
    - `./libraries/strata.py` - Static classes used for stratified sampling.
* `/data/*`   - All saved simulation data in csv files.
* `/images/*` - Contains all plots and images generated and saved for the report.
* `/notebooks/*` - Notebooks with data analysis and plots of simulation results
* `main.py`      - Used to run simulations via the CLI
* `requirements.txt` - Lists the required Python packages and their versions.


## Installation

1. Clone the repository:
```bash
git clone https://github.com/HollydP/MandelbrotSet.git
```
2. Navigate to the project root directory.
```
cd ./MandelbrotSet/
```
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage of CLA's

The simulations can be run and saved via the terminal.

Structure of command line argument:
```bash
python3 main.py method [--help] [-n N_samples] [-i ITERATIONS] [-s SIMULATIONS] [--symmetry] [--stratified] [--save]
```
`method` is the only mandatory argument and must be one of the following: [random, hypercube, orthogonal]

`-n` is used to pass the number of samples, must have an integer square root (default is 2500).

`-i` is the precision used when checking for convergence (default is 500 iterations).

`-s` number of simulations to run (default is 10).

`--symmetry` to exploit symmetry in the x-axis when estimating the area.

`--stratified` to enable stratified sampling (to reduce variance)

`--save` saves results in a csv-file in `./data/`.



### Example usage
Running and saving 10 simulations with stratified random sampling with 2500 samples and iteration limit of 500
```bash
python3 main.py random -n 2500 -i 500 -s 10 --save
```
After executing the simulations, main.py will print the mean area and the corresponding sample variance.
```
Area found using random sampling: 1.4918592
Variance: 0.0018081583103999972
```

Running and saving 50 simulations of stratified hypercube sampling with 4096 samples and iteration limit of 1000:
```bash
python3 main.py hypercube -n 4096 -i 1000 -s 10 --save
```

For a summary on the usage of main.py and its commandline arguments, run:
```bash
python3 main.py -h
```
## Licensing
This project is licensed under the [MIT License](LICENSE.md) - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

Code for the Mandlebrot visuals and Julia set images were adapted from [this report](https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f).
This code was accessed via its public repository on github: [Mandelbrot-Set](https://github.com/blakesanie/Mandelbrot-Set)
