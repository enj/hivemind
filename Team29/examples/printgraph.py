import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

from hivemind.pipeline import Task
from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks, read_csv

from datagenerator import DataGenerator


tasks = json_to_tasks('sarah.json')

dg = DataGenerator()
#framework = PipelineFramework(tasks)
framework = dg.get_disconnected_pipeline()

patients = read_csv('sarah.csv')
concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row, ""))

p = concrete_pipelines[0]

# Need to create a layout when doing
# separate calls to draw nodes and edges
#pos = nx.spring_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.random_layout(G)
#pos = nx.shell_layout(G)
pos = nx.fruchterman_reingold_layout(p.dag, scale=1)


edge_colours = ['black' for edge in p.dag.edges()]
black_edges = [edge for edge in p.dag.edges()]
nx.draw_networkx_nodes(p.dag, pos, cmap=plt.get_cmap('jet'), node_color='y')
nx.draw_networkx_edges(p.dag, pos, edgelist=black_edges, arrows=True)
nx.draw_networkx_labels(p.dag, pos, {task : str(task._uid) + "," + str(task._pid) for task in p.dag.nodes()}, font_size=12)

plt.show()
