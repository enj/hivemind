#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Represents the Master node."""

from Queue import PriorityQueue, Queue

from ..util import tags, make_path, tmp_checkpoint_dir, join
from ..pipeline import PipelineFramework, ConcretePipeline


class Master(object):
    """The Master node controls the Worker nodes."""

    def __init__(self, mpi, tasks, patients, ranker=None, checkpoint_dir=None, dry_run=False):
        """Create the Master node which maintains all the concrete pipelines and the Worker/Task queues.

        :param mpi: the global MPI object
        :type mpi: global MPI object
        :param tasks: the Tasks and their requirements
        :type tasks: iterable of tuples, each with a Task and its list of required UIDs
        :param patients: iterable of directories, one dictionary per row in the patient data
        :type patients: iterable
        :param ranker: Ranker function to use on PipelineFramework, defaults to None
        :type ranker: function, optional
        :param checkpoint_dir: directory for checkpointing, randomly generated if unspecified, defaults to None
        :type checkpoint_dir: string, optional
        :param dry_run: Turns off checkpointing regardless of any other configuration, defaults to False
        :type dry_run: bool, optional
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
        # We no longer use sent_tasks but get_completed_tasks still needs to be called for all concrete_pipelines
        # get_completed_tasks must be called before calling get_ready_tasks
        self.sent_tasks = sum(p.get_completed_tasks() for p in self.concrete_pipelines)
        self.out_tasks = {}
        self.closed_workers = 0
        self.dry_run = dry_run

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
        """
        If there are ready Tasks and idle Workers, send the Tasks to the Workers.

        If there are more Workers than the max concurrency of the concrete pipelines,
        close out the unnecessary Workers.
        """
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
            w = self.workers.get()
            self.send(w, None, tags.EXIT)
            self.closed_workers += 1

        # This is the old logic for closing out Workers
        # Left in place in case the max concurrency stuff does not work out
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
        """Wait to receive a completion message from a Worker node.

        This finishes the associated Task and enqueues the sending Worker.
        """
        message = self.comm.recv(source=self.mpi.ANY_SOURCE, tag=self.mpi.ANY_TAG, status=self.status)
        source = self.status.Get_source()

        if __debug__:
            self.log.debug("Received {} from {}".format(message, source))

        self.finish_task(self.out_tasks.pop(message))
        self.workers.put(source)

    def finish_task(self, task):
        """Finish the given Task.

        This involves checkpointing, setting it as done, updating
        the max concurrency and queuing the ready successors.

        :param task: the input Task
        :type task: Task
        """
        self.checkpoint(task)
        pipeline = self.concrete_pipelines[task._pid]
        pipeline.set_done(task)
        pipeline.update_max_concurrency()
        for t in pipeline.get_ready_successors(task):
            self.queue.put(t)

    def checkpoint(self, task):
        """Checkpoint the given Task by creating the _.done file.

        :param task: the input Task
        :type task: Task
        """
        if self.dry_run:
            return

        f = join(self.checkpoint_dir, str(task._pid), str(task._uid), "_.done")
        make_path(f)

        if __debug__:
            self.log.debug("Creating checkpoint for {}".format(f))

        # Create the file if it does not exist
        open(f, "a").close()

    def max_concurrency(self):
        """Get the max concurrency based on all the concrete pipelines.

        :returns: the max concurrency
        :rtype: {int}
        """
        return sum(p.mc for p in self.concrete_pipelines)

    def loop(self):
        """Loop between receive and orchestrate until all Workers are closed."""
        self.orchestrate()
        while self.closed_workers != self.total_workers:
            self.receive()
            self.orchestrate()
