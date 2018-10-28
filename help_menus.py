"""
File: help-menus.py
Purpose: Help menus for the various commands
"""

import datetime as dt

from click import echo, style
import splashscreen


def dalton_help():
    # Splash screen, copyright, etc.
    echo(style(splashscreen.text, fg="red"))
    echo("The stoichiometric command line tool")
    echo("Copyright (c) 2018 - %s Aidan T. Manning" % dt.date.today().year)
    echo("Type " + style("dalton --license", fg="blue") + " for full license")
    echo()

    # Instructions
    echo("Usage: dalton <command> <mode> <args>")
    echo()

    # Options
    echo("Options:")
    echo("  --help/-h : Display this help menu")
    echo("  --version : Display version info")
    echo("  --license : Display software license")
    echo()

    # Commands
    echo("Commands (type " + style("dalton <command>", fg="blue") + " for more info):")
    echo("  %6s : Get mass info about a compound" % "calc")
    echo("  %6s : Work with user-defined chemical symbols" % "moiety")
    echo("  %6s : Save compound information for later" % "hist")
    echo("  %6s : Work with Dalton-CLi settings" % "config")

def calc_help():
    echo("Usage: dalton calc <mode> <symbol> <formula>")
    echo()
    echo("  Get mass info about a compound")
    echo()
    echo("Modes:")
    echo("  -M, --mass-spec : Get a theoretical mass spectrum for a compound")
    echo("  -i, --histogram : Use with -M/--mass-spec to display the mass spec as a histogram")
    echo("  -h, --help : Display this help menu")


def moiety_help():
    echo("Usage: dalton moiety <command> <args>")
    echo()
    echo("  Work with user-defined chemical symbols")
    echo()
    echo("Commands:")
    echo("  add: Register a new moiety")
    echo("  list: Show all currently registered moieties")
    echo("        (set the -v/--verbose flag to see it in a table view)")
    echo("  change: Edit the formula of a moiety")
    echo("  rename: Edit the symbol of an already-registered moiety")
    echo("  delete: Unregister a moiety (set the -A/--all flag to delete all of them)")


def hist_help():
    echo("Usage: dalton hist <command> <args>")


if __name__ == '__main__':
    moiety_help()
