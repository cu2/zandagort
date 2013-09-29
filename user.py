"""
User class
"""


class User(object):
    """Simple struct-like class for storing user data"""
    
    def __init__(self, name, email, password, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
