"""
CLI for creating and interacting with tasks.
"""

import os
import pathlib

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
    """
    task = Task(
        image_url=image_url,
        args=args.split(),
        parent=pathlib.Path(os.getcwd()),
    )
    print(task.process.pid)