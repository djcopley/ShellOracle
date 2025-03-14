import click

from shelloracle.cli.config.edit import edit
from shelloracle.cli.config.init import init
from shelloracle.cli.config.show import show


@click.group()
def config(): ...


config.add_command(edit)
config.add_command(init)
config.add_command(show)
