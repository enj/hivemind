#!/usr/bin/env python
# encoding: utf-8

from mpi4py import MPI

from task import Task
from pipeline import Pipeline
from util import MASTER, tags
from master import Master
from worker import Worker
from queue import TaskQueue

a = Task("/Users/srbaucom/Documents1", "a.out")
b = Task("/Users/srbaucom/Documents2", "a.out")
c = Task("/Users/srbaucom/Documents3", "a.out")
p = Pipeline(a, b, c)
q = TaskQueue(p)

rank = MPI.COMM_WORLD.rank

if rank == MASTER:
	m = Master(MPI, q)
	while m.completed_tasks != m.num_tasks:
		m.receive()
else:
	w = Worker(MPI)
	while w.tag != tags.EXIT:
		w.receive()
