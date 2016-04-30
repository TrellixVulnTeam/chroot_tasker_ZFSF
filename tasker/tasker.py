"""
Create and interact with tasks in a chroot jail.
"""

import os
import subprocess
import tarfile
import urllib2
import uuid

import pathlib


def _create_filesystem_dir(image_url, parent):
    """
    Download a ``.tar`` file, extract it into ``parent`` and delete the
    ``.tar`` file.

    :param str image_url: The url of a ``.tar`` file.
    :param pathlib.Path parent: The parent to extract the downloaded image
        into.

    :rtype: pathlib.Path
    :returns: The path to the extracted image.
    """
    image = urllib2.urlopen(image_url)
    # Use ``image.url`` below instead of image_url in case of a redirect.
    image_path = pathlib.Path(urllib2.urlparse.urlparse(image.url).path)
    tar_file = parent.joinpath(image_path.name)
    with open(str(tar_file), 'wb') as tf:
        tf.write(image.read())

    unique_id = uuid.uuid4().hex
    filesystem_path = parent.joinpath(image_path.stem + unique_id)
    with tarfile.open(str(tar_file)) as tf:
        tf.extractall(str(filesystem_path))

    tar_file.unlink()
    return filesystem_path


def _run_chroot_process(filesystem, args):
    """
    Create a chroot jail and run a process in it.

    :param pathlib.Path filesystem: The directory which should be the root of
        the new process.
    :param list args: List of strings. See ``subprocess.Popen.args``.

    :return subprocess.Popen: The newly started process.
    """
    real_root = os.open("/", os.O_RDONLY)
    os.chroot(str(filesystem))
    process = subprocess.Popen(args=args)
    os.fchdir(real_root)
    os.chroot(".")
    os.close(real_root)
    return process
