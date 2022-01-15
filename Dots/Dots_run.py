import numpy as np
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
def InfectionArea():
    AreaCoordTR = [new_x + infection_diameter, new_y + infection_diameter]
    AreaCoordTL = [new_x + infection_diameter, new_y - infection_diameter]
    AreaCoordBR = [new_x - infection_diameter, new_y + infection_diameter]
    AreaCoordBL = [new_x - infection_diameter, new_y - infection_diameter]
    person.infectionAreaTR.append(AreaCoordTR)
    person.infectionAreaTL.append(AreaCoordTL)
    person.infectionAreaBR.append(AreaCoordBR)
    person.infectionAreaBL.append(AreaCoordBL)
    return


infection_diameter = 3
people = []
num_people = 100
simlength = 1000
Boundary.x = 100
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
        InfectionArea()
        person.x = np.append(person.x, new_x)
        person.y = np.append(person.y, new_y)
    people.append(person)
