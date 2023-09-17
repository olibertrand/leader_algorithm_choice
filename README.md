# leader_algorithm_choice

Les outils proposés dans ce dépôt permettent:

- de définir des réseaux dont les connexions dépendent de la distance entre 2 noeuds (comme dans le cas de réseaux sans fil)
- de déterminer, pour une configuration donnée, quel algorithme permet d'obtenir le noeud du réseau d'excentricité minimale (recherche du centre géométrique, recherche du centre de gravité, ABC-Center ou k-BFS)
-  de produire une représentation graphique d'un réseau
-  en combinant les possibilités données ci-dessus, de produire un lot de représentations graphiques pour un lot de configurations stockées dans des fichiers `csv`, en classant les images obtenues par algorithme vainqueur. On produit ainsi des données pouvant être acceptées en entrée d'un réseau de neurones convolutif.


Créer/Visualiser/Modifier une configuration
Ouvrir le fichier monde_robots.py à l'aide d'un interpréteur Python. La fenêtre de gauche représente l'espace dans lequel évoluent les nœuds du réseau. La création de nouveau nœuds se fait à la souris, les nœuds peuvent être déplacés par cliquer-déplacer et supprimés par un clic-droit.

Les cases à cocher "centreGrav", "centreGeom" et "kBFS" permettent de colorier respectivement le centre de gravité en rouge, le centre géométrique en vert et les candidats de l'algorithme kBFS en cyan.

La case "affichage" permet de visualiser dans la console des étapes intermédiaires des algorithmes itératifs.

Le bouton "Best" affiche les performances (numéro du nœud, excentricité) des leaders obtenus par 5 algorithmes (centreGeom, centreGrav, ABC-Center, slowABC, 10-BFS) ainsi que le noeud d'excentricité minimale. Il détermine l'algorithme vainqueur en choisissant en cas d'égalité le premier dans la liste.

Le bouton "importer une configuration" permet de choisir un fichier csv indiquant les positions des noeuds.

L'exemple ci-dessous donne le format attendu:

id,x,y,portee 6,89.38286224583192,274.21103835165434,85

....

Comment
