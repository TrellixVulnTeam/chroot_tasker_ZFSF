"""
Tests for ``tasker.tasker``.
"""

import tarfile

import pathlib

from tasker.tasker import _create_filesystem_dir


class TestCreateFilestystemDir(object):
    """
    Tests for ``_create_filesystem_dir``.
    """

    def test_filesystem_dir_created(self, tmpdir):
        """
        The given ``.tar`` file is downloaded and extracted to the given
        parent.
        """
        server = tmpdir.mkdir('server')
        filesystem = server.mkdir('filesystem')
        text_file = tmpdir.mkdir("sub").join("hello.txt")
        text_file.write("content")
        tar_file = tmpdir.join('filesystem.tar')
        with tarfile.open(tar_file.strpath, 'w') as tar:
            tar.add(filesystem.strpath, arcname=filesystem.basename)
        image_url = pathlib.Path(tar_file.strpath).as_uri()

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
        server = tmpdir.mkdir('server')
        filesystem = server.mkdir('filesystem')
        text_file = tmpdir.mkdir("sub").join("hello.txt")
        text_file.write("content")
        tar_file = tmpdir.join('filesystem.tar')
        with tarfile.open(tar_file.strpath, 'w') as tar:
            tar.add(filesystem.strpath, arcname=filesystem.basename)
        image_url = 'file://' + tar_file.strpath

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
        server = tmpdir.mkdir('server')
        filesystem = server.mkdir('filesystem')
        text_file = tmpdir.mkdir("sub").join("hello.txt")
        text_file.write("content")
        tar_file = tmpdir.join('filesystem.tar')
        with tarfile.open(tar_file.strpath, 'w') as tar:
            tar.add(filesystem.strpath, arcname=filesystem.basename)
        image_url = 'file://' + tar_file.strpath

        client = pathlib.Path(tmpdir.mkdir('client').strpath)
        extracted_filesystem = _create_filesystem_dir(
            image_url=image_url,
            parent=client,
        )

        client_files = [item for item in client.iterdir()]
        assert client_files == []
        # Assert that the tar file is not at some location.
        # Separate tar creation out.


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
