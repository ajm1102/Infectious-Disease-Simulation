from objects import *
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def probs():
   y = int((norm.rvs(size=1, loc=0.5, scale=0.15)[0]*10).round(0)*10)
   return y


initialinfected = 1
infectionchance = 280
infectiontime = 8
Numpeople = 500
SimNum = 200
immuneWear = 1

people = []
Totalinfected = []
immune = []
startinfectors = np.random.randint(1, Numpeople, initialinfected)
for index in range(Numpeople):
    if index in startinfectors:
        people.append(Individual(probs(), 1))
    else:
        people.append(Individual(probs(), 0))
count = 0
count2 = 0
count3 = 0
for t in range(SimNum):
    for x in people:
        if x.status == 3:
            count3 = count3 + 1
            if np.random.randint(0, 1000, 1) < immuneWear:
                print("Spnt")
                x.status = 1
        if x.status == 1:
            count = count + 1
    Totalinfected.append(count)
    immune.append(count3)
    if count < 1:
        SimNum = t + 1
        break
    if t > infectiontime:
        RanRecovered = np.random.randint(1, Numpeople, Totalinfected[count2])
        for z in RanRecovered:
            people[z].status = 3
        count2 = count2 + 1
    for i in people:
        if i.status == 1:
            Numf = np.random.randint(1, Numpeople, i.friends)
            for o in Numf:
                if people[o].status != 3 and people[o].status != 1:
                    if i.contagiousness > (np.random.randint(1, infectionchance, 1)):
                        people[o].status = 1
    count = 0
    count3 = 0
print(sum(Totalinfected))
print(sum(immune))

time = np.linspace(0, SimNum, SimNum)
plt.plot(time, immune)
plt.plot(time, Totalinfected)

plt.show()
