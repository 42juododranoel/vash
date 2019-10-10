import click
from click_aliases import ClickAliasedGroup


@click.group(cls=ClickAliasedGroup)
def cli():
    pass
