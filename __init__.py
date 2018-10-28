from commands import *
from dalton import dalton
from commands.config import config
from commands.calc import calc
from commands.moiety import moiety
from commands.hist import hist

dalton.add_command(config)
dalton.add_command(hist)
dalton.add_command(moiety)
dalton.add_command(calc)


def main():
    dalton()
