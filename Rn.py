from functools import lru_cache


class CoordDescriptor:
    """Coordinate attribute that accepts only int or float values."""

    def __set_name__(self, owner, name):
        self.storage_name = "_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if isinstance(value, bool):
            raise TypeError(self.storage_name[1:] + " can't be a boolean")
        if not isinstance(value, (int, float)):
            raise TypeError(self.storage_name[1:] + " must be int or float")
        instance.__dict__[self.storage_name] = value


@lru_cache
def make_point_class(n, name=None):
    """Return a class of points in R^n with coordinates x0, ..., x(n-1).

    Repeated calls with the same arguments return the same class.
    """
    if not name:
        name = "Point" + str(n)

    attributes = {}
    for i in range(n):
        attributes["x" + str(i)] = CoordDescriptor()

    def __init__(self, *coords):
        if len(coords) != n:
            raise TypeError(name + " needs " + str(n) + " coordinates, got " + str(len(coords)))
        for i in range(n):
            setattr(self, "x" + str(i), coords[i])

    def to_tuple(self):
        values = []
        for i in range(n):
            values.append(getattr(self, "x" + str(i)))
        return tuple(values)

    attributes["__init__"] = __init__
    attributes["to_tuple"] = to_tuple

    return type(name, (), attributes)



