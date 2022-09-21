import math

from class_track import Track
import numpy as np


def getClosest(val1, val2, target):
    if target - val1 >= val2 - target:
        return val2
    else:
        return val1


def findClosest(arr, n, target):
    if target <= arr[0]:
        return arr[0]
    if target >= arr[n - 1]:
        return arr[n - 1]
    i = 0
    j = n
    mid = 0
    while i < j:
        mid = (i + j) // 2
        if arr[mid] == target:
            return arr[mid]
        if target < arr[mid]:

            if mid > 0 and target > arr[mid - 1]:
                return getClosest(arr[mid - 1], arr[mid], target)
            j = mid
        else:
            if mid < n - 1 and target < arr[mid + 1]:
                return getClosest(arr[mid], arr[mid + 1], target)

            i = mid + 1
    return arr[mid]


class Robot:
    def __init__(self, track: Track, v_max=1.5, a_t_max=10, a_n_max=6):

        self.track = track

        self.v_max = v_max
        self.a_t_max = a_t_max
        self.a_n_max = a_n_max

        self.v_hist = [0]
        self.v = 0

        self.a_t = 0
        self.a_t_hist = [0]

        self.a_n = 0
        self.a_n_hist = [0]

        self.total_time = 0

        self.current_distance = 0
        self.current_pos = [[0, 0.19]]

        self.delta_t = 0.01

        self.counter = 0

    def get_alphas(self):
        alphas = []
        v_x = np.diff([x[0] / self.delta_t for x in self.current_pos])
        v_y = np.diff([x[1] / self.delta_t for x in self.current_pos])
        for i in range(len(v_x)):
            alphas.append(math.atan(v_y[i] / v_x[i]))
        return alphas

    def speed(self):
        self.v_hist.append(self.v)

        stopping_dst = self.v_max / self.a_t_max * self.v_max / 2

        if self.track.distances_from_zero[-1] - self.current_distance <= stopping_dst:
            final_velocity = self.v - self.a_t_max * self.delta_t
        else:
            possible_velocities = np.linspace(0, 1.5, 150)

            resulting_a_ns = [v ** 2 / self.track.curvature_radius(self.current_pos[-1][0]) for v in
                              possible_velocities]

            if any(i >= self.a_n_max for i in resulting_a_ns):
                for idx, a_n in enumerate(resulting_a_ns):
                    if a_n > self.a_n_max:
                        break
                    temp_idx = idx
                final_velocity = possible_velocities[temp_idx]
            else:
                final_velocity = self.v + self.a_t_max * self.delta_t

        self.v = final_velocity
        if self.v > self.v_max:
            self.v = self.v_max
        if self.v < 0:
            self.v = 0
        return self.v

    def t_acceleration(self):
        prev_v = self.v
        curr_v = self.speed()
        self.a_t_hist.append((curr_v - prev_v) / self.delta_t)

    def n_acceleration(self):
        self.a_n = self.v ** 2 / self.track.curvature_radius(self.current_pos[-1][0])
        self.a_n_hist.append(self.a_n)

    def dist_to_coords(self, current_distance):
        idx = self.track.distances_from_zero.index(
            findClosest(self.track.distances_from_zero, len(self.track.distances_from_zero), current_distance))
        return [self.track.xs[idx], self.track.ys[idx]]

    def update_pos(self):

        temp_dst = self.current_distance + self.v * self.delta_t

        self.current_distance = temp_dst
        self.current_pos.append(self.dist_to_coords(self.current_distance))
        # if self.counter > 1 and self.current_pos[-1][0] == self.track.xs[-2]:
        #     return "Break"
        if self.v == 0:
            return "Break"
        return 0

    def delta_t_tick(self):
        self.counter += 1
        # print("Robot Position: ", self.current_pos[-1][0], self.current_pos[-1][1])

        self.t_acceleration()
        self.n_acceleration()

        res = self.update_pos()
        self.total_time += self.delta_t
        if res == "Break":
            self.t_acceleration()
            self.n_acceleration()
            self.update_pos()
            return False
        else:
            return True
