import networkx as nx
#import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle

from task import Task
from pipeline import PipelineFramework, ConcretePipeline
from util import json_to_tasks, read_csv


a = Task(1, False, [], "", "")
b = Task(2, False, [1], "", "")
c = Task(3, False, [], "", "")
d = Task(4, False, [2, 3], "", "")
e = Task(5, False, [], "", "")
f = Task(6, False, [4, 5], "", "")
g = Task(7, False, [], "", "")
h = Task(8, False, [6, 7], "", "")
i = Task(9, False, [6], "", "")
j = Task(10, False, [8, 9], "", "")


test = Task(6, False, [4, 5], "", "")
pickled = pickle.dumps(test)

tasks = json_to_tasks('pipeline.json')


#p = PipelineFramework(a, b, c, d, e, f, p.dag, h, i, j)
framework = PipelineFramework(*tasks)


patients = read_csv('test.csv')
concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row))


#p.set_done(test)
#p.set_done(g)

#p=concrete_pipelines[0]
#print p.dag.nodes()[0]

#q = p.get_ready_successors(p.dag.nodes()[0])
#print q

#for t in q:
#    print "Add to queue:", t.uid


#print "h successors:", p.dag.successors(h)
#print "test successors:", p.dag.successors(test)
#print "Pickled in graph?", p.dag.has_node(pickle.loads(pickled))

#val_map = {'A': 1.0,
#           'D': 0.5714285714285714,
#           'H': 0.0}

#values = [val_map.get(node, 0.25) for node in p.dag.nodes()]

# Specify the edges you want here

# Need to create a layout when doing
# separate calls to draw nodes and edges
#pos = nx.spring_layout(G)
#pos = nx.circular_layout(G)
#pos = nx.fruchterman_reingold_layout(G)
#pos = nx.random_layout(G)
#pos = nx.shell_layout(G)
for p in concrete_pipelines:
    edge_colours = ['black' for edge in p.dag.edges()]
    black_edges = [edge for edge in p.dag.edges()]
    pos = nx.spring_layout(p.dag,scale=1)
    nx.draw_networkx_nodes(p.dag, pos, cmap=plt.get_cmap('jet'), node_color='y')
    #nx.draw_networkx_edges(p.dag, pos, edgelist=red_edges, edge_color='r', arrows=True)
    nx.draw_networkx_edges(p.dag, pos, edgelist=black_edges, arrows=True)
    nx.draw_networkx_labels(p.dag, pos, {task : str(task._uid) + "," + str(task._pid) for task in p.dag.nodes()}, font_size=12)
    #plt.show()
    plt.show()
