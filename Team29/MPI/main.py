#!/usr/bin/env python
# encoding: utf-8

from mpi4py import MPI

from task import Task
from pipeline import Pipeline
from util import MASTER, tags
from master import Master
from worker import Worker
from queue import TaskQueue

s1 = Task("/pvfs2/srbaucom/bin", "app", "This ")
s2 = Task("/pvfs2/srbaucom/bin", "app", "is ")
s3 = Task("/pvfs2/srbaucom/bin", "app", "a ")
s4 = Task("/pvfs2/srbaucom/bin", "app", "test ")
s5 = Task("/pvfs2/srbaucom/bin", "app", "sentence.")
sp = Pipeline(s1, s2, s3, s4, s5)


q = TaskQueue(sp)

rank = MPI.COMM_WORLD.rank

if rank == MASTER:
    m = Master(MPI, q)
    while m.completed_tasks != m.num_tasks:
        m.receive()
else:
    w = Worker(MPI)
    while w.tag != tags.EXIT:
        w.receive()
