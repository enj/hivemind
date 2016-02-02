#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TODO"""


class TaskQueue(object):
    """TODO"""

    def __init__(self, *pipelines):
        """TODO"""
        self.num_tasks = sum(len(p) for p in pipelines)
        self.queue = [p.head for p in pipelines]

    def push(self, task):
        """TODO"""
        if task:
            self.queue.append(task)

    def pop(self):
        """TODO"""
        if self.queue:
            return self.queue.pop(0)

    def __len__(self):
        """TODO"""
        return self.queue.__len__()
