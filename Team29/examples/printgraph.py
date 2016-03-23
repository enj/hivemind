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

patients = read_csv('dna.csv')
concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row, ""))

p = concrete_pipelines[0]

#print p.dag.nodes()

G = nx.DiGraph()
for task in p.dag.nodes():
    G.add_node(task._uid)
    for successor in p.dag.successors(task):
        G.add_edge(task._uid, successor._uid)

# Need to create a layout when doing
# separate calls to draw nodes and edges
#pos = nx.spring_layout(p.dag)
#pos = nx.circular_layout(p.dag)
#pos = nx.random_layout(p.dag)
#pos = nx.shell_layout(p.dag)
#pos = nx.fruchterman_reingold_layout(p.dag)
pos = graphviz_layout(G, prog='dot')
#pos = nx.layout.collections(p.dag)



edge_colours = ['black' for edge in G.edges()]
black_edges = [edge for edge in G.edges()]
nx.draw_networkx_nodes(G, pos, node_shape='o', node_color=range(G.number_of_nodes()), linewidths=0.5, cmap=plt.cm.Paired, node_size=100)
nx.draw_networkx_edges(G, pos, width=.25, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=4)
#nx.draw_networkx_labels(p.dag, pos, {task : str(task._uid) + "," + str(task._pid) for task in p.dag.nodes()}, font_size=12)

plt.axis("off")
plt.gca().xaxis.set_major_locator(NullLocator())
plt.gca().yaxis.set_major_locator(NullLocator())
plt.margins(0,0)
#plt.figure(dpi=200)
#plt.show()
plt.savefig("graph.png", bbox_inches='tight', pad_inches=0, dpi=200)
#write_dot(G, stdout)
