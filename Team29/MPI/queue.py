#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TODO."""


class TaskQueue(object):
    """[summary].

    [description]
    """

    def __init__(self, *pipelines):
        """[summary].

        [description]
        :param *pipelines: [description]
        :type *pipelines: [type]
        """
        self.num_tasks = sum(len(p) for p in pipelines)
        self.queue = [p.head for p in pipelines]

    def push(self, task):
        """[summary].

        [description]
        :param task: [description]
        :type task: [type]
        """
        if task:
            self.queue.append(task)

    def pop(self):
        """[summary].

        [description]
        :returns: [description]
        :rtype: {[type]}
        """
        if self.queue:
            return self.queue.pop(0)

    def __len__(self):
        """[summary].

        [description]
        :returns: [description]
        :rtype: {[type]}
        """
        return self.queue.__len__()
