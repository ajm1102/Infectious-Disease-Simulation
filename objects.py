import numpy as np
class Individual:

    def __init__(self, contagiousness, status):
        self.contagiousness = contagiousness
        self.status = status
        self.friends = np.random.randint(0, 5, 1)



