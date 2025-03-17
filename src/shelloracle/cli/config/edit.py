from __future__ import annotations

from typing import TYPE_CHECKING

import click

if TYPE_CHECKING:
    from shelloracle.cli.application import Application


@click.command()
@click.pass_obj
def edit(app: Application):
    """Edit shelloracle configuration."""
    click.edit(filename=app.config_path)
