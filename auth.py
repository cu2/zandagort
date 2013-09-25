import config
from user import User


class Auth(object):
    
    def __init__(self):
        self._users = []
        self._users.append(User(
            config.ADMIN_USER_NAME,
            config.ADMIN_USER_EMAIL,
            config.ADMIN_USER_PASSWORD,
            True
        ))
        self._loggedin = False
        self._current_user = None
