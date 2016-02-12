#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Worker node."""

from .util import tags, MASTER


class Worker(object):
    """A Worker node runs Tasks that are provided by the Master node.

    :param SLEEP_TIME: Time to sleep during WAIT stage
    :type SLEEP_TIME: int
    """

    def __init__(self, mpi):
        """Construct a Worker with the global MPI object.

        :param mpi: the global MPI object
        :type mpi: MPI
        """
        self.mpi = mpi
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.tag = tags.WORK

        if __debug__:
            name = mpi.Get_processor_name()
            rank = self.comm.Get_rank()

            from logging import getLogger
            self.log = getLogger("%s %s %d" % (__name__, name, rank))

    def send(self, task=None):
        """Send the given Task to the Master node using the supplied Tag.

        :param tag: the Tag of the message
        :type tag: Tag Enum
        :param task: the Task to send
        :type task: Task
        """
        self.comm.send(task, dest=MASTER, tag=self.tag)

    def receive(self):
        """Receive and act upon a message from the Master node."""
        task = self.comm.recv(source=MASTER, tag=self.mpi.ANY_TAG, status=self.status)
        self.tag = self.status.Get_tag()

        if self.tag == tags.WORK:
            self.task = task

    def run(self):
        """Run the given Task.

        :param task: the Task to run
        :type task: Task
        """
        if self.tag == tags.EXIT:
            return

        if __debug__:
            self.log.debug("Start Task %s" % self.task)

        if self.task.skip is False:  # TODO should we log this?
            self.task.run()

        if __debug__:
            self.log.debug("Finished Task %s" % self.task)

        self.send(self.task)
