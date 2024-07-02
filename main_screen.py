import pickle
from os import get_terminal_size as gts

import utils
from constants import *


class MainScreen:

    def __init__(self):
        self.enabled = False
        self.buffer_string = ""
        self.buffer_changed = True

        self.border_char = "#"
        self.bullet_char = "▷"  # > → ▷ ↪

        self.game_title = "Snake Term"

        self.options = ("Play", "Reset High Score", "Help", "Exit")
        longest_word_len = len(max(self.options, key=lambda x: len(x)))
        self.option_dict = {
            k: v.ljust(longest_word_len)
            for k, v in enumerate(self.options, 5)
        }
        self.selected_option = min(self.option_dict.keys())

        self.help_shown = False

        self.start_game = False
        self.exit_game = False
        self.high_score = 0

        self.update()

    def update(self):
        if not self.buffer_changed:
            return

        term_size = gts()

        self.buffer_string = ""

        if self.help_shown:
            self.buffer_string += self.game_title.center(term_size.columns)
            self.buffer_string += ("-" * len(self.game_title)).center(
                term_size.columns)
            with open("data/help.txt") as file:
                self.buffer_string += file.readline().center(term_size.columns)
                self.buffer_string += file.read()
            return
        # self.buffer_changed = True

        for y in range(term_size.lines):
            if y == 0 or y == term_size.lines - 1 or y == 3:
                self.buffer_string += self.border_char * term_size.columns
                continue
            elif y == 1:
                self.buffer_string += self.border_char
                self.buffer_string += self.game_title.center(
                    term_size.columns - 2)
                self.buffer_string += self.border_char
            elif y == 2:
                self.buffer_string += self.border_char
                self.buffer_string += (
                    "-" * len(self.game_title)).center(term_size.columns - 2)
                self.buffer_string += self.border_char
            elif y in self.option_dict:
                self.buffer_string += self.border_char
                temp_str = ""
                if self.selected_option == y:
                    temp_str += self.bullet_char + "  "

                temp_str += self.option_dict.get(y, "")

                self.buffer_string += temp_str.center(term_size.columns - 2)
                self.buffer_string += self.border_char

            elif y == term_size.lines - 2:
                self.buffer_string += "#"
                self.buffer_string += f"High Score: {self.high_score}".center(
                    term_size.columns - 2)
                self.buffer_string += "#"

            else:
                self.buffer_string += self.border_char
                self.buffer_string += " ".center(term_size.columns - 2)
                self.buffer_string += self.border_char

            self.buffer_string += "\n"

    def menu_up(self):
        self.selected_option -= 1
        if self.selected_option < min(self.option_dict.keys()):
            self.selected_option = max(self.option_dict.keys())
        self.buffer_changed = True

    def menu_down(self):
        self.selected_option += 1
        if self.selected_option > max(self.option_dict.keys()):
            self.selected_option = min(self.option_dict.keys())
        self.buffer_changed = True

    def invoke_menu_action(self):
        if self.selected_option == min(self.option_dict.keys()):
            self.start_game = True

        elif self.selected_option == max(self.option_dict.keys()):
            self.exit_game = True

        elif "Reset High Score" in self.option_dict.get(self.selected_option):
            utils.save_score(0)
            self.high_score = 0
            self.selected_option = min(self.option_dict.keys())
            self.buffer_changed = True
            self.update()

        elif "Help" in self.option_dict.get(self.selected_option):
            self.help_shown = True
            self.buffer_changed = True
            self.update()

    def key_press(self, key):

        if key == Key.BACKSPACE:
            if self.help_shown:
                self.help_shown = False
                self.buffer_changed = True
                self.update()

        if self.help_shown:
            return

        if key == Key.UP:
            self.menu_up()
            self.update()

        elif key == Key.DOWN:
            self.menu_down()
            self.update()

        elif key == Key.RETURN:
            self.invoke_menu_action()
