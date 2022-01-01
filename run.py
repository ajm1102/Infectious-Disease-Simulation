import matplotlib.pyplot as plt
from objects import *
import numpy as np

from objects import *
import numpy as np
import matplotlib.pyplot as plt
Numpeople = 100
SimNum = 1000
people = []
susceptible = []
infected = []
count = 0
# infected = [x for x in range(100) if people[x].status == 1]
for n in range(Numpeople):
    people.append(Individual(0, 0))
while Individual.time < SimNum:
    susceptible = np.random.randint(1, Numpeople, 1)
    for i in susceptible:
        if people[i].status == 0:
            people[i].status = 1
            count = count + 1

    infected.append(count)
    Individual.time = Individual.time + 1

plt.plot(np.linspace(0, Numpeople, SimNum), infected)
plt.show()



