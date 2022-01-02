from objects import *
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def probs():
   y = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0]*10).round(0)*10)
   return y


infectiontime = 10
Numpeople = 1000
startinfectors = np.random.randint(1, Numpeople, 5)
SimNum = 160
people = []
infected = []
recovered = []

for n in range(Numpeople):
    people.append(Individual(probs(), 0))
for j in startinfectors:
    people[j].status = 1
count = 0
count2 = 0
for t in range(SimNum):
    for x in people:
        if x.status == 1:
            count = count + 1
    infected.append(count)
    if t > infectiontime:
        recoveredi = infected[-1] - infected[count2]
        recovered.append(recoveredi)
        count2 = count2 + 1

    for i in people:
        if i.status == 1:
            Numf = np.random.randint(1, Numpeople, i.friends)
            for o in Numf:
                if i.contagiousness > (np.random.randint(1, 1000, 1)):
                    people[o].status = 1
    count = 0
t = np.linspace(0, SimNum, SimNum)

differenceLen = len(infected) - len(recovered)
pad = infected[0:(infectiontime+1)]
recovered = pad + recovered
plt.plot(t, recovered)
plt.plot(t, infected)
recovered = np.array(infected) - np.array(recovered)



plt.show()