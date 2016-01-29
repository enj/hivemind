#!/usr/bin/env python
# encoding: utf-8


class TaskQueue(object):
    def __init__(self, *pipelines):
        self.num_tasks = sum(len(p) for p in pipelines)
        self.queue = [p.head for p in pipelines]

    def push(self, task):
        if task:
            self.queue.append(task)

    def pop(self):
        if self.queue:
            return self.queue.pop(0)

    def __len__(self):
        return self.queue.__len__()
