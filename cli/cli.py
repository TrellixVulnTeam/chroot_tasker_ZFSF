"""
CLI for creating and interacting with tasks.
"""

import os
import pathlib
import shlex

from signal import Signals

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

    print(task.id)


@cli.command('health_check')
@click.argument('task_id')
def health_check(task_id):
    """
    Check the health of a task.

    :param str task_id: The id of an existing task.
    """
    task = Task(existing_task=int(task_id))
    health = task.get_health()
    print('exists: ' + health['exists'])
    print('status: ' + health['status'])


@cli.command('send_signal')
@click.argument('task_id')
@click.argument('signal')
def send_signal(task_id, signal):
    """
    Send a signal to a process started by an existing task.

    :param str task_id: The id of an existing task.
    :param str signal: The signal to send.
    """
    task = Task(existing_task=int(task_id))
    task.send_signal(Signals[signal])
