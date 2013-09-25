class GetController(object):
    """Handles all GET requests"""
    
    def __init__(self, game):
        self._game = game
    
    def get_time(self):
        return self._game.get_time()
