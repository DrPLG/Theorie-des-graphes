# -*- coding: utf-8 -*-
# Programme permettant une coloration optimale d'un graphe.
# Utilisation de networkX

# V 0.01 Mise en place d'un graphe, et coloration de chaque sommet par une couleur distincte. Validé le 13.05.2015
# V 0.02 Mise en place de l'algorithme glouton. Validé le 13.05.2015
# V 0.03 Mise en place de l'algorithme DSATUR. Validé le 14.05.2015



import networkx as nx
import matplotlib.pyplot as plt


# Création du graphe
G = nx.Graph()
H = range(8)
G.add_nodes_from(H,dsat=0)
G.add_edges_from([(1,2),(1,3),(4,5),(5,7),(4,7),(1,7),(3,6)])


# Ordre du graphe
numberOfNodes = len(G)

## Coloration de chaque sommet par une couleur distincte
#for i in range(8):
#    G.node[i]['color']=i    

# Liste des sommets dans l'ordre décroissant des degrés
degres =nx.degree(G)
liste = sorted(degres, key=degres.get, reverse=True)


# Coloration des sommets par DSATUR


degreMax = max(degres.values())
#print degremax
numberOfColoredNodes = 0
nonColoredNodes = liste[:]
#print nonColoredNodes

# Calcul des DSAT version PLG (prise en compte du degré)
# dsat = nombre de voisins colorés + degre/(degreMax+1)
for sommet in liste:
    G.node[sommet]['dsat']=float(nx.degree(G,sommet))/(degreMax+1)

# Coloration d'un maximum de sommets avec la première couleur
for sommet in liste:
    #print sommet
    #print nx.get_node_attributes(G,'dsat').values()
    voisins = nx.neighbors(G, sommet)
    couleurDesVoisins = nx.get_node_attributes(G.subgraph(voisins),'color').values()
    #print couleurDesVoisins
    if not (1 in couleurDesVoisins):
        G.node[sommet]['color']=1
        numberOfColoredNodes += 1
        nonColoredNodes.remove(sommet)
        for voisin in voisins:
            G.node[voisin]['dsat'] +=1
        #print nx.get_node_attributes(G,'dsat').values()
    #else:
        #G.node[sommet]['color']=0

#print nx.get_node_attributes(G,'dsat').values()

# Tant que tous les sommets ne sont pas colorés :
while numberOfColoredNodes<numberOfNodes:
    # Tri des sommets par DSAT (et degres) décroissant
    #degres =nx.degree(G)
    #liste = sorted(degres, key=degres.get, reverse=True)
    dsat = nx.get_node_attributes(G.subgraph(nonColoredNodes),'dsat')
    
    sommet = max(dsat, key=dsat.get)
    voisins = nx.neighbors(G, sommet)
    couleurDesVoisins = nx.get_node_attributes(G.subgraph(voisins),'color').values()
    
    couleur = 1
    while True:
        if not (couleur in couleurDesVoisins):
            G.node[sommet]['color']=couleur
            numberOfColoredNodes += 1
            nonColoredNodes.remove(sommet)
            for voisin in voisins:
                G.node[voisin]['dsat'] +=1
            break   
        else:
            couleur += 1

# print nx.get_node_attributes(G,'color').values()    
              
# Tracé du graphe
pos=nx.spring_layout(G)
nx.draw_networkx(G,pos,node_color=nx.get_node_attributes(G,'color').values())
plt.show()