"""
Create and interact with tasks in a chroot jail.
"""


def _create_filesystem_dir(image_url, parent):
    """
    Download a ``.tar`` file, extract it into ``parent`` and delete the
    ``.tar`` file.

    :param str image_url: The url of a ``.tar`` file.

    :rtype: pathlib.Path
    :returns: The path to the extracted parent.
    """
    pass

class Task(object):
    """
    A process in a chroot jail.
    """

    def __init__(self):
        """
        Create a new task.

        :rtype: None
        """
        pass
