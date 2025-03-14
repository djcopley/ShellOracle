import click
import pygments
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import PygmentsTokens
from pygments.lexers import TOMLLexer

from shelloracle.cli.application import Application


@click.command()
@click.pass_obj
def show(app: Application):
    """Display shelloracle configuration."""
    with app.config_path.open("r") as f:
        tokens = list(pygments.lex(f.read(), lexer=TOMLLexer()))
    print_formatted_text(PygmentsTokens(tokens))
