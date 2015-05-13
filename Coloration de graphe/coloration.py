# -*- coding: utf-8 -*-
# Programme permettant une coloration optimale d'un graphe.
# Utilisation de networkX

# V 0.01 Mise en place d'un graphe, et coloration de chaque sommet par une couleur distincte. Validé le 13.05.2015



import networkx as nx
import matplotlib.pyplot as plt


# Création du graphe
G = nx.Graph()
H = range(8)
G.add_nodes_from(H)
G.add_edges_from([(1,2),(1,3),(4,5),(5,7),(4,7),(1,7),(3,6)],color='r')

# Coloration de chaque sommet par une couleur distincte
for i in range(8):
    G.node[i]['color']=i    


# Tracé du graphe
pos=nx.spring_layout(G)
nx.draw_networkx(G,pos,node_color=nx.get_node_attributes(G,'color').values())
plt.show()