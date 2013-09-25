class GetController(object):
    """Handles all GET requests"""
    
    def __init__(self, world):
        self._world = world
    
    def get_time(self):
        return self._world.get_time()
