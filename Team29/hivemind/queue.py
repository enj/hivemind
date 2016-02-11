#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Contains different implementations of queues."""

from collections import deque

from .pipeline import ConcretePipeline
from .util import zero_in_degree


class TaskQueue(object):
    """A TaskQueue is a set of Tasks that belong to different Pipelines.

    The order of Tasks is arbitrary as they are unrelated.
    """

    def __init__(self, pipelines):
        """Construct a TaskQueue based on the given Pipelines.

        :param *pipelines: the Pipelines to queue
        :type *pipelines: iterable of Pipelines
        """
        self.queue = deque()
        self.num_tasks = sum(len(p) for p in pipelines)
        for p in pipelines:
            self.extend(zero_in_degree(p.dag)) #TODO test

    def append(self, task):
        """Add the given Task to the right of the TaskQueue.

        :param task: the Task to add
        :type task: Task
        """
        if task:
            self.queue.append(task)

    def extend(self, tasks):
        """Add the given Task to the right of the TaskQueue.

        :param task: the Task to add
        :type task: Task
        """
        if tasks:
            self.queue.extend(tasks)

    def popleft(self):
        """Remove the leftmost Task from the TaskQueue.

        :returns: the leftmost Task from the TaskQueue
        :rtype: {Task}
        """
        return self.queue.popleft()

    def __len__(self):
        """Determine the length of the TaskQueue.

        :returns: the number of Tasks in this TaskQueue
        :rtype: {int}
        """
        return self.queue.__len__()


class WorkerQueue(object):
    """A WorkerQueue is a set of Tasks that belong to different Pipelines.

    The order of Tasks is arbitrary as they are unrelated.
    """

    def __init__(self):
        """Construct a TaskQueue based on the given Pipelines.

        :param *pipelines: the Pipelines to queue
        :type *pipelines: iterable of Pipelines
        """
        self.queue = deque()

    def append(self, worker):
        """Add the given Task to the right of the TaskQueue.

        :param task: the Task to add
        :type task: Task
        """
        self.queue.append(worker)

    def popleft(self):
        """Remove the leftmost Task from the TaskQueue.

        :returns: the leftmost Task from the TaskQueue
        :rtype: {Task}
        """
        return self.queue.popleft()

    def __len__(self):
        """Determine the length of the TaskQueue.

        :returns: the number of Tasks in this TaskQueue
        :rtype: {int}
        """
        return self.queue.__len__()
