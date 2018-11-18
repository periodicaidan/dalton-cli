"""
File: models/History.py
Purpose: Business logic for working with the user_history.yaml file
"""


import os.path as path

from yaml import load, dump

from calculator import *


USER_HISTORY_PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), "user_history.yaml")
with open(USER_HISTORY_PATH, "r") as uh_yaml:
    history = load(uh_yaml) or {}


def get(alias="*"):
    if alias == "*":
        return history
    else:
        if alias not in history.keys():
            return {"formula": None, "mass": None}
        else:
            return history[alias]


def keys():
    return history.keys()


def save(formula, alias):
    mass = get_mass(formula)
    new_compound = {
        "formula": formula,
        "mass": mass
    }
    history[alias] = new_compound
    commit()
    return new_compound["mass"]


def show(verbose):  # todo: These functions shouldn't deal with I/O. Return the output instead of printing it
    from click import echo
    if verbose:
        echo("NAME      |  FORMULA  |      MASS")
        echo("---------------------------------")
        for name, info in history.items():
            name_cell = name.ljust(9)
            # formats a format string
            # Using default settings, this becomes `%s | %9s | %9.3f`
            list_row = "%%s | %%%ds | %%%d.%df" % (9, 9, 3)
            echo(list_row % (name_cell, info["formula"], info["mass"]))
    else:
        for name, info in history.items():
            list_row = "%9s : %9.3f"  # :todo set padding dynamically
            echo(list_row % (name, info["mass"]))


def remove(alias):
    del history[alias]
    commit()


def clear():
    history.clear()
    commit()


def commit():
    with open(USER_HISTORY_PATH, "w") as uh_yaml:
        dump(history, uh_yaml, default_flow_style=False)