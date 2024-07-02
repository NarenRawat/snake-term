from constants import Direction


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Point):
            if (self.x == __o.x and self.y == __o.y):
                return True
        return False

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, value):
        if isinstance(value, (tuple, list)) and len(value) == 2:
            self.x, self.y = value
        else:
            raise ValueError("pos must be of type (x, y)")

    def clone(self):
        return Point(self.x, self.y)
