"""
General config file

Usage:
You can change basically any value. Just bear the consequences. :-)

How to:
- simple values: ALLCAPS = <something>
change <something>
- enums: class CamelCase(MyEnum): values = [<list>]
change <list>
- dictionaries: ALLCAPS = { <key>: <value>, <key>: <value>, ... }
change <key> and/or <value>, add key-value pairs, delete them
- overrides: <something> *= 2  # i.e. <something> = <something> * 2
change it as you like, just don't create syntax error
"""

from myenum import MyEnum
from utils import multi_config


# Server
SERVER_HOST = "localhost"
SERVER_PORT = 3492
SERVER_VERSION = "Zandagort/2.0"

SERVER_LOG_DIR = "logs"  # not trailing slash
SERVER_LOG_FILES = {
    "access": "access.log",
    "error": "error.log",
    "sys": "sys.log",
}
SERVER_LOG_STDOUT = {
    "access": True,
    "error": True,
    "sys": False,
}


# Cookie
AUTH_COOKIE_NAME = "zuid"
AUTH_COOKIE_EXPIRY = 7 * 24 * 60 * 60

# Game
ADMIN_USER_NAME = "admin"
ADMIN_USER_EMAIL = "admin@admin"
ADMIN_USER_PASSWORD = "admin"

# Speed
CRON_BASE_DELAY = 1
CRON_SIM_INTERVAL = 2
CRON_DUMP_INTERVAL = 5


# Planets
class PlanetClasses(MyEnum):
    values = ["A", "B", "C", "D", "E"]

# Ecosystem
class Species(MyEnum):
    values = ["null", "ebony", "panda", "tiger"]

MINIMUM_VIABLE_POPULATION = 10

BETAMATRIXES = {
    PlanetClasses.B: {
        (Species.ebony, Species.null): 10,
        (Species.ebony, Species.ebony): -0.01,
        (Species.ebony, Species.panda): -0.1,
        (Species.panda, Species.ebony): 0.01,
        (Species.panda, Species.panda): -0.1,
    },
}

INITIAL_SPECIES = {
    "": {},  # just a placeholder, don't change it
    PlanetClasses.B: {
        Species.ebony: 1000,
        Species.panda: 100,
        Species.tiger: 10,
    },
}


# Economy

## Resources
class Resources(MyEnum):
    values = ["raw_stone", "stone", "lumber"]

## Buildings
class Buildings(MyEnum):
    values = ["quarry", "sawmill"]

## IO Matrix
BASIC_IOMATRIX = {
    (Buildings.quarry, Resources.raw_stone): -100,
    (Buildings.quarry, Resources.stone): 50,
    (Buildings.sawmill, Species.ebony): -100,
    (Buildings.sawmill, Resources.lumber): 50,
}
IOMATRIXES = multi_config(BASIC_IOMATRIX, PlanetClasses)

IOMATRIXES[PlanetClasses.B][(Buildings.quarry, Resources.stone)] = 75

## Initial resources
BASIC_INITIAL_RESOURCES = {
    Resources.raw_stone: 500000,
}
INITIAL_RESOURCES = multi_config(BASIC_INITIAL_RESOURCES, PlanetClasses)

INITIAL_RESOURCES[PlanetClasses.B][Resources.raw_stone] *= 2

## Initial buildings
BASIC_INITIAL_BUILDINGS = {
    Buildings.quarry: 2,
}
INITIAL_BUILDINGS = multi_config(BASIC_INITIAL_BUILDINGS, PlanetClasses)
