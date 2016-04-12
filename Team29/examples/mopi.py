#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Mo made me."""

# from mpi4py import MPI
from argparse import ArgumentParser

from networkx import OrderedDiGraph, topological_sort_recursive

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks
import time

# rank = MPI.COMM_WORLD.Get_rank()
# size = MPI.COMM_WORLD.Get_size()

parser = ArgumentParser(description="Utility for 'printing' a pipeline")
parser.add_argument("-j", "--json", nargs="+", help="JSON files", required=True)
args = parser.parse_args()

tasks = [task for j in args.json for task in json_to_tasks(j)]
patients = [{}]

PipelineFramework.DiGraph = OrderedDiGraph
framework = PipelineFramework(tasks)

ConcretePipeline.validate_field = lambda x, y: True  # Do not validate
concrete_pipelines = [
    ConcretePipeline(i, framework, data, "")
    for i, data in enumerate(patients)
]

pipeline = concrete_pipelines[0]
nodes = topological_sort_recursive(pipeline.dag)


start = time.time()
# while nodes:
#     node = nodes.pop()
#     start = time.time()
#     print framework.get_max_concurrency()
#     print "Took {}s to get concurrency".format((time.time()-start))
#     framework.dag.node[node]['done'] = True

# counts = {}
# for _ in xrange(64):
#     nodes = topological_sort_recursive(framework.dag)
#     for n in nodes:
#         framework.dag.node[n]['done'] = False
#     st = ""
#     while nodes:
#         node = nodes.pop()
#         st += "{}".format(framework.get_max_concurrency())
#         framework.dag.node[node]['done'] = True

#     if not st in counts:
#         counts[st] = 1
#     else:
#         counts[st] += 1
# print counts
# for node in nodes:
#     if node._uid == "A" or node._uid == "C" or node._uid == "E" or node._uid == "G":
#         pipeline.set_done(node)

while nodes:
    node = nodes.pop()
    pipeline.update_max_concurrency()
    print pipeline.mc
    pipeline.set_done(node)
print "Took {}s to get concurrency".format((time.time() - start))
