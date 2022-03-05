# Infection-population-Models

The code above is simulation of a infections disease. The people are represted as dots that are spawned randomly in cartesian cordinates inside a bound rectangle. Each dot also spawns with a x and y velocity, allowing the dot to move as a vector with a random magnitude and direction. This all happens in the dots_run file where the paths of each dot is calculated and stored in a object as a list of x and y positions. A list of these objects is created to represnt multiple people moveing around the inside the bound rectangle.

Each dot has status parameter of one of the following "Suceptible", "Infected", "Immune", "Dead" these statuses determine how each dot interacts with its neigbours. Susceptible can be infected, infected becomes immune after a period of time while having a chance to become dead. A square area is drawn around each dot that is specified with given initial diamter. If a suceptible dot lies in this region of a infected dot the infection will have a chance to spread. This is calaculed in the analysi file

The initial conditions for this program are storesd in json. This file contains the dimensions for the rectangle how mant are 
https://towardsdatascience.com/simulating-the-pandemic-in-python-2aa8f7383b55
