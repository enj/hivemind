#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI
from time import sleep
from argparse import ArgumentParser
from traceback import print_exc

from hivemind.pipeline import PipelineFramework, ConcretePipeline, rank_by_total_successors as ranker
from hivemind.util import MASTER, tags, json_to_tasks, read_csv
from hivemind.mpi import Master, Worker

try:

    if __debug__:
        from logging import basicConfig, getLogger, DEBUG
        basicConfig(level=DEBUG)
        log = getLogger(__name__)

    rank = MPI.COMM_WORLD.Get_rank()

    if __debug__:
        log.debug("I am node {} running on processor {}".format(rank, MPI.Get_processor_name()))

    if rank == MASTER:

        parser = ArgumentParser(description="Example of running a MPI pipeline")
        parser.add_argument('-j', '--json', action='append', help="JSON files", required=True)
        parser.add_argument('-c', '--csv', action='append', help="CSV files", required=True)
        parser.add_argument('-p', '--checkpoint', help="Checkpoint directory", required=True)
        args = parser.parse_args()

        tasks = [task for j in args.json for task in json_to_tasks(j)]
        patients = [patient for c in args.csv for patient in read_csv(c)]

        framework = PipelineFramework(tasks)
        ranker(framework)

        concrete_pipelines = [
            ConcretePipeline(i, framework, data, args.checkpoint)
            for i, data in enumerate(patients)
        ]

        m = Master(MPI, concrete_pipelines)
        while m.closed_workers != m.total_workers:
            m.receive()
            m.orchestrate()

    else:

        size = MPI.COMM_WORLD.Get_size()
        comm = 16
        mod = size / comm + 1
        sleep(rank % mod)

        w = Worker(MPI)
        w.send()
        while w.tag != tags.EXIT:
            w.receive()
            w.run()

        if __debug__:
            log.debug("Worker {} spent {} seconds waiting for the master".format(rank, w.wait_time))

    if __debug__:
        log.debug("Node {} running on processor {} EXITing".format(rank, MPI.Get_processor_name()))

except:
    print_exc()
    MPI.COMM_WORLD.Abort(1)
