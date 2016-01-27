#!/usr/bin/env python
# encoding: utf-8


class JobQueue(object):
    def __init__(self, *pipelines):
        self.queue = [p.head for p in pipelines]

    def push(self, task):
        if task:
            self.queue.append(task)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)

    def __len__(self):
        return self.queue.__len__()
