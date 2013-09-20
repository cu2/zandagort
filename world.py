from galaxy import Galaxy


class World(object):
    
    def __init__(self, number_of_planets=0):
        self._players = []
        self._galaxy = Galaxy(number_of_planets)
        self._time = 0
    
    def sim(self):
        self._galaxy.sim()
        self._time += 1
    
    def get_time(self):
        return self._time
