#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from util import tags
from queue import WorkerQueue


class Master(object):
    """The Master node controls the Worker nodes."""

    def __init__(self, mpi, queue):
        """Construct a Master node that will work on the given TaskQueue.

        :param mpi: the global MPI object
        :type mpi: global MPI object
        :param queue: the TaskQueue to work on
        :type queue: TaskQueue
        """
        self.queue = queue
        self.workers = WorkerQueue()
        self.sent_tasks = 0
        # self.completed_tasks = 0
        self.closed_workers = 0

        self.mpi = mpi
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.total_workers = self.comm.Get_size() - 1

        if __debug__:
            name = mpi.Get_processor_name()

            from logging import getLogger
            self.log = getLogger("%s %s" % (__name__, name))

    def orchestrate(self):
        """TODO"""
        while self.queue and self.workers:
            w = self.workers.popleft()
            t = self.queue.popleft()
            self.send(w, t, tags.WORK)
            self.sent_tasks += 1

        if self.sent_tasks == self.queue.num_tasks:
            while self.workers:
                w = self.workers.popleft()
                self.send(w, None, tags.EXIT)
                self.closed_workers += 1

    def send(self, target, task, tag):
        """Send the given Task to the target Worker node with the specified Tag.

        :param target: the rank of the Worker node to send to
        :type target: int
        :param task: the Task to send
        :type task: Task
        :param tag: the specified Tag
        :type tag: Tag Enum
        """
        if __debug__:
            self.log.debug("Sending %s to %d with Tag %d" % (task, target, tag))

        self.comm.send(task, dest=target, tag=tag)

    def receive(self):
        """Wait to receive a Task from a Worker node."""
        task = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
        self.queue.append(task)
        source = self.status.Get_source()
        self.workers.append(source)

        if __debug__:
            self.log.debug("Received %s from %d" % (task, source))
