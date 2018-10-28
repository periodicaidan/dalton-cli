"""
File: models/Config.py
Purpose: Business logic for working with user settings
"""

import os.path as path

from yaml import load, dump


class Config (object):
    PATH = path.join(path.dirname(path.dirname(path.abspath(__file__))), "user_config.yaml")
    DEFAULTS = {
        "mass-spec-precision": 1,
        "sig-figs": 3,
        "units": "g/mol"
    }

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def setup(cls):
        with open(cls.PATH, "r") as uc_yaml:
            conf = cls()
            settings = load(uc_yaml)
            if type(settings) == Config:
                conf = settings
            else:
                conf = cls(**settings)
            return conf
        # try:
        #     uc_yaml = open(cls.PATH, "r+")
        #     settings = load(uc_yaml)
        #     if type(settings) == Config:
        #         conf = settings
        #     else:
        #         conf = cls(**settings)
        # except FileNotFoundError:
        #     dump(uc_yaml, cls.DEFAULTS, default_flow_style=False)
        #     conf = cls(**cls.DEFAULTS)
        # finally:
        #     uc_yaml.close()
        #     return conf

    def commit(self):
        with open(Config.PATH, "w") as uc_yaml:
            dump(self, uc_yaml, default_flow_style=False)

    def set(self, setting, value):
        if setting in self.__dict__.keys():
            self[setting] = value
            self.commit()
            return True
        else:
            return False

    def restore_defaults(self):
        self.__dict__.update(Config.DEFAULTS)
        self.commit()

    def __getitem__(self, item):
        return self.__dict__[item]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __str__(self):
        settings_string = ""
        for setting, value in self.__dict__.items():
            settings_string += "%s : %s\n" % (setting, value)
        return settings_string
