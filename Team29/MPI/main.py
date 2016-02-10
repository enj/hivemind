#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI

from task import Task
from pipeline import PipelineFramework, ConcretePipeline
from util import MASTER, tags, json_to_tasks, read_csv
from master import Master
from worker import Worker
from queue import TaskQueue

if __debug__:
    from logging import basicConfig, getLogger, DEBUG
    basicConfig(level=DEBUG)
    log = getLogger(__name__)


rank = MPI.COMM_WORLD.Get_rank()

if __debug__:
    log.debug("I am node %d running on processor %s" % (rank, MPI.Get_processor_name()))

if rank == MASTER:
    # s1 = Task("/pvfs2/srbaucom/bin", "app", "This ")
    # s2 = Task("/pvfs2/srbaucom/bin", "app", "is ")
    # s3 = Task("/pvfs2/srbaucom/bin", "app", "a ")
    # s4 = Task("/pvfs2/srbaucom/bin", "app", "test ")
    # s5 = Task("/pvfs2/srbaucom/bin", "app", "sentence.\n")
    # sp = Pipeline(s1, s2, s3, s4, s5)

    # m1 = Task("/pvfs2/srbaucom/bin", "catter", "-in", "t1.txt", "-out", "t2.txt", "-cat", "This ", "-sleep", "5000")
    # m2 = Task("/pvfs2/srbaucom/bin", "catter", "-in", "t2.txt", "-out", "t3.txt", "-cat", "is ", "-sleep", "5000")
    # m3 = Task("/pvfs2/srbaucom/bin", "catter", "-in", "t3.txt", "-out", "t4.txt", "-cat", "Mo.", "-sleep", "5000")
    # mp = Pipeline(m1, m2, m3)

    tasks = json_to_tasks('pipeline.json')
    framework = PipelineFramework(*tasks)
    patients = read_csv('test.csv')
    concrete_pipelines = []
    for i, row in enumerate(patients):
        concrete_pipelines.append(ConcretePipeline(i, framework, row))

    #q = TaskQueue(sp, mp)
    m = Master(MPI, concrete_pipelines)
    while m.closed_workers != m.total_workers:
        m.receive()
        m.orchestrate()
else:
    w = Worker(MPI)
    w.send()
    while w.tag != tags.EXIT:
        w.receive()
        w.run()

if __debug__:
    log.debug("Node %d running on processor %s EXITing" % (rank, MPI.Get_processor_name()))
