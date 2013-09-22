import ecosystem
import economy


class Planet(object):
    
    def __init__(self, class_):
        self._class = class_
        self._ecosystem = ecosystem.Ecosystem(self._class)
        self._economy = economy.Economy(self._class)
    
    def sim(self):
        self._ecosystem.sim()
        self._economy.sim()
