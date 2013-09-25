import datetime

import config


class PostController(object):
    """Handles all POST requests"""
    
    def __init__(self, game):
        self._game = game
        self._auth = self._game.auth
        self._world = self._game.world
    
    def login(self, auth_cookie_value, name, password):
        user = self._auth.get_user_by_name(name)
        if user is None:
            return {"error": "No user"}
        if user.password != password:
            return {"error": "Wrong password"}
        new_auth_cookie_value = self._auth.generate_auth_cookie()
        user.auth_cookie = {
            "value": new_auth_cookie_value,
            "expiry": datetime.datetime.now() + datetime.timedelta(seconds=config.AUTH_COOKIE_EXPIRY),
        }
        return {"auth_cookie_value": new_auth_cookie_value, "success": "Successful login"}
    
    def set_time(self, auth_cookie_value, time):
        return self._world.set_time(time)
