"""
CLI for creating and interacting with tasks.
"""

import os
import pathlib
import psutil
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
    """
    task = Task(
        image_url=image_url,
        args=shlex.split(args),
        download_path=pathlib.Path(os.getcwd()),
    )

    process = psutil.Process(task.process.pid)

    # Print the process's parent id
    print process.ppid()
