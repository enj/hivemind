#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import MASTER, tags, json_to_tasks, read_csv
from hivemind.master import Master
from hivemind.worker import Worker
from hivemind.rank import rank_by_total_successors as ranker

if __debug__:
    from logging import basicConfig, getLogger, DEBUG
    basicConfig(level=DEBUG)
    log = getLogger(__name__)


rank = MPI.COMM_WORLD.Get_rank()

if __debug__:
    log.debug("I am node %d running on processor %s" % (rank, MPI.Get_processor_name()))

if rank == MASTER:

    checkpoint_dir = 'progress'
    json_file = 'sarah.json'
    csv_file = 'sarah.csv'

    tasks = json_to_tasks(json_file)
    patients = read_csv(csv_file)

    framework = PipelineFramework(tasks)
    ranker(framework)

    concrete_pipelines = []
    completed_tasks = 0

    for i, data in enumerate(patients):
        p = ConcretePipeline(i, framework, data, checkpoint_dir)
        concrete_pipelines.append(p)
        for task in p.dag.nodes_iter():
            if p.is_done_by_file(task):
                completed_tasks += 1

    m = Master(MPI, concrete_pipelines, checkpoint_dir, completed_tasks)
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
