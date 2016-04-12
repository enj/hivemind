import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import cPickle as pickle
from networkx.drawing.nx_agraph import graphviz_layout

from hivemind.pipeline import Task
from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks, read_csv

from datagenerator import DataGenerator

from sys import stdout
from networkx.drawing.nx_pydot import write_dot


tasks = json_to_tasks('sarah_pipeline.json')

dg = DataGenerator()
framework = PipelineFramework(tasks)
#framework = dg.get_loose_pipeline()

patients = read_csv('sarah.csv')
concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row, ""))

p = concrete_pipelines[0]
queue = [task for task in p.get_ready_tasks()]
print queue

for task in queue:
    #queue.put(task)
    print "Setting", task._uid, "to done"
    p.set_done(task)


print p.get_maximum_concurrency()


