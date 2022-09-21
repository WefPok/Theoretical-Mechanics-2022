import math
from scipy.misc import derivative
import numpy as np


class Track:
    def __init__(self, A=1, O_m=3, theta_0=0.2, sampling=4000):
        self.A = A
        self.O_m = O_m
        self.theta_0 = theta_0
        self.sampling = sampling

        self.xs = np.linspace(0, 4, self.sampling)
        self.ys = [self.trajectory(x) for x in self.xs]

        self.distances_from_zero = []

        diff_x = np.diff(self.xs)
        diff_y = np.diff(self.ys)
        for idx, x_to in enumerate(diff_x):
            temp = 0
            for idx1, x in enumerate(diff_x):
                if idx1 == idx:
                    break
                temp += math.sqrt(x ** 2 + diff_y[idx1] ** 2)
            self.distances_from_zero.append(temp)

    def trajectory(self, x):
        return self.A * math.sin(self.O_m * x + self.theta_0)

    def deriv(self, x, order=1):
        return derivative(self.trajectory, x, dx=0.01, n=order)

    def curvature_radius(self, x):
        return abs(((1 + (self.deriv(x) ** 2)) ** 1.5) / (self.deriv(x, 2)))
