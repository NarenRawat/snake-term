from os import get_terminal_size as gts
from time import sleep

import utils
from constants import *
from food import Food
from point import Point
from snake import Snake


class GameScreen:

    def __init__(self):
        self.game_over = True
        self.paused = False

        self.snake = Snake()
        self.food = Food()

        self.snake_moved = False

        self.buffer_string = ""
        self.buffer_changed = False

        self.fillchar = "·"

        self.high_score = 0
        self.current_score = 0

        self.increase_speed = False

    @property
    def snake_direction(self):
        return self.snake.direction

    @snake_direction.setter
    def snake_direction(self, value):
        self.snake.direction = value

    def update(self):

        if self.paused or self.game_over:
            return

        term_size = gts()

        self.buffer_changed = True
        self.buffer_string = ""

        self.snake.move_forward()
        self.snake_moved = True

        if self.snake.collide_self():
            self.reset()
            self.game_over = True

        if self.snake.head == self.food.position:
            self.snake.add_body_part(self.food.position.clone())
            self.food.regrow()

            self.current_score += 1
            if self.current_score % 2 == 0:
                self.increase_speed = True
            if self.high_score < self.current_score:
                self.high_score = self.current_score

        for y in range(term_size.lines - 1):
            for x in range(term_size.columns):
                pos_point = Point(x, y)
                if pos_point == self.snake.head:
                    self.buffer_string += self.snake.head_symbol
                elif pos_point == self.food.position:
                    self.buffer_string += self.food.symbol
                elif pos_point in self.snake.body:
                    self.buffer_string += self.snake.body_symbol(pos_point)
                else:
                    self.buffer_string += self.fillchar

            self.buffer_string += "\n"

        temp_str = f"Current Score: {self.current_score}"
        self.buffer_string += temp_str
        remaining_cols = term_size.columns - len(temp_str)
        self.buffer_string += f"High Score: {self.high_score}".rjust(
            remaining_cols)

    def reset(self):
        utils.save_score(self.high_score)
        self.current_score = 0
        self.snake.reset()
        self.food.regrow()

    def key_press(self, key):

        if key == Key.UP:
            self.paused = False
            if self.snake_direction in (Direction.LEFT, Direction.RIGHT):
                if not self.snake_moved:
                    return
                self.snake_direction = Direction.UP
                self.snake_moved = False

        elif key == Key.DOWN:
            self.paused = False
            if self.snake_direction in (Direction.LEFT, Direction.RIGHT):
                if not self.snake_moved:
                    return
                self.snake_direction = Direction.DOWN
                self.snake_moved = False

        elif key == Key.LEFT:
            self.paused = False
            if self.snake_direction in (Direction.UP, Direction.DOWN):
                if not self.snake_moved:
                    return
                self.snake_direction = Direction.LEFT
                self.snake_moved = False

        elif key == Key.RIGHT:
            self.paused = False
            if self.snake_direction in (Direction.UP, Direction.DOWN):
                if not self.snake_moved:
                    return
                self.snake_direction = Direction.RIGHT
                self.snake_moved = False

        elif key == Key.ESCAPE:
            self.reset()
            self.game_over = True

        elif key == Key.R:
            self.paused = True
