#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Worker node."""

from ..util import tags, MASTER


class Worker(object):
    """A Worker node runs Tasks that are provided by the Master node."""

    def __init__(self, mpi, master=MASTER):
        """Construct a Worker with the global MPI object.

        :param mpi: the global MPI object
        :type mpi: MPI
        :param master: the id of the Master node, defaults to MASTER (0)
        :type master: int, optional
        """
        self.mpi = mpi
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.tag = tags.WORK
        self.master = master

        if __debug__:
            name = mpi.Get_processor_name()
            rank = self.comm.Get_rank()

            from logging import getLogger
            self.log = getLogger("{} {} {}".format(__name__, name, rank))

    def send(self, message):
        """Send the given message to the Master node.

        :param message: the message to send
        :type message: object
        """
        self.comm.send(message, dest=self.master, tag=self.tag)

    def receive(self):
        """Receive and act upon a message/Task from the Master node."""
        task = self.comm.recv(source=self.master, tag=self.mpi.ANY_TAG, status=self.status)
        self.tag = self.status.Get_tag()

        if self.tag == tags.WORK:
            self.task = task

    def run(self):
        """Run the current Task unless exiting.  Sends the PID and UID to the Master after completion."""
        if self.tag == tags.EXIT:
            return

        if __debug__:
            self.log.debug("Start Task {}".format(self.task._uid))

        if self.task.skip is False:  # This should always be False
            self.task.run()

        if __debug__:
            self.log.debug("Finished Task {}".format(self.task))

        self.send((self.task._pid, self.task._uid))

    def loop(self):
        """Loop between receive and run until told to exit."""
        while self.tag != tags.EXIT:
            self.receive()
            self.run()
