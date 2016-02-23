#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI
from time import sleep
from argparse import ArgumentParser

from hivemind.pipeline import PipelineFramework, ConcretePipeline, rank_by_total_successors as ranker
from hivemind.util import MASTER, tags, json_to_tasks, read_csv
from hivemind.mpi import Master, Worker

if __debug__:
    from logging import basicConfig, getLogger, DEBUG
    basicConfig(level=DEBUG)
    log = getLogger(__name__)


rank = MPI.COMM_WORLD.Get_rank()

if __debug__:
    log.debug("I am node %d running on processor %s" % (rank, MPI.Get_processor_name()))

if rank == MASTER:
    checkpoint_dir = ''
    json_files = []
    csv_files = []

    try:
        parser = ArgumentParser(description="Process some stuff")
        parser.add_argument('-j', '--json', action='append', help="JSON files", required=True)
        parser.add_argument('-c', '--csv', action='append', help="CSV files", required=True)
        parser.add_argument('-p', '--checkpoint', help="Checkpoint directory", required=True)
        args = vars(parser.parse_args())
        checkpoint_dir = args['checkpoint']
        json_files = args['json']
        csv_files = args['csv']
    except:
        MPI.COMM_WORLD.Abort(1)

    tasks = []
    for j in json_files:
        for j2 in json_to_tasks(j):
            tasks.append(j2)

    patients = []
    for c in csv_files:
        for p in read_csv(c):
            patients.append(p)

    framework = PipelineFramework(tasks)
    ranker(framework)

    concrete_pipelines = [
        ConcretePipeline(i, framework, data, checkpoint_dir)
        for i, data in enumerate(patients)
    ]

    m = Master(MPI, concrete_pipelines)
    while m.closed_workers != m.total_workers:
        m.receive()
        m.orchestrate()
else:
    sleep(rank/64)
    w = Worker(MPI)
    w.send()
    while w.tag != tags.EXIT:
        w.receive()
        w.run()
    if __debug__:
        log.debug("Worker %d spent %d seconds waiting for the master" % (rank, w.wait_time))

if __debug__:
    log.debug("Node %d running on processor %s EXITing" % (rank, MPI.Get_processor_name()))
