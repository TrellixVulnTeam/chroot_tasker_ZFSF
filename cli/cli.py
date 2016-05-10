"""
CLI for creating and interacting with tasks.
"""

import os
import pathlib
import shlex

import click

from tasker.tasker import Task


@click.group()
def cli():
    """
    Holder for various comands.
    """
    pass


@cli.command('create')
@click.argument('image_url')
@click.argument('args')
def create(image_url, args):
    """
    Create a ``Task``.

    :param str image_url: The URL (or URI) pointing to an image to download,
        extract and use as the root of a new process.
    :param str args: Commands to run as a new process.
    """
    task = Task(
        image_url=image_url,
        args=shlex.split(args),
        download_path=pathlib.Path(os.getcwd()),
    )
    print(task.process.pid)
