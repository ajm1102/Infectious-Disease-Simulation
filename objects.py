import numpy as np
class Individual:

    time = 0

    def __init__(self, contagiousness, status):
        self.contagiousness = contagiousness
        self.status = status
        self.time = 0
        self.removed = 0
        self.friends = np.random.randint(0, 6, 1)



