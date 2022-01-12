import random
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from Dots_Objects import *

def CheckBoundaryLimits(x, y):
    if x > 100:
        x = 100
        person.vx = person.vx * -1
    if y > 100:
        y = 100
        person.vy = person.vy * -1
    if x < -100:
        x = -100
        person.vx = person.vx * -1
    if y < -100:
        y = -100
        person.vy = person.vy * -1
    return x, y


simlength = 7000 #
Boundary.x = 100
Boundary.y = 100
person = Dot()

# Initial x and y position
person.x = np.random.randint((-1 * Boundary.x), Boundary.y, 1)
person.y = np.random.randint((-1 * Boundary.x), Boundary.y, 1)

# Initial x and y velocity
person.vx, person.vy = np.random.uniform(-6, 6, 1), np.random.uniform(-6, 6, 1)

for i in range(simlength):
    new_x = person.x[-1] + person.vx
    new_y = person.y[-1] + person.vy
    new_x, new_y = CheckBoundaryLimits(new_x, new_y)

    person.x = np.append(person.x, new_x)
    person.y = np.append(person.y, new_y)


x_data = []
y_data = []

fig, ax = plt.subplots()
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
redDot, = ax.plot(person.x[0], person.y[0], "ro")

simlength = len(person.y)
print(len(person.y))
print(len(person.x))

def animation_frame(i):
    redDot.set_xdata(person.x[i])
    redDot.set_ydata(person.y[i])
    return redDot


animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, simlength, 1), interval=10)


plt.show()
