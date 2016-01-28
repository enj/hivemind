#!/usr/bin/env python
# encoding: utf-8

class Worker(object):
    def __init__(self, node):
        self.node = node

    def run(self, task):
        task.run()
        return task.next
