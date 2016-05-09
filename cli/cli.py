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
    """
    task = Task(
        image_url=image_url,
        args=shlex.split(args),
        download_path=pathlib.Path(os.getcwd()),
    )

    print task.id


@cli.command('health_check')
@click.argument('task_id')
def health_check(task_id):
    """
    TODO
    """


@cli.command('send_signal')
@click.argument('task_id')
@click.argument('signal')
def send_signal(task_id, signal):
    """
    TODO
    """
