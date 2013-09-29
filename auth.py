"""
Authorization class
"""

import datetime

import config
from user import User
from utils import generate_random_hexstring


class Auth(object):
    """
    Authorization class that stores users and sessions
    
    - stores users
    - stores sessions (multiple session/user)
    - provides some functions to handle users and sessions
    """
    
    def __init__(self):
        self._users = []
        self._users.append(User(
            config.ADMIN_USER_NAME,
            config.ADMIN_USER_EMAIL,
            config.ADMIN_USER_PASSWORD,
            True
        ))
        self._guest = User("guest", "guest", "guest")  # special guest user, used for internal purposes for not logged in users
        self._sessions = []
    
    def create_new_session(self):
        """Generate random auth cookie until unique is found and create new session with it"""
        while True:
            value = generate_random_hexstring(32)
            if self.get_user_by_auth_cookie(value) is None:
                break
        self._sessions.append((value, datetime.datetime.now() + datetime.timedelta(seconds=config.AUTH_COOKIE_EXPIRY), self._guest))
        return (value, self._guest)
    
    def renew_session(self, auth_cookie_value):
        """Renew session"""
        for value, expiry, user in list(self._sessions):
            if value == auth_cookie_value:
                if expiry >= datetime.datetime.now():
                    self._sessions.remove((value, expiry, user))
                    self._sessions.append((value, datetime.datetime.now() + datetime.timedelta(seconds=config.AUTH_COOKIE_EXPIRY), user))
    
    def login(self, new_user, auth_cookie_value):
        """Login user on a session"""
        for value, expiry, user in list(self._sessions):
            if value == auth_cookie_value:
                if expiry >= datetime.datetime.now():
                    self._sessions.remove((value, expiry, user))
                    self._sessions.append((value, expiry, new_user))
    
    def logout(self, old_user, auth_cookie_value):
        """Logout user on a session"""
        for value, expiry, user in list(self._sessions):
            if value == auth_cookie_value and user == old_user:
                if expiry >= datetime.datetime.now():
                    self._sessions.remove((value, expiry, user))
                    self._sessions.append((value, expiry, self._guest))
    
    def delete_invalid_sessions(self):
        """Delete invalid sessions. Should be called on a regular basis."""
        for value, expiry, user in list(self._sessions):
            if expiry < datetime.datetime.now():
                self._sessions.remove((value, expiry, user))
    
    def get_user_by_name(self, name):
        """Return user with given name or None"""
        for one_user in self._users:
            if one_user.name == name:
                return one_user
        return None

    def get_user_by_auth_cookie(self, auth_cookie_value):
        """Return user with given valid auth cookie or guest or None"""
        for value, expiry, user in self._sessions:
            if value == auth_cookie_value:
                if expiry >= datetime.datetime.now():
                    return user
        return None
    
    def is_guest(self, user):
        """Check if user is guest"""
        return user == self._guest
