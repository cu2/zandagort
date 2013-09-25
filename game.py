from auth import Auth
from world import World


class Game(object):
    
    def __init__(self):
        self.auth = Auth()
        self.world = World()
    
    def sim(self):
        self.world.sim()
    
    def get_time(self):
        return self.world.get_time()
