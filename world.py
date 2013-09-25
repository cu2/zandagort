from galaxy import Galaxy


class World(object):
    
    def __init__(self):
        self._players = []
        self._galaxy = Galaxy()
        self._time = 0
    
    def sim(self):
        self._galaxy.sim()
        self._time += 1
    
    def get_time(self):
        return self._time
    
    def set_time(self, time_):
        self._time = time_
        return self._time
