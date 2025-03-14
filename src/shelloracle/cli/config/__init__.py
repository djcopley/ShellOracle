import click

from shelloracle.cli.config.init import init


@click.group()
def config(): ...


config.add_command(init)
