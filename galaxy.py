import planet


class Galaxy(object):
    
    def __init__(self, number_of_planets=0):
        self._planets = []
        for _ in range(number_of_planets):
            self._planets.append(planet.PlanetClassB())
    
    def sim(self):
        for planet in self._planets:
            planet.sim()
