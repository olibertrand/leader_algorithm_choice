from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nx
#from itertools import chain

import sys, os, threading
import random
from math import sqrt


from tkinter import *
from tkinter import filedialog 

from PIL import Image, ImageDraw, ImageChops

NOIR = "#000000"#(0,0,0)
ROUGE = "#FF0000"#(255,0,0)
VERT = "#00FF00"#(0,255,0)
BLEU = "#0000FF"#(0,0,255)
CYAN = "#00FFFF"#(0,255, 255)
affichage = False


def euclidienne(x1, y1, x2, y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
       
class Point:
    """
    représente les noeuds du réseau
    ...

    Attributs
    ----------
    coordonnees : tuple[float,float]
        coordonnées du point (dans le monde)
        
    tkinterID : int
        identifiant du point dans l'interface tkinter
        
    voisins : dict[int,int]
        tableau associant à l'indice d'un voisin dans le monde l'identifiant de l'arete correspondante dans l'interface tkinter
        
    couleur : tuple[int, int, int]
        couleur du point
        
    profondeur : int
        profondeur du point dans l'arbre en cours d'utilisation par l'algorithme treeCentrality

    Méthodes
    -------
    distance(coor1, coor2)
        renvoie la distance euclidienne entre les deux couples de coordonnées donnés en paramètre
        
    ajouteVoisin(idPoint, idArete)
        ajoute le couple (idPoint,tkinterId) au dictionnaire 'voisins'
        
    getVoisins()
        renvoie le dictionnaire 'voisins'
                
    getTkinterId()
        renvoie l'identifiant du point dans l'interface tkinter

    getX()
        renvoie    l'abscisse du point dans le monde (pas sur le canvas)
        
    getY()
        renvoie l'ordonnée du point dans le monde (pas sur le canvas)
        
    getCoordonnees()
        renvoie les coordonnées du point dans le monde (pas sur le canvas)
        
    getCouleur()
        renvoie dans une chaîne de caractères les composantes de la couleur du point en hexadécimal
        
    __eq__(autre)
        renvoie un booléen indiquant si le point est égal à celui passé en paramètre

    setCouleur(couleur)
        fixe la couleur du point à partir du tuple d'entiers passé en paramètre.
        

    setProfondeur(prof)
        fixe self.profondeur

    setPosition(newX, newY)
        fixe self.x et self.y

    positionEcran(zoom)
        renvoie les coordonnées du point sur l'écran
        
    
    distanceReelle(position)
        renvoie la distance avec la position (x,y) passée en paramètre
        
    distance(autre)
        renvoie la distance avec le point passé en paramètre
        
    distanceEcran(position, zoom)
        renvoie la distance, en pixels entre la position (x,y) et le point
        tient compte du facteur de zoom entre le monde et le canvas

    """
    def __init__(self, tkinterID, x, y, couleur=NOIR):
        
        self.coordonnees = (x,y)
        self.tkinterID = tkinterID
        self.voisins = {}
        self.couleur = couleur;
        self.profondeur = -1
        #self.reseau = None
        
    def ajouteVoisin(self, idPoint:int, idArete:int):
        """
        Paramètres
        ----------
        idPoint : int
            indice d'un point voisin
        idArete : int
            identifiant d'une arete dans l'interface tkinter
            
        Action
        ------
        ajoute un couple (idPoint,tkinterId) au dictionnaire "voisins"
        """
        self.voisins[idPoint] = idArete
        
    def getVoisins(self)->dict[int,int]:
        return self.voisins
                
    def getTkinterId(self)->int:
        """            
        Valeur renvoyée
        ---------------
        int
            identifiant du point dans l'interface tkinter
        """
        return self.tkinterID

    def getX(self)->float:
        """            
        Valeur renvoyée
        ---------------
        float
            abscisse du point dans le monde (pas sur le canvas)
        """
        return self.coordonnees[0]
        
    def getY(self)->float:
        """            
        Valeur renvoyée
        ---------------
        float
            ordonnée du point dans le monde (pas sur le canvas)
        """
        return self.coordonnees[1]
        
    def getCoordonnees(self)->tuple[float,float]:
        """            
        Valeur renvoyée
        ---------------
        tuple[float,float]
            coordonnées du point dans le monde (pas sur le canvas)
        """
        return self.coordonnees

    def getCouleur(self)->str:
        """            
        Valeur renvoyée
        ---------------
        str
            chaîne de caractères représentant la couleur du point au format html
        """
        
        r = self.couleur[0]
        g = self.couleur[1]
        b = self.couleur[2]
        return '#{:02x}{:02x}{:02x}'. format(r, g, b)
        
    def __eq__(self, autre)->bool:
        """
        Paramètre
        ---------
        autre : Point
            
        Valeur renvoyée
        ---------------
        bool
            valeur indiquant si les deux points sont égaux
        """
        return self.getCoordonnees == autre.getCoordonnees
        
    def setCouleur(self, couleur:tuple[int,int,int]):
        """            
        Paramètre
        ---------
        couleur : tuple[int, int, int]
        """        
        self.couleur = couleur
        
    def setProfondeur(self, prof:int):
        """            
        Paramètre
        ---------
        prof : int
        """            
        self.profondeur = prof

    def setPosition(self, newX:float, newY:float):
        """            
        Paramètre
        ---------
        newX, newY : float
        """    
        self.x = newX
        self.y = newY
        

    def positionEcran(self, zoom:float)->tuple[float,float]:
        """            
        Paramètre
        ---------
        zoom : float
            facteur de zoom entre le monde et le canvas
            
        Valeur renvoyée
        ---------------
        coordonnées du point dans l'interface graphique
        """    
        return (zoom*self.x, zoom*self.y)
        
    # def setReseau(self, r):
        # self.reseau = r
                
    # def getReseau(self):
        # '''renvoie l'objet Reseau auquel appartient le point'''
        # return self.reseau

    def distanceReelle(self, position:tuple[float,float])->float:
        """            
        Paramètre
        ---------
        position : tuple[float,float]
            couple de coordonnées dans le monde
            
        Valeur renvoyée
        ---------------
        float
            distance avec la position (x,y) passée en paramètre
        """
        return euclidienne(position[0], position[1], self.getX(), self.getY())
        
    def distance(self, autre)->float:
        """
        Paramètre
        ---------
        autre : Point
        
        Valeur renvoyée
        ---------------
            distance avec le point passé en paramètre
        """
        return self.distanceReelle( (autre.getX(), autre.getY()) )

    def distanceEcran(self, position, zoom):
        """
        Paramètre
        ---------
            position : tuple[float, float]
                un couple de coordonnées sur le canvas
            zoom : float
                le facteur de zoom entre le monde et le canvas
                
        Valeur renvoyée
        ---------------
        float
            la distance, en pixels entre la position (x,y) et le point
        """
        return euclidienne(position[0], position[1], self.x*zoom, self.y*zoom)
        
    # def dessiner(self, fenetre, zoom, rayon):
        # pygame.draw.circle(fenetre, self.couleur, self.positionEcran(zoom), rayon)

       
class Monde(Canvas):
    """
    représente l'espace dans lequel seront créés les points
    ainsi que la surface graphique sur laquelle ils seront représentés.
    hérite de la classe tkinter.Canvas
    ...

    Attributs
    ----------
    portee : int
        la distance en dessous de laquelle deux noeuds sont connectés
    
    width : int
        largeur du Canvas
    
    height : int
        hauteur du Canvas
    
    zoom_factor : int
        rapport entre la largeur du monde et la largeur de la surface graphique
        ramené provisoirement à 1 par simplicité
    
    rayon : int
        rayon du disque représentant un point sur le canvas
    
    reseaux : list[Reseau]
        liste des composantes connexes du graphe global
    
    points : dict[int,Point]
        dictionnaire (tableau associatif) associant à chaque indice de point un objet Point
    
    indexIds : dict[int, int]
        dictionnaire permettant de retrouver l'indice d'un point à partir de son identifiant dans l'interface graphique tkinter
        ensemble de couples idTkinter:idPoint
    
    fichier : str
        nom du fichier csv où son référencés les indices des points et leurs coordonnées
    
    graphe : networkx.Graph
        objet du module networkx représentant le graphe défini par les coordonnées des points et la portée des communications
    
    k : int
        nombre de points extérieurs choisis pour l'algorithme kBFS
        cette valeur est fixée par l'utilisateur dans l'interface graphique
    
    selObject : boolean
        variable indiquant si un point a été sélectionné à la souris
    
    affichage :  boolean
        variable indiquant s'il faut afficher le détail des opérations effectuées par les algorithmes (débuggage)
    
    showGrav : boolean
        indique s'il faut colorier le centre de gravité
    
    showGeom : boolean
        indique s'il faut colorier le centre géométrique
    
    showCandidates : boolean
        indique s'il faut colorier les candidats obtenus après exécution de kBFS
    

    Méthodes
    -------
    distance(coor1, coor2)
        renvoie la distance euclidienne entre les deux couples de coordonnées donnés en paramètre
    
    setVoisins(idPoint)
        détermine les points voisins du point dont l'id est passée en paramètre
        met à jour le dictionnaire "voisins" de ce point ainsi que celui des points voisins
    
    nouveauPoint(event)
        crée un nouveau point aux coordonnées de la souris                
    
    ajoute_point(x, y, idPoint=-1)
        ajoute un point sur le Canvas et l'enregistre dans le monde
        renvoie un booléen indiquant si l'ajout a été réalisé
    
    ajouteListe(listePoints)
        ajoute une liste de points en faisant appel à ajoute_point
        renvoie le nombre de points effectivement ajoutés
        
    mouseDown(event)
        appelé lors d'un clic de souris. 
        Crée un nouveau point ou sélectionne un point existant
        
    mouseMove(event)
        appelé lors d'un déplacement de la souris. 
        modifie les coordonnées du point sélectionné, s'il existe
        
    mouseDownBis(event)
        appelé lors d'un clic droit. 
        supprime le point cliqué

    mouseUp(self, event)
        appelée au relâchement du bouton de la souris.
        déselectionne un éventuel point sélectionné

    effaceVoisinage(idPoint)
        efface les références au voisinage d'un point
        à appeler avant de déplacer ou de supprimer le point

    dicoVoisins()
        renvoie un tableau associant à chaque indice de point la liste des indices de ses voisins
        (représentation du graphe à l'aide de listes d'adjacence)
        
    setGraphe()
        construit le graphe (objet networkx.Graph) représentant le réseau
        fixe la valeur de self.graphe
        détermine les composantes connexes du graphe et remplit self.reseaux
          
    getGraphe()
        renvoie la valeur de self.graphe
        
    composanteConnexe(i0)
        renvoie la liste des indices des points de la composante connexe du point d'indice i0
        
    reseauPrincipal()
        renvoie le réseau représentant la composante connexe la plus importante
        
    setCouleurs(affichage=False)
        fixe la couleur des points dans chacune des composantes connexes du monde
       
    bestAlgorithmes(affichage=False)
        appelle bestAlgorithme (comparaison des algorithmes d'élection)
        sur la composante connexe principale
        
    chargeCSV(nomFichier)
        lis le contenu du fichier dont le nom est passé en paramètre et ajoute les points dans le monde. 
        renvoie un booléen indiquant si le fichier existe

    sauveCSV(nom="test.csv", indices=None)
        enregistre les coordonnées des points dans un csv dont le nom est donné en paramètre
        test.csv est le nom de fichier par défaut
    
    sauvePNG(nom="test.png", indices=None, radius = self.rayon, aretes=True)
        enregistre une image représentant le réseau dans un png dont le nom est donné en paramètre
        test.png est le nom de fichier par défaut   
        
    ecrire()
        enregistre les coordonnées de tous les points
        dans le fichier dont le nom figure dans self.fichier (fichier ouvert et modifié)
        
    monde2Ecran(x, padding)
        reçoit la valeur d'une coordonnée dans le monde et renvoie sa valeur sur le canvas
        
    
    """
    
    def __init__(self, width, height, portee, zoom, boss):
        self.portee = portee*zoom
        self.width = width*zoom
        self.height = height*zoom
        self.zoom_factor = zoom
        self.rayon = 3
        self.reseaux = []
        self.points = {} #id:Point
        self.indexIds = {} #idTkinter:id
        self.fichier = None
        self.graphe = None
        self.k = 10
        self.selObject = None
        self.affichage = False
        Canvas.__init__(self, boss, width=self.width, height=self.height, bg='white')
        self.bind("<Button-1>", self.mouseDown)
        self.bind("<Button-3>", self.mouseDownBis)
        self.bind("<Button1-Motion>", self.mouseMove)
        self.bind("<Button1-ButtonRelease>", self.mouseUp)
        self.showGrav = False
        self.showGeom = False
        self.showCandidats = False

    def distance(self, coor1: tuple[float,float], coor2: tuple[float,float])-> float:
        """
        Paramètres
        ----------
        coor1, coor2 : tuple[float,float]
            deux couples de coordonnées
       
        Valeur renvoyée
        ---------------
        float
            la distance euclidienne entre les deux couples coor1 et coor2
        """
        return sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
  

    def setVoisins(self, idPoint:int):
        """
        Paramètres
        ----------
        idPoint : int
            l'indice d'un des points dans le monde
       
        Action
        ---------------
        détermine les points voisins du point dont l'id est passée en paramètre
        met à jour le dictionnaire "voisins" de ce point ainsi que celui des points voisins
        """

        depart = self.points[idPoint].coordonnees
        #On tient compte du facteur de zoom pour ce calcul
        voisins = [pId for pId in self.points if self.distance(self.points[pId].coordonnees, depart) < self.portee and pId != idPoint]           

        for autreId in voisins:
            x, y = self.points[idPoint].coordonnees
            xp, yp = self.points[autreId].coordonnees
            f = self.zoom_factor
            #on crée une nouvelle arete
            nouvelle = self.create_line(x*f,y*f,xp*f,yp*f)
            #chaque voisin est un couple id:arete
            self.points[autreId].ajouteVoisin(idPoint, nouvelle)
            self.points[idPoint].ajouteVoisin(autreId, nouvelle)

    def nouveau_point(self, event):
        """
        Paramètres
        ----------
        event : événement créé par un clic de souris sur le canvas
       
        Action
        ------       
        crée un nouveau point aux coordonnées de la souris
        """
        x, y = event.x, event.y
        self.ajoute_point(x,y)
        #print(self.dicoVoisins())
        self.setGraphe()
            
    def ajoute_point(self, x:float, y:float, idPoint=-1)->bool:
        """
        crée un nouveau point aux coordonnées de la souris
        ajoute un point sur le Canvas et l'enregistre dans le monde après division par le zoom
        
        Paramètres
        ----------
        x,y : float
            couple de coordonnées d'un nouveau point sur le canvas
       [idPoint] : int
            identifiant du nouveau point
            
        Valeur renvoyée
        ---------------       
        bool
            valeur indiquant si l'ajout a été réalisé
        """
        #vérifie si la place est libre
        for indice in self.points:
            if self.points[indice].distanceReelle((x,y)) <= 1:
                return False
                
        #création sur le canvas d'un nouvel objet tkinter
        tkinterPoint = self.create_oval(x-self.rayon, y-self.rayon, x+self.rayon, y+self.rayon, fill=NOIR)
        #print(tkinterPoint)
        #calcul de l'id du point
        if idPoint == -1:
            #on doit créer l'identifiant du nouveau point
            if self.points == {}:
                nouvelId = 0
            else:
                nouvelId = max(self.points.keys())+1
        else:
            nouvelId = idPoint
            
        #création d'une nouvelle entrée [idPoint: Point] dans le dictionnaire self.points
        #ou mise à jour de l'entrée existante si l'indice existait déjà
        self.points[nouvelId] = Point(tkinterPoint, x/self.zoom_factor, y/self.zoom_factor, NOIR)
        #On met à jour l'index des idTkinter
        self.indexIds[tkinterPoint] = nouvelId
        #On détermine l'ensemble des voisins du nouveau point
        self.setVoisins(nouvelId)
        #print(self.dicoVoisins())
        #important: C'est la fonctiopn appelante qui met le graphe à jour lorsqu'elle a fini de créer les points
        return True
        
    def ajouteListe(self, listePoints:list)->int:
        """
        ajoute une liste de points en faisant appel à ajoute_point
        
        Paramètres
        ----------
            listePoints : list[(float, float)] ou list[(float, float, int)]
                liste de coordonnées de points, éventuellement avec l'indice du point

        Valeur renvoyée
        ---------------       
        int:
            nombre de points effectivement ajoutés
        """
        nombreSucces = 0
        for p in listePoints:
            if len(p)==2:
                if self.ajoute_point(p[0], p[1]):
                    nombreSucces += 1
            elif len(p)==3:
                if self.ajoute_point(p[0], p[1], p[2]):
                    nombreSucces += 1
        self.setGraphe()
        return nombreSucces
      
    def pointClique(self, x:float,y:float)->list[int]:
        """
        Paramètres
        ----------
            x,y : float
                couples de coordonnees

         Valeur renvoyée
         ---------------       
         list[int]
            liste des identifiants des points pour lesquels la distance à (x,y) est minimale
            renvoie plusieurs identifiants uniquement s'il y a des exaequo
        """
        #coordonnees dans le monde échelle 1
        x = x/self.zoom_factor
        y = y/self.zoom_factor
        distNuage = [self.distance((x,y), self.points[pId].coordonnees) for pId in self.points]
        if distNuage != []:
            dMin = min(distNuage)
            if dMin < self.rayon/self.zoom_factor:
                return [pId for pId in self.points if self.distance((x,y), self.points[pId].coordonnees) == dMin]
        return []

    def mouseDown(self, event):
        """
        appelé lors d'un clic de souris. 
        Crée un nouveau point ou sélectionne un point existant
        
        Paramètres
        ----------
        event : évenement créé par un clic de souris
        """
        x, y = event.x, event.y
        #liste des id des points à la distance Min
        closest = self.pointClique(x,y)
        if closest !=[]:
            #récupère l'id tkinter (dans le canvas) du point cliqué
            self.selObject = self.points[closest[0]].getTkinterId()
            if self.affichage:
                print(closest[0],self.points[closest[0]].getCoordonnees(), " sélectionné")
            self.itemconfig(self.selObject, width =5)
        else:
            self.nouveau_point(event)
            self.setGraphe()


    def mouseMove(self, event):
        """
        appelé lors d'un déplacement de la souris. 
        
        Paramètres
        ----------
        event : évenement créé par un déplacement de souris
        
        Action
        ------
        modifie les coordonnées du point sélectionné, s'il existe
        met à jour le graphe en conséquence
        """        
        #print("on bouge")
        newx = event.x
        newy = event.y
        #print("nouveaux: ",newx, newy)
        if self.selObject:
            pId = self.indexIds[self.selObject]
            #coordonnées de l'objet tkinter (ellipse)
            a,b,c,d = self.coords(self.selObject)
            dx = newx - (a+c)//2
            dy = newy - (b+d)//2
            #print("move: ",dx, dy)
            self.move(self.selObject, dx, dy)
            f = self.zoom_factor
            self.points[pId].coordonnees = (newx/f, newy/f)
            #Supprimer les anciennes aretes
            self.effaceVoisinage(pId)
             #et en créer de nouvelles
            self.setVoisins(pId)
            self.setGraphe()




    def mouseDownBis(self, event):
        """
        appelée lors d'un clic droit. 
        
        Paramètres
        ----------
        event : évenement créé par un clic droit
        
        Action
        ------
        supprime le point cliqué
        met à jour le graphe en conséquence
        """ 
        #print("clic droit")
        x, y = event.x, event.y
        closest = self.pointClique(x,y)
        if closest !=[]:
            #identifiants monde et canvas
            choisi = closest[0]
            idTkChoisi = self.points[choisi].getTkinterId()
            self.effaceVoisinage(choisi)
            #supprime le point
            self.points.pop(choisi)
            #met à jour le graphe
            #print(self.dicoVoisins())
            self.setGraphe()
            #le point était-il élu dans un des réseaux?
            for r in self.reseaux:
                if r.getCentreGrav()==choisi:
                    r.setCentreGrav()
                if r.getCentreGeom()==choisi:
                    r.setCentreGeom()
                listekBFS = r.getidkBFS()
                if choisi in listekBFS:
                    listekBFS.remove(choisi)
            #efface le point - méthode du canvas
            self.delete(idTkChoisi)
            

    def mouseUp(self, event):
        """
        appelée au relâchement du bouton de la souris.
        
        Paramètres
        ----------
        event : évenement créé par le relâchement du bouton
        
        Action
        ------
        déselectionne un éventuel point sélectionné
        """
        #self.selObject contient l'id du point sélectionné
        if self.selObject:
            #taille normale
            self.itemconfig(self.selObject, width =1)
            self.selObject = None
            
    def effaceVoisinage(self,idPoint:int):
        """
         Paramètres
        ----------
        idPoint : int
            identifiant d'un point
            
        Actions
        -------
        efface le voisinage d'un point en vidant son dictionnaire des voisins 
        efface les références à ce point chez ses anciens voisins
        fonction appelée avant de déplacer ou de supprimer un point
        """
        for autreId in self.points[idPoint].voisins:
            #efface l'arete
            self.delete(self.points[idPoint].voisins[autreId])
            self.points[autreId].voisins.pop(idPoint)
        self.points[idPoint].voisins = {}
        

        
    def dicoVoisins(self):
        """        
        Valeur renvoyée:
        ----------------
        dict[int, list[int]]
            tableau associant à chaque indice de point la liste des indices de ses voisins
            (représentation du graphe à l'aide de listes d'adjacence)
        """
        res = {}
        #les ids dans le monde sont les indices dans la liste
        for numSommet in self.points.keys():
            res[numSommet] = list(self.points[numSommet].voisins.keys())
        return res

    def setGraphe(self):
        """
        Action
        ------       
        construit le graphe (objet networkx.Graph) représentant le réseau
        fixe la valeur de self.graphe
        détermine les composantes connexes du graphe et remplit self.reseaux
        """
        G = nx.Graph()

        if self.points!={}:
            #On parcourt les indices des points
            for i in self.points.keys():
                G.add_node(i)
            #print(G.nodes)
            d = self.dicoVoisins()
            edges = [(i,j) for i in d.keys() for j in d[i]]
            #print("dico des Voisins: ",d)
            G.add_edges_from(edges)
            self.graphe = G
            #print(G.nodes)
            #suppression des couleurs
            for pId in self.points:
                self.itemconfig(pId, fill=NOIR, width =1)
            #Recherche des composantes connexes et construction d'autant de réseaux
            for r in self.reseaux:
                r.effaceCouleurs()

            nonAffectes = list(self.points.keys())
            #print(len(nonAffectes)," noeuds à affecter")
            self.reseaux = []
            while nonAffectes !=[]:
                #on récupère la liste constituant la composante connexe du 1er
                comp = self.composanteConnexe(nonAffectes[0])
                #print(len(comp)," dans un réseau")
                self.reseaux.append(Reseau(self, comp))
                nonAffectes = [i for i in nonAffectes if i not in comp]
                #print("reseau ",len(self.reseaux))
            #print("construit: ",G)
            self.setCouleurs()
        else:
            #a-t-on effacé tous les points?
            self.reseaux = []

    def getGraphe(self):
        return self.graphe    
        
    def composanteConnexe(self, i0:int)->list[int]:
        """
         Paramètres
        ----------
        i0  : int
            identifiant d'un point
            
        Valeur renvoyée
        ---------------
        list[int]
            liste des indices des points de la composante connexe de i0
        """
        #on utilise le dictionnaire des voisins (= liste d'adjacence)
        #pour effectuer un parcours en largeur
        d = self.dicoVoisins()
        res = [i0]
        explo = [i0]
        while explo !=[]:
            i = explo.pop(0)
            for indice in d[i]:
                if indice not in res:
                    res.append(indice)
                    explo.append(indice)
        return res    

    def reseauPrincipal(self):
        """        
        Valeur renvoyée
        ---------------
        Reseau
            le réseau représentant la composante connexe la plus importante
        """
        if self.reseaux !=[]:
            tailleMax = self.reseaux[0].getTaille()
            resultat = self.reseaux[0]
            for r in self.reseaux:
                if r.getTaille()>tailleMax:
                    tailleMax = r.getTaille()
                    resultat = r
            return resultat
                    
        
    def setCouleurs(self, affichage=False):
        """
         Paramètres
        ----------
        affichage: bool
        
        Action
        ------
        appelle setCouleurs sur chacune des composantes connexes du monde
        """
        for r in self.reseaux:
            r.setCouleurs(affichage)
       
    def bestAlgorithmes(self, affichage=False):
        """
         Paramètres
        ----------
        affichage: bool
        
        Action
        ------
        appelle bestAlgorithme (comparaison des algorithmes d'élection)
        sur la composante connexe principale
        """
        R = self.reseauPrincipal()
        R.bestAlgorithme(affichage)
        #for r in self.reseaux:
        #    r.bestAlgorithme(affichage)

    # def setPosition(self, num, x, y):
        # self.positions[num].setPosition(x, y)
        


    def chargeCSV(self, nomFichier:str)->bool:
        """
        Paramètres
        ----------
        nomFichier : str
            nom d'un fichier csv
        
        Action
        ------
        lis le contenu du fichier dont le nom est passé en paramètre et ajoute les points dans le monde. 
        
        Valeur renvoyée
        ---------------
        bool
            valeur indiquant si le fichier existe
        """
        #print("lecture du contenu de ",nomFichier)
        self.delete("all")
        self.points = {}
        self.fichier = nomFichier
        with open(self.fichier, 'r') as fichier:
            lignes = fichier.readlines()
            rempli = len(lignes)>1
            if (rempli):
                f = self.zoom_factor
                for ligne in lignes[1:]:
                    #print(ligne)
                    contenu = ligne.split(",")
                    self.ajoute_point(float(contenu[1])*f, float(contenu[2])*f, int(contenu[0]))
        self.setGraphe()
        self.setCouleurs()
        #if self.affichage:
        #    for r in self.reseaux:
        #        r.bestAlgorithme(True)

            
    def sauveCSV(self, nom="test.csv", indices=None):
        """
        Paramètre
        ----------
        nom : str
            nom d'un fichier csv
        indices : list[int]
            liste des indices des points dont il faut sauvegarder les caractéristiques
        
        Action
        ------
           enregistre les coordonnées des points dans un csv dont le nom est donné en paramètre
        """
        if indices==None:
            indices = list(self.points.keys())
        target = open(nom,"w")
        target.write("id,x,y,portee\n")
        for i in indices:
            p = self.points[i]
            target.write(str(i)+","+str(float(p.getX()))+","+str(float(p.getY()))+","+str(self.portee)+"\n")
        target.close()       
    

    def sauvePNG0(self, nom="test.png", indices=None, radius = -1, aretes=True, couleurs=False):
        """
        Paramètre
        ----------
        nom : str
            nom du fichier de sortie
        
        indices : list[int]
            liste des indices des points dont il faut sauvegarder les caractéristiques

        radius : int
            rayon des disques représentant les noeuds du réseau
            
        aretes : bool
            indique s'il faut dessiner les aretes
            
        couleurs : bool
            indique si on doit colorer le centre de gravité
            
        Action
        ------
           enregistre une image représentant le réseau dans un png dont le nom est donné en paramètre
        """
        valTransparence = 150
        codesCouleurs = [(231, 29, 67, valTransparence), (255, 0, 0,valTransparence),(255, 55, 0, valTransparence), (255, 110, 0, valTransparence),
                        (255, 165, 0, valTransparence), (255, 195, 0, valTransparence), (255, 225, 0, valTransparence), (255, 255, 0, valTransparence),
                         (170, 213, 0, valTransparence), (85, 170, 0, valTransparence), (0, 128, 0, valTransparence), (0, 85, 85, valTransparence),
                          (0, 43, 170, valTransparence), (0, 0, 255, valTransparence), (25, 0, 213, valTransparence), (50, 0, 172, valTransparence),
                           (75, 0, 130, valTransparence), (129, 43, 166, valTransparence), (184, 87, 202, valTransparence), (208, 58, 135, valTransparence)] 
        if indices == None:
            indices = list(self.points.keys())
        if radius == -1:
            radius = self.rayon
        
        padding = 5
        imSize = (self.width+2*padding,self.height+2*padding)
        #Création de l'image (fond blanc)
        target = Image.new(mode="RGB", size=imSize, color=(255,255,255))
        #Un premier "calque" sur lequel on posera le points avec transparence
        transp1 = Image.new(mode="RGBA", size=imSize, color=(255,255,255,127))
        for R in self.reseaux:
            centre = R.setCentreGeom()
            for i in [k for k in R.indices if k in indices]:
                point = self.points[i]
                x, y = self.points[i].coordonnees
                x = self.monde2Ecran(x,padding)
                y = self.monde2Ecran(y,padding)
                r = radius
                #nouveau "calque" pour le point et ses aretes
                transp2 = Image.new('RGBA', imSize, (255,255,255,0)) 
                draw = ImageDraw.Draw(transp2, "RGBA")
                if couleurs:
                    d = R.graphDistance(centre, i)
                    if d<20:
                        draw.ellipse(xy=(x-r,y-r,x+r,y+r), outline=(0,0,0), width=5, fill=codesCouleurs[d])
                    else:
                        draw.ellipse(xy=(x-r,y-r,x+r,y+r), outline=(0,0,0), width=5, fill=codesCouleurs[19])
                else:
                    draw.ellipse(xy=(x-r,y-r,x+r,y+r), outline=(0,0,0), width=5, fill=(150,0,0,130))
            
                if aretes:
                    for autreId in point.voisins:                    
                        xp, yp = self.points[autreId].coordonnees
                        xp = self.monde2Ecran(xp,padding)
                        yp= self.monde2Ecran(yp,padding)
                        #dessine l'arete
                        draw.line(xy=(x,y,xp,yp), fill=(0,0,0), width=10)
                    
                # Alpha composite two images together and replace first with result.
                transp1.paste(Image.alpha_composite(transp1, transp2))
            
        target = transp1.convert("RGB")
        target.save(nom)


    def sauvePNG(self, nom="test.png", indices=None, radius = -1, aretes=False):
        """
        Paramètre
        ----------
        nom : str
            nom du fichier de sortie
        
        indices : list[int]
            liste des indices des points dont il faut sauvegarder les caractéristiques

        radius : int
            rayon des disques représentant les noeuds du réseau
            
        aretes : bool
            indique s'il faut dessiner les aretes
            
        couleurs : bool
            indique si on doit colorer le centre de gravité
            
        Action
        ------
           enregistre une image représentant le réseau dans un png dont le nom est donné en paramètre
        """
        valTransparence = 150
        codesCouleurs = [(231, 29, 67, valTransparence), (255, 0, 0,valTransparence),(255, 55, 0, valTransparence), (255, 110, 0, valTransparence),
                        (255, 165, 0, valTransparence), (255, 195, 0, valTransparence), (255, 225, 0, valTransparence), (255, 255, 0, valTransparence),
                         (170, 213, 0, valTransparence), (85, 170, 0, valTransparence), (0, 128, 0, valTransparence), (0, 85, 85, valTransparence),
                          (0, 43, 170, valTransparence), (0, 0, 255, valTransparence), (25, 0, 213, valTransparence), (50, 0, 172, valTransparence),
                           (75, 0, 130, valTransparence), (129, 43, 166, valTransparence), (184, 87, 202, valTransparence), (208, 58, 135, valTransparence)] 
        if indices == None:
            indices = list(self.points.keys())
        if radius == -1:
            radius = self.rayon
        
        padding = 5
        imSize = (self.width+2*padding,self.height+2*padding)
        #Création de l'image (fond blanc)
        target = Image.new(mode="RGB", size=imSize, color=(0,0,0))
        #Un premier "calque" sur lequel on posera le points avec transparence
        transp1 = Image.new(mode="RGBA", size=imSize, color=(0,0,0,255))
        for R in self.reseaux:
            for i in [k for k in R.indices if k in indices]:
                point = self.points[i]
                x, y = self.points[i].coordonnees
                x = self.monde2Ecran(x,padding)
                y = self.monde2Ecran(y,padding)
                r = radius
                #nouveau "calque" pour le point et ses aretes
                transp2 = Image.new('RGBA', imSize, (0,0,0,0)) 
                draw = ImageDraw.Draw(transp2, "RGBA")
                #dessin du disque rouge
                draw.ellipse(xy=(x-r,y-r,x+r,y+r), outline=(0,0,0), width=0, fill=(255,0,0,130))
            
                if aretes:
                    for autreId in point.voisins:                    
                        xp, yp = self.points[autreId].coordonnees
                        xp = self.monde2Ecran(xp,padding)
                        yp= self.monde2Ecran(yp,padding)
                        #dessine l'arete
                        draw.line(xy=(x,y,xp,yp), fill=(0,0,0), width=10)
                    
                # Alpha composite two images together and replace first with result.
                transp1.paste(Image.alpha_composite(transp1, transp2))
            
        target = transp1.convert("RGB")
        
        #On ajoute sur le canal vert une valeur donnant la distance au centre
        verte = Image.new(mode="RGB", size=imSize, color=(0,0,0))
        draw = ImageDraw.Draw(verte, "RGB")
        for R in self.reseaux:
            centre = R.setCentreGeom()
            for i in [k for k in R.indices if k in indices]:
                x, y = self.points[i].coordonnees
                x = self.monde2Ecran(x,padding)
                y = self.monde2Ecran(y,padding)
                r = radius
                #dessin du disque vert
                d = R.graphDistance(centre, i)
                draw.ellipse(xy=(x-r,y-r,x+r,y+r), outline=(0,0,0), width=0, fill=(0,15*d,0))
                
        target = ImageChops.add(target, verte)

        
        target.save(nom)

    def ecrire(self):
        """
        Action
        ------
        enregistre les coordonnées de tous les points
        dans le fichier dont le nom figure dans self.fichier (fichier ouvert et modifié)
        """
        self.sauveCSV(self.fichier)
        
    def monde2Ecran(self, x, padding)->float:
        """
        Paramètre
        ----------
        x : float
            coordonnée dans le monde
        padding : float
            marge autour du réseau dans le canvas
        
        Valeur renvoyée
        ---------------
        float
           valeur de la coordonnée sur la surface graphique
        """
        return x*self.zoom_factor + padding
       
        



class Reseau:
    """
    Représente un réseau connexe inclus dans un monde.
    Créé par une instance de la classe Monde
    ...

    Attributs
    ----------
    monde : Monde
        le monde dans lequel le réseau a été créé
        
    indices : list[int]
        liste des indices des points qui font partie du réseau
    
    graphe : objet networkx.Graph
        le sous-graphe de monde.graphe représentant le réseau
        
    idMin : int
        identifiant minimum présent dans le réseau
        
    idGrav : int
        indice du centre de gravité du réseau

    idGeom : int
        indice du centre géométrique du réseau
        
    idkBFS : list[int]
        liste des indices des candidats obtenus après exécution de l'algorithme kBFS
        
    exterieurs : list[int]
        liste des indices des noeuds exterieurs déterminés par l'algorithme kBFS


    Méthodes
    -------
    dicoVoisins()
        renvoie un tableau associant à chaque indice de point la liste des indices de ses voisins
        (représentation du graphe à l'aide de listes d'adjacence)
    
    getIndices():
        renvoie les indices des points constituant le réseau

    getTaille()
        renvoie le nombre de noeuds du réseau
    
    getCoordonnees(i:int)
        renvoie les coordonnées du point dont l'indice est passé en paramètre
    
    getCoordonneesReseau()
        renvoie la liste des coordonnées de tous les points du réseau
        
    getIndice(point)
        renvoie l'indice du point ou -1 si le point n'est pas dans le monde
        
    dMax(idPoint, listeIds)
        renvoie la distance maximale (calculée avec graphDistance) 
        entre le noeud dont l'id est passée en paramètre et les noeuds dont les indices sont dans la liste constituant le 2e paramètre
        
        renvoie -1 si un des points n'est pas dans le réseau.

    graphDistance(id0, id1)
        renvoie la longueur du chemin le plus court entre les points dont les ids sont passés en paramètre
        renvoie -1 si un des points n'est pas dans le réseau.
        
    distances(id0, listeIds)
        renvoie la liste des distances entre le point d'indice id0 et ceux dont l'indice est dans listeIds
        la liste renvoyée contient -1 si un des points n'est pas dans le réseau
        
    dMax(id0, listeIds)
        renvoie la distance maximale entre le point d'indice id0 et ceux dont l'indice est dans listeIds
    
    distanceSum(id0, listeIds)
        renvoie la somme des distances entre le point d'indice id0 et ceux dont l'indice est dans listeIds
    
    plusLoin(id0, listeIds)
        renvoie    l'id du point dont l'indice figure dans listeIds qui est le plus éloigné de celui d'indice id0
        En cas d'égalité, renvoie l'identifiant minimal
        renvoie -1 si un des points n'est pas dans le réseau ou s'il y a une erreur dans le calcul des distances
    
    plusLoinDuGroupe(listeIds)
        renvoie l'id du point du réseau le plus éloigné de ceux dont l'indice figure dans listeIds (somme des distances)
        En cas d'égalité, renvoie l'identifiant minimal
        renvoie -1 en cas d'erreur
        
    dicoArbre(id0)   
        renvoie un dictionnaire représentant l'arbre associé à un parcours en largeur de racine id0
        associe à chaque indice l'objet Noeud(id, parent, profondeur)
        
    distancePlusProche(x,y)
        renvoie la distance entre les coordonnées (x,y) et le point le plus proche dans le réseau
        renvoie -1.0 en cas d'erreur

    plusProcheCoord(x, y)
        renvoie    l'indice du point du réseau le plus proche de (x,y)
        renvoie -1 en cas d'erreur
    
    idTkinter(idPoint)
        renvoie l'identifiant tkinter du point dont l'indice est donné en paramètre
        
    effaceCouleurs()
        remet en noir tous les points spéciaux (différents types de leader) du réseau
    
    setCouleurs(affichage=False)
        détermine les indices des différents leaders et fixe leur couleur
        La recherche des leaders est détaillée dans la console si le paramètre affichage vaut True         
        
    setCentreGrav()
       détermine le point le plus proche du centre de gravité du réseau
       fixe la valeur de l'attribut idGrav
       renvoie la valeur de idGrav
        
    getCentreGrav()
        renvoie la valeur de idGrav

    setCentreGeom()
       détermine le point le plus proche du centre du rectangle de base horizontale contenant le réseau
       fixe la valeur de l'attribut idGeom
       renvoie la valeur de idGeom

    getCentreGeom()
       renvoie la valeur de idGeom

    treeCentralityCandidates()
        renvoie la liste des indices des noeuds sélectionnés par l'algorithme 'tree-based-centrality' (noeuds de profondeur moyenne)
    
    ABCCandidates(affichage=False)
        renvoie la liste des indices des noeuds sélectionnés après stabilisation de 'ABC-Center'
        le paramètre 'affichage' indique s'il faut afficher le détail des étapes de l'algorithme
    
    slowABCCandidates(affichage=False)
        renvoie la liste des indices des noeuds sélectionnés après stabilisation d'une variante de 'ABC-Center'
        (le choix des candidats est plus laxiste sur les premières itérations)
        le paramètre 'affichage' indique s'il faut afficher le détail des étapes de l'algorithme
    
    kBFSCandidates(k, affichage=False)
        renvoie la liste des indices des noeuds sélectionnés après  k itérations de 'kBFS'
        fixe la valeur des attributs 'idkBFS' et 'exterieurs'
        le paramètre 'affichage' indique s'il faut afficher le détail des étapes de l'algorithme
        
    getidkBFS()
        renvoie la valeur de l'attribut idkBFS (liste des candidats déterminés par kBFS)
        
    bestAlgorithme(affichage=False, algos = ['centreGeom', 'centreGrav', 'ABC', 'slowABC', 'kBFS'])
        renvoie parmi les algorithmes de la liste passée en paramètre celui qui donne le meilleur résultat
    """
    
    def __init__(self, monde, listeIndices):
        '''reçoit une liste d'indices de points du monde'''
        self.monde = monde        
        self.indices = listeIndices #liste d'indices de points
        self.graphe = nx.subgraph(self.monde.getGraphe(), self.indices)
        self.idMin = min(self.indices)
        self.idGrav = None
        self.idGeom = None
        self.idkBFS = []
        self.exterieurs = []
        #print(self.graphe)
        #print(self.monde.getGraphe())
        
    def __str__(self):
        return str(self.indices)
        
    def dicoVoisins(self):
        """        
        Valeur renvoyée:
        ----------------
        dict[int, list[int]]
            tableau associant à chaque indice de point la liste des indices de ses voisins
            (représentation du graphe à l'aide de listes d'adjacence)
        """
        res = {}
        #les ids dans le monde sont les indices dans la liste
        for numSommet in self.indices:
            res[numSommet] = list(self.monde.points[numSommet].voisins.keys())
        return res

    
    def getIndices(self):
        """
        Valeur renvoyée:
        ----------------
        list[int]
            les indices des points constituant le réseau
        """
        return self.indices
                         
    def getTaille(self):
        """
        Valeur renvoyée:
        ----------------
        int
            le nombre de noeuds du réseau
        """
        return len(self.indices)

    def getCoordonnees(self, i:int)->tuple[float,float]:
        """
        Paramètre
        ---------
        i : int
            indice d'un des points du réseau
            
        Valeur renvoyée:
        ----------------
        tuple[float,float]
            les coordonnées du point dont l'indice est passé en paramètre
        """        
        p = self.monde.points[i]
        return (p.getX(), p.getY())
        
    def getCoordonneesReseau(self)->list[tuple[float,float]]:
        """           
        Valeur renvoyée:
        ----------------
        list[tuple[float,float]]
            liste des coordonnées de tous les points du réseau
        """        
        return [self.getCoordonnees(i) for i in self.indices]

    def contient(self, i:int)->bool:
        """
        Paramètre
        ---------
        i : int
            indice d'un des points du réseau
            
        Valeur renvoyée:
        ----------------
        bool
            une valeur indiquant si le point appartient au réseau
        """        
        return i in self.indices

    def getIndice(self, point)->int:
        """
        Paramètre
        ---------
        point : Point
            instance de la classe Poinr
            
        Valeur renvoyée:
        ----------------
        int
            l'indice du point.
            renvoie -1 si le point n'appartient pas au monde
        """        
        for i in self.indices:
            if self.monde.getPoint(i) == point:
                return i
        return -1
                                  
                                
    
    def graphDistance(self, id0:int, id1:int)->int:
        """
        Paramètre
        ---------
        id0, id1 : int
            indices de deux points du réseau
                   
        Valeur renvoyée:
        ----------------
        int
            longueur du chemin le plus court entre les points d'indice id0 et id1
            renvoie -1 si un des points n'est pas dans le réseau.
        """
        try:
            res = nx.shortest_path_length(self.graphe,id0,id1)
            return res
        except:
            #ne doit jamais arriver car le réseau est censé être connexe
            return -1
        
    def distances(self, id0:int, listeIds:list[int])->list[int]:
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        listeIds : list[int]
            liste d'indices de points du réseau
            
        Valeur renvoyée:
        ----------------
        list[int]
            liste des distances entre le noeud d'indice id0 et les noeuds dont l'indice figure dans listeIds
            cette liste contient -1 si un des noeuds n'est pas dans le réseau
        """
        #Precondition
        if not self.contient(id0):
            return [-1]
        return [self.graphDistance(id0,y) for y in listeIds]
        
        
    def dMax(self, id0:int, listeIds:list[int])->int:
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        listeIds : list[int]
            liste d'indices de points du réseau
            
        Valeur renvoyée:
        ----------------
        int
            distance maximale entre le noeud d'indice id0 et les noeuds dont l'indice figure dans listeIds
            renvoie -1 si un des points n'est pas dans le réseau.
        """
        distances = self.distances(id0, listeIds)
        if -1 in distances or distances == []:
            return -1
                
        return max(distances)

    def distanceSum(self, id0:int, listeIds:list[int])->int:
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        listeIds : list[int]
            liste d'indices de points du réseau
            
        Valeur renvoyée:
        ----------------
        int
            somme des distances entre le noeud d'indice id0 et les noeuds dont l'indice figure dans listeIds
            renvoie -1 si un des points n'est pas dans le réseau.
        """
        distances = self.distances(id0, listeIds)
        if -1 in distances or distances == []:
            return -1
                
        return sum(distances)

    
    def exc(self, id0:int)->int:
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        Valeur renvoyée:
        ----------------
        int        
            excentricité du point d'indice id0
        """
        if self.graphe is None:
            return -1
        return self.dMax(id0, self.graphe.nodes)
        #try:
         #   e = nx.eccentricity(self.graphe, idPoint)
          #  return e
        #except:
         #   return -1
    
        
    def plusLoin(self, id0:int, listeIds:list[int])->int:
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        listeIds : list[int]
            liste d'indices de points du réseau

        Valeur renvoyée:
        ----------------
        int        
            id du point dont l'indice figure dans listeIds qui est le plus éloigné de celui d'indice id0
            En cas d'égalité, renvoie l'identifiant minimal
        """
        dMax = self.dMax(id0, listeIds)
        if dMax>0:
            listePlusLoins = [ idx for idx in listeIds if self.graphDistance(id0,idx) == dMax]
            return min(listePlusLoins)
        else:
            return -1
        #nx.shortest_path(G,p) donne le dictionnaire des chemins depuis p
        #distances = [len(chemin)-1 for point,chemin in nx.shortest_path(self.graphe,idPoint).items() if point in ensemble]

    
    def plusLoinDuGroupe(self, listeIds:list[int])->int:
        """
        Paramètre
        ---------
        listeIds : list[int]
            liste d'indices de points du réseau
        
        Valeur renvoyée:
        ----------------
        int        
            id du point du réseau le plus éloigné de ceux dont l'indice figure dans listeIds (somme des distances)
            En cas d'égalité, renvoie l'identifiant minimal
        """
        sommes = [self.distanceSum(idx, listeIds) for idx in self.graphe.nodes if idx not in listeIds]
        if sommes == [] or -1 in sommes:
            sommeMax = 0
            listePlusLoins = []
        else:
            sommeMax = max(sommes)
            listePlusLoins = [ idx for idx in self.graphe.nodes if self.distanceSum(idx,listeIds) == sommeMax and idx not in listeIds]
            #tri des ids par ordre croissant
            listePlusLoins.sort()
        #print("sommeMax: ",sommeMax)
        if len(listePlusLoins)==0:
            return -1
        else:
            #print("plus loin: ",listePlusLoins[0],", à la distance ",self.distanceSum(listePlusLoins[0], listeIdPoints))
            return listePlusLoins[0]

        
    def dicoArbre(self, id0):   
        """
        Paramètre
        ---------
        id0 : int
            indice d'un point du réseau
        
        Valeur renvoyée:
        ----------------
        dict[int, Noeud] 
            dictionnaire représentant l'arbre associé à un parcours en largeur de racine id0
            associe à chaque indice l'objet Noeud(id, parent, profondeur)
        """
        #construction de l'arbre
        #P représente le parcours en largeur
        #E représente la liste des sommets dont il faut explorer les voisins
        P = [id0]
        E = [id0]
        arbre = {id0:Noeud(id0, None, 0)}
        while len(E)>0 :
            c = E.pop(0)
            for v in self.monde.points[c].voisins.keys():
                if v not in P:
                    profondeur = arbre[c].getProfondeur()+1
                    arbre[v] = Noeud(v, arbre[c], profondeur)
                    arbre[c].layerUpdate(1)
                    P.append(v)
                    E.append(v)
        return arbre
        

    def distancePlusProche(self, x:float,y:float)->float:
        """
        Paramètre
        ---------
        x,y : float
            couple de coordonnées dans le monde (pas dans le canvas)
        
        Valeur renvoyée:
        ----------------
        float
            distance entre les coordonnées (x,y) et le point le plus proche dans le réseau
            -1.0 en cas d'erreur
        """
        #coordonnees dans le monde échelle 1
        distNuage = [self.monde.distance((x,y), self.monde.points[pId].coordonnees) for pId in self.indices]
        if distNuage != []:
            return min(distNuage)
        return -1.0

    def plusProcheCoord(self, x:float,y:float)->int:
        """
        Paramètre
        ---------
        x,y : float
            couple de coordonnées dans le monde (pas dans le canvas)
        
        Valeur renvoyée:
        ----------------
        int
            indice du point du réseau le plus proche de (x,y). En cas d'égalité l'indice minimum.
            -1 en cas d'erreur
        """
        dMin = self.distancePlusProche(x,y)
        if dMin >=0:
            #print("point le plus proche à distance ",dMin)
            res = [pId for pId in self.monde.points if self.monde.distance((x,y), self.monde.points[pId].coordonnees) == dMin]
            return res[0]
        return -1

    def idTkinter(self, idPoint):
        """
        Paramètre
        ---------
        idPoint : int
            indice d'un point dans le monde (pas dans le canvas)
        
        Valeur renvoyée:
        ----------------
        int
            identifiant tkinter du point sur le canvas
        """
        return self.monde.points[idPoint].getTkinterId()
        
    def effaceCouleurs(self):
        """      
        Action
        ------
        remet en noir tous les points spéciaux du réseau
        """
        if self.idGrav != None:
            #print("reconfigure centre Grav")
            #print(self.idTkinter(self.idGrav))
            self.monde.itemconfig(self.idTkinter(self.idGrav), fill=NOIR)
            self.idGrav = None

        if self.idGeom != None:
            #print("reconfigure centre Geom")
            self.monde.itemconfig(self.idTkinter(self.idGeom), fill=NOIR)
            self.idGeom = None

        if self.idkBFS != []:
            for i in self.idkBFS:
                self.monde.itemconfig(self.idTkinter(i), fill=NOIR)
            self.idkBFS = []

    def setCouleurs(self, affichage=False):
        """
        Paramètre
        ---------
        affichage : bool
            valeur indiquant si la recherche des différents leaders doit être détaillée dans la console
        
        Action
        ------
        détermine les indices des différents leaders et fixe leur couleur          
        """    
        self.effaceCouleurs()
        if self.monde.showGrav:
            self.setCentreGrav()
            #print("après: ",self.idGrav, self.idGeom)
            self.monde.itemconfig(self.idTkinter(self.idGrav), fill=VERT)
            
        if self.monde.showGeom:
            self.setCentreGeom()
            self.monde.itemconfig(self.idTkinter(self.idGeom), fill=ROUGE)
        
        if self.monde.showCandidats:
            #print("kBFS depuis ", self.idMin)
            self.idkBFS = self.kBFSCandidates(self.monde.k, affichage)
            #print(self.idkBFS)
            for i in self.idkBFS:
                self.monde.itemconfig(self.idTkinter(i), fill=CYAN)
                
            #Visualiser les exterieurs
            #for i in self.exterieurs:
                #self.monde.itemconfig(self.idTkinter(i), fill=NOIR, width=5)
        self.slowABCCandidates(affichage)

                    
    def setCentreGrav(self):
        """
        Action
        ------
           détermine le point le plus proche du centre de gravité du réseau
           fixe la valeur de l'attribut idGrav
        
        Valeur renvoyée
        ---------------
        int
           indice du point le plus proche du centre de gravité
        """
        if self.indices==[]:
            return None
        points = [self.monde.points[i] for i in self.indices]
        abscisses = [p.getX() for p in points]
        ordos = [p.getY() for p in points]
        #print(sum(abscisses)/len(abscisses), sum(ordos)/len(ordos))
        self.idGrav = self.plusProcheCoord(sum(abscisses)/len(abscisses), sum(ordos)/len(ordos))
        #print("centre de gravité: ",self.idGrav)
        return self.idGrav
        
    def getCentreGrav(self):
        return self.idGrav

    def setCentreGeom(self):
        """
        Action
        ------
           détermine le point le plus proche du centre du rectangle de base horizontale contenant le réseau
           fixe la valeur de l'attribut idGeom
        
        Valeur renvoyée
        ---------------
        int
           indice du point le plus proche du centre du rectangle
        """
        if self.indices ==[]:
            return None
        points = [self.monde.points[i] for i in self.indices]
        abscisses = [p.getX() for p in points]
        ordos = [p.getY() for p in points]
        x = (max(abscisses) + min(abscisses))/2
        y = (max(ordos) + min(ordos))/2
        self.idGeom = self.plusProcheCoord(x,y)
        #print("centre géométrique: ",self.idGeom)
        return self.idGeom

    def getCentreGeom(self):
        return self.idGeom

    def treeCentralityCandidates(self)->list[int]:
        """
        Valeur renvoyée
        ---------------
        list[int]
           liste des indices des noeuds sélectionnés par l'algorithme 'tree-based-centrality'
           (noeuds de profondeur moyenne)
        """
        #La racine de l'arbre est le noeud d'identifiant minimal
        id0 = min(self.indices)
        #Représentation de l'arbre couvrant à l'aide de la classe Noeud
        arbre = self.dicoArbre(id0)
        
        sommeProfondeurs = 0
        for noeud in arbre.values():
            sommeProfondeurs += noeud.getProfondeur()
        if sommeProfondeurs == 0:
            return []
        profMoyenne = round(sommeProfondeurs/(len(arbre.keys())))
        res= [x for x in arbre.keys() if arbre[x].getLayer()==profMoyenne]
        #print(res)
        return res

    def ABCCandidates(self, affichage=False)->list[int]:
        """
        Paramètre
        ---------       
        affichage : bool
            valeur indiquant s'il faut afficher le détail des étapes de l'algorithme
            
        Valeur renvoyée
        ---------------
        list[int]
           liste des indices des noeuds sélectionnés après stabilisation de 'ABC-Center'
        """
        candidates = list(self.indices)
        actifs = []
        
        while len(candidates) > 1 and len(candidates) != len(actifs):
            #les noeuds actifs sont les vainqueurs de l'itération précédente
            actifs = list(candidates)
            self.exterieurs = []
            #identifiant de départ de l'arbre
            id0 = min(actifs)
            #Préciser à la fonction plusLoin quel est l'ensemble de référence (self.indices par défaut?)
            self.exterieurs.append(self.plusLoin(id0, actifs))
            if affichage:
                print("ABC depuis ",id0,self.getCoordonnees(id0),", exterieur ",self.exterieurs[0])
            if self.exterieurs == []:
                return []
            nouveau = self.plusLoin(self.exterieurs[0], actifs)
            if nouveau !=-1:
                self.exterieurs.append(nouveau)
            else:
                return []
            if affichage:
                print("exterieurs: ",self.exterieurs)
            #calcul des distances à B et C
            ecarts = [(i, abs(self.graphDistance(i,self.exterieurs[0])-self.graphDistance(i,self.exterieurs[1]))) for i in actifs]
            ecartMin = min([e[1] for e in ecarts])
            candidates = [e[0] for e in ecarts if e[1]==ecartMin]
            if affichage:
                print("candidats: ",[(x, self.exc(x)) for x in candidates])
        return candidates#, dMaxAcceptable

        
    def slowABCCandidates(self, affichage=False)->list[int]:
        """
        Paramètre
        ---------        
        affichage : bool
            valeur indiquant s'il faut afficher le détail des étapes de l'algorithme

        Valeur renvoyée
        ---------------
        list[int]
           liste des indices des noeuds sélectionnés après stabilisation d'une variante de 'ABC-Center'
           La variante consiste à être un peu plus laxiste sur le choix des candidats dans les premières itérations
        """
        candidates = list(self.indices)
        actifs = []
        #la marge de tolérance
        marge=2
        
        while len(candidates) > 1 and len(candidates) != len(actifs):
            #les noeuds actifs sont les vainqueurs de l'itération précédente
            actifs = list(candidates)
            self.exterieurs = []
            #identifiant de départ de l'arbre
            id0 = min(actifs)
            #Préciser à la fonction plusLoin quel est l'ensemble de référence (self.indices par défaut?)
            self.exterieurs.append(self.plusLoin(id0, actifs))
            if affichage:
                print("slowABC depuis ",id0,self.getCoordonnees(id0),", exterieur ",self.exterieurs[0])
            if self.exterieurs == []:
                return []
            nouveau = self.plusLoin(self.exterieurs[0], actifs)
            if nouveau !=-1:
                self.exterieurs.append(nouveau)
            else:
                return []
            if affichage:
                print("exterieurs: ",self.exterieurs)
            ecarts = [(i, abs(self.graphDistance(i,self.exterieurs[0])-self.graphDistance(i,self.exterieurs[1]))) for i in actifs]
            if affichage:
                print("ecarts: ",ecarts)
            ecartMin = min([e[1] for e in ecarts])
            candidates = [e[0] for e in ecarts if e[1] <= ecartMin+marge]
            if affichage:
                print("candidats: ",[(x, self.exc(x)) for x in candidates])
            #diminution de la marge
            marge = max(0,marge-2)
        return candidates#, dMaxAcceptable


    def kBFSCandidates(self, k:int, affichage=False)->list[int]:
        """
        Paramètre
        ---------
        k : int
            Le nombre de points extérieurs à déterminer            
        
        affichage : bool
            valeur indiquant s'il faut afficher le détail des étapes de l'algorithme
        
        
        Valeur renvoyée
        ---------------
        int
           liste des indices des noeuds sélectionnés après  k itérations de 'kBFS'
        """
        #print("recherche de candidats par l'algo kBFS")
        id0 = min(self.indices)
        if k <=1:
            return []
        self.exterieurs = []
        nouvel_exterieur = self.plusLoin(id0, self.indices)
        if nouvel_exterieur != -1:
            self.exterieurs.append(nouvel_exterieur)
        if affichage:
            print("depuis ",id0,", exterieur ",self.exterieurs[0])
        if self.exterieurs == []:
            if affichage:
                print("pas de 1er point exterieur")
            return []
        candidates = []
        k = min(k, len(self.indices)-1)
        dMaxAcceptable = -1
        for i in range(1,k):
            #print("iteration ",i)
            nouveau = self.plusLoinDuGroupe(self.exterieurs)
            if nouveau !=-1:
                self.exterieurs.append(nouveau)
            else:
                if affichage:
                    print("pas de nouvel exterieur, n vaut ",len(self.indices))
                return []
            if affichage:
                print("exterieurs: ",self.exterieurs)
            distsExt = [self.dMax(x, self.exterieurs) for x in self.graphe.nodes if x not in self.exterieurs]
#             if affichage:
#                 print("interieurs: ",[x for x in self.graphe.nodes if x not in exterieurs])
#                 print("distances aux exterieurs: ",distsExt)
            if distsExt==[]:
                dMaxAcceptable = -1
            else:
                dMaxAcceptable = min(distsExt)
                #print(dMaxAcceptable)
        candidates = [x for x in self.graphe.nodes if x not in self.exterieurs and self.dMax(x, self.exterieurs)==dMaxAcceptable]
        if affichage:
            print("candidats: ",[(x, self.exc(x)) for x in candidates])
        return candidates#, dMaxAcceptable
        
    def getidkBFS(self):
        return self.idkBFS

    def bestAlgorithme(self, affichage=False, algos = ['centreGeom', 'centreGrav', 'ABC', 'slowABC', 'kBFS', 'exact'])->str:
        """
        Paramètre
        ---------      
        affichage : bool
            valeur indiquant s'il faut afficher le détail des étapes de l'algorithme
            
        algos : list[str]
            liste des noms des algorithmes utilisables
        
        Valeur renvoyée
        ---------------
        str
           nom de l'algorithme qui donne un leader d'excentricité minimale.
           En cas d'égalité, renvoie le nom du 1er qui a été testé
        """
        resultats = {}
        if 'centreGeom' in algos:
            self.setCentreGeom()
            resultats['centreGeom'] = (self.idGeom, self.exc(self.idGeom))
        if 'centreGrav' in algos:
            self.setCentreGrav()
            resultats['centreGrav'] = (self.idGrav, self.exc(self.idGrav))
        if 'tree' in algos:
            candidats = self.treeCentralityCandidates()
            if candidats != []:
                winner = min(candidats)
                resultats['tree'] = (winner, self.exc(winner))
        if 'ABC' in algos:
            candidats = self.ABCCandidates(False)
            if candidats != []:
                winner = min(candidats)
                resultats['ABC'] = (winner, self.exc(winner))
        if 'slowABC' in algos:
            candidats = self.slowABCCandidates()
            if candidats != []:
                winner = min(candidats)
                resultats['slowABC'] = (winner, self.exc(winner))        
        if 'kBFS' in algos:
            self.idkBFS = self.kBFSCandidates(10, False)
            if self.idkBFS !=[]:
                winner = min(self.idkBFS)
                resultats['kBFS'] = (winner, self.exc(winner))           
        if 'exact' in algos:
            minExc = min([self.exc(i) for i in self.indices])
            elu = min([i for i in self.indices if self.exc(i) == minExc])
            resultats['exact'] = (elu, self.exc(elu))
        if affichage:
            print(resultats)
        if resultats == []:
            return "erreur"
        else:
            meilleurScore = min([ res[1] for res in resultats.values() ])
            meilleursAlgos =  [ cle for (cle, res) in resultats.items() if res[1] == meilleurScore ]      
            if affichage:
                print("meilleur: ",meilleursAlgos[0])
            return meilleursAlgos[0]

    
class Noeud:
    """
    Classe facilitant la représentation d'un arbre couvrant
    (utilisée par Reseau.dicoArbre() pour l'algorithme treeCentrality
    
    Attributs
    ---------
    id : int
        indice du point représentant le noeud
        
    parent : int
        indice du parent dans l'arbre couvrant
        
    profondeur : int
        profondeur du noeud
        
    layer : int
        niveau du noeud depuis sa base
        
    Méthodes
    --------
    setParent(unNoeud)
    setProfondeur(prof)
    getProfondeur()
    setLayer(layer)
    getLayer()
    """
    def __init__(self, idx, parent, prof):
        self.id = idx
        self.parent = parent
        self.profondeur = prof
        self.layer = 0
           
    def setParent(self, unNoeud):
        self.parent = unNoeud
        
    def getProfondeur(self):
        return self.profondeur
    
    def setProfondeur(self, prof):
        self.profondeur = prof

    def getLayer(self):
        return self.layer
    
    def setLayer(self, layer):
        self.layer = layer
        
    def layerUpdate(self, valeur):
        self.layer = max(self.layer, valeur)
        if self.parent is not None:
            self.parent.layerUpdate(self.layer+1)
            
    def __str__(self):
        return "(parent: "+str(self.parent)+", prof: "+str(self.profondeur)+", layer: "+str(self.layer)+")"



################# Programme principal ##################################

if (__name__ == "__main__"):

    def open_file_dialog():
        file_path = filedialog.askopenfilename()
        canvas.chargeCSV(file_path)
        
    def calcule():
        canvas.affichage = valAffichage.get()
        canvas.showGrav = valGrav.get()
        canvas.showGeom = valGeom.get()
        canvas.showCandidats = valCandidats.get()
        canvas.setCouleurs(canvas.affichage)
        
    def kdown():
        if canvas.k>1:
            canvas.k -= 1
            valk.set(str(canvas.k))
            canvas.setCouleurs(canvas.affichage)

    def kup():
        if canvas.k<10:
            canvas.k += 1
            valk.set(str(canvas.k))
            canvas.setCouleurs(canvas.affichage)

    def fixek(event):
        canvas.k = int(valk.get())
        canvas.setCouleurs(canvas.affichage)
        
    def best():
        canvas.bestAlgorithmes(True)

    graphique = True


    if graphique:
        LARGEUR = 800   
        HAUTEUR = 800       
               
        fen = Tk()
        
        canvas = Monde(500, 500, 85,1, fen)
        canvas.grid(column=0, rowspan=5)
        button1 = Button(fen, text="Importer une configuration", command=open_file_dialog)
        button1.grid(column=1, row=0)
        button2 = Button(fen, text="Sauver en PNG", command=canvas.sauvePNG)
        button2.grid(column=1, row=1)
        button3 = Button(fen, text="Sauver en CSV", command=canvas.sauveCSV)
        button3.grid(column=1, row=2)
        button3 = Button(fen, text="Best", command=best)
        button3.grid(column=1, row=4)
        
        cadre_cases = LabelFrame(fen, text="Options d'affichage")
        cadre_cases.grid(column=1, row=3, padx=10, pady=10)
        
        # Création des cases à cocher dans le cadre
        valGrav = IntVar()
        valGeom = IntVar()
        #valABC = IntVar()
        valCandidats = IntVar()
        valAffichage = IntVar()
        valk = IntVar()
        c1 = Checkbutton(cadre_cases, text="Affichage", height=2, width=20, variable=valAffichage, command=calcule)
        c2 = Checkbutton(cadre_cases, text="Centre geom", height=2, width=20, variable=valGeom, command=calcule)
        c3 = Checkbutton(cadre_cases, text="Centre grav", height=2, width=20, variable=valGrav, command=calcule)
        #c4 = Checkbutton(cadre_cases, text="ABC-Center", height=2, width=20, variable=valABC, command=calcule)
        valk.set("10")
        c1.pack()
        c2.pack()
        c3.pack()
        #c4.pack()
        controlek = Frame(cadre_cases)
        controlek.pack()
        c4 = Checkbutton(controlek, text="kBFS", height=2, width=10, variable=valCandidats, command=calcule)
        champk = Entry(controlek, textvariable=valk, width=2)
        BoutonMoins = Button(controlek, text = chr(0x2191), command=kup)
        BoutonPlus = Button(controlek, text = chr(0x2193), command=kdown)
        c4.pack(side=LEFT)
        champk.pack(side =LEFT)
        BoutonMoins.pack(side =LEFT)
        BoutonPlus.pack(side =LEFT)
#        c1.grid(column=0, row=0, padx=10, pady=5, columnspan=3)
#        c2.grid(column=3, row=0, padx=10, pady=5)
#        c3.grid(column=0, row=1, padx=10, pady=5, columnspan=3)
#        c4.grid(column=3, row=1, padx=10, pady=5)
#        champk.grid(column=0, row=2)
#        BoutonMoins.grid(column=1, row=2)
#        BoutonPlus.grid(column=2, row=2)

        champk.bind("<Return>", fixek)



        fen.mainloop()

    
