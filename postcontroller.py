"""
Handles all POST requests
"""

import datetime

import config
from controller import Controller
from utils import public


class PostController(Controller):
    """
    Handles all POST requests
    
    For details: see controller.py
    """
    
    @public
    def login(self, name, password):
        """Try to login user with name and password"""
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
    
    def set_time(self, time):  # TEST
        """Set world time. Only test method."""
        return self._world.set_time(time)
