from Dots_run import people, Boundary, num_people, simlength
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=np.inf)
print(people[0].infectionAreaTR[1])

reddots = []
x_data = []
y_data = []
fig2, ax2 = plt.subplots()
ax2.set_xlim(-Boundary.x, Boundary.x)
ax2.set_ylim(-Boundary.y, Boundary.y)
count = 4
for k in range(num_people):
    redDotTR, = ax2.plot(people[k].infectionAreaTR[0][0], people[k].infectionAreaTR[0][1], "bo",
                         markersize=5)
    redDotTL, = ax2.plot(people[k].infectionAreaTL[0][0], people[k].infectionAreaTL[0][1], "bo",
                         markersize=5)
    redDotBR, = ax2.plot(people[k].infectionAreaBR[0][0], people[k].infectionAreaBR[0][1], "bo",
                         markersize=5)
    redDotBL, = ax2.plot(people[k].infectionAreaBL[0][0], people[k].infectionAreaBL[0][1], "bo",
                         markersize=5)
    reddots.append(redDotTR)
    reddots.append(redDotTL)
    reddots.append(redDotBR)
    reddots.append(redDotBL)

def animation_frame(frame, s):
    for d in range(num_people):
        reddots[(0+s)].set_xdata(people[d].infectionAreaTR[frame][0])
        reddots[(0+s)].set_ydata(people[d].infectionAreaTR[frame][1])
        reddots[1+s].set_xdata(people[d].infectionAreaTL[frame][0])
        reddots[1+s].set_ydata(people[d].infectionAreaTL[frame][1])
        reddots[2+s].set_xdata(people[d].infectionAreaBR[frame][0])
        reddots[2+s].set_ydata(people[d].infectionAreaBR[frame][1])
        reddots[3+s].set_xdata(people[d].infectionAreaBL[frame][0])
        reddots[3+s].set_ydata(people[d].infectionAreaBL[frame][1])
        s = s + 4
    return reddots


s = 0
animation = FuncAnimation(fig2, func=animation_frame, frames=np.arange(0, simlength, 1), interval=10, fargs=(s,))

plt.show()
