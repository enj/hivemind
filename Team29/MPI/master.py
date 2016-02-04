#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from util import tags


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

    def send(self, target, task, tag):
        """Send the given Task to the target Worker node with the specified Tag.

        :param target: the rank of the Worker node to send to
        :type target: int
        :param task: the Task to send
        :type task: Task
        :param tag: the specified Tag
        :type tag: Tag Enum
        """
        self.comm.send(task, dest=target, tag=tag)

    def receive(self):
        """Wait to receive a Task from a Worker node."""
        task = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
        self.queue.push(task)
        source = self.status.Get_source()
        tag = self.status.Get_tag()

        if tag == tags.DONE:
            pass
            # TODO do we need done?
            # self.completed_tasks += 1
        elif tag == tags.READY:
            if self.queue:
                self.send(source, self.queue.pop(), tags.START)
                self.sent_tasks += 1
            elif self.sent_tasks == self.queue.num_tasks:

                if __debug__:
                    self.log.debug("Tell", source, "to exit")

                self.send(source, None, tags.EXIT)
                self.closed_workers += 1
            else:
                self.send(source, None, tags.WAIT)
