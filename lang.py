"""
Language module to handle translations
"""

from myenum import MyEnum
from ecosystem import Species


class Languages(MyEnum):
    """List of available languages"""
    values = ["english"]


class Lang(object):
    """Language class provides translations"""
    
    def __init__(self):
        self._translations = {}
        self._translations[Languages.english] = {
            Species.ebony: "Ebony",
            Species.panda: "Panda",
            Species.tiger: "Tiger",
        }
    
    def name(self, item, lng=Languages.english):
        """Return translation or str() of item if there's no translation"""
        if lng not in self._translations:
            return str(item)
        if item not in self._translations[lng]:
            return str(item)
        return self._translations[lng][item]
