"""
File: commands/config.py
Purpose: Interface for viewing and setting various settings
"""

import click

from models.Config import Config


@click.command(help="Adjust Dalton-CLI options")
@click.option("--show-all",
              is_flag=True, default=False)
@click.option("--sig-figs", "sf",
              type=click.IntRange(0, 10, clamp=True),
              required=False, default=None)
@click.option("--mass-spec-precision", "msp",
              type=click.IntRange(0, 5, clamp=True),
              required=False, default=None)
@click.option("--units",
              type=click.Choice(["daltons", "gpm"]),
              required=False, default=None)
def config(show_all, sf, msp, units):
    cfg = Config.setup()
    if show_all:
        click.echo(cfg.show())
    elif any(locals().values()):
        for setting, value in locals().items():
            if value is not None:
                successful = cfg.set(setting, value)
                if successful:
                    click.echo("Set %s to %s" % (setting, value))
                else:
                    click.echo("Could not set %s" % setting)
