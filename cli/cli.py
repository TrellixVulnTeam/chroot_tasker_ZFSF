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
@click.argument('args', nargs=-1)
def create(image_url, args):
    """
    Create a ``Task``.
    """
    Task(
        image_url=pathlib.Path(image_url),
        args=list(args),
        parent=os.getcwd(),
    )
