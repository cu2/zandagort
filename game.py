from auth import Auth
from world import World


class Game(object):
    
    def __init__(self):
        self._auth = Auth()
        self._world = World()
    
    def sim(self):
        self._world.sim()
    
    def get_time(self):
        return self._world.get_time()
