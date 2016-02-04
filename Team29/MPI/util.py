#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents utility functions."""


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
