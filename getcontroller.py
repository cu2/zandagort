import datetime

import config


class GetController(object):
    """Handles all GET requests"""
    
    def __init__(self, game):
        self._game = game
        self._auth = self._game.auth
        self._world = self._game.world
    
    def get_time(self, auth_cookie_value):
        cu = self._auth.get_user_by_auth_cookie(auth_cookie_value)  # TODO: refactor into decorator(?)
        if cu is None:
            return {"error": "Access denied. You have to login."}
        cu.auth_cookie["expiry"] = datetime.datetime.now() + datetime.timedelta(seconds=config.AUTH_COOKIE_EXPIRY)
        return {"auth_cookie_value": auth_cookie_value, "time": self._game.get_time()}
        return self._game.get_time()
