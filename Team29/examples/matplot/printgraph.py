import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from networkx.drawing.nx_agraph import graphviz_layout

from hivemind.pipeline import PipelineFramework, ConcretePipeline
from hivemind.util import json_to_tasks, read_csv


tasks = json_to_tasks('../../tests/blackbox/sarah_pipeline.json')
patients = read_csv('../dna/dna.csv')

framework = PipelineFramework(tasks)

concrete_pipelines = []
for i, row in enumerate(patients):
    concrete_pipelines.append(ConcretePipeline(i, framework, row, ""))

p = concrete_pipelines[0]

G = nx.DiGraph()
for task in p.dag.nodes():
    G.add_node(task._uid)
    for successor in p.dag.successors(task):
        G.add_edge(task._uid, successor._uid)

# Need to create a layout
pos = graphviz_layout(G, prog='dot')

edge_colours = ['black' for edge in G.edges()]
black_edges = [edge for edge in G.edges()]
nx.draw_networkx_nodes(G, pos, node_shape='o', node_color=range(G.number_of_nodes()), linewidths=0.5, cmap=plt.cm.Paired, node_size=100)
nx.draw_networkx_edges(G, pos, width=.25, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=4)

plt.axis("off")
plt.gca().xaxis.set_major_locator(NullLocator())
plt.gca().yaxis.set_major_locator(NullLocator())
plt.margins(0, 0)

plt.savefig("graph.png", bbox_inches='tight', pad_inches=0, dpi=200)
