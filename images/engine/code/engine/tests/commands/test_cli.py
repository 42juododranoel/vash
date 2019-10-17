from click_aliases import ClickAliasedGroup

from engine.commands.cli import cli


def test_support_aliases():
    assert isinstance(cli, ClickAliasedGroup)
