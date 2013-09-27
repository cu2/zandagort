"""
Game class
"""

from auth import Auth
from world import World


class Game(object):
    """
    Game connects users with the in-game world
    
    - auth = users
    - world = in-game world
    """
    
    def __init__(self):
        self.auth = Auth()
        self.world = World()
    
    def sim(self):
        """Simulate in-game world"""
        self.world.sim()
    
    def get_time(self):
        """Return in-game time"""
        return self.world.get_time()
