import config


class Ecosystem(object):
    
    def __init__(self, class_):
        self._class = class_
        self._species = config.INITIAL_SPECIES[self._class]
        self._area = 2000000
    
    def __str__(self):
        outstr = ""
        for species, count in self._species.iteritems():
            outstr += str(round(count, 2)) + " x " + str(species) + "\n"
        return outstr
    
    def sim(self):
        new_species = self._species.copy()
        for (species, other_species), beta in config.BETAMATRIXES[self._class].iteritems():
            if other_species == config.Species.null:
                new_species[species] += 1.0 * beta
            else:
                new_species[species] += 1.0 * beta / (self._area/100000) * self._species[other_species]
        for species, count in new_species.iteritems():
            if count < config.MINIMUM_VIABLE_POPULATION:
                new_species[species] = 0
        self._species = new_species.copy()
