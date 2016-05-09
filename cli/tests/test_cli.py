"""
Tests for ``cli.cli``.
"""

import os

from click.testing import CliRunner
import pytest

from cli.cli import cli
from common.testtools import ROOTFS_URI
from tasker.tasker import Task


@pytest.skip()
class TestCreate(object):
    """
    Tests for creating a Task from the CLI.
    """

    def test_create_task(self, tmpdir, capsys):
        """
        It is possible to start a Task from the CLI.
        """
        # Change directory to temporary directory so as not to pollute current
        # working directory with downloaded filesystem.
        os.chdir(tmpdir.strpath)

        runner = CliRunner()
        commands = 'sleep 10'
        result = runner.invoke(cli, ['create', ROOTFS_URI, commands])
        assert result.exit_code == 0

        task = Task(existing_id=int(result.output))._process.cmdline()
        assert task._process.cmdline() == commands.split()

    def test_send_signal_healthcheck(self, tmpdir):
        """
        Sending a SIGTERM signal to a task stops the process running.
        The status before and after is relayed by the healthcheck function.
        """
        # Change directory to temporary directory so as not to pollute current
        # working directory with downloaded filesystem.
        os.chdir(tmpdir.strpath)

        runner = CliRunner()
        create = runner.invoke(cli, ['create', ROOTFS_URI, 'sleep 100'])
        task_id = create.output

        healthcheck = runner.invoke(cli, ['healthcheck', task_id])
        assert healthcheck.output == ''
        runner.invoke(cli, ['signal', task_id, 'SIGTERM'])
        assert healthcheck.output == ''
