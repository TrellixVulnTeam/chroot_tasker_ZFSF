"""
Create and interact with tasks in a chroot jail.
"""

import os
import psutil
import subprocess
import tarfile
import time
import urllib.parse
import urllib.request
import uuid

import pathlib


def _create_filesystem_dir(image_url, download_path):
    """
    Download a ``.tar`` file, extract it into ``download_path`` and delete the
    ``.tar`` file.

    :param str image_url: The url of a ``.tar`` file.
    :param pathlib.Path download_path: The parent to extract the downloaded
        image into.

    :rtype: pathlib.Path
    :returns: The path to the extracted image.
    """
    image = urllib.request.urlopen(image_url)
    # Use ``image.url`` below instead of image_url in case of a redirect.
    image_path = pathlib.Path(urllib.parse.urlparse(image.url).path)
    tar_file = download_path.joinpath(image_path.name)
    with open(str(tar_file), 'wb') as tf:
        tf.write(image.read())

    unique_id = uuid.uuid4().hex
    filesystem_path = download_path.joinpath(image_path.stem + unique_id)
    with tarfile.open(str(tar_file)) as tf:
        tf.extractall(str(filesystem_path))

    tar_file.unlink()
    return filesystem_path


def _run_chroot_process(filesystem, args, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE):
    """
    Create a chroot jail and run a process in it.

    Prints the PID of the new process.

    :param pathlib.Path filesystem: The directory which should be the root of
        the new process.
    :param list args: List of strings. See ``subprocess.Popen.args``.
    :param stdout: See
        https://docs.python.org/3.1/library/subprocess.html#subprocess.Popen.
    :param stderr: See
        https://docs.python.org/3.1/library/subprocess.html#subprocess.Popen.

    :return subprocess.Popen: The newly started process.
    """
    real_root = os.open("/", os.O_RDONLY)
    os.chroot(str(filesystem))
    process = subprocess.Popen(
        args=args,
        stdout=stdout,
        stderr=stderr,
    )
    os.fchdir(real_root)
    os.chroot(".")
    os.close(real_root)

    # On some platforms it seems to take some time for a process to start,
    # even after this point. Therefore sleep for 5ms to ensure platform
    # parity. This seems to be necessary on Travis CI hosted.
    time.sleep(0.05)

    return process


class Task(object):
    """
    A process in a chroot jail.
    """

    def get_health(self):
        """
        Get details of the task's health.

        :rtype: dict
        :returns: The task's process's status.
        """
        if self._process is not None:
            try:
                status = self._process.status()
                return {'exists': True, 'status': status}
            except psutil.NoSuchProcess:
                pass

        return {'exists': False, 'status': None}

    def send_signal(self, signal):
        """
        Send a signal to the task's process.

        :param int signal: The signal to send.
        """
        self._process.send_signal(signal)
        try:
            os.wait()
        except OSError:  # pragma: no cover
            pass

    def __init__(self, image_url=None, args=None, download_path=None,
                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                 existing_task=None):
        """
        Create a new task, which is a process running inside a chroot with root
        being a downloaded image's root.

        :param str image_url: The url of a ``.tar`` file.
        :param list args: List of strings. See ``subprocess.Popen.args``.
        :param pathlib.Path download_path: The parent to extract the downloaded
        image into.
        :param stdout: See
        https://docs.python.org/3.1/library/subprocess.html#subprocess.Popen.
        :param stderr: See
        https://docs.python.org/3.1/library/subprocess.html#subprocess.Popen.
        :param existing_task: The id of an existing task. If this is given,
            other parameters are ignored and no new process is started.

        :ivar int id: An identifier for the task.
        """
        if existing_task is not None:
            try:
                self._process = psutil.Process(existing_task)
            except psutil.NoSuchProcess:
                self._process = None

            self.id = existing_task
        else:
            filesystem = _create_filesystem_dir(
                image_url=image_url,
                download_path=download_path,
            )

            process = _run_chroot_process(
                filesystem=filesystem,
                args=args,
                stdout=stdout,
                stderr=stderr,
            )

            self.id = process.pid
            self._process = psutil.Process(self.id)
