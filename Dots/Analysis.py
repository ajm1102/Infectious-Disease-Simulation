import json
from matplotlib import colors
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from Dots_run import persontrajectories

import numpy as np
from scipy.interpolate import make_interp_spline


def checkinfectedneighbours(bl, tr, p):
    if bl[0] < p[0] < tr[0] and bl[1] < p[1] < tr[1]:
        return True
    else:
        return False


def initial_infected(virus1, people):
    i_infected = virus1.initialinfected
    infected_recordf = {}
    count2 = 0
    while count2 < i_infected:
        people[count2].status = "Infected"
        infected_recordf.update({people[count2]: [[0, virus1.infectionduration]]})
        count2 = count2 + 1
    return infected_recordf


def animatedots(Boundary, num_people, people, simlength, infected_record, new_sus, dead):
    # generates an empty plot with legend
    fig, ax = plt.subplots()
    ax.set_xlim(-Boundary.x, Boundary.x)
    ax.set_ylim(-Boundary.y, Boundary.y)
    legend_elements = [Line2D([0], [0], marker='o', color='w', label='Susceptible',
                              markerfacecolor=(0, 0, 1), markersize=5),
                       Line2D([0], [0], marker='o', color='w', label='Infected',
                              markerfacecolor=(1, 0, 0), markersize=5),
                       Line2D([0], [0], marker='o', color='w', label='Recovered',
                              markerfacecolor=(0, 1, 0), markersize=5),
                       Line2D([0], [0], marker='o', color='w', label='Dead',
                              markerfacecolor='k', markersize=5),
                       ]
    ax.legend(handles=legend_elements, loc='upper right')
    # dots are added to the graph in their initial state then added to a list
    graph_dots = []
    for k in range(num_people):
        graph_dot, = ax.plot(people[k].x[0], people[k].y[0], "bo", markersize=5)
        graph_dots.append(graph_dot)
    # animated plot calls the animation_frame function
    animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(0, simlength, 1), interval=0.11, fargs=(
        graph_dots, num_people, people, infected_record, new_sus, dead))
    plt.show()
    return


def animation_frame(frame, graph_dots, num_people, people, infected_record, new_sus, dead):
    # Each time this is called frame is incremented by one
    for d in range(num_people):
        # Check if the dot is dead by seeing if the colour is on the greyscale
        color = list(colors.to_rgb(graph_dots[d].get_color()))  # needs to be list so we can chang
        result = color.count(color[0]) == len(color)
        if sum(color) >= 2.94:
            continue

        # moves the dot to the next position on graph
        graph_dots[d].set_xdata(people[d].x[frame])
        graph_dots[d].set_ydata(people[d].y[frame])

        # Function to update the colours of each
        change_colours_animation(frame, graph_dots, people, infected_record, new_sus, dead, d, result)
        if result and sum(color) < 2.94:
            print(sum(color))
            color = np.array(color) + 0.005
            graph_dots[d].set_color(tuple(color))
    return graph_dots


def fade_along_gray_scale():
    return


def change_colours_animation(frame, graph_dots, people, infected_record, new_sus, dead, d, result):
    if dead.get(people[d]):
        for change in dead.get(people[d]):
            if frame == change:
                graph_dots[d].set_color((0, 0, 0))
    if infected_record.get(people[d]) and not result:
        for change in infected_record.get(people[d]):
            if frame == change[0]:
                graph_dots[d].set_color((1, 0, 0))
            if frame == change[1]:
                graph_dots[d].set_color((0, 1, 0))
    if new_sus.get(people[d]) and not result:
        for change in new_sus.get(people[d]):
            if frame == change:
                graph_dots[d].set_color((0, 0, 1))
    return


# dictionaries are used to store when people change state
def AddToDict(personobj, dict1, infof):
    # Appends to key if person is present in dict otherwise adds person and key
    if dict1.get(personobj):
        new = dict1.get(personobj)
        new.append(infof)
        s = {personobj: new}
        dict1.update(s)
    else:
        dict1.update({personobj: [infof]})
    return dict1


def writejson(num_infected, num_dead, num_recovered, t, sim_length):
    t = t.tolist()
    temp = []
    for i in range(sim_length):
        json_infected = [{"Time": t[i], "Dead": num_dead[i], "Infected": num_infected[i],
                          "Recovered": num_recovered[i]}, ]
        temp.append(json_infected)
    with open("file.json", "w") as f:
        # Write it to file
        json.dump(temp, f, indent=2)
    return


def InterpolateFunc(t, num_infected):
    xnew = np.linspace(t.min(), t.max(), 150)
    power_smooth = make_interp_spline(t, num_infected)(xnew)
    return xnew, power_smooth


def main():
    # function in dots_run.py file calculates paths of dots/people
    num_people, simlength, people, virus1, Boundary = persontrajectories()

    # dict stores when a person changes status
    infected_record = initial_infected(virus1, people)  # dict for infected requires an initial infection
    dead, new_sus = {}, {}
    # used to count number of people of a certain status and add to list each time frame
    num_infected, num_dead, num_recovered = [], [], []
    count_infected, count_dead, count_recovered = 0, 0, 0
    for i in range(simlength):
        for person in people:
            if virus1.deathchance >= np.random.randint(0, 1000, 1) and person.status == "Infected":
                person.status = "Dead"
                dead = AddToDict(person, dead, i)
                count_dead = count_dead + 1
            if person.status == "Infected":
                Susceptible = [person for person in people if "Susceptible" in person.status]
                for p_susceptible in Susceptible:
                    # finds if the susceptible person is close enough to be become infected
                    in_area = checkinfectedneighbours(p_susceptible.infectionAreaBL[i],
                                                      p_susceptible.infectionAreaTR[i], [person.x[i], person.y[i]])
                    if in_area:
                        if p_susceptible.infectionChance >= np.random.randint(0, 100, 1):
                            p_susceptible.status = "Infected"
                            recovertime = i + virus1.infectionduration
                            info = [i, recovertime]
                            infected_record = AddToDict(p_susceptible, infected_record, info)
            if person.status == "Infected":
                count_infected = count_infected + 1
                if infected_record.get(person):
                    for infection in infected_record.get(person):
                        if i == infection[1]:
                            person.status = "Recovered"
            if person.status == "Recovered" and virus1.immune_wear >= np.random.randint(0, 10000, 1):
                person.status = "Susceptible"
                new_sus = AddToDict(person, new_sus, i)
            if person.status == "Recovered":
                count_recovered = count_recovered + 1
        num_infected.append(count_infected)
        num_dead.append(count_dead)
        num_recovered.append(count_recovered)
        count_infected = 0
        count_recovered = 0
        count_dead = 0
    animatedots(Boundary, num_people, people, simlength, infected_record, new_sus, dead)

    # plots time against num of infected people
    t = np.linspace(0, simlength - 1, simlength)
    # we use an interpolation function to make the plot smooth
    t_inter, num_infected_inter = InterpolateFunc(t, num_infected)
    plt.figure(2)
    plt.plot(t_inter, num_infected_inter)
    plt.figure(3)
    plt.plot(t, num_dead)
    plt.show()

    writejson(num_infected, num_dead, num_recovered, t, simlength)
    return


if __name__ == "__main__":
    main()
