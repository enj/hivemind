#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TODO."""

from util import tags


class Master(object):
    """[summary].

    [description]
    """

    def __init__(self, mpi, queue):
        """[summary].

        [description]
        :param mpi: [description]
        :type mpi: [type]
        :param queue: [description]
        :type queue: [type]
        """
        self.queue = queue
        self.sent_tasks = 0
        self.completed_tasks = 0
        self.closed_workers = 0
        self.mpi = mpi
        self.name = mpi.Get_processor_name()
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.receive()

    def send(self, target, task, tag):
        """[summary].

        [description]
        :param target: [description]
        :type target: [type]
        :param task: [description]
        :type task: [type]
        :param tag: [description]
        :type tag: [type]
        """
        self.comm.send(task, dest=target, tag=tag)

    def receive(self):
        """[summary].

        [description]
        """
        task = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
        self.queue.push(task)
        source = self.status.Get_source()
        tag = self.status.Get_tag()
        if tag == tags.DONE:
            self.completed_tasks += 1
        elif tag == tags.READY:
            if self.queue:
                self.send(source, self.queue.pop(), tags.START)
                self.sent_tasks += 1
            elif self.sent_tasks == self.queue.num_tasks:
                # print "Master telling node", source, "to exit"
                self.send(source, None, tags.EXIT)
                self.closed_workers += 1
            else:
                # print "Master telling node", source, "to exit"
                self.send(source, None, tags.WAIT)
#                self.send(source, None, tags.EXIT)
#                self.closed_workers += 1
