#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mo made me."""

from mpi4py import MPI
from argparse import ArgumentParser
from time import time
from collections import defaultdict as dd

from networkx import topological_sort

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks


size = MPI.COMM_WORLD.Get_size()

parser = ArgumentParser(description="MIS Testing")
parser.add_argument("-j", "--json", nargs="+", help="JSON files", required=True)
args = parser.parse_args()

tasks = [task for j in args.json for task in json_to_tasks(j)]

for t, _ in tasks:  # Do no parse booleans
    t.skip = t.shell = False

framework = PipelineFramework(tasks)

ConcretePipeline.validate_field = lambda self, field: None  # Do not validate
pipeline = ConcretePipeline(0, framework, {}, "")

start = time()

if size == 1:
    nodes = topological_sort(pipeline.dag, reverse=True)
    while nodes:
        print pipeline.mc
        node = nodes.pop()
        pipeline.set_done(node)
        pipeline.update_max_concurrency()
else:
    rounds = 2**10
    counts = dd(int)
    for _ in xrange(rounds):
        pipeline.update_max_concurrency()
        counts[pipeline.mc] += 1
    print counts

print "Took {}s to get concurrency".format((time() - start))
