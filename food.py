from os import get_terminal_size as gts
from random import randint

from point import Point


class Food:

    def __init__(self):
        self.position = Point(*self._get_random_pos())
        self.symbol = "●"

    def regrow(self):
        self.position.pos = self._get_random_pos()

    def _get_random_pos(self):
        term_size = gts()
        x = randint(0, term_size.columns - 1)
        y = randint(0, term_size.lines - 2)
        return (x, y)
