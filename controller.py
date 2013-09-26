class Controller(object):
    """Base class for get and post controllers"""
    
    def __init__(self, game):
        self._game = game
        self._auth = self._game.auth
        self._world = self._game.world
        self.auth_cookie_value = ""
        self.current_user = None
