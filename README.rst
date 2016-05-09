.. image:: https://requires.io/github/adamtheturtle/chroot_tasker/requirements.svg?branch=master
     :target: https://requires.io/github/adamtheturtle/chroot_tasker/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/adamtheturtle/chroot_tasker.svg?branch=master
    :target: https://travis-ci.org/adamtheturtle/chroot_tasker

.. image:: https://coveralls.io/repos/github/adamtheturtle/chroot_tasker/badge.svg?branch=master :target: https://coveralls.io/github/adamtheturtle/chroot_tasker?branch=master

Tasker
------

This is a programming challenge for Giant Swarm specified at
https://gist.github.com/zeisss/4c28f6c31bcd756eec81.

CLI
---

``tasker`` is a CLI for creating tasks which run in ``chroot`` jails.

To install ``tasker``:

.. code:: sh

   pip install -e .

To use ``tasker``:

.. code:: sh

   tasker create <IMAGE_URL> "<COMMANDS>"

Creating a ``chroot`` jail requires root priviledges.

One way to use this is:

.. code:: sh

   $ sudo $(which tasker) create <IMAGE_URL> "<COMMANDS>"
   8935 # This is the PID of the new process.

``tasker`` downloads the image from the given ``<IMAGE_URL>`` into the current working directory.
Also in the directory, the image is untarred to create a "filesystem".
The downloaded image is then deleted.
The commands in ``"<COMMANDS>"`` are then run in a chroot jail, with the "filesystem" root as the root.

Library
-------

``tasker`` is a Python library.

To install ``tasker``:

.. code:: sh

   pip install -e .

To use ``tasker``:

.. code:: python

   import os
   import pathlib

   from tasker.tasker import Task

   # An image to download, extract and create a chroot jail in.
   image_url = 'http://example.com/image.tar'

   # The image will be downloaded and extracted into the download_path.
   download_path = pathlib.Path(os.getcwd())

   # See ``args`` at
   # https://docs.python.org/2/library/subprocess.html#subprocess.Popen
   args = ['echo', '1']

   task = Task(
      image_url=image_url,
      args=args,
      download_path=download_path,
   )

   pid = task.process.pid

Supported platforms
-------------------

This has been tested on Ubuntu 14.04 with Python 3.5.

Tests
-----

Requires `Vagrant <https://www.vagrantup.com>`_.

Create a Vagrant VM:

.. code:: sh

   vagrant up

SSH into the Vagrant box:

.. code:: sh

   vagrant ssh

In the Vagrant box, create a ``virtualenv``:

.. code:: sh

   mkvirtualenv -p python3.5 chroot_tasker

Install the test dependencies:

.. code:: sh

   cd /vagrant
   pip install -e .[dev]

Run tests:

.. code:: sh

   sudo $(which py.test)

Design decisions
----------------

Language choice
^^^^^^^^^^^^^^^

I know Python and its ecosystem better than I do other languages,
and so in the interest of speed this is written in Python.

Parent directory
^^^^^^^^^^^^^^^^

There are at least three options for the directory in which to create the filesystem.

1. A hardcoded directory, perhaps configurable in a configuration file.

   This makes it difficult to create different filesystems in different places.
   If the directory is hardcoded the chosen directory may not be suitable.

2. The current working directory.

   This allows for calling code to choose where to place the filesystems.

3. Configurable as a command line option.

   This alone requires more work to be put into each call.

The current implementation is (2).
Ideally there would be multiple of the above, with (2) as the default.
The issue for this is https://github.com/adamtheturtle/chroot_tasker/issues/24.