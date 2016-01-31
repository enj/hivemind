#!/usr/bin/env python
# encoding: utf-8


class Pipeline(object):

    def __init__(self, *tasks):
        self.len = len(tasks)
        self.head = tasks[0]

        for i in xrange(len(tasks) - 1):
            tasks[i].link(tasks[i + 1])

    def __len__(self):
        return self.len
