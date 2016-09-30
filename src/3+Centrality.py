
# coding: utf-8

# In[1]:

get_ipython().magic('reload_ext watermark')
get_ipython().magic('watermark -p networkx -v -n')


# In[2]:

import networkx as nx
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')

G = nx.read_gexf('data/homer.gexf')


# # Quick Results

# In[3]:


sorted(G.degree().items(), key=lambda x:x[1], reverse=True)[:10]


# In[4]:

sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[5]:

sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[6]:

sorted(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[7]:

sorted(nx.harmonic_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# # Centrality
# 
# - Definition of Centrality
# - Compare and contrast popular centrality measures on dataset
#     - Degree  :   
#     - Closeness ： 
#     - Betweenness: 
#     - Eigenvector
# 
# <img width="500" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Graph_betweenness.svg/2000px-Graph_betweenness.svg.png">

# ## Degree Centrality
# 
# The __degree__ of a node is the number of other nodes to which it is connected. 
# 
# ![](https://www.openabm.org/files/books/1928/fig102.png)
# 
# NetworkX's degree centrality is calculated by taking the degree of the node and dividing by `n-1` where where `n` is the number of nodes in `G`.
# 
# $$ {C_D (u)} = \frac{deg(u)}{{n-1}} $$
# 
# ⚠️ __NOTE__: `In a directed graph, both in-degree and out-degree centrality can be calculated.`

# Let's find the degree of our main character `Grey`.

# In[8]:

G.degree("HT")  #Hector


# In[9]:

G.degree("AC")  #Achilles


# Likewise, we can find the degree of each cast member.

# In[10]:

# Here's the top 5. version 1.x
sorted(G.degree().items(), key=lambda x:x[1], reverse=True)[:10]


# In[11]:

# Here's the top 5. version 2.x
#b = dict(list(G.degree()))
#sorted(b.items(), key=lambda x:x[1], reverse=True)[:5]


# While knowing the raw number is great, most centrality measures are _normalized_ between zero and one so that they can be more easily compared to one another.
# 
# For the **degree centrality** measure, the normalized interpretion is really intuitive:  
# 
# > _What percentage of nodes is this node connected to?_
# 
# Or for our Grey's Anatomy example: 
# 
# > _What percentage of the cast has this character been invovled with?_
# 
# 
# 

# Let's calculate the degree centrality for `Grey`.

# In[12]:

b = dict(list(G.degree()))

# Degree for the 'HT' node
degree_HT = G.degree("HT")  

# Total number of nodes (excluding HT) 
total_nodes_minus_HT = len(G.degree())-1.  

# Degree centrality for HT
degree_centrality_HT = (degree_HT / total_nodes_minus_HT)
print("Calculated degree centrality for HT:", degree_centrality_HT)

# Double check
print("Networkx degree centrality for HT:", nx.degree_centrality(G)["HT"])


# Likewise, let's find the degree centrality for all characters.

# In[13]:

# Top 5.  Percent of cast this character has been with.
sorted(nx.degree_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[14]:

# apply measurements back to Graph
nx.set_node_attributes(G, 'degree centrality', nx.degree_centrality(G))


# In[15]:

G.node['HT']


# ## Closeness Centrality
# Closeness Centrality measures how many "hops" it would take to reach every other node in a network (taking the shortest path). It can be informally thought as 'average distance' to all other nodes.
# 
# <img style="float: center" src="https://toreopsahl.files.wordpress.com/2008/12/geodesic-n1.png?w=455">
# 
# In NetworkX, it the reciporical of of the *average* value, which normalizes the value in a 0 to 1 range. 
# 
# $$ C_C (u) = \frac{n - 1}{\sum_{v=1}^{n-1} d(v, u)} $$
# 
# If you again take the reciporical of this, you'll find the *average* distance to all other nodes.

# In[16]:

# Shortest path between Grey and other characters
HT_shortest_path = nx.shortest_path_length(G)['HT']
HT_shortest_path


# In[17]:

# Sum of the shortest paths to all other characters
HT_sum_shortest_path = sum(HT_shortest_path.values())  # 77

# Closeness centrality for HT
closeness_centrality_HT = (total_nodes_minus_HT / HT_sum_shortest_path)
print("Calculated closeness centrality for HT:", closeness_centrality_HT)

# Double check
print("Networkx closeness centrality for HT:", nx.closeness_centrality(G)["HT"])



# Interesting...our calculated measure is not the same as the one in NetworkX.  
# 
# _What happened here?_
# 
# This error occured because __the character relationship graph is not fully connected.__ (i.e., there are groups of characters that do not have relationships with one another).

# In[18]:

# View members of different subgraphs
sorted(nx.connected_components(G), key = len, reverse=True)


# To correct for this, we will use the number of nodes in the `Grey` subgraph instead of the total number of nodes to calculated degree centrality.  Additionally, we'll normalized to `(n-1)/(|G|-1)` where `n` is the number of nodes in the connected part of graph containing the node.

# In[19]:

total_nodes_minus_HT_sub = len(HT_shortest_path)-1.0  

# Closeness centrality for HT (unnormalized)
closeness_centrality_HT = (total_nodes_minus_HT_sub / HT_sum_shortest_path) 

# Closeness centrality for HT (normalized)
closeness_centrality_HT_normalized = closeness_centrality_HT * (total_nodes_minus_HT_sub/total_nodes_minus_HT)
print("Calculated closeness centrality for HT (normalized):", closeness_centrality_HT_normalized)

# Double check
print("Networkx closeness centrality for HT:", nx.closeness_centrality(G)["HT"])



# Let's find the closeness centrality for all characters.

# In[20]:

# top 5
sorted(nx.closeness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[21]:

# apply measurements back to Graph
nx.set_node_attributes(G, 'closeness centrality', nx.closeness_centrality(G))


# In[22]:

# average distance of torres:
1.0 / nx.closeness_centrality(G)['HT']


# In[23]:

7.0/(len(G.nodes()) - 1)


# ## Betweeness Centrality
# 
# Betweenness centrality quantifies the number of times a node acts as a bridge (or "broker") along the shortest path between two other nodes.  
# 
# ![](https://intl520-summer2011-mas.wikispaces.com/file/view/Simple_Network.gif/238734999/480x360/Simple_Network.gif)
# 
# In this conception, vertices that have a high probability to occur on a randomly chosen shortest path between two randomly chosen vertices have a high betweenness.
# 
# $$ C_B(v) =\sum_{s,t \in V} \frac{\sigma(s, t|v)}{\sigma(s, t)} $$
# 
# where ${\sigma(s, t)}$ is total number of shortest paths from node ${s}$ to node ${t}$ and ${\sigma(s, t|v)}$ is the number of those paths that pass through ${v}$.

# In[24]:

# top 5
sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# ## Eigenvector Centrality
# 
# A node is high in eigenvector centrality if it is connected to many other nodes who are themselves well connected. Eigenvector centrality for each node is simply calculated as the proportional eigenvector values of the eigenvector with the largest eigenvalue.
# 
# <img align="middle" src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/6_centrality_measures.png/350px-6_centrality_measures.png">
# 
# _**Middle Left ("C"):** Eigenvector Centrality.  **Middle Right ("D"):** Degree Centrality_
# 
# 

# In[25]:

sorted(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1], reverse=True)[:10]


# In[26]:

max_value = max(nx.eigenvector_centrality_numpy(G).items(), key=lambda x: x[1])

ec_scaled = {}
for k in nx.eigenvector_centrality(G).keys():
    ec_scaled[k] = nx.eigenvector_centrality(G)[k] / max_value[1]

# Scaled by the most central character (karev)
sorted(ec_scaled.items(), key=lambda x:x[1], reverse=True)[0:10]


# ## Harmonic Centrality
# 
# 

# In[27]:

sorted(nx.harmonic_centrality(G).items(), key=lambda x: x[1], reverse=True)[:10]


# ## Other Centrality Measures
# 
# * [Harmonic Centrality](https://networkx.readthedocs.io/en/latest/reference/generated/networkx.algorithms.centrality.harmonic_centrality.html)
# * [Katz Centrality](https://en.wikipedia.org/wiki/Katz_centrality)
# * [Game Theoretic Centrality](http://game-theoretic-centrality.com/)
# 
