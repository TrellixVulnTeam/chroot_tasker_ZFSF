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
        parent_process = psutil.Process(int(result.output))
        [child_process] = parent_process.children()
        cmdline = child_process.cmdline()
        child_process.kill()

        assert result.exit_code == 0
        assert cmdline == commands.split()

    def test_send_signal(self, tmpdir):
        """
        TODO
        """
        # Change directory to temporary directory so as not to pollute current
        # working directory with downloaded filesystem.
        os.chdir(tmpdir.strpath)

        runner = CliRunner()
        create = runner.invoke(cli, ['create', ROOTFS_URI, 'sleep 100'])
        task_id = create.output

        healthcheck = runner.invoke(cli, ['create', ROOTFS_URI, 'sleep 100'])
        # TODO Use healthcheck to check that
        runner.invoke(cli, ['signal', task_id, 'SIGTERM'])
        # assert not psutil.pid_exists(child_process.pid)

    def test_health_check(self, tmpdir):
        os.chdir(tmpdir.strpath)

        runner = CliRunner()
        create = runner.invoke(cli, ['create', ROOTFS_URI, 'sleep 100'])
        ppid_str = create.output

        child_process = 'TODO'
        # TODO Use healthcheck instead of direct process manipulation
        # assert psutil.pid_exists(child_process.pid)
        runner.invoke(cli, ['signal', ppid_str, 'SIGTERM'])
        # assert not psutil.pid_exists(child_process.pid)
