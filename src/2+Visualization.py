
# coding: utf-8

# In[1]:

get_ipython().magic('reload_ext watermark')
get_ipython().magic('watermark -p networkx,matplotlib,circos -v -n')


# <img width="500" src="images/homer_neo4j.png">
# 

# In[2]:

import networkx as nx
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[3]:

G = nx.read_gexf('data/homer.gexf')
print(nx.info(G))


# # Easy

# In[4]:

nx.draw(G, with_labels=True)


# In[5]:

# Graph Layouts are random...
nx.draw(G, with_labels=True)


# ## NetworkX Detailed Plotting

# In[6]:

# Some matplotlib options
plt.figure(figsize=(8,8))
plt.axis('off')

# generate the layout and place nodes and edges
layout = nx.circular_layout(G)

# plot nodes, labels, and edges with options
nx.draw_networkx_nodes(G, pos=layout, node_size=500, alpha=0.8)
nx.draw_networkx_edges(G, pos=layout, width=3, style='dotted',
                       edge_color='orange')
nx.draw_networkx_labels(G, pos=layout, font_size=15)

plt.show()


# # Circos Plot

# In[7]:

from circos import CircosPlot

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

nodes = sorted(G.nodes())
edges = G.edges()
#node_cmap = {'male':'blue', 'female':'red'}
#nodecolors = [node_cmap[G.node[n]['gender']] for n in G.nodes()]

c = CircosPlot(nodes, edges, radius=10, ax=ax, fig=fig)
c.draw()  
plt.savefig('images/circos.png', dpi=300)

