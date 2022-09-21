import matplotlib.pyplot as plt
from class_robot import Robot
from class_track import Track
import numpy as np
a_t_max = 10
a_n_max = 10
v_max = 1.5

track = Track(sampling=4000)
robot = Robot(track)

res = True
while res:
    res = robot.delta_t_tick()

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5, 5)
ax.set_xlabel('time, s')


time = np.linspace(0, robot.total_time, len(robot.current_pos))

# ax.plot(track.xs, track.ys, color="red", label="Trajectory")
# ax.plot([x[0] for x in robot.current_pos], robot.a_n_hist, color="green", label="a_n")
# ax.plot([x[0] for x in robot.current_pos], robot.a_t_hist, color="blue", label="a_t")
# ax.plot([x[0] for x in robot.current_pos], robot.v_hist, color="orange", label="v")

ax.plot(time, robot.a_n_hist, color="green", label="a_n")
ax.plot(time, robot.a_t_hist, color="blue", label="a_t")
ax.plot(time, robot.v_hist, color="orange", label="v")
ax.plot(time, [x[1] for x in robot.current_pos], color="red", label="Y")


ax.legend()
plt.show()
fig.savefig('NoskovNikita_graphs(t).png')
