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

TODO

Tests
-----

Requires :Vagrant:`https://www.vagrantup.com`.

Create a Vagrant VM:

```
vagrant up
```

SSH into the Vagrant box:

```
vagrant ssh
```

In the Vagrant box, create a ``virtualenv``:

```
mkvirtualenv chroot_tasker
```

Install the test dependencies:

```
cd /vagrant
pip install -e .[dev]
```

Run tests:

```
sudo $(which py.test)
```
