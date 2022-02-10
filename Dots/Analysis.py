import json
from matplotlib import colors
from matplotlib.animation import FuncAnimation
from pymongo import MongoClient
from matplotlib.lines import Line2D
from Dots_run import persontrajectories
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import os


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
    # need tp add file index here to save all gifs
    # Writer = writers['pillow']
    # Writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    # animation.save("animation.gif", Writer)
    return


def animation_frame(frame, graph_dots, num_people, people, infected_record, new_sus, dead):
    # Each time this is called frame is incremented by one
    for d in range(num_people):
        # Check if the dot is dead by seeing if the colour is on the greyscale
        color = list(colors.to_rgb(graph_dots[d].get_color()))
        result = color.count(color[0]) == len(color)
        if sum(color) >= 2.94:
            continue

        # Moves the dot to the next position on the graph
        graph_dots[d].set_xdata(people[d].x[frame])
        graph_dots[d].set_ydata(people[d].y[frame])

        # Function to update the colours of each
        change_colours_animation(frame, graph_dots, people, infected_record, new_sus, dead, d, result)
        if result and sum(color) < 2.94:
            color = np.array(color) + 0.005
            graph_dots[d].set_color(tuple(color))

    return graph_dots


def change_colours_animation(frame, graph_dots, people, infected_record, new_sus, dead, d, result):
    #
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


# Works better with tableau
def writejsonold(num_infected, num_dead, num_recovered, t, sim_length, run_num):
    filename = "file.json"
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("InitialConditions.json") as f:
            data = json.load(f)
    else:
        with open(filename) as f:
            data = json.load(f)
    t = t.tolist()
    for i in range(sim_length):
        json_infected = {f"Time{run_num}": t[i], f"Dead{run_num}": num_dead[i], f"Infected{run_num}": num_infected[i],
                         f"Recovered{run_num}": num_recovered[i]}
        data['results'].append(json_infected)
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    # if data["Simulation_attempts"] == (run_num + 1):
    # mongodbUpload(data)
    return


def CreateId(data):
    # For this to work everything to be included in the ID must be placed before results in InitialConditions.json
    ids = ""
    for i in data:
        if i == "results":
            break
        ids = ids + "_" + str(data[i])
    ids = {"_id": ids}
    return ids


def writejson2(num_infected, num_dead, num_recovered, t, sim_length, run_num):
    filename = "file.json"
    try:
        with open(filename) as f:
            data = json.load(f)
    except FileNotFoundError:
        with open("InitialConditions.json") as f:
            data = json.load(f)
            ids = CreateId(data)
            data.update(ids)
    else:
        with open(filename) as f:
            data = json.load(f)
    for i in range(sim_length):
        if run_num > 0:
            data["results"][i]["Time"].append(t[i])
            data["results"][i]["Dead"].append(num_dead[i])
            data["results"][i]["Infected"].append(num_infected[i])
            data["results"][i]["Recovered"].append(num_recovered[i])
        else:
            json_infected = {"Time": [t[i]], "Dead": [num_dead[i]], "Infected": [num_infected[i]],
                             "Recovered": [num_recovered[i]]}
            data["results"].append(json_infected)

    with open(filename, "w") as f:
        json.dump(data, f, indent=3)
    if data["Simulation_attempts"] == (run_num + 1):
        mongodbUpload(data)
    return


def InterpolateFunc(t, num_infected):
    xnew = np.linspace(t.min(), t.max(), 150)
    power_smooth = make_interp_spline(t, num_infected)(xnew)
    return xnew, power_smooth


def mongodbUpload(data):
    cluster = MongoClient(f'mongodb+srv://ajm1102:{os.environ.get("ajm1102")}@cluster0.ruv0x.mongodb.net'
                          f'/myFirstDatabase?retryWrites '
                          '=true&w=majority')
    db = cluster["Infection_Simulations"]
    collection = db["Simulations"]
    collection.insert_one(data)
    return


def main(run_num):
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
            if virus1.deathchance > np.random.randint(0, 1000, 1) and person.status == "Infected":
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

        count_infected, count_recovered = 0, 0

    # animatedots(Boundary, num_people, people, simlength, infected_record, new_sus, dead)

    # plots time against num of infected people
    t = np.linspace(0, simlength - 1, simlength)
    # we use an interpolation function to make the plot smooth
    t_inter, num_infected_inter = InterpolateFunc(t, num_infected)
    plt.figure(2)
    plt.plot(t_inter, num_infected_inter)
    writejson2(num_infected, num_dead, num_recovered, t, simlength, run_num)
    return


def run():
    with open("InitialConditions.json") as f:
        data = json.load(f)
    return data["Simulation_attempts"]


if __name__ == "__main__":
    runtimes = run()
    for num in range(runtimes):
        found = True
        main(num)
    os.remove("file.json")
