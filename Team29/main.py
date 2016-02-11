#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import MASTER, tags, json_to_tasks, read_csv
from hivemind.master import Master
from hivemind.worker import Worker

if __debug__:
    from logging import basicConfig, getLogger, DEBUG
    basicConfig(level=DEBUG)
    log = getLogger(__name__)


json_file = 'pipeline.json'
csv_file = 'test.csv'
rank = MPI.COMM_WORLD.Get_rank()

if __debug__:
    log.debug("I am node %d running on processor %s" % (rank, MPI.Get_processor_name()))

if rank == MASTER:
    tasks = json_to_tasks(json_file)
    framework = PipelineFramework(tasks)
    patients = read_csv(csv_file)
    concrete_pipelines = []
    for i, row in enumerate(patients):
        concrete_pipelines.append(ConcretePipeline(i, framework, row))

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
