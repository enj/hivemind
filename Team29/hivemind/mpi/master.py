#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from Queue import PriorityQueue, Queue

from ..util import tags, make_path, tmp_checkpoint_dir, join
from ..pipeline import PipelineFramework, ConcretePipeline


class Master(object):
    """The Master node controls the Worker nodes."""

    def __init__(self, mpi, tasks, patients, ranker=None, checkpoint_dir=None):
        """Construct a Master node that will work on the given TaskQueue.

        :param mpi: the global MPI object
        :type mpi: global MPI object
        :param queue: the TaskQueue to work on
        :type queue: TaskQueue
        """

        self.checkpoint_dir = checkpoint_dir or tmp_checkpoint_dir()
        framework = PipelineFramework(tasks)
        if ranker:
            ranker(framework)

        self.concrete_pipelines = [
            ConcretePipeline(i, framework, data, self.checkpoint_dir)
            for i, data in enumerate(patients)
        ]

        self.queue = PriorityQueue()
        self.workers = Queue()

        # This takes checkpointing into consideration
        self.sent_tasks = sum(p.get_completed_tasks() for p in self.concrete_pipelines)
        self.out_tasks = {}
        self.closed_workers = 0

        self.mpi = mpi
        self.comm = mpi.COMM_WORLD
        self.status = mpi.Status()

        size = self.comm.Get_size()
        for w in xrange(1, size):
            self.workers.put(w)
        self.total_workers = size - 1

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
            self.sent_tasks += 1
            t = self.queue.get()
            if t.skip:
                self.finish_task(t)
                continue
            w = self.workers.get()
            self.send(w, t, tags.WORK)
            self.out_tasks[(t._pid, t._uid)] = t

        while not self.workers.empty() and ((self.total_workers - self.closed_workers) > self.max_concurrency()):
            #print "Current workers: {}\tMax Concurrency:{}".format(self.total_workers - self.closed_workers, self.max_concurrency())
            w = self.workers.get()
            self.send(w, None, tags.EXIT)
            self.closed_workers += 1

        # if self.sent_tasks == self.num_tasks:
        #     while not self.workers.empty():
        #         w = self.workers.get()
        #         self.send(w, None, tags.EXIT)
        #         self.closed_workers += 1

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

        self.finish_task(self.out_tasks.pop(message))
        self.workers.put(source)

    def finish_task(self, task):
        pipeline = self.concrete_pipelines[task._pid]
        pipeline.set_done(task)
        self.checkpoint(task)
        for t in pipeline.get_ready_successors(task):
            self.queue.put(t)

    def checkpoint(self, task):
        f = join(self.checkpoint_dir, str(task._pid), str(task._uid), "_.done")
        make_path(f)

        if __debug__:
            self.log.debug("Creating checkpoint for {}".format(f))

        open(f, "a").close()

    def max_concurrency(self):
        max_c = 0
        for p in self.concrete_pipelines:
            max_c += p.get_max_concurrency()
        return max_c

    def loop(self):
        self.orchestrate()
        while self.closed_workers != self.total_workers:
            self.receive()
            self.orchestrate()
