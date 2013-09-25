class PostController(object):
    """Handles all POST requests"""
    
    def __init__(self, world):
        self._world = world
    
    def set_time(self, time):
        return self._world.set_time(time)
