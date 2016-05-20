.. image:: https://requires.io/github/adamtheturtle/chroot_tasker/requirements.svg?branch=master
     :target: https://requires.io/github/adamtheturtle/chroot_tasker/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/adamtheturtle/chroot_tasker.svg?branch=master
    :target: https://travis-ci.org/adamtheturtle/chroot_tasker

Tasker
------

This is a programming challenge for an interview.

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

   # Root permissions are necessary to create the task.
   $ sudo $(which tasker) create <IMAGE_URL> "sleep 100"
   8935 # This is the ID of the new task.
   $ tasker health_check 8935
   exists: True
   status: sleeping
   $ sudo $(which tasker) send_signal SIGINT
   $ tasker health_check 8935
   exists: False
   status: None

``tasker`` downloads the image from the given ``<IMAGE_URL>`` into the current working directory.
Also in the directory, the image is untarred to create a "filesystem".
The downloaded image is then deleted.
The commands in ``"<COMMANDS>"`` are then run in a chroot jail, with the "filesystem" root as the root.

Library
-------

``tasker`` is a Python library.

Installation
^^^^^^^^^^^^

.. code:: sh

   pip install -e .

API
^^^

To use ``tasker``:

.. code:: python

   import os
   import pathlib
   import signal

   from tasker.tasker import Task

   task = Task(
      # An image to download, extract and create a chroot jail in.
      image_url='http://example.com/image.tar',
      # A command to run in the extracted filesystem.
      args=['sleep', '5'],
      # Where the image will be downloaded and extracted into.
      download_path=pathlib.Path(os.getcwd()),
      # It is also possible to customise stdout and stderr by passing
      # ``stdout`` or ``stderr`` parameters, as per
      # https://docs.python.org/3.1/library/subprocess.html#subprocess.Popen.
   )

   task_health = task.get_health()
   # {"exists": True, "status": "sleeping"}

   task.send_signal(signal.SIGTERM)

   task_health = task.get_health()
   # {"exists": False, "status": None}

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

   mkvirtualenv -p python3.5 tasker

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

Identifiers
^^^^^^^^^^^

This uses PIDs as identifiers.
This is not safe - PIDs get reused and so this could end up with a user manipulating the wrong process.
This was a simple to implement strategy.
A long term solution might be stateful and have a mapping of tasks to unique identifiers.
