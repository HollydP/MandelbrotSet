import numpy as np

def in_mandelbrot_set(c: complex, max_iters) -> bool: 
    """
    Returns true if complex number c in Mandelbrot set, else False.
    If z not diverged after MAX_ITERS, point lies in the set.
    """
    z = 0 
    iters = 0
    while iters < max_iters and abs(z) <= 2:
        z = z**2 + c 
        iters += 1
    return iters == max_iters

class Strata:
    """Represents a strata with an importance factor."""

    def __init__(self, x_range, y_range, weight) -> None:
        assert x_range[0] < x_range[1] and y_range[0] < y_range[1]
        self.x_range = x_range
        self.y_range = y_range
        self.total_area = abs(x_range[1] - x_range[0]) * abs(y_range[1] - y_range[0])
        self.importance = weight
        self.num_samples = None
    
    def set_num_samples(self, samples):
        self.num_samples = samples
    
    def add_sample(self, number):
        self.num_samples += number

    def estimate_area(self, sampling_func, max_iters):
        assert self.num_samples
        complex_samples = sampling_func(self.x_range, self.y_range, self.num_samples)
        boolean_arr = np.array([in_mandelbrot_set(sample, max_iters) for sample in complex_samples])
        return self.total_area * sum(boolean_arr)/len(boolean_arr)


class StrataCollection:
    """Represents grid of strata with each strata some samples."""
    def __init__(self) -> None:
        self.strata = []
        self.create_empty_strata()
        # sort strata by importance
        self.strata = sorted(self.strata, key=lambda x: x.importance, reverse=True)
    
    def distribute_samples(self, samples):
        [strata.set_num_samples(int(samples*strata.importance)) for strata in self.strata]

        # add remaining samples to stratum with highest importance
        remaining_samples = samples - sum(strata.num_samples for strata in self.strata)
        self.strata[0].add_sample(remaining_samples)

        # confirm all samples are used
        assert samples == sum(strata.num_samples for strata in self.strata)

    def create_empty_strata(self):
        # un-interesting strata (weight=0.01)
        weight=0.01
        self.strata = [
            Strata((-0.5, 0.2), (0, 0.45), weight),
            Strata((-2, -1.75), (0.45, 1.2), weight),
            Strata((-1.3, -0.8), (0, 0.2), weight),
            Strata((-0.7, -0.5), (0, 0.2), weight),
            Strata((-0.6, -0.5), (0.2, 0.4), weight)
        ]

        # Interesting strata (weight = 0.05)
        weight=0.05
        self.strata.append(Strata((-2, -1.3), (0, 0.2), weight))
        self.strata.append(Strata((-0.8, -0.7), (0, 0.2), weight))
        self.strata.append(Strata((0.2, 0.6), (0, 0.45), weight))
        self.strata.append(Strata((0.1, 0.6), (0.45, 0.7), weight))
        self.strata.append(Strata((-0.35, 0.1), (0.45, 1.2), weight))
        self.strata.append(Strata((-0.7, -0.35), (0.45, 0.8), weight))
        self.strata.append(Strata((-0.6, -0.5), (0.4, 0.45), weight))
        self.strata.append(Strata((-0.8, -0.6), (0.2, 0.45), weight))
        self.strata.append(Strata((-1.4, -0.8), (0.2, 0.45), weight))

        # in between (weight = 0.03)
        weight=0.03
        self.strata.append(Strata((0.1, 0.6), (0.7, 1.2), weight))
        self.strata.append(Strata((-0.7, -0.35), (0.8, 1.2), weight))
        self.strata.append(Strata((-1.75, -0.7), (0.45, 1.2), weight))
        self.strata.append(Strata((-2, -1.4), (0.2, 0.45), weight))
        assert abs(sum([strata.total_area for strata in self.strata]) - 2.6*1.2) <= 0.001
         
    def estimate_area(self, samples, sampling_func, max_iters):
        self.distribute_samples(samples)
        area = sum([strata.estimate_area(sampling_func, max_iters) for strata in self.strata])
        return area * 2