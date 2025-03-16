import click

from shelloracle.cli import Application


@click.command()
@click.pass_obj
def init(app: Application):
    """Install shelloracle keybindings."""
    # nest this import in a function to avoid expensive module loads
    from shelloracle.bootstrap import bootstrap_shelloracle

    bootstrap_shelloracle(app.config_path)
