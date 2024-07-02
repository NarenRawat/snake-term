import msvcrt
import threading
import time
from os import get_terminal_size as gts

import utils
from constants import *
from game_screen import GameScreen
from main_screen import MainScreen


class Main:

    def __init__(self):
        self.main_scr = MainScreen()
        self.game_scr = GameScreen()

        self.current_screen = "main"

        self.running = False

        self.fps = 10
        self.buffer_string = ""
        self.buffer_changed = True

        self.keyboard_thread = None

        self.high_score = utils.get_score()
        self.main_scr.high_score = self.high_score
        self.game_scr.high_score = self.high_score
        self.main_scr.update()

    @property
    def high_score(self):
        return utils.get_score()

    @high_score.setter
    def high_score(self, value):
        utils.save_score(value)
        self.main_scr.high_score = value
        self.game_scr.high_score = value

    @property
    def period(self):
        return 1 / self.fps

    def start(self):
        utils.clear_scr()

        self.validate_term_size()

        self.keyboard_thread = threading.Thread(target=self.keyboard_listener,
                                                name="keyboard_thread",
                                                daemon=True)
        self.keyboard_thread.start()

        self.running = True

        self.main_loop()

    def validate_term_size(self):
        print("Resize terminal window to a bigger size to continue")

        while True:
            term_size = gts()

            if term_size.lines < 15 or term_size.columns < 60:
                continue
            else:
                break

    def keyboard_listener(self):
        while True:
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getch()

                    if key == b"\xe0":
                        next_key = msvcrt.getch()
                        if next_key == b"H":
                            key = b"w"
                        elif next_key == b"P":
                            key = b"s"
                        elif next_key == b"K":
                            key = b"a"
                        elif next_key == b"M":
                            key = b"d"
                        else:
                            continue

                    if key in (b"w", b"W"):
                        self.key_press(Key.UP)

                    elif key in (b"s", b"S"):
                        self.key_press(Key.DOWN)

                    elif key in (b"a", b"A"):
                        self.key_press(Key.LEFT)

                    elif key in (b"d", b"D"):
                        self.key_press(Key.RIGHT)

                    elif key in (b"r", b"R"):
                        self.key_press(Key.R)

                    elif key in b"\r\n":
                        self.key_press(Key.RETURN)

                    elif key == b"\x1b":
                        self.key_press(Key.ESCAPE)

                    elif key == b"\x08":
                        self.key_press(Key.BACKSPACE)

            except KeyboardInterrupt:
                continue

    def key_press(self, key):

        if key == Key.UP:
            if self.current_screen == "game":
                self.game_scr.key_press(key)

            elif self.current_screen == "main":
                self.main_scr.key_press(key)

        elif key == Key.DOWN:
            if self.current_screen == "game":
                self.game_scr.key_press(key)

            elif self.current_screen == "main":
                self.main_scr.key_press(key)

        elif key == Key.LEFT:
            if self.current_screen == "game":
                self.game_scr.key_press(key)

        elif key == Key.RIGHT:
            if self.current_screen == "game":
                self.game_scr.key_press(key)

        elif key == Key.R:
            if self.current_screen == "game":
                self.game_scr.key_press(key)

        elif key == Key.RETURN:
            if self.current_screen == "main":
                self.main_scr.key_press(key)

        elif key == Key.ESCAPE:
            if self.current_screen == "main":
                pass
                # self.running = False
            elif self.current_screen == "game":
                self.game_scr.key_press(key)

        elif key == Key.BACKSPACE:
            if self.current_screen == "main":
                self.main_scr.key_press(key)

    def main_loop(self):
        before_time = time.time()

        while self.running:
            try:
                self.screen_update()
                self.screen_blit()

                after_time = time.time()

                time_diff = after_time - before_time
                sleep_time = (self.period - time_diff)

                if sleep_time < 0:
                    sleep_time = 0

                time.sleep(sleep_time)

                before_time = time.time()

            except KeyboardInterrupt:
                continue
        self.exit_game()

    def screen_update(self):
        if self.current_screen == "game":

            if self.game_scr.game_over:
                self.fps = 10
                self.high_score = self.game_scr.high_score
                self.main_scr.update()
                self.current_screen = "main"
                self.main_scr.buffer_changed = True
                self.game_scr.buffer_changed = True
                return

            self.game_scr.update()

            if self.game_scr.increase_speed:
                self.game_scr.increase_speed = False
                self.fps += 1 / 2

        elif self.current_screen == "main":
            if self.main_scr.start_game:

                self.main_scr.start_game = False
                self.game_scr.game_over = False

                self.current_screen = "game"

                self.main_scr.buffer_changed = True
                self.game_scr.buffer_changed = True

                self.high_score = self.main_scr.high_score

            elif self.main_scr.exit_game:
                self.main_scr.exit_game = False
                self.game_scr.game_over = True
                self.running = False

    def screen_blit(self):

        if self.current_screen == "game":
            self.buffer_string = self.game_scr.buffer_string
            self.buffer_changed = self.game_scr.buffer_changed

        else:
            self.buffer_string = self.main_scr.buffer_string
            self.buffer_changed = self.main_scr.buffer_changed

        if self.buffer_changed:
            self.main_scr.buffer_changed = False
            self.game_scr.buffer_changed = False
            utils.clear_scr()
            print(self.buffer_string, end="")

    def exit_game(self):

        utils.clear_scr()
        utils.typewrite(f"High Score: {self.high_score}")
        utils.typewrite("Thanks for playing!")
        utils.typewrite("Bye!")
        exit(0)


if __name__ == "__main__":
    Main().start()
