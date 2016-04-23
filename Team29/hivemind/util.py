#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents utility functions."""

from json import load
from csv import DictReader
from os.path import dirname, exists, join
from os import makedirs
from tempfile import gettempdir
from datetime import datetime


def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python.

    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    :param *sequential: the values of the enum (required)
    :type *sequential: iterable of strings
    :param **named: used to give names to sequential's items
    :type **named: dictionary
    :returns: a new enum type based on the input
    :rtype: {Enum}
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type("Enum", (), enums)

# Each of the different states a worker can be in
tags = enum("WORK", "EXIT")

# The MPI rank of the master
MASTER = 0


def json_to_tasks(f):
    """Convert the input JSON file to a list of Tasks.

    :param f: The input JSON file's location
    :type f: string
    :returns: A list of tuples each containing a Task and a list of requirements
    :rtype: {list}
    """
    from .pipeline import Task

    def task_decoder(t):
        """Convert JSON to Task.

        :param t: The dictionary representation of a Task and its requirements
        :type t: dictionary
        :returns: A tuple containing a Task and a list of requirements
        :rtype: {tuple}
        """
        return (
            Task(
                t["_uid"],
                t.get("skip", False),
                t.get("shell", False),
                t["exe"],
                t.get("verify_exe", None),
                t["wd"],
                *t.get("args", [])
            ),
            t.get("_requires", []),
        )

    with open(f, "rb") as fp:
        return load(fp, object_hook=task_decoder)


def read_csv(f):
    """Read the input CSV file.

    :param f: The input CSV file"s location
    :type f: string
    :returns: A list of directories, one dictionary per row in the CSV file
    :rtype: {list}
    """
    with open(f, "rb") as fp:
        return list(DictReader(fp, delimiter=","))


def to_bool(val):
    """Convert an input value to a bool.

    :param val: A value to convert to a val
    :returns: The boolean representation of val
    :rtype: {bool}
    :raises: ValueError
    """
    if isinstance(val, bool):
        return val

    orig = val

    convert = {
        "1": True,
        "0": False,
        "true": True,
        "false": False,
        "t": True,
        "f": False,
        "": False,
        None: False,
        1: True,
        0: False
    }

    if isinstance(val, unicode):
        val = val.encode("ascii", "ignore")
    if isinstance(val, str):
        val = val.lower()

    out = convert.get(val)
    if out is None:
        raise ValueError("{} cannot be converted to a bool.".format(orig))

    return out


def make_path(f):
    """Create the directory that the input file would be located in if it does not exist.

    :param f: the location of the input file
    :type f: string
    """
    basedir = dirname(f)
    if not exists(basedir):
        makedirs(basedir)


def tmp_checkpoint_dir():
    """Generate a (most likely unique) temporary directory for checkpointing.

    :returns: the path to the directory
    :rtype: {string}
    """
    return join(gettempdir(), __package__, datetime.now().strftime("%Y-%m-%dT%H_%M_%S.%f"))
