"""
Tests for ``tasker.tasker``.
"""

import tarfile
import time

import pathlib
import psutil

from common.testtools import ROOTFS_URI
from tasker.tasker import _create_filesystem_dir, _run_chroot_process, Task


class TestCreateFilestystemDir(object):
    """
    Tests for ``_create_filesystem_dir``.
    """

    def _create_tarfile(self, tmpdir):
        """
        Create a ``.tar`` file containing ``hello.txt`` when extracted.

        :param tmpdir: The directory in which to create the archive and text
            file.

        :rtype: str
        :return: URI of the tar file.
        """
        text_file = tmpdir.join("hello.txt")
        text_file.write("content")
        tar_file = tmpdir.join('filesystem.tar')
        with tarfile.open(tar_file.strpath, 'w') as tar:
            tar.add(text_file.strpath, arcname=text_file.basename)
        image_url = pathlib.Path(tar_file.strpath).as_uri()
        return image_url

    def test_filesystem_dir_created(self, tmpdir):
        """
        The given ``.tar`` file is downloaded and extracted to the given
        parent.
        """
        image_url = self._create_tarfile(tmpdir=tmpdir.mkdir('server'))

        client = pathlib.Path(tmpdir.mkdir('client').strpath)
        extracted_filesystem = _create_filesystem_dir(
            image_url=image_url,
            parent=client,
        )

        assert extracted_filesystem.parent == client
        assert extracted_filesystem.joinpath('hello.txt').exists()

    def test_multiple_filesystems(self, tmpdir):
        """
        Multiple filesystem directories can exist from the same image.
        """
        image_url = self._create_tarfile(tmpdir=tmpdir.mkdir('server'))

        client = pathlib.Path(tmpdir.mkdir('client').strpath)
        extracted_filesystem_1 = _create_filesystem_dir(
            image_url=image_url,
            parent=client,
        )

        extracted_filesystem_2 = _create_filesystem_dir(
            image_url=image_url,
            parent=client,
        )

        assert extracted_filesystem_1 != extracted_filesystem_2

    def test_image_removed(self, tmpdir):
        """
        The downloaded image is deleted.
        """
        image_url = self._create_tarfile(tmpdir=tmpdir.mkdir('server'))

        client = pathlib.Path(tmpdir.mkdir('client').strpath)
        extracted_filesystem = _create_filesystem_dir(
            image_url=image_url,
            parent=client,
        )

        client_children = [item for item in client.iterdir()]
        assert client_children == [extracted_filesystem]


class TestRunChrootProcess(object):
    """
    Tests for ``_run_chroot_process``.
    """

    def test_run_chroot_process(self, tmpdir):
        """
        A new process is created from the given arguments in a chroot jail
        of the given filesystem path.
        """
        filesystem = _create_filesystem_dir(
            image_url=ROOTFS_URI,
            parent=pathlib.Path(tmpdir.strpath),
        )

        _run_chroot_process(
            filesystem=filesystem,
            args=['touch', '/example.txt'],
        )

        # ``touch`` takes a short time to work.
        time.sleep(0.01)
        assert filesystem.joinpath('example.txt').exists()

    def test_process_returned(self, tmpdir):
        """
        A new process with a new process ID is created, and the process object
        is returned.
        """
        filesystem = _create_filesystem_dir(
            image_url=ROOTFS_URI,
            parent=pathlib.Path(tmpdir.strpath),
        )

        old_pids = psutil.pids()
        process = _run_chroot_process(
            filesystem=filesystem,
            args=['touch', '/example.txt'],
        )
        new_pids = set(psutil.pids()) - set(old_pids)
        assert process.pid in new_pids

    def test_default_io(self, tmpdir):
        """
        By default there is a pipe to the standard I/O streams.
        """
        filesystem = _create_filesystem_dir(
            image_url=ROOTFS_URI,
            parent=pathlib.Path(tmpdir.strpath),
        )

        process = _run_chroot_process(
            filesystem=filesystem,
            args=['echo', '1'],
        )

        assert process.stdout.read() == '1\n'


class TestTask(object):
    """
    Tests for ``Task``.
    """

    def test_create_task(self, tmpdir):
        """
        A task can be created which starts a new process running a given
        command.
        """
        args = ['echo', '1']
        parent = pathlib.Path(tmpdir.strpath)
        task = Task(image_url=ROOTFS_URI, args=args, parent=parent)
        assert isinstance(task.process.pid, int)

    def test_send_signal(self, tmpdir):
        # http://www.linuxjournal.com/article/10815
        # http://www.tsheffler.com/blog/2010/11/21/python-multithreaded-daemon-with-sigterm-support-a-recipe/


        import shlex
        # trap 'touch /example.txt' INT
        script = 'sleep 100'
        # script = "/bin/sh -c echo 1; while /usr/bin/true ; do sleep 30; done"
        args = shlex.split(script)

        parent = pathlib.Path(tmpdir.strpath)
        task = Task(image_url=ROOTFS_URI, args=args, parent=parent)
        time.sleep(0.01)
        process = task.process
        parent_id = psutil.Process(task.process.pid).ppid()
        # parent_process = psutil.Process(parent_id)
        import signal, os
        os.kill(parent_id, signal.SIGINT)
        assert psutil.pid_exists(process.pid)
        # parent_process.send_signal(signal.SIGTERM)
        assert not psutil.pid_exists(process.pid)
        # filesystem = [item for item in parent.iterdir()][0]
        # files = [item for item in filesystem.iterdir()]
        # assert filesystem.joinpath('example.txt') in files
