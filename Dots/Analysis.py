from Dots_run import people, Boundary, num_people, simlength
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt


def solve(bl, tr, p):
    if bl[0] < p[0] < tr[0] and bl[1] < p[1] < tr[1]:
        return True
    else:
        return False


def initial_infected():
    i_infected = 1
    count2 = 0
    while count2 < i_infected:
        people[count2].status = "Infected"
        count2 = count2 + 1
    return


def animatedots():
    reddots = []
    fig, ax = plt.subplots()
    ax.set_xlim(-Boundary.x, Boundary.x)
    ax.set_ylim(-Boundary.y, Boundary.y)
    for k in range(num_people):
        redDot, = ax.plot(people[k].x[0], people[k].y[0], "bo", markersize=5)
        reddots.append(redDot)
    animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, simlength, 1), interval=10, fargs=(
        reddots,))
    plt.show()
    return


def animation_frame(frame, reddots):
    reddots[0].set_color((0.1, 0.1, 0.1))
    for d in range(num_people):
        reddots[d].set_xdata(people[d].x[frame])
        reddots[d].set_ydata(people[d].y[frame])
        if d != 0:
            if frame == record[people[d]]:
                reddots[d].set_color((0.1, 0.1, 0.1))
    return reddots


initial_infected()
num_Infected = []
record = {}
count = 0

for i in range(simlength):
    for person in people:
        if person.status == "Infected":
            Susceptible = [person for person in people if "Susceptible" in person.status]
            for p_susceptible in Susceptible:
                in_area = solve(p_susceptible.infectionAreaBL[i], p_susceptible.infectionAreaTR[i],
                                [person.x[i], person.y[i]])
                if in_area:
                    if p_susceptible.infectionChance >= np.random.randint(0, 100, 1):
                        p_susceptible.status = "Infected"
                        record.update({p_susceptible: i})
    for it in people:
        if it.status == "Infected":
            count = count + 1
    num_Infected.append(count)
    count = 0
t = np.linspace(0, simlength, simlength)
plt.plot(t, num_Infected)
plt.show()