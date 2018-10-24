"""
File: main.py
Purpose: Entry point of the program, handles the I/O
"""


from sys import argv

from app_info import *
from calculator import *
from help_menus import *

# def main(*argv):
#   dalton()

# Entry point
@click.group("dalton", invoke_without_command=True)
@click.option("--version", is_flag=True, default=False)
@click.option("--license", is_flag=True, default=False)
@click.option("--help", "-h", "help_", is_flag=True, default=False)
def dalton(help_, version, license):
    if help_ or len(argv) == 1:
        dalton_help()
    if version:  # :todo: displays version number
        pass
    if license:
        click.echo(mit_license())


@dalton.command(help="Get the mass of a molecule")
@click.option("-M", "--mass-spec",
              is_flag=True, default=False,
              help="Get a theoretical mass spectrum of a molecule")
@click.option("-h", "--histogram",
              is_flag=True, default=False,
              help="Use with -M/--mass-spec to display the mass spec as a histogram")
@click.argument("formula")
def calc(formula, mass_spec, histogram):
    if mass_spec:
        click.echo(get_mass_spec(formula, histogram))
    else:
        click.echo("%.3f g/mol" % get_mass(formula))


@dalton.command(help="Work with custom chemical symbols")
@click.option("-a", "--add",
              is_flag=True, default=False,
              help="Register a new moiety to be called when calculating formulas")
@click.option("-l", "--list", "list_",
              is_flag=True, default=False,
              help="List registered moieties with their masses")
@click.option("-v", "--verbose",
              is_flag=True, default=False,
              help="Used with -l/--list to display all moiety information")
@click.option("-c", "--change",
              is_flag=True, default=False,
              help="Change the equivalent formula of a moiety")
@click.option("-r", "--rename",
              is_flag=True, default=False,
              help="Rename a registered moiety")
@click.option("-d", "--delete",
              is_flag=True, default=False,
              help="Unregister a moiety")
@click.option("-D", "--delete-all",
              is_flag=True, default=False,
              help="Unregister all moieties")
@click.argument("symbol", required=False)
@click.argument("formula", required=False)
@click.help_option()
@click.pass_context
def moiety(ctx,  # command context
           list_, verbose, change, rename, delete, add, delete_all,  # flags
           symbol, formula):  # args
    from models import Moiety
    local_vars = [v for k, v in locals().items() if k != "Moiety" and k != "ctx"]
    if not any(local_vars):
        click.echo(ctx.get_help())
    if list_:
        if len(Moiety.get()) == 0:
            click.echo("No moieties have been added yet.")
        else:
            Moiety.show(verbose)
    if add:
        if symbol in Moiety.symbols():
            click.echo("%s is already registered" % symbol)
        elif symbol in table:
            click.echo("%s is an element" % symbol)
        else:
            mass = Moiety.add(symbol, formula)
            click.echo("%s added to moiety profile (mass: %.3f g/mol)" % (symbol, mass))
    if delete:
        if symbol in Moiety.symbols():
            Moiety.delete(symbol)
            click.echo("Removed %s from user moieties" % symbol)
        else:
            click.echo("You have not registered any moiety %s" % symbol)
    if change:
        if symbol in Moiety.symbols():
            mass = Moiety.change(symbol, formula)
            click.echo("Changed value of %s to %s (%.3f g/mol)" % (symbol, formula, mass))
        else:
            click.echo("%s has not been added to user moieties." % symbol)
            added = click.confirm("Would you like to add it?")
            if added:
                Moiety.add(symbol, formula)
    if rename:  # For this flag, the `formula` is just the new symbol
        if symbol not in Moiety.symbols():
            click.echo("%s has not been added to user moieties." % symbol)
        elif formula in Moiety.symbols():
            click.echo("%s already exists in your moiety profile." % formula)
        else:
            Moiety.rename(symbol, formula)
            click.echo("%s renamed to %s" % (symbol, formula))
    if delete_all:
        click.confirm("This will delete all the moieties you've registered. Are you sure?")
        Moiety.delete_all()
        click.echo("All moieties unregistered.")


@dalton.command(help="Save compounds for future reference")
@click.option("-s", "--save",
              is_flag=True, default=False,
              help="Save a compound to your history")
@click.option("-l", "--list", "list_",
              is_flag=True, default=False,
              help="Show history")
@click.option("-v", "--verbose",
              is_flag=True, default=False,
              help="Use with -l/--list to show history in a table format")
@click.option("-r", "--remove",
              is_flag=True, default=False,
              help="Remove a compound from your history")
@click.option("-K", "--clear",
              is_flag=True, default=False,
              help="Clear your whole history")
@click.argument("name", required=False)
@click.argument("formula", required=False)
@click.pass_context
def hist(ctx,  # command context
         save, list_, verbose, remove, clear,  # flags
         formula, name):  # args
    from models import History
    local_vars = [v for k, v in locals().items() if k != "History" and k != "ctx"]
    if not any(local_vars):
        click.echo(ctx.get_help())
    if save:
        if name in History.keys():
            click.echo("%s already saved in history" % name)
        else:
            History.save(formula, name)
            click.echo("%s saved to user history" % name)
    if list_:
        if any(History.get()):
            History.show(verbose)
        else:
            click.echo("You have not saved any compounds")
    if remove:
        if name in History.keys():
            History.remove(name)
            click.echo("%s removed from user histroy" % name)
        else:
            click.echo("You have not saved a compound %s" % name)
    if clear:
        if any(History.get()):
            History.clear()
            click.echo("History cleared")
        else:
            click.echo("You have not saved any compounds")


@dalton.command(help="Adjust Dalton-CLI options")
@click.option("--sig-figs", "sf",
              type=click.IntRange(1, 10, clamp=True))
@click.option("--units",
              type=click.Choice(["daltons", "gpm"]))
def opts(sf, units):  # todo: this will require making a whole config file
    pass
