import matplotlib.pyplot as plt

from objects import *
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def probs():
   y = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0]*10).round(0)*10)
   return y


Numpeople = 1000
startinfectors = np.random.randint(1, Numpeople, 1)
SimNum = 15

people = []
infected = []

for n in range(Numpeople):
    people.append(Individual(probs(), 0))

for j in startinfectors:
    people[j].status = 1

count = 0

for t in range(SimNum):
    for x in people:
        if x.status == 1:
            count = count + 1
    infected.append(count)
    for i in people:
        if i.status == 1:
            Numf = np.random.randint(1, Numpeople, i.friends)
            for o in Numf:
                if i.contagiousness > (np.random.randint(1, 100, 1)):
                    people[o].status = 1

    count = 0

t = np.linspace(0, SimNum, SimNum)

plt.plot(t, infected)
plt.show()
print(infected)
