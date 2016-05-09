"""
Tests for ``cli.cli``.
"""

import os

from click.testing import CliRunner

from cli.cli import cli
from common.testtools import ROOTFS_URI
from tasker.tasker import Task


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
        commands = 'top'
        result = runner.invoke(cli, ['create', ROOTFS_URI, commands])
        assert result.exit_code == 0

        task = Task(existing_task=int(result.output))
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
        create = runner.invoke(cli, ['create', ROOTFS_URI, 'top'])
        task_id = create.output

        before_int = runner.invoke(cli, ['health_check', task_id])
        assert before_int.output == 'exists: True\nstatus: running\n'
        runner.invoke(cli, ['send_signal', task_id, 'SIGINT'])
        after_int = runner.invoke(cli, ['health_check', task_id])
        assert after_int.output == 'exists: False\nstatus: None\n'
