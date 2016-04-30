"""
Tests for ``tasker.tasker``.
"""

from tasker.tasker import _create_filesystem_dir, _run_chroot_process, Task


class TestCreateFilestystemDir(object):
    """
    Tests for ``_create_filesystem_dir``.
    """

    def test_filesystem_dir_created(self):
        """
        The given ``.tar`` file is downloaded and extracted to the given
        parent.
        """

    def test_multiple_filesystems(self):
        """
        Multiple filesystem directories can exist from the same image.
        """

    def test_image_removed(self):
        """
        The downloaded image is deleted.
        """


class TestTask(object):
    """
    Tests for ``Task``.
    """

    def test_create_task(self):
        """
        A task can be created which starts a new process running a given
        command.
        """

class TestRunChrootProcess(object):
    """
    Tests for ``_run_chroot_process``.
    """

    def test_run_chroot_process(self):
        """
        A new process is created from the given arguments in a chroot jail
        of the given filesystem path.
        """
