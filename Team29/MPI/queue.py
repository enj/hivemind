#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Queue of Tasks."""

from collections import deque


class TaskQueue(object):
    """A TaskQueue is a set of Tasks that belong to different Pipelines.

    The order of Tasks is arbitrary as they are unrelated.
    """

    def __init__(self, *pipelines):
        """Construct a TaskQueue based on the given Pipelines.

        :param *pipelines: the Pipelines to queue
        :type *pipelines: iterable of Pipelines
        """
        self.num_tasks = sum(len(p) for p in pipelines)
        self.queue = deque(p.head for p in pipelines)

    def push(self, task):
        """Add the given Task to the right of the TaskQueue.

        :param task: the Task to add
        :type task: Task
        """
        if task:
            self.queue.append(task)

    def pop(self):
        """Remove the leftmost Task from the TaskQueue.

        :returns: the leftmost Task from the TaskQueue
        :rtype: {Task}
        """
        if self.queue:
            return self.queue.popleft()

    def __len__(self):
        """Determine the length of the TaskQueue.

        :returns: the number of Tasks in this TaskQueue
        :rtype: {int}
        """
        return self.queue.__len__()
