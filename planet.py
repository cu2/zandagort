import ecosystem
import economy


class Planet(object):
    
    def __init__(self):
        self._ecosystem = ecosystem.Ecosystem()
        self._economy = economy.Economy()
    
    def sim(self):
        self._ecosystem.sim()
        self._economy.sim()


class PlanetClassB(Planet):
    
    def __init__(self):
        super(PlanetClassB, self).__init__()
        self._ecosystem = ecosystem.EcosystemClassB()
        self._economy = economy.EconomyClassB()
