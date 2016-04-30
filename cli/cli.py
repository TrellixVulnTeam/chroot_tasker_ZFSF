"""
CLI for creating and interacting with tasks.
"""

import click

# from tasker.tasker import Task

@click.group()
def cli():
    pass


@cli.command('create')
def create():
    pass
