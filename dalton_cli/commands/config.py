import click
from dalton_scripts import dalton


@dalton.command(help="Adjust Dalton-CLI options")
@click.option("--sig-figs", "sf",
              type=click.IntRange(0, 10, clamp=True))
@click.option("--mass-spec-precision", "msp",
              type=click.IntRange(0, 5, clamp=True))
@click.option("--units",
              type=click.Choice(["daltons", "gpm"]))
def config(sf, msp, units):  # todo: this will require making a whole config file
    pass
