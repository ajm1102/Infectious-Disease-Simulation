class Dot:
    def __init__(self):
        self.info = [0, 0, 0, 0]
        self.status = "Susceptible"
        self.infectionChance = 100
        self.infectionAreaTL = []
        self.infectionAreaTR = []
        self.infectionAreaBL = []
        self.infectionAreaBR = []

    @property
    def x(self):
        return self.info[0]

    @x.setter
    def x(self, x):
        self.info[0] = x

    @property
    def y(self):
        return self.info[1]

    @y.setter
    def y(self, y):
        self.info[1] = y

    @property
    def vx(self):
        return self.info[2]

    @vx.setter
    def vx(self, vx):
        self.info[2] = vx

    @property
    def vy(self):
        return self.info[3]

    @vy.setter
    def vy(self, vy):
        self.info[3] = vy

class Boundary:
    def __init__(self, maxY, maxX):
        self.x = maxX
        self.y = maxY
class virus:
    def __init__(self, initialinfected, infection_diameter, Tl, TR, BL, BR, ICM, dura, immune, deathchance):
        self.initialinfected = initialinfected
        self.infection_diameter = infection_diameter
        self.infectionChanceMod = ICM
        self.infectionduration = dura
        self.immune_wear = immune
        self.deathchance = deathchance
