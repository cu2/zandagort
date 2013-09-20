class User(object):
    
    def __init__(self, name, email, password, admin=False):
        self._name = name
        self._email = email
        self._password = password
        self._admin = admin
