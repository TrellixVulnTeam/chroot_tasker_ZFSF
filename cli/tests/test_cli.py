"""
Tests for ``cli.cli``.
"""

import os

import psutil

from click.testing import CliRunner

from cli.cli import cli
from common.testtools import ROOTFS_URI


class TestCreate(object):
    """
    Tests for creating a Task from the CLI.
    """

    def test_create_task(self, tmpdir):
        """
        It is possible to start a Task from the CLI.
        """
        # Change directory to temporary directory so as not to pollute current
        # working directory with downloaded filesystem.
        os.chdir(tmpdir.strpath)

        runner = CliRunner()
        # TODO Generate this
        subcommand = 'create'
        commands = 'sleep 10'
        result = runner.invoke(cli, [subcommand, ROOTFS_URI, commands])

        # The PID of the new process is outputted.
        [pid] = map(int, result.output.splitlines())
        process = psutil.Process(pid)
        cmdline = process.cmdline()
        process.kill()

        assert result.exit_code == 0
        assert cmdline == commands.split()
