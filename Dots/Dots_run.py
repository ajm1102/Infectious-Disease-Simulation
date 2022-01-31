import numpy as np
from Dots_Objects import *
import json
import cProfile


# Changes x and y coordinates and velocity direction if they outside a rectangle
def CheckBoundaryLimits(x, y, person):
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


# Calculate a rectangles coordinates around a point
def InfectionArea(new_x, new_y, infection_diameter, person):
    AreaCoordTR = [new_x + infection_diameter, new_y + infection_diameter]
    AreaCoordTL = [new_x + infection_diameter, new_y - infection_diameter]
    AreaCoordBR = [new_x - infection_diameter, new_y + infection_diameter]
    AreaCoordBL = [new_x - infection_diameter, new_y - infection_diameter]
    person.infectionAreaTR.append(AreaCoordTR)
    person.infectionAreaTL.append(AreaCoordTL)
    person.infectionAreaBR.append(AreaCoordBR)
    person.infectionAreaBL.append(AreaCoordBL)
    return


def createvirus():
    with open("InitialConditions.json") as f:
        data = json.load(f)
    # Added virus class to allow the addition of variants
    # Chance to be infected will be combination of a persons susceptibility and virus effectiveness
    virus_chance = 100  # does nothing only dot class chance works

    infection_diameter = data["infection_diameter"]
    initialinfected = data["initialinfected"]
    infection_duration = data["infection_duration"]
    immune_wear = data["immune_wear"]
    deathchance = data["deathchance"]
    num_people = data["Number_people"]
    createdvirus = virus(initialinfected, infection_diameter, [], [], [], [], virus_chance, infection_duration,
                         immune_wear, deathchance)
    return createdvirus, num_people


def persontrajectories():
    virus1, num_people = createvirus()
    people = []
    simlength = 1000
    Boundary.x = 200
    Boundary.y = 200
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
            new_x, new_y = CheckBoundaryLimits(new_x, new_y, person)
            InfectionArea(new_x, new_y, virus1.infection_diameter, person)
            person.x = np.append(person.x, new_x)
            person.y = np.append(person.y, new_y)
        people.append(person)

    return num_people, simlength, people, virus1, Boundary
