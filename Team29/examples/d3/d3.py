#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""D3 Pipeline Printer."""

from random import seed, choice
from argparse import ArgumentParser

from networkx import DiGraph
from networkx.drawing.nx_pydot import write_dot

from hivemind.pipeline import PipelineFramework
from hivemind.util import json_to_tasks

from http_server import load_url

parser = ArgumentParser(description="Utility for 'printing' a pipeline")
parser.add_argument('-j', '--json', action='append', help="JSON files", required=True)
parser.add_argument('-s', '--seed', type=int, default=2016, help="Optional seed for random coloring")
args = parser.parse_args()

seed(args.seed)
tasks = [task for j in args.json for task in json_to_tasks(j)]

framework = PipelineFramework(tasks)

with open("colors.txt", "rb") as f:
    colors = [c.strip() for c in f]

G = DiGraph()
for task in framework.dag.nodes_iter():
    G.add_node(task._uid)
    for successor in framework.dag.successors(task):
        G.add_edge(task._uid, successor._uid)

G.graph["node"] = dict(rx=5, ry=5, labelStyle="font: 300 14px 'Helvetica Neue', Helvetica")
G.graph["edge"] = dict(labelStyle="font: 300 14px 'Helvetica Neue', Helvetica")

for attr in G.edge.itervalues():
    for edge in attr:
        attr[edge]["style"] = "stroke: #454545; stroke-width: 2px;"
        attr[edge]["arrowheadStyle"] = "fill: #454545"

for attr in G.node.itervalues():
    attr["style"] = "fill: {}".format(choice(colors))

write_dot(G, "graph.txt")

load_url("d3.html")
