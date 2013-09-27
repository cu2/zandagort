"""
World class
"""

from galaxy import Galaxy


class World(object):
    """
    Describes everything in the in-game world
    
    - players: not users, but in-game players, that can be either avatars of users or NPCs
    - galaxy: the galaxy that contains planets and fleets
    """
    
    def __init__(self):
        self._players = []
        self._galaxy = Galaxy()
        self._time = 0
    
    def sim(self):
        """Simulate in-game world"""
        self._galaxy.sim()
        self._time += 1
    
    def get_time(self):
        """Return in-game time"""
        return self._time
    
    def set_time(self, time_):
        """Set in-game time"""
        self._time = time_
        return self._time
