#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Pipeline of Tasks."""


class Pipeline(object):
    """A Pipeline is a series of sequential Tasks"""

    def __init__(self, *tasks):
        """Contstruct a Pipeline based on the given Tasks

        :param tasks: A list of Tasks from which to create the Pipeline
        :type tasks: iterable of Tasks
        """
        self.len = len(tasks)
        self.head = tasks[0]

        for i in xrange(len(tasks) - 1):
            tasks[i].link(tasks[i + 1])

    def __len__(self):
        """Returns the length of the Pipeline

        :returns: the number of tasks in this Pipeline
        """
        return self.len
