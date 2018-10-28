"""
File: commands/calc.py
Purpose: Performs calculations in response to user input, and outputs the result
"""

from sys import argv

import click

from calculator import *
from models import History
from models.Config import Config
from help_menus import calc_help


@click.group("calc", invoke_without_command=True)
@click.option("-M", "--mass-spec",
              is_flag=True, default=False,
              help="Get a theoretical mass spectrum of a molecule")
@click.option("-i", "--histogram",
              is_flag=True, default=False,
              help="Use with -M/--mass-spec to display the mass spec as a histogram")
@click.argument("formula", required=False)
def calc(mass_spec, histogram, formula):
    config = Config.setup()  # todo: Pass as context
    if not any(locals().items()) or len(argv) == 2:
        calc_help()
    else:
        if mass_spec:
            click.echo(get_mass_spec(formula, histogram))
        else:
            click.echo("%.3f %s" % (get_mass(formula), config.units))