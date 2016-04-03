#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Demo of running a MPI Pipeline."""

from mpi4py import MPI
from argparse import ArgumentParser
from traceback import print_exc

from hivemind.pipeline import rank_by_total_successors, rank_by_successors
from hivemind.util import MASTER, json_to_tasks, read_csv
from hivemind.mpi import Master, Worker

try:

    if __debug__:
        from logging import basicConfig, getLogger, DEBUG
        basicConfig(level=DEBUG)
        log = getLogger(__name__)

    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    if __debug__:
        log.debug("I am node {} running on processor {}".format(rank, MPI.Get_processor_name()))

    if rank == MASTER:

        rankers = (rank_by_total_successors, rank_by_successors)
        rankers_help = ", ".join("{}: {}".format(i, f.func_name) for i, f in enumerate(rankers))

        parser = ArgumentParser(description="Example of running a MPI pipeline")
        parser.add_argument("-j", "--json", nargs="+", help="JSON files", required=True)
        parser.add_argument("-c", "--csv", nargs="+", help="CSV files", required=True)
        parser.add_argument("-p", "--checkpoint", help="Optional checkpoint directory")
        parser.add_argument("-r", "--ranker", type=int, choices=xrange(len(rankers)),
                            help="Optional rank function ID as %(type)s (for task priority) {}".format(rankers_help))
        args = parser.parse_args()
        ranker = rankers[args.ranker] if args.ranker is not None else None

        if size == 1:
            raise ValueError("No workers available, number of MPI processes must be greater than one.")

        tasks = [task for j in args.json for task in json_to_tasks(j)]
        patients = [patient for c in args.csv for patient in read_csv(c)]

        m = Master(MPI, tasks, patients, ranker, args.checkpoint)
        m.loop()

    else:

        w = Worker(MPI)
        w.loop()

        if __debug__:
            log.debug("Worker {} spent {} seconds waiting for the master".format(rank, w.wait_time))

    if __debug__:
        log.debug("Node {} running on processor {} EXITing".format(rank, MPI.Get_processor_name()))

except BaseException as e:
    if not isinstance(e, SystemExit):
        print_exc()
    MPI.COMM_WORLD.Abort(1)
