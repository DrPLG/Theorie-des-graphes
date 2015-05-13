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
G.add_edges_from([(1,2),(1,3),(4,5),(5,7),(4,7),(1,7),(3,6)],color=None)

# Ordre du graphe
numberOfNodes = len(G)

## Coloration de chaque sommet par une couleur distincte
#for i in range(8):
#    G.node[i]['color']=i    

# Liste des sommets dans l'ordre décroissant des degrés
degres =nx.degree(G)
liste = sorted(degres, key=degres.get, reverse=True)

# Coloration des sommets par l'algorithme glouton
for sommet in liste:
    voisins = nx.neighbors(G, sommet)
    couleurDesVoisins = nx.get_node_attributes(G.subgraph(voisins),'color').values()
    print couleurDesVoisins
    couleur = 0
    while True:
        if (couleur in couleurDesVoisins):
            couleur += 1
        else:
            G.node[sommet]['color']=couleur
            break
        
# Tracé du graphe
pos=nx.spring_layout(G)
nx.draw_networkx(G,pos,node_color=nx.get_node_attributes(G,'color').values())
plt.show()