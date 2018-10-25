import os.path as path

from yaml import load, dump

from calculator import *


USER_MOIETIES_PATH = path.join(path.dirname(path.abspath(__file__)), "user_moieties.yaml")
with open(USER_MOIETIES_PATH, "r") as um_yaml:
    moieties = load(um_yaml) or {}


def get(symbol="*"):
    if symbol == "*":
        return moieties
    else:
        if symbol not in moieties.keys():
            raise KeyError
        else:
            return moieties[symbol]


def items():
    return moieties.items()


def symbols():
    return moieties.keys()


def add(symbol, eq_form):
    mass = get_mass(eq_form)
    new_moiety = {
        "eq_form": eq_form,
        "mass": mass
    }
    moieties[symbol] = new_moiety
    commit()
    return new_moiety["mass"]


def show(verbose):  # todo: These functions shouldn't deal with I/O. Return the output instead of printing it
    from click import echo
    if verbose:
        echo("MOIETY  | EQUIVALENT FORMULA |       MASS")
        echo("-----------------------------------------")
        for moiety, info in moieties.items():
            moiety_cell = moiety.ljust(7)
            # formats a format string
            # Using default settings, this becomes `%s | %18s | %10.3f`
            list_row = "%%s | %%%ds | %%%d.%df" % (18, 10, 3)
            echo(list_row % (moiety_cell, info["eq_form"], info["mass"]))
    else:
        for moiety, info in moieties.items():
            list_row = "%10s : %10.3f"  # :todo set padding dynamically
            echo(list_row % (moiety, info["mass"]))


def change(symbol, new_eq_form):
    profile = moieties[symbol]
    profile["eq_form"] = new_eq_form
    profile["mass"] = get_mass(new_eq_form)
    moieties[symbol] = profile
    commit()
    return profile["mass"]


def rename(symbol, new_symbol):
    moieties[new_symbol] = moieties[symbol]
    del moieties[symbol]
    commit()


def delete(symbol):
    del moieties[symbol]
    commit()


def delete_all():
    moieties.clear()
    commit()


def commit():
    with open(USER_MOIETIES_PATH, "w") as um_yaml:
        dump(moieties, um_yaml, default_flow_style=False)
