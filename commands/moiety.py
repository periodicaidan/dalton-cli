from sys import argv

import click

import periodictable
from help_menus import moiety_help
from dalton_scripts.main import dalton
from models import Moiety


@dalton.group("moiety",
              help="Work with custom chemical symbols",
              invoke_without_command=True)
@click.option("-h", "--help", "help_",
              is_flag=True, default=False)
def moiety(help_):
    if help_ or len(argv) == 2:
        moiety_help()


@moiety.command("add")
@click.argument("symbol")
@click.argument("formula")
def add(symbol, formula):
    if symbol in Moiety.symbols():
        click.echo("%s is already registered" % symbol)
    elif symbol in periodictable.table:
        click.echo("%s is an element" % symbol)
    else:
        mass = Moiety.add(symbol, formula)
        click.echo("%s added to moiety profile (mass: %.3f g/mol)" % (symbol, mass))


@moiety.command("list")
@click.option("-v", "--verbose",
              is_flag=True, default=False)
def list_(verbose):
    if len(Moiety.get()) == 0:
        click.echo("No moieties have been added yet.")
    else:
        Moiety.show(verbose)


@moiety.command("change")
@click.argument("symbol")
@click.argument("formula")
def change(symbol, formula):
    if symbol in Moiety.symbols():
        mass = Moiety.change(symbol, formula)
        click.echo("Changed value of %s to %s (%.3f g/mol)" % (symbol, formula, mass))
    else:
        click.echo("%s has not been added to user moieties." % symbol)
        added = click.confirm("Would you like to add it?")
        if added:
            Moiety.add(symbol, formula)


@moiety.command
@click.argument("old")
@click.argument("new")
def rename(old, new):
    if old not in Moiety.symbols():
        click.echo("%s has not been added to user moieties." % old)
    elif new in Moiety.symbols():
        click.echo("%s already exists in your moiety profile." % new)
    else:
        Moiety.rename(old, new)
        click.echo("%s renamed to %s" % (old, new))


@moiety.command
@click.argument("symbols", nargs=-1)
def delete(symbols):
    for symbol in symbols:
        if symbol in Moiety.symbols():
            Moiety.delete(symbol)
            click.echo("Removed %s from user moieties" % symbol)
        else:
            click.echo("You have not registered any moiety %s" % symbol)


@moiety.command
def delete_all():
    click.confirm("This will delete all the moieties you've registered. Are you sure?")
    Moiety.delete_all()
    click.echo("All moieties unregistered.")
