"""
Tests for ``tasker.tasker``.
"""

import tarfile
import time

import pathlib
import psutil

from tasker.tasker import _run_chroot_process, _create_filesystem_dir


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

    def _get_filesystem(self, tmpdir):
        """
        Return the ``pathlib.Path`` of an extracted filesystem.

        This filesystem ``.tar`` file was created with:

        ```
        $ docker run --name rootfs alpine ls
        $ docker export rootfs > rootfs.tar
        ```
        """
        rootfs = pathlib.Path(__file__).with_name('rootfs.tar')
        return _create_filesystem_dir(
            image_url=rootfs.as_uri(),
            parent=pathlib.Path(tmpdir.strpath),
        )

    def test_run_chroot_process(self, tmpdir):
        """
        A new process is created from the given arguments in a chroot jail
        of the given filesystem path.
        """
        filesystem = self._get_filesystem(tmpdir=tmpdir)
        _run_chroot_process(
            filesystem=filesystem,
            args=['touch', '/example.txt'],
        )

        # ``touch`` takes a short time to work.
        time.sleep(0.01)
        children = [item for item in filesystem.iterdir()]
        assert filesystem.joinpath('example.txt') in children

    def test_process_returned(self, tmpdir):
        """
        A new process with a new process ID is created, and the process object
        is returned.
        """
        filesystem = self._get_filesystem(tmpdir=tmpdir)
        old_pids = psutil.pids()
        process = _run_chroot_process(
            filesystem=filesystem,
            args=['touch', '/example.txt'],
        )
        new_pids = set(psutil.pids()) - set(old_pids)
        assert process.pid in new_pids
