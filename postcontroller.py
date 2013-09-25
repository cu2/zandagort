class PostController(object):
    """Handles all POST requests"""
    
    def __init__(self, game):
        self._game = game
    
    def set_time(self, time):
        return self._game._world.set_time(time)
