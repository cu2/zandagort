from myenum import MyEnum
from ecosystem import Species


class Resources(MyEnum):
    
    values = ["raw_stone", "stone", "lumber"]


class Buildings(MyEnum):
    
    values = ["quarry", "sawmill"]


class Economy(object):
    
    def __init__(self):
        self._resources = {
            Resources.raw_stone: 500000,
        }
        self._buildings = {
            Buildings.quarry: 2,
        }
        self._iomatrix = {
            (Buildings.quarry, Resources.raw_stone): -100,
            (Buildings.quarry, Resources.stone): 50,
            (Buildings.sawmill, Species.ebony): -100,
            (Buildings.sawmill, Resources.lumber): 50,
        }
    
    def sim(self):
        pass


class EconomyClassB(Economy):
    
    def __init__(self):
        super(EconomyClassB, self).__init__()
        self._resources[Resources.raw_stone] *= 2
