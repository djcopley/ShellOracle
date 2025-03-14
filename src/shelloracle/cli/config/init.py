import click


@click.command()
def init():
    """Install shelloracle keybindings."""
    # nest this import in a function to avoid expensive module loads
    from shelloracle.bootstrap import bootstrap_shelloracle

    bootstrap_shelloracle()
