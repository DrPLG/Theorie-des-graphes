# -*- coding: utf-8 -*-
# Programme permettant une coloration optimale d'un graphe.
# Utilisation de networkX

# V 0.01 Mise en place d'un graphe, et coloration de chaque sommet par une couleur distincte. Validé le 13.05.2015
# V 0.02 Mise en place de l'algorithme glouton. Validé le 13.05.2015
# V 0.03 Mise en place de l'algorithme DSATUR. Validé le 14.05.2015
# V 0.04 Calcul de la taille de la clique maximale, pour obtenir un minorant du nombre chromatique. Validé le 14.05.2015
# V 0.05 Lecture de fichiers pour tester sur le programme sur d'autres graphes. Validé le 14.05.2015
# V 0.06 Algorithme de Sikov (1/2). Contractions. Validé le 14.05.2015 
# V 0.07 Algorithme de Sikov (2/2). Ajout d'arête. Validé le 15.05.2015
# Mise en garde : à utiliser uniquement avec des petits graphes, et beaucoup d'arêtes.
# V 0.08 Utilisation du minorant pour identifier avant et pendant l'algorithme une solution optimale. Validé le 15.05.2015

import networkx as nx
import matplotlib.pyplot as plt
import sys

global minorant

################################################################################
# Fonctions auxiliaires


def Sikov(Gs,couleurs):
    global minorant
    degres = nx.degree(Gs)
    ordre = len(Gs)
    # Identification d'une clique
    if (min(degres.values())+1==ordre):
        couleur = 0
        for sommet in Gs:
            couleurs[sommet] = couleur
            couleur += 1
        return (couleurs,ordre)
    else:
        liste = sorted(degres, key=degres.get, reverse=True)
        # Choix du sommet de degré le plus élevé, mais inférieur strictement à ordre-1
        i = 0
        while True:
            if degres[liste[i]]<ordre-1:
                sommetAccueil = liste[i]
                break
            else:
                i += 1
        # Choix du sommet de degré le plus faible, non voisin du précédent.
        voisinsA = nx.neighbors(Gs, sommetAccueil)
        i = -1
        while True:
            if liste[i] not in voisinsA:
                sommetSupprime = liste[i]
                break
            else:
                i -= 1
        # Contraction
        # Copie du graphe, 
        Hs = Gs.copy()
        # Ajout des nouvelles arêtes
        voisinsS = nx.neighbors(Hs, sommetSupprime)
        for voisin in voisinsS:
            Hs.add_edge(sommetAccueil, voisin)
        # Et suppression du sommetSupprime
        Hs.remove_node(sommetSupprime)
        couleursHs= couleurs[:]
        couleursHs[sommetSupprime] = "c"+str(sommetAccueil)
        
        # Ajout d'arête
        Is = Gs.copy()
        Is.add_edge(sommetAccueil, sommetSupprime)
        couleursIs = couleurs[:]
        # Calcul des deux colorations avec les deux nouveaux graphes
        outHs = Sikov(Hs,couleursHs)
        if outHs[1]==minorant:
            return (outHs[0][:],outHs[1])
        outIs = Sikov(Is,couleursIs)
        print outHs[1], outIs[1]
        if outHs[1]<=outIs[1]:
            return (outHs[0][:],outHs[1])
        else:
            return (outIs[0][:],outIs[1])
        
    



################################################################################  
# Emplacement du fichier data
fileLocation = sys.argv[1].strip()
inputDataFile = open(fileLocation, 'r')
inputData = ''.join(inputDataFile.readlines())
inputDataFile.close()

# Lecture du fichier data
lines = inputData.split('\n')
tempData = open('tempData','w')
firstLine = lines[0].split()
nodeCount = int(firstLine[0])
edgeCount = int(firstLine[1])


# Création du graphe
G=nx.Graph()
G.add_nodes_from(range(0,nodeCount))

for i in range(1, edgeCount+1):
    line=lines[i]
    parts = line.split()
    G.add_edge(int(parts[0]), int(parts[1]))

## Création du graphe
#G = nx.Graph()
#H = range(8)
#G.add_nodes_from(H,dsat=0)
#G.add_edges_from([(1,2),(1,3),(4,5),(5,7),(4,7),(1,7),(3,6)])

################################################################################  
# Ordre des cliques maximales
minorant = nx.graph_clique_number(G)
temp =raw_input(str(minorant))
################################################################################  
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
numberOfColors = max(nx.get_node_attributes(G,'color').values() )
if numberOfColors == minorant:
    print "Coloration optimale. Le nombre chromatique est "+str(minorant)+"."
else:
    print "Le nombre chromatique est compris entre "+str(minorant)+" et "+str(numberOfColors)+"."
 
################################################################################  
# Début de l'algorithme avec contractions de Sikov
# Nécessité d'une telle étaoe ?
if numberOfColors > minorant:


    # Remise à -1 des couleurs
    for sommet in liste:
        G.node[sommet]['color']=-1
        
    out = Sikov(G,nx.get_node_attributes(G,'color').values())                      
    couleurs = out[0]
    gamma = out[1]
    
    print couleurs
    
    # Sans doute à revoir dans le futur, besoin de plusieurs passages ?
    for sommet in liste:
        if type(couleurs[sommet]) == int:
            G.node[sommet]['color']=couleurs[sommet]
        else:
            G.node[sommet]['color']=couleurs[int(couleurs[sommet][1:])]
                                                            
    print "Coloration optimale. Le nombre chromatique est "+str(gamma)+"."                                                                                                                    
                                                                                                                                                                                
                                                                                                                                                                                                                                                                                                    
################################################################################                                                              
# Tracé du graphe
#pos={0:(1,2),
     #1:(1,0),
     #2:(0,1),
     #3:(2,1),
     #4:(4,2),
     #5:(4,0),
     #6:(3,1),
     #7:(5,1)}
pos=nx.shell_layout(G)
nx.draw_networkx(G,pos,node_color=nx.get_node_attributes(G,'color').values())
plt.show()