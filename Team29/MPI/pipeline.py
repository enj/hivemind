#!/usr/bin/env python
# encoding: utf-8


class Pipeline(object):

    def __init__(self, *tasks):
        assert tasks
        self.len = 1
        i = tasks.__iter__()
        self.head = i.next()
        current = self.head
        try:
            while True:
                temp = i.next()
                current.link(temp)
                current = temp
                self.len += 1
        except StopIteration, _:
            pass

    def __len__(self):
        return self.len
