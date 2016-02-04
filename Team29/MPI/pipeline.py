#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""


class Pipeline(object):
    """A Pipeline is a series of sequential Tasks."""

    def __init__(self, *tasks):
        """Construct a Pipeline based on the given Tasks by linking them together.

        :param *tasks: A list of Tasks from which to create the Pipeline
        :type *tasks: iterable of Tasks
        """
        self.len = len(tasks)
        self.head = tasks[0]

        for i in xrange(len(tasks) - 1):
            tasks[i].link(tasks[i + 1])

    def __len__(self):
        """Determine the length of the Pipeline.

        :returns: the number of Tasks in this Pipeline
        :rtype: {int}
        """
        return self.len
