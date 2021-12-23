
class Individual:

    time = 0

    def __init__(self, location, status):
        self.location = location
        self.status = status
        self.time = 0
        self.removed = 0


class area:

    def __init__(self, people, probability, size):
        self.people = 100
        self.probability = 0
