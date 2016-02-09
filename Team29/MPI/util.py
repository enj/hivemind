#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents utility functions."""

from json import load

from task import Task


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
    with open(f, 'r') as fp:
        return load(fp, object_hook=task_decoder)

def task_decoder(t):
    return (
        Task(
            t["uid"],
            t.get("skip", False),
            t["exe_path"],
            t["exe"],
            *t.get("args", [])
        ),
        t.get("requires", []),
    )
