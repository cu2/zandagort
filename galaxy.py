import config
import planet


class Galaxy(object):
    
    def __init__(self):
        self._planets = []
        # TODO: implement galaxy generation
        for _ in range(config.NUMBER_OF_PLANETS):
            self._planets.append(planet.Planet(config.PlanetClasses.B))
    
    def sim(self):
        for one_planet in self._planets:
            one_planet.sim()
