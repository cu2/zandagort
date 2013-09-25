"""
Custom Enumeration

Has the following properties:
- same value from same enum is identic
- same value from different enum is different
- type of enum value can be checked (enum "contains" enum value)
- hashable
- serializable
- readable in code
- __str__ contains enum type and name
- __repr__ contains enum type, name and value

Usage:
class Animal(MyEnum):
    values = ["Horse", "Dog", "Cat"]

Animal.Horse
Animal.Dog
Animal.Cat

Inspiration:
http://stackoverflow.com/a/4092436/1012495
http://docs.python.org/3.4/library/enum.html
http://www.python.org/dev/peps/pep-0435/
"""


class MyEnumValue(tuple):
    """
    Custom tuple subclass for enum values

    For easy recognizing and custom str/repr.
    """
    
    def __str__(self):
        """Return enum_type.name"""
        return str(self[0]) + "." + str(self[2])
    
    def __repr__(self):
        """Return <enum_type.name: value>"""
        return "<" + str(self[0]) + "." + str(self[2]) + ": " + str(self[1]) + ">"


class MyEnumMetaclass(type):
    """MyEnum and its subclasses are never instanced, so all stuff is defined as a metaclass"""
    
    def __getattr__(mcs, name):
        """Return MyEnumValue"""
        if name not in mcs.values:
            raise ValueError(name + " is not " + mcs.__name__)
        return MyEnumValue((mcs.__name__, mcs.values.index(name), name))
    
    def contains(mcs, value):
        """Check if value is MyEnumValue and comes from this subclass of MyEnum"""
        if not isinstance(value, MyEnumValue):
            return False
        return value[0] == mcs.__name__
    
    def get_all_values(mcs):
        """Return list of all values"""
        return [getattr(mcs, value) for value in mcs.values]


class MyEnum(object):  # pylint: disable-msg=R0903
    """Custom enum base class"""
    
    __metaclass__ = MyEnumMetaclass
