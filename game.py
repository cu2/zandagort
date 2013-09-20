import config
from user import User
from world import World


class Game(object):
    
    def __init__(self, number_of_planets=0):
        self._users = []
        self._users.append(User(
            config.ADMIN_USER_NAME,
            config.ADMIN_USER_EMAIL,
            config.ADMIN_USER_PASSWORD,
            True
        ))
        self._world = World(number_of_planets)
    
    def sim(self):
        self._world.sim()
