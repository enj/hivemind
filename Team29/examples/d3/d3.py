#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""D3 Pipeline Printer."""

from random import seed, shuffle
from argparse import ArgumentParser

from networkx import OrderedDiGraph
from networkx.drawing.nx_pydot import write_dot
from fuzzywuzzy import process

from hivemind.pipeline import PipelineFramework
from hivemind.util import json_to_tasks

from http_server import load_url


def get_key(task, choices, cutoff=90):
    """Get exe value for color keying."""
    exe = " ".join(task.cmd)
    data = process.extractOne(exe, choices, score_cutoff=cutoff)
    return data[0] if data else exe


def get_colors():
    """Get a list of colors in random order."""
    with open("colors.txt", "rb") as f:
        colors = [c.strip() for c in f]
    shuffle(colors)
    return colors

parser = ArgumentParser(description="Utility for 'printing' a pipeline")
parser.add_argument("-j", "--json", nargs="+", help="JSON files", required=True)
parser.add_argument("-s", "--seed", type=int, default=2016, help="Optional seed for random coloring")
args = parser.parse_args()

seed(args.seed)
tasks = [task for j in args.json for task in json_to_tasks(j)]

PipelineFramework.DiGraph = OrderedDiGraph
framework = PipelineFramework(tasks)

colors = get_colors()
colors_exe = {}
G = OrderedDiGraph(
    node=dict(rx=5, ry=5, labelStyle="font: 300 14px 'Helvetica Neue', Helvetica"),
    edge=dict(labelStyle="font: 300 14px 'Helvetica Neue', Helvetica"))
for task in framework.dag.nodes_iter():
    colors = colors or get_colors()
    G.add_node(task._uid, style=colors_exe.setdefault(
        get_key(task, colors_exe.iterkeys()),
        "fill: {}".format(colors.pop())))
    for successor in framework.dag.successors(task):
        G.add_edge(task._uid, successor._uid,
                   style="stroke: #454545; stroke-width: 2px;", arrowheadStyle="fill: #454545")

write_dot(G, "graph.txt")

load_url("d3.html")
