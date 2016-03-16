#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents utility functions."""

from json import load
from csv import DictReader
from os.path import dirname, exists
from os import makedirs
from datetime import datetime


def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python.

    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    :param *sequential: the values of the enum (required)
    :type *sequential: iterable of strings
    :param **named: used to do reverse mapping from value to enum (optional)
    :type **named: dictionary
    :returns: a new enum type based on the input
    :rtype: {Enum}
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Each of the different states a worker can be in
tags = enum('WORK', 'EXIT')

# The MPI rank of the master
MASTER = 0


def json_to_tasks(f):

    from .pipeline import Task

    def task_decoder(t):
        return (
            Task(
                t["_uid"],
                t.get("skip", False),
                t["exe"],
                t.get("verify_exe", None),
                t["wd"],
                *t.get("args", [])
            ),
            t.get("_requires", []),
        )

    with open(f, 'r') as fp:
        return load(fp, object_hook=task_decoder)


def read_csv(f):
    with open(f, 'r') as fp:
        return list(DictReader(fp, delimiter=','))


def to_bool(val):
    if isinstance(val, bool):
        return val

    convert = {
        '1': True,
        '0': False,
        'true': True,
        'false': False,
        't': True,
        'f': False,
        '': False,
        None: False,
        1: True,
        0: False
    }

    if isinstance(val, unicode):
        val = val.encode('ascii', 'ignore')
    if isinstance(val, str):
        val = val.lower()

    out = convert.get(val)
    if out is None:
        raise ValueError("{} cannot be converted to a bool.".format(val))

    return out


def make_path(f):
    basedir = dirname(f)
    if not exists(basedir):
        makedirs(basedir)


def tmp_checkpoint_dir():
    return "/tmp/hivemind/{}".format(datetime.now().isoformat())
