"""
File: models/Config.py
Purpose: Business logic for working with user settings
"""

import os.path as path

from yaml import load, dump


USER_CONFIG_PATH = path.join(path.dirname(path.abspath(__file__)), "user_config.yaml")
with open(USER_CONFIG_PATH, "r") as uc_yaml:
    config = load(uc_yaml)  # This will always be populated


def show():
    for setting, value in config.items():
        print(f"{setting} : {value}")


def set_sig_figs(sf):
    config["sig-figs"] = sf
    commit()


def set_mass_spec_precision(msp):
    config["mass-spec-precision"] = msp
    commit()


def set_units(u):
    config["units"] = u
    commit()


def commit():
    with open(USER_CONFIG_PATH, "w") as uc_yaml:
        dump(config, uc_yaml, default_flow_style=False)


if __name__ == '__main__':
    show()
