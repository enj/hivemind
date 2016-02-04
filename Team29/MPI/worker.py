#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents a Worker node."""

#from time import sleep

from util import tags, MASTER


class Worker(object):
    """A Worker node runs Tasks that are provided by the Master node.

    :param SLEEP_TIME: Time to sleep during WAIT stage
    :type SLEEP_TIME: int
    """

    #SLEEP_TIME = 10

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
        # self.tag = tag
        self.comm.send(task, dest=MASTER, tag=self.tag)

    def receive(self):
        """Receive and act upon a message from the Master node."""
        task = self.comm.recv(source=MASTER, tag=self.mpi.ANY_TAG, status=self.status)
        self.tag = self.status.Get_tag()

        if self.tag == tags.WORK:
            self.run(task)

        # if self.tag == tags.START:
        #     self.run(task)
        # elif self.tag == tags.WAIT:
        #
        #     if __debug__:
        #         self.log.debug("WAITing")
        #
        #     sleep(self.SLEEP_TIME)
        #     self.ready()

    def run(self, task):
        """Run the given Task.

        :param task: the Task to run
        :type task: Task
        """
        if __debug__:
            self.log.debug("Start Task %s" % task)

        task.run()
        #self.done(task)
        self.send(task.next)

    # def ready(self, task=None):
    #     """Signal to the Master that this Worker is done with the given Task.
    #
    #     This is accomplished by sending the next Task in the Pipeline to the Master.
    #
    #     :param task: the current (completed) Task in the Pipeline
    #     :type task: Task
    #     """
    #     self.send(task, tags.WORK) # TODO probably don't need WORK anymore

    # def ready(self):
    #     """Signal to the Master that this Worker is ready for more Tasks."""
    #     self.send(None, tags.READY)
