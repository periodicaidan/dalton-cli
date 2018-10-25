from click import echo, style
import splashscreen


def dalton_help():
    # Splash screen, copyright, etc.
    echo(style(splashscreen.text, fg="red"))
    echo("The stoichiometric command line utility")
    echo("Copyright (c) 2018 Aidan T. Manning")
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
    echo("  calc")
    echo("  moiety")
    echo("  hist")
    echo("  config")

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
    pass


def hist_help():
    pass
