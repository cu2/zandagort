from myenum import MyEnum


class Species(MyEnum):
    
    values = ["null", "ebony", "panda", "tiger"]


class Ecosystem(object):
    
    def __init__(self):
        self._species = {}
        self._crossmatrix = {}
    
    def __str__(self):
        outstr = ""
        for species in self._species:
            outstr += str(round(self._species[species], 2)) + " x " + str(species) + "\n"
        return outstr
    
    def sim(self):
        new_species = self._species.copy()
        for species, other_species in self._crossmatrix:
            if other_species == Species.null:
                new_species[species] += 1.0 * self._crossmatrix[(species, other_species)]
            else:
                new_species[species] += 1.0 * self._crossmatrix[(species, other_species)] * self._species[other_species]
        for species in new_species:
            if new_species[species] < 0:
                new_species[species] = 0
        self._species = new_species.copy()


class EcosystemClassB(Ecosystem):
    
    def __init__(self):
        self._species = {Species.ebony: 1000,
                         Species.panda: 100,
                         Species.tiger: 10}
        self._crossmatrix = {
            (Species.ebony, Species.null): 10,
            (Species.ebony, Species.ebony): -0.01,
            (Species.ebony, Species.panda): -0.1,
            (Species.panda, Species.ebony): 0.01,
            (Species.panda, Species.panda): -0.1,
        }
