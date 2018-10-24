from sys import argv

import click

import periodictable
from help_menus import hist_help
from dalton_scripts.main import dalton
from models import History


@dalton.group("hist",
              help="",
              invoke_without_command=True)
@click.option("-h", "--help", "help_",
              is_flag=True, default=False)
def hist(help_):
    if help_ or len(argv) == 2:
        hist_help()
