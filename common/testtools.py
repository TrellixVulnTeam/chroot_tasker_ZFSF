import pathlib

ROOTFS_URI = pathlib.Path(__file__).with_name('rootfs.tar').absolute().as_uri()
