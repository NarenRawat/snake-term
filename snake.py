from os import get_terminal_size as gts

from constants import *
from point import Point


class Snake:

    def __init__(self):
        term_size = gts()
        self.head = Point(term_size.columns // 2, term_size.lines // 2)
        self.body = [Point()]
        self._direction = Direction.RIGHT
        self.speed_x = 1
        self.speed_y = 1

    def __len__(self):
        return 1 + len(self.body)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value in (Direction.UP, Direction.DOWN, Direction.LEFT,
                     Direction.RIGHT):
            self._direction = value

    @property
    def head_symbol(self):
        if self.direction == Direction.UP:
            return "▲"
        elif self.direction == Direction.DOWN:
            return "▼"
        elif self.direction == Direction.LEFT:
            return "◀"
        elif self.direction == Direction.RIGHT:
            return "▶"

    def body_symbol(self, body_pos):
        return "■"

        # TODO: return appropriate body_symbol based on direction
        # "◤◣◥◢"

        # if len(self) <= 2:
        #     return "■"
        # body_index = self.body.index(body_pos)
        # if body_index == 0:
        #     if body_pos.x == self.head.x:

        #     if side == Direction.UP:
        #         return "◥"
        #     elif side == Direction.DOWN:
        #         return "◢"
        #     elif side == Direction.LEFT:
        #         return "◣"
        #     elif side == Direction.RIGHT:
        #         return "◢"
        # return "■"

    def move_forward(self):
        term_size = gts()
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].pos = self.body[i - 1].pos

        if len(self.body) > 0:
            self.body[0].pos = self.head.pos

        if self.direction == Direction.UP:
            self.head.y -= self.speed_y
            if self.head.y < 0:
                self.head.y = term_size.lines - 2
        elif self.direction == Direction.DOWN:
            self.head.y += self.speed_y
            if self.head.y >= term_size.lines - 1:
                self.head.y = 0
        elif self.direction == Direction.LEFT:
            self.head.x -= self.speed_x
            if self.head.x < 0:
                self.head.x = term_size.columns - 1
        elif self.direction == Direction.RIGHT:
            self.head.x += self.speed_x
            if self.head.x >= term_size.columns:
                self.head.x = 0

    def is_tail(self, point):
        return self.body.index(point) == len(self.body) - 1

    def add_body_part(self, point):
        self.body.insert(0, point)

    def collide_self(self):
        for bp in self.body:
            if bp == self.head:
                return True
        return False

    def reset(self):
        term_size = gts()
        self.head.pos = (term_size.columns // 2, term_size.lines // 2)
        self.body = [Point()]
        self.direction = Direction.RIGHT
