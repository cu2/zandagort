import config


class Ecosystem(object):
    
    def __init__(self, class_):
        self._class = class_
        self._species = config.INITIAL_SPECIES[self._class]
        self._area = 2000000
    
    def __str__(self):
        outstr = ""
        for species in self._species:
            outstr += str(round(self._species[species], 2)) + " x " + str(species) + "\n"
        return outstr
    
    def sim(self):
        new_species = self._species.copy()
        for species, other_species in config.BETAMATRIXES[self._class]:
            if other_species == config.Species.null:
                new_species[species] += 1.0 * config.BETAMATRIXES[self._class][(species, other_species)]
            else:
                new_species[species] += 1.0 * config.BETAMATRIXES[self._class][(species, other_species)] / (self._area/100000) * self._species[other_species]
        for species in new_species:
            if new_species[species] < config.MINIMUM_VIABLE_POPULATION:
                new_species[species] = 0
        self._species = new_species.copy()
