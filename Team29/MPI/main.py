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

m1 = Task("/pvfs2/mmkhan/bin", "catter", "-in", "t1.txt", "-out", "t2.txt", "-cat", "This ")
m2 = Task("/pvfs2/mmkhan/bin", "catter", "-in", "t2.txt", "-out", "t3.txt", "-cat", "is ")
m3 = Task("/pvfs2/mmkhan/bin", "catter", "-in", "t3.txt", "-out", "t4.txt", "-cat", "Mo.")
mp = Pipeline(m1, m2, m3)


q = TaskQueue(sp, mp)
print("Pipelines added to Queue")

rank = MPI.COMM_WORLD.rank

if rank == MASTER:
    m = Master(MPI, q)
    while m.completed_tasks != m.num_tasks:
        m.receive()
else:
    w = Worker(MPI)
    while w.tag != tags.EXIT:
        w.receive()
