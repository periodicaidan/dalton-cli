"""
File: dalton.py
Purpose: The root-command for the program, shows app information
"""

from sys import argv

import click

from app_info import mit_license
from help_menus import dalton_help


@click.group("dalton", invoke_without_command=True)
@click.option("--version", is_flag=True, default=False)
@click.option("--license", "license_", is_flag=True, default=False)
@click.option("--help", "-h", "help_", is_flag=True, default=False)
def dalton(help_, version, license_):
    if help_ or len(argv) == 1:
        dalton_help()
    if version:  # :todo: displays version number
        pass
    if license_:
        click.echo(mit_license())