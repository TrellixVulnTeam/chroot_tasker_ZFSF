"""
Tests for ``cli.cli``.
"""

from click.testing import CliRunner

from cli.cli import cli


class TestCreate(object):
    """
    Tests for creating a Task from the CLI.
    """

    def test_create_task(self):
        """
        It is possible to start a Task from the CLI.
        """
        # OS change directory to tmpdir
        runner = CliRunner()
        image_url = 'file:///vagrant/tasker/tests/rootfs.tar'
        passed = ['create', image_url, 'sleep 10000']
        result = runner.invoke(cli, passed)
        # Assert that the sleep comand is there
        # kill the sleep command.
        assert result == 0
