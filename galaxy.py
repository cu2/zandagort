import config
import planet


class Galaxy(object):
    
    def __init__(self, number_of_planets=0):
        self._planets = []
        for _ in range(number_of_planets):
            self._planets.append(planet.Planet(config.PlanetClasses.B))
    
    def sim(self):
        for one_planet in self._planets:
            one_planet.sim()
