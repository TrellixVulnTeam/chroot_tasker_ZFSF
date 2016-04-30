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

TODO

Library
-------

``tasker`` is a Python library.

To install ``tasker``:

.. code:: sh

   pip install -e .

To use tasker:

.. code:: python

   import os
   import pathlib

   from tasker.tasker import Task

   # An image to download, extract and create a chroot jail in.
   image_url = 'http://example.com/image.tar'

   # The image will be downloaded and extracted into the parent.
   parent = pathlib.Path(os.getcwd())

   # See ``args`` at
   # https://docs.python.org/2/library/subprocess.html#subprocess.Popen
   args = ['echo', '1']

   task = Task(
      image_url=image_url,
      args=args,
      parent=parent,
   )

Tests
-----

Requires :Vagrant:`https://www.vagrantup.com`.

Create a Vagrant VM:

.. code:: sh

   vagrant up

SSH into the Vagrant box:

.. code:: sh

   vagrant ssh

In the Vagrant box, create a ``virtualenv``:

.. code:: sh

   mkvirtualenv chroot_tasker

Install the test dependencies:

.. code:: sh

   cd /vagrant
   pip install -e .[dev]

Run tests:

.. code:: sh

   sudo $(which py.test)
