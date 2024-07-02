from os import system
import pickle
from time import sleep


def clear_scr():
    system("cls")


def typewrite(value, wps=20, end="\n"):
    delay = 1 / (wps * 5)
    for char in value:
        print(char, end="", flush=True)
        sleep(delay)

    print(end, end="")


def save_score(score):
    if not isinstance(score, int):
        raise TypeError(
            f"score argument must be an int, not '{score.__class__.__name__}'")

    with open("data/high_score.dat", "wb") as file:
        pickle.dump(score, file)


def get_score():
    try:
        with open("data/high_score.dat", "rb") as file:
            score = pickle.load(file)
            return score
    except Exception:
        save_score(0)
        return 0

