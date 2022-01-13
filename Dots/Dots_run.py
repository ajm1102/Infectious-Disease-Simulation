from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from Dots_Objects import *

def CheckBoundaryLimits(x, y):
    if x > Boundary.x:
        x = Boundary.x
        person.vx = person.vx * -1
    if y > Boundary.y:
        y = Boundary.y
        person.vy = person.vy * -1
    if x < -Boundary.x:
        x = -Boundary.x
        person.vx = person.vx * -1
    if y < -Boundary.y:
        y = -Boundary.y
        person.vy = person.vy * -1
    return x, y


people = []
num_people = 25
simlength = 7000
Boundary.x = 50
Boundary.y = 100

for j in range(num_people):
    person = Dot()
    # Initial x and y position
    person.x = np.random.randint((-1 * Boundary.x), Boundary.y, 1)
    person.y = np.random.randint((-1 * Boundary.x), Boundary.y, 1)
    # Initial x and y velocity
    person.vx, person.vy = np.random.uniform(-2, 2, 1), np.random.uniform(-2, 2, 1)

    for i in range(simlength):
        new_x = person.x[-1] + person.vx
        new_y = person.y[-1] + person.vy
        new_x, new_y = CheckBoundaryLimits(new_x, new_y)

        person.x = np.append(person.x, new_x)
        person.y = np.append(person.y, new_y)
    people.append(person)

reddots = []
x_data = []
y_data = []

fig, ax = plt.subplots()
ax.set_xlim(-Boundary.x, Boundary.x)
ax.set_ylim(-Boundary.y, Boundary.y)
for k in range(num_people):
    redDot, = ax.plot(people[k].x[0], people[k].y[0], "bo", markersize=20)
    reddots.append(redDot)


def animation_frame(frame):
    for d in range(num_people):
        reddots[d].set_xdata(people[d].x[frame])
        reddots[d].set_ydata(people[d].y[frame])
    return reddots


animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, simlength, 1), interval=10)


plt.show()
