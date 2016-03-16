import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

from hivemind.pipeline import Task
from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks, read_csv

from datagenerator import DataGenerator


tasks = json_to_tasks('dna.json')

dg = DataGenerator()
framework = PipelineFramework(tasks)
#framework = dg.get_loose_pipeline()

patients = read_csv('dna.csv')
concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row, ""))

p = concrete_pipelines[0]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(p.dag)
#pos = nx.circular_layout(p.dag)
#pos = nx.random_layout(p.dag)
#pos = nx.shell_layout(p.dag)
#pos = nx.fruchterman_reingold_layout(p.dag)


edge_colours = ['black' for edge in p.dag.edges()]
black_edges = [edge for edge in p.dag.edges()]
nx.draw_networkx_nodes(p.dag, pos, cmap=plt.get_cmap('jet'), node_color='y')
nx.draw_networkx_edges(p.dag, pos, edgelist=black_edges, arrows=True)
nx.draw_networkx_labels(p.dag, pos, {task : str(task._uid) + "," + str(task._pid) for task in p.dag.nodes()}, font_size=12)

plt.show()
