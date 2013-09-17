from galaxy import Galaxy


class World(object):
    
    def __init__(self, number_of_planets=0):
        self._players = []
        self._galaxy = Galaxy(number_of_planets)
    
    def sim(self):
        self._galaxy.sim()
