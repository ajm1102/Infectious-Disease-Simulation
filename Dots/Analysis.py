import cProfile

from Dots_run import persontrajectories
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def checkinfectedneighbours(bl, tr, p):
    if bl[0] < p[0] < tr[0] and bl[1] < p[1] < tr[1]:
        return True
    else:
        return False


def initial_infected(virus1, people):
    i_infected = virus1.initialinfected
    recordf = {}
    count2 = 0
    while count2 < i_infected:
        people[count2].status = "Infected"
        recordf.update({people[count2]: [[0, virus1.infectionduration]]})
        count2 = count2 + 1
    return recordf


def animatedots(Boundary, num_people, people, simlength, record, new_sus):
    reddots = []
    fig, ax = plt.subplots()
    ax.set_xlim(-Boundary.x, Boundary.x)
    ax.set_ylim(-Boundary.y, Boundary.y)
    for k in range(num_people):
        redDot, = ax.plot(people[k].x[0], people[k].y[0], "bo", markersize=5)
        reddots.append(redDot)
    animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, simlength, 1), interval=0.11, fargs=(
        reddots, num_people, people, record, new_sus))
    plt.show()
    return


def animation_frame(frame, reddots, num_people, people, record, new_sus):
    for d in range(num_people):
        reddots[d].set_xdata(people[d].x[frame])
        reddots[d].set_ydata(people[d].y[frame])
        if record.get(people[d]):
            for change in record.get(people[d]):
                if frame == change[0]:
                    reddots[d].set_color((1, 0, 0))
                if frame == change[1]:
                    reddots[d].set_color((0, 1, 0))
        if new_sus.get(people[d]):
            for change in new_sus.get(people[d]):
                if frame == change:
                    reddots[d].set_color((0, 0, 1))
    return reddots

# dictionaries are used to store when people change state
def AddToDict(personobj, dict1, infof):

    if dict1.get(personobj):
        new = dict1.get(personobj)
        new.append(infof)
        s = {personobj: new}
        dict1.update(s)
    else:
        dict1.update({personobj: [infof]})
    return dict1

def main():
    num_people, simlength, people, virus1, Boundary = persontrajectories()

    dead = {}
    record = initial_infected(virus1, people)
    num_Infected = []
    new_sus = {}
    count = 0

    for i in range(simlength):
        for person in people:
            if person.status == "Infected":
                Susceptible = [person for person in people if "Susceptible" in person.status]
                for p_susceptible in Susceptible:
                    in_area = checkinfectedneighbours(p_susceptible.infectionAreaBL[i], p_susceptible.infectionAreaTR[i],
                                                      [person.x[i], person.y[i]])
                    if in_area:
                        if p_susceptible.infectionChance >= np.random.randint(0, 100, 1):
                            p_susceptible.status = "Infected"
                            recovertime = i + virus1.infectionduration
                            info = [i, recovertime]
                            record = AddToDict(p_susceptible, record, info)
            if person.status == "Recovered" and virus1.immune_wear >= np.random.randint(0, 10000, 1):
                person.status = "Susceptible"
                new_sus = AddToDict(person, new_sus, i)
            if person.status == "Infected":
                count = count + 1
                if record.get(person):
                    for infection in record.get(person):
                        if i == infection[1]:
                            person.status = "Recovered"

        num_Infected.append(count)
        count = 0
    t = np.linspace(0, simlength, simlength)
    animatedots(Boundary, num_people, people, simlength, record, new_sus)

    xnew = np.linspace(t.min(), t.max(), 150)
    power_smooth = make_interp_spline(t, num_Infected)(xnew)
    plt.figure(2)
    plt.plot(xnew, power_smooth)
    plt.figure(3)
    plt.plot(t, num_Infected)
    plt.show()

    return


if __name__ == "__main__":
    cProfile.run("main()", sort="tottime")

