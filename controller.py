"""
Base class for get and post controllers
"""

class Controller(object):
    """
    Base class for get and post controllers
    
    Usage:
    - instantiate GetController or PostController subclass with Game
    - set Controller.current_user
    - call Controller.<method>
    
    Contains the Game it controls.
    
    Rationale for auth_cookie_value and current_user:
    
    1. Shortcut
    Typical client-server usage would be to pass these as arguments for each call separately.
    But for the possible several dozen controller methods it seems a cleaner solution.
    Because of the single threaded nature of the server, methods are called one after the other,
    so there's no possibility mixing these values among separate requests.
    
    2. Test and other not client-server usecases
    For direct testing, AI development, etc. it might be even better to set user once,
    and call methods hunders of times.
    """
    
    def __init__(self, game):
        self._game = game
        self._auth = self._game.auth
        self._world = self._game.world
        self.auth_cookie_value = ""
        self.current_user = None
