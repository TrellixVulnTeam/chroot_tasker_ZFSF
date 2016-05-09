"""
Create and interact with tasks in a chroot jail.
"""

import os
import psutil
import subprocess
import tarfile
import urllib2
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
    image = urllib2.urlopen(image_url)
    # Use ``image.url`` below instead of image_url in case of a redirect.
    image_path = pathlib.Path(urllib2.urlparse.urlparse(image.url).path)
    tar_file = download_path.joinpath(image_path.name)
    with open(str(tar_file), 'wb') as tf:
        tf.write(image.read())

    unique_id = uuid.uuid4().hex
    filesystem_path = download_path.joinpath(image_path.stem + unique_id)
    with tarfile.open(str(tar_file)) as tf:
        tf.extractall(str(filesystem_path))

    tar_file.unlink()
    return filesystem_path


def _run_chroot_process(filesystem, args, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """
    # TODO Remove options for stdin, out, err
    Create a chroot jail and run a process in it.

    Prints the PID of the new process.

    :param pathlib.Path filesystem: The directory which should be the root of
        the new process.
    :param list args: List of strings. See ``subprocess.Popen.args``.

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
        return {'status': self._process.status()}

    def send_signal(self, signal):
        """
        Send a signal to the task's process.

        :param int signal: The signal to send.
        """
        self._process.send_signal(signal)
        os.wait()

    def __init__(self, image_url, args, download_path):
        """
        Create a new task.

        :TODO: params, ivars
        """
        filesystem = _create_filesystem_dir(
            image_url=image_url,
            download_path=download_path,
        )

        process = _run_chroot_process(
            filesystem=filesystem,
            args=args,
        )

        self.id = process.pid
        self._process = psutil.Process(self.id)
