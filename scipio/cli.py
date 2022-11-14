#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: scipio.cli
.. moduleauthor:: Richard Julian <richard@rjulian.net>
"""
import logging
import click
from .__init__ import __version__
from .aws import Aws
from .aws_iam import AwsIam

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Context:
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Context, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(context: Context, verbose: int):
    """Run scipio."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    context.verbose = verbose


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.group()
@pass_info
def aws(context: Context):
    """Work within the context of AWS cloud."""
    context.aws = Aws()


@aws.command()
@pass_info
def info(context: Context):
    """Gives you account info."""
    click.echo(context.aws.display_configured_account(), nl=False)


@aws.group()
@pass_info
def iam(context: Context):
    """IAM related actions and scanning"""
    context.aws_iam = AwsIam(context.aws)


@iam.command()
@pass_info
def create_privileged_access(context: Context):
    """Generates users and policies that allow for privilege escalation."""
    context.aws_iam.create_user_privileged_access()
    click.echo("Created privileged access.")


@iam.command()
@pass_info
def destroy_aws_iam_resources(context: Context):
    """Destroys users and policies created by scipio"""
    context.aws_iam.destroy_scipio_users_policies()
    click.echo("Destroyed user resources.")
