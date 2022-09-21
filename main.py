import matplotlib.pyplot as plt
import numpy as np
import math
from class_track import Track
from matplotlib.animation import PillowWriter
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from class_robot import Robot
import statistics as st

track = Track(sampling=4000)
robot = Robot(track)

res = True
while res:
    res = robot.delta_t_tick()

fps = int(len(robot.current_pos) / robot.total_time)
alphas = robot.get_alphas()

print("Time: ", robot.total_time)
print("Fps: ", fps)
print("Avg speed: ", st.mean(robot.v_hist))
print("Points: ", len(robot.current_pos))


fig, ax = plt.subplots(1, 1)


def animate(i):
    ax.clear()
    ax.plot(track.xs, track.ys, label="trajectory")
    try:
        ax.arrow(robot.current_pos[i][0], robot.current_pos[i][1], math.cos(alphas[i])*robot.v_hist[i], math.sin(alphas[i])*robot.v_hist[i], width=0.05, length_includes_head=True)
    except IndexError as e:
        pass
    ax.plot(robot.current_pos[i][0], robot.current_pos[i][1], color='red',
            label='original', marker='o')
    ax.set_xlim([0, 7])
    ax.set_ylim([-2, 2])


ani = FuncAnimation(fig, animate, frames=len(robot.current_pos),
                    repeat=False, interval=1)

writervideo = animation.FFMpegWriter(fps=fps)
ani.save("NoskovN_robot_run.mp4", writer=writervideo)

plt.show()
