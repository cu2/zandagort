import datetime

import config
from controller import Controller
from utils import public


class PostController(Controller):
    """Handles all POST requests"""
    
    @public
    def login(self, name, password):
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
        self.auth_cookie_value = new_auth_cookie_value
        return "Successful login"
    
    def set_time(self, time):
        return self._world.set_time(time)
