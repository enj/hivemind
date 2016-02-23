#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from Queue import PriorityQueue, Queue

from ..util import tags, make_path


class Master(object):
    """The Master node controls the Worker nodes."""

    def __init__(self, mpi, concrete_pipelines):
        """Construct a Master node that will work on the given TaskQueue.

        :param mpi: the global MPI object
        :type mpi: global MPI object
        :param queue: the TaskQueue to work on
        :type queue: TaskQueue
        """
        self.queue = PriorityQueue()
        self.workers = Queue()
        self.concrete_pipelines = concrete_pipelines
        self.sent_tasks = sum(p.get_completed_tasks() for p in concrete_pipelines)
        self.out_tasks = {}
        self.checkpoint_dir = concrete_pipelines[0].checkpoint_dir
        self.closed_workers = 0

        self.mpi = mpi
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()
        self.total_workers = self.comm.Get_size() - 1

        self.num_tasks = sum(len(p) for p in self.concrete_pipelines)
        for p in self.concrete_pipelines:
            for task in p.get_ready_tasks():
                self.queue.put(task)

        if __debug__:
            name = mpi.Get_processor_name()

            from logging import getLogger
            self.log = getLogger("{} {}".format(__name__, name))

    def orchestrate(self):
        """TODO"""
        while not self.queue.empty() and not self.workers.empty():
            w = self.workers.get()
            t = self.queue.get()
            self.send(w, t, tags.WORK)
            self.out_tasks[(t._pid, t._uid)] = t
            self.sent_tasks += 1

        if self.sent_tasks == self.num_tasks:
            while not self.workers.empty():
                w = self.workers.get()
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
            self.log.debug("Sending {} to {} with Tag {}".format(task, target, tag))

        self.comm.send(task, dest=target, tag=tag)

    def receive(self):
        """Wait to receive a Task from a Worker node."""
        message = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
        source = self.status.Get_source()

        if __debug__:
            self.log.debug("Received {} from {}".format(message, source))

        if message:
            task = self.out_tasks[message]
            del self.out_tasks[message]

            pid, uid = message
            pipeline = self.concrete_pipelines[pid]
            pipeline.set_done(task)
            self.checkpoint(pid, uid)
            ready_successors = pipeline.get_ready_successors(task)
            for t in ready_successors:
                self.queue.put(t)

        self.workers.put(source)

    def checkpoint(self, pid, uid):
        f = "{}/{}/{}/_.done".format(self.checkpoint_dir, pid, uid)
        make_path(f)

        if __debug__:
            self.log.debug("Creating checkpoint for {}".format(f))

        open(f, "a").close()
