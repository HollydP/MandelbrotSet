# Area of the Mandelbrot Set
### Stochastic Simulations - Assignment 1
Holly - , Nina - 12896934, Raphael -

## Table of Contents

* [Introduction](#introduction)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Project Summary](#project-summary)
* [Acknowledgements](#acknowledgements)

## Introduction
This project contains all code used to generate the results that can be found in the submitted report for the stochastic simulations course at UvA, assignment 1.

The area of the Mandelbrot set is approached via three different sampling methods: random, latin hypercube and orthogonal. Convergence of the area is investigated for varying number of samples and mandelbrot iterations. Finding the area of the Mandelbrot set is a challenging open problem, due to the finite precision of computers. In order to reduce variance, a stratified sampling method is employed.

## Project Structure

* `/libraries/*`     -  All the classes and functions used to run simulations in this folder.
    - `./methods.py` - The main area estimation class, `Mandelbrot`.
    - `./sampling_methods.py` - All the sampling functions for orthogonal, hypercube and random sampling. Used in `methods.py`
    - `./libraries/strata.py` - Static classes used for stratified sampling.
* `/data/*`   - All saved simulation data in csv files.
* `/images/*` - Plotted images of the Mandelbrot set and plots used in the report.
* `/notebooks/*` - Notebooks with data analysis and plots of simulation results
* `main.py`      - Code to run simulations via the CLI
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

The simulations can be run via the terminal.

Structure of command line argument:
```bash
python3 main.py method [--help] [-n N_samples] [-i ITERATIONS] [-s SIMULATIONS] [--symmetry] [--stratified] [--save]
```
`method` is the only mandatory argument and must be one of the following: [random, hypercube, orthogonal]

`-n` is used to pass the number of samples (default is 2500).

`-i` is the precision used when checking for convergence(default is 500 iterations).

`-s` number of simulations to run (default is 10).

`--symmetry` use symmetry in the x-axis when estimating the area.

`--stratified` use stratified sampling (to reduce variance)

`--save` saves results in a csv-file in `./data/`.

For a summary on the usage of main.py and its commandline arguments, run:
```bash
python3 main.py -h
```

### Example


## Project Summary

Summary of the results found? 


## Acknowledgements

The mandlebrot visuals and julia set images were inspired by the report 
https://medium.com/swlh/visualizing-the-mandelbrot-set-using-python-50-lines-f6aa5a05cf0f
This code was accessed via the public repository on github 
https://github.com/blakesanie/Mandelbrot-Set
- Author: Blake Sanie (2020)
