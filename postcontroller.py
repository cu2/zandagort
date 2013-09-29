"""
Handles all POST requests
"""

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
        if not self._auth.is_guest(self.current_user):
            return {"error": "Already logged in"}
        user = self._auth.get_user_by_name(name)
        if user is None:
            return {"error": "No user"}
        if user.password != password:
            return {"error": "Wrong password"}
        self._auth.login(user, self.auth_cookie_value)
        return "Successful login"
    
    def logout(self):
        """Try to logout user"""
        if self._auth.is_guest(self.current_user):
            return {"error": "Not logged in"}  # since logout is not public, this line should never be reached
        self._auth.logout(self.current_user, self.auth_cookie_value)
        return "Successful logout"

    def set_time(self, time):  # TEST
        """Set world time. Only test method."""
        return self._world.set_time(time)
