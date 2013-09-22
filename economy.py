import config


class Economy(object):
    
    def __init__(self, class_):
        self._class = class_
        self._resources = config.INITIAL_RESOURCES[self._class]
        self._buildings = config.INITIAL_BUILDINGS[self._class]
    
    def sim(self):
        pass
