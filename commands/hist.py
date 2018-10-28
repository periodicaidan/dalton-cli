"""
File: commands/hist.py
Purpose: Defines commands for saving named compounds
"""

from sys import argv

import click

from help_menus import hist_help
from models import History


@click.group("hist",
              help="",
              invoke_without_command=True)
@click.option("-h", "--help", "help_",
              is_flag=True, default=False)
def hist(help_):
    if help_ or len(argv) == 2:
        hist_help()


@hist.command("save")
@click.argument("name")
@click.argument("formula")
def save(name, formula):
    if name in History.keys():
        click.echo("%s already saved in history" % name)
    else:
        History.save(formula, name)
        click.echo("%s saved to user history" % name)


@hist.command("list")
@click.option("-v", "--verbose",
              is_flag=True, default=False)
def list_(verbose):
    if any(History.get()):
        History.show(verbose)
    else:
        click.echo("You have not saved any compounds")


@hist.command("remove")
@click.argument("name")
def remove(name):
    if name in History.keys():
        History.remove(name)
        click.echo("%s removed from user histroy" % name)
    else:
        click.echo("You have not saved a compound %s" % name)


@hist.command("clear")
@click.confirmation_option()
def clear():
    if any(History.get()):
        History.clear()
        click.echo("History cleared")
    else:
        click.echo("You have not saved any compounds")
