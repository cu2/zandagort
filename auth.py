"""
Authorization class

- stores users (with data and session)
- provides some functions to handle users
"""

import datetime

import config
from user import User
from utils import generate_random_hexstring


class Auth(object):
    """Authorization class that stores users"""
    
    def __init__(self):
        self._users = []
        self._users.append(User(
            config.ADMIN_USER_NAME,
            config.ADMIN_USER_EMAIL,
            config.ADMIN_USER_PASSWORD,
            True
        ))
    
    def get_user_by_name(self, name):
        """Return user with given name or None"""
        for one_user in self._users:
            if one_user.name == name:
                return one_user
        return None

    def get_user_by_auth_cookie(self, auth_cookie_value):
        """Return user with given valid auth cookie or None"""
        for one_user in self._users:
            if one_user.auth_cookie["value"] == auth_cookie_value and one_user.auth_cookie["expiry"] >= datetime.datetime.now():
                return one_user
        return None

    def generate_auth_cookie(self):
        """Generate random auth cookie until unique is found"""
        while True:
            auth_cookie = generate_random_hexstring(32)
            if self.get_user_by_auth_cookie(auth_cookie) is None:
                break
        return auth_cookie
