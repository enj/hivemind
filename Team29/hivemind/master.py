#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from Queue import PriorityQueue
from os.path import dirname, exists
from os import makedirs

from .util import tags
from .queue import WorkerQueue


class Master(object):
    """The Master node controls the Worker nodes."""

    def __init__(self, mpi, concrete_pipelines, checkpoint_dir, sent_tasks=0):
        """Construct a Master node that will work on the given TaskQueue.

        :param mpi: the global MPI object
        :type mpi: global MPI object
        :param queue: the TaskQueue to work on
        :type queue: TaskQueue
        """
        self.queue = PriorityQueue()
        self.workers = WorkerQueue()
        self.concrete_pipelines = concrete_pipelines
        self.sent_tasks = sent_tasks
        self.checkpoint_dir = checkpoint_dir
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
            self.log = getLogger("%s %s" % (__name__, name))

    def orchestrate(self):
        """TODO"""
        while not self.queue.empty() and self.workers:
            w = self.workers.popleft()
            t = self.queue.get(True)
            self.send(w, t, tags.WORK)
            self.sent_tasks += 1

        if self.sent_tasks == self.num_tasks:
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
        source = self.status.Get_source()

        if __debug__:
            self.log.debug("Received %s from %d" % (task, source))

        if task:
            pipeline = self.concrete_pipelines[task._pid]
            pipeline.set_done(task)
            self.checkpoint(task._pid, task._uid)
            ready_successors = pipeline.get_ready_successors(task)
            for t in ready_successors:
                self.queue.put(t)

        self.workers.append(source)

    def checkpoint(self, pid, uid):
        f = "%s/%d/%s/_.done" % (self.checkpoint_dir, pid, uid)
        basedir = dirname(f)
        if not exists(basedir):
            makedirs(basedir)

        if __debug__:
            self.log.debug("Creating checkpoint for %s" % path)

        open(f, 'a').close()
