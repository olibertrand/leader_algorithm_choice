from monde_robots import *
import random, time, os
import numpy as np



def stats(n:int, nbPoints:int, distribution:str, algos:list[str], repertoire:str, ensemble:str, prefixe:str, radius:int, aretes:bool, couleurs = False, affichage=False, sauve = True)->dict[str,int]:
    """
    crée n configurations
    les classe après avoir déterminé lequel des algorithmes de la liste algos était le plus performant
    les enregistre dans repertoire/ensemble/'essai'+prefixe+x.*
    
    Paramètres
    ----------
    n : int
        nombre de configurations à créer
        
    nbPoints : int
        nombre de noeuds dans chaque configuration
        
    distribution : str
        'uniforme' ou 'gaussienne'

    algos : list[str]
        liste des noms des algorithmes à comparer
        
    repertoire, ensemble : str
        éléments du chemin vers l'emplacement où seront enregistrés les fichiers
        
    prefixe : str
        prefixe ajouté dans le nom des fichiers, avant le numéro de l'essai
        
    radius : int
        rayon du cercle représentant le noeud
        
    aretes : bool
        valeur indiquant si les aretes du réseau doivent être dessinées
        
    affichage : bool
        valeur indiquant si le détail des exécutions des algorithmes doit être affiché
        
    sauve : bool
        valeur indiquant si les configurations doivent être enregistrées (fichier csv + fichier png)
        
    
    Valeur renvoyée
    ---------------
    dict[str, int]
        Un dictionnaire associant à chaque nom d'algorithme le nombre de fois où il a été choisi
    """
    fen = Tk()    
    resultats = {nomAlgo:0 for nomAlgo in algos}
    racine = repertoire+'/'
    if sauve:
        #création éventuelle des répertoires
        for typeFichier in [ensemble+'/', 'csv/'+ensemble+'/']:
            for rep in resultats:
                os.makedirs(racine+typeFichier+rep, exist_ok=True)
    debut = time.time()
    for essai in range(n):
        M = Monde(500,500,85, 1, fen)
        M.points = {}
        effectif = random.randint(10, 200)#nbPoints#
        #ajoute une liste de points aléatoires
        if distribution == 'uniforme':
            L = [(random.random()*500, random.random()*500) for i in range(effectif)]
        else:
            L = [(np.random.normal(250, 100), np.random.normal(250, 100)) for i in range(effectif)]
        #On essaie de tous les ajouter (marche bien s'il n'y a pas de recouvrement entre les noeuds)
        nombreSucces = M.ajouteListe(L)
        #On complète éventuellement si plusieurs points étaient au même endroit
        deficit = effectif - nombreSucces
        if deficit > 0:
            print(essai,": création de ",deficit," points supplémentaires")
        supplement = 0
        while supplement < deficit:
            if M.ajoute_point(random.random()*500, random.random()*500):
                supplement += 1
            
        R = M.reseauPrincipal()
        resultat = R.bestAlgorithme(affichage, algos)
        resultats[resultat]+=1
        if sauve:
            M.sauveCSV(racine+'csv/'+ensemble+'/'+resultat+"/essai"+prefixe+"_"+str(essai)+".csv", R.getIndices())
            M.sauvePNG(racine+'/'+ensemble+'/'+resultat+"/essai"+prefixe+"_"+str(essai)+".png", R.getIndices(), radius, aretes)
    fin = time.time()
    print(fin-debut)
    return resultats
    
def stabilite(n, nbPoints, ecart, repertoire, ensemble, prefixe, affichage=False, sauve = True):
    """
    crée n configurations
    les classe après avoir déterminé la distance entre le centre de gravité et le point qui en est le plus proche.
    les enregistre dans repertoire/ensemble/'essai'+prefixe+x.*
    
    Paramètres
    ----------
    n : int
        nombre de configurations à créer
        
    nbPoints : int
        nombre de noeuds dans chaque configuration
        
    ecart : int
        la distance entre le centre et son représentant au-delà de laquelle la configuration est considérée comme instable.
            
    repertoire, ensemble : str
        éléments du chemin vers l'emplacement où seront enregistrés les fichiers
        
    prefixe : str
        prefixe ajouté dans le nom des fichiers, avant le numéro de l'essai
        
    affichage : bool
        variable indiquant si le détail des exécutions des algorithmes doit être affiché
        
    sauve : bool
        variable indiquant si les configurations doivent être enregistrées (fichier csv + fichier png)
        
    
    Valeur renvoyée
    ---------------
    dict[str, int]
        Un dictionnaire associant à chaque catégorie le nombre de fois où elle a été choisie
    """
    fen = Tk()    
    resultats = {'stable':0, 'instable':0}
    racine = repertoire+'/'
    if sauve:
        #création éventuelle des répertoires
        for typeFichier in [ensemble+'/', 'csv/'+ensemble+'/']:
            for rep in resultats:
                os.makedirs(racine+typeFichier+rep, exist_ok=True)
    debut = time.time()
    for essai in range(n):
        M = Monde(500,500,85, 1, fen)
        M.points = {}
        effectif = nbPoints
        #ajoute une liste de points aléatoires
        L = [(random.random()*500, random.random()*500) for i in range(effectif)]
        #On complète éventuellement si on a voulu mettre plusieurs points au même endroit
        nombreSucces = M.ajouteListe(L)
        deficit = effectif - nombreSucces
        if deficit > 0:
            print(essai,": création de ",deficit," points supplémentaires")
        supplement = 0
        while supplement < deficit:
            if M.ajoute_point(random.random()*500, random.random()*500):
                supplement += 1
            
        R = M.reseauPrincipal()
        coordonnees = R.getCoordonneesReseau()
        abscisses = [C[0] for C in coordonnees]
        ordonnees = [C[1] for C in coordonnees]
        #xGrav = sum(abscisses)/len(abscisses)
        #yGrav = sum(ordonnees)/len(ordonnees)
        xGeom = (min(abscisses)+max(abscisses))/2
        yGeom = (min(ordonnees)+max(ordonnees))/2
        if R.distancePlusProche(xGeom, yGeom) < ecart:
            resultat = 'stable'
        else:
            resultat = 'instable'
        
        resultats[resultat]+=1
        if sauve:
            M.sauveCSV(racine+'csv/'+ensemble+'/'+resultat+"/essai"+prefixe+"_"+str(essai)+".csv", R.getIndices())
            M.sauvePNG(racine+'/'+ensemble+'/'+resultat+"/essai"+prefixe+"_"+str(essai)+".png", R.getIndices())
    fin = time.time()
    print(fin-debut)
    return resultats
    

def tailleMoyenne(repertoire:str)->float:
    """
    Paramètre
    ---------
    repertoire : str
        le nom d'un répertoire contenant des fichiers csv (chaque fichier csv décrit une configuration)
        
    Valeur renvoyée
    ---------------
    float
        le nombre moyen de noeuds dans la composante connexe principale des configurations
    """
    fen = Tk()    
    S = 0
    N = 0
    for fichier in os.listdir(repertoire):
        M = Monde(500,500,85, 1, fen)
        M.chargeCSV(repertoire+'/'+fichier)
        R = M.reseauPrincipal()
        S += R.getTaille()
        N += 1
    return S/N
        


def redessine(repertoire:str, nomCible:str, radius:int, aretes:bool, affichage=False, sauve = True)->int:
    """
    redessine les configurations enregistrées dans repertoire/csv/
    et enregistre les images dans repertoire/nomCible
    
    Paramètres
    ----------
           
    repertoire : str
        chemin où sont enregistrées les configurations
        
    nomCible : str
        sous-répertoire dans lequel seront enregistrées les images
        
    radius : int
        rayon du cercle représentant le noeud
        
    aretes : bool
        valeur indiquant si les aretes du réseau doivent être dessinées

    affichage : bool
        variable indiquant si le détail des exécutions des algorithmes doit être affiché
        
    sauve : bool
        variable indiquant si les configurations doivent être enregistrées (fichier csv + fichier png)
        
    
    Valeur renvoyée
    ---------------
    dict[str, int]
        Un dictionnaire associant à chaque catégorie le nombre de fois où elle a été choisie
    """
    fen = Tk()    
    racine = repertoire+'/'
    source = repertoire+'/csv'
    cible = repertoire+'/'+ nomCible
    debut = time.time()
    #lire le fichier
    for categorie in os.listdir(source):#train, validation, test...
        for rep in os.listdir(source+'/'+categorie):
            cheminSource = source+'/' + categorie +'/'+rep
            cheminCible = cible+'/' + categorie +'/'+rep
            os.makedirs(cheminCible, exist_ok=True)
            for fichier in os.listdir(cheminSource):
                M = Monde(500,500,85, 1, fen)
                M.chargeCSV(cheminSource+'/'+fichier)
                R = M.reseauPrincipal()
                M.sauvePNG(cheminCible+'/'+fichier[:-4]+'.png', R.getIndices(), radius, aretes)
    fin = time.time()
    print(fin-debut)
    return 0



def analyse(repertoire:str, ensemble:str, sousEnsemble:str, algos:list[str], affichage=False)->dict[str,int]:
    """
    lit les configurations dans repertoire/csv/ensemble/sousensemble
    détermine pour chacune l'algorithme le plus performant parmi ceux présents dans la liste algos
    affiche les statistiques
    
    Paramètres
    ----------
           
    algos : list[str]
        liste des noms des algorithmes à comparer

    repertoire : str
        chemin où sont enregistrées les configurations
        
    ensemble : str
        sous-répertoire de repertoire
        
    sousEnsemble : str
        sous-répertoire de ensemble

    affichage : bool
        variable indiquant si le détail des exécutions des algorithmes doit être affiché
        
    sauve : bool
        variable indiquant si les configurations doivent être enregistrées (fichier csv + fichier png)
        
    
    Valeur renvoyée
    ---------------
    dict[str, int]
        Un dictionnaire associant à chaque catégorie le nombre de fois où elle a été choisie
    """
    fen = Tk()    
    resultats = {nomAlgo:0 for nomAlgo in algos}
    racine = repertoire+'/'
    chemin = repertoire+'/csv/'+ensemble+'/'+sousEnsemble
    debut = time.time()
    #lire le fichier
    for fichier in os.listdir(chemin):
        M = Monde(500,500,85, 1, fen)
        M.chargeCSV(chemin+'/'+fichier)
        R = M.reseauPrincipal()
        resultat = R.bestAlgorithme(affichage, algos)
        resultats[resultat]+=1
    fin = time.time()
    print(fin-debut)
    print(resultats)
    return resultats
    
    
    
def analyse_et_redessine(repertoire:str, nomCible:str, radius:int, aretes:bool, algos:list[str], affichage=False, sauve = True)->dict[str,int]:
    """
    lit les configurations dans repertoire/csv/*/**
    détermine l'algorithme le plus performant parmi ceux présents dans algos
    les enregistre dans repertoire/nomcible/*/algo
    
    Valeur renvoyée
    ---------------
    dict[str, int]
        Un dictionnaire associant à chaque nom d'algorithme le nombre de fois où il a été choisi
    """
    fen = Tk()    
    resultats = {nomAlgo:0 for nomAlgo in algos}
    racine = repertoire+'/'
    source = repertoire+'/csv'
    cible = repertoire+'/'+ nomCible
    debut = time.time()
    #lire le fichier
    for categorie in os.listdir(source):#train, validation, test...
        for algo in algos:
            os.makedirs(cible+'/'+categorie+'/'+algo, exist_ok=True)

        for rep in os.listdir(source+'/'+categorie):
            cheminSource = source+'/' + categorie +'/'+rep
            for fichier in os.listdir(cheminSource):
                M = Monde(500,500,85, 1, fen)
                M.chargeCSV(cheminSource+'/'+fichier)
                R = M.reseauPrincipal()
                resultat = R.bestAlgorithme(affichage, algos)
                resultats[resultat]+=1
                cheminCible = cible+'/' + categorie +'/'+resultat
                M.sauvePNG(cheminCible+'/'+fichier[:-4]+'.png', R.getIndices(), radius, aretes)

    fin = time.time()
    print(fin-debut)
    return resultats

def excentriciteCentre(repertoire:str, ensemble:str):
    """
    lit les configurations dans repertoire/csv/ensemble/sousensemble
    et renvoie l'excentricité du centre géométrique
    
    Valeur renvoyée
    ---------------
    repertoire : str
        Le répertoire contenant les données ('csv' est un sous-répertoire)
        
    ensemble : str
        Le sous-répertoire étudié (train, validation, test,...)
        
    """
    fen = Tk()    
    chemin = repertoire+'/csv/'+ensemble
    debut = time.time()
    for categorie in os.listdir(chemin):#centreGeom, kBFS,...
        resume = open("excentricites_"+categorie+".csv","w")
        resume.write("taille,exc_Centre\n")           
        #lire les fichiers
        for fichier in os.listdir(chemin+"/"+categorie):
            M = Monde(500,500,85, 1, fen)
            M.chargeCSV(chemin+"/"+categorie+"/"+fichier)
            R = M.reseauPrincipal()
            centre = R.setCentreGeom()
            resume.write(str(len(R.indices))+","+str(R.exc(centre))+"\n")
        resume.close()
    fin = time.time()
    print(fin-debut)


    
def lancement(questions, types, defauts, fonction):
	'''lance une fonction après avoir demandé un à un les paramètres à l'utilisateur
	
	Paramètres
	----------
	questions:	list[str]		liste des questions à poser
	types    :	list[function]	liste des fonctions permettant la conversion de str vers le type attendu
	defauts	 :	list[str]		liste des réponses par défaut (si simple appui sur Entrée)
	fonction :	function		nom de la fonction à appeler
	'''		
	reponses = []
	for i, enonce in enumerate(questions):
		rep = input(enonce)
		
		if rep == "":
			rep = defauts[i]
		else:
			rep = types[i](rep)		
		reponses.append(rep)
		
	fonction(*reponses)
	
	
		
if __name__ == '__main__':

	#Contenu des menus guidant le lancement de chaque fonction
	dico_choix_actions = {
						1:[["nombre de configurations à créer:[10] ",
							"nombre de points par configuration:[50] ", 
							"distribution ('gaussienne' ou 'uniforme'):[uniforme] ", 
							"liste des algorithmes à tester (juste les noms séparés par des virgules). \n par défaut: centreGeom, kBFS: ", 
							"Répertoire où enregistrer les configurations:[mesConfigs] ",
							"sous-répertoire (typiquement: 'train', 'validation' ou 'test'):[train] ",
							"prefixe ajouté dans le nom des fichiers, avant le numéro de l'essai:[] ",
							"rayon du disque représentant un noeud sur l'image (int):[43] ",
							"faut-il dessiner les arêtes? (1 pour oui, 0 pour non):[0] "
							], 
							[int, int, str, lambda s:s.split(","), str, str, str, int, lambda x:bool(int(x))],
							[10, 50, 'uniforme', ['centreGeom', 'kBFS'], 'mesConfigs', 'train', '', 43, False],
							stats],
						2:[["Répertoire où se trouve le répertoire 'csv':[mesConfigs] ",
							"sous-répertoire où enregistrer les images:[newImages] ",
							"rayon du disque représentant un noeud sur l'image (int):[43] ",
							"faut-il dessiner les arêtes? (1 pour oui, 0 pour non):[0] "],
							[str, str, int, lambda x:bool(int(x))],
							['mesConfigs', 'newImages', 43, False],
							redessine],
						3:[["Répertoire où se trouve le répertoire 'csv':[mesConfigs] ",
							"sous-répertoire étudié:[train] ",
							"sous-sous-répertoire:[centreGeom] ",
							"algorithmes à comparer:[centreGeom, kBFS] "],
							[str, str, str, lambda s:s.split(",")],
							['mesConfigs', 'train', 'centreGeom', ['centreGeom', 'kBFS']],
							analyse],
						4:[["Répertoire où se trouve le répertoire 'csv':[mesConfigs] ",
							"Répertoire cible:[nouveau] ",
							"rayon du disque représentant un noeud sur l'image (int):[43] ",
							"faut-il dessiner les arêtes? (1 pour oui, 0 pour non):[0] ",
							"algorithmes à comparer:[centreGeom, kBFS] "],
							[str, str, int, lambda x:bool(int(x)), lambda s:s.split(",")],
							['mesConfigs', 'nouveau', 43, False, ['centreGeom', 'kBFS']],
							analyse_et_redessine],
	}
				

	#Menu principal
	continuer = True
	options = ["Créer une série de configurations et les classer",
				"Reconstruire (sans reclasser) les représentation graphiques d'une série de configurations",
				"Comparer les performances de plusieurs algorithmes sur une série de configurations",
				"Reconstruire et reclasser les représentation graphiques d'une série de configurations classées",
				"Quitter"
				]		
	print("\n\n")
	while continuer == True:
		#On demande son choix à l'utilisateur
		i = 0 
		for choix in options:
			i+=1
			print(str(i)+" - "+ choix +" \n")
		choix = 0
		while choix not in [x for x in range(1,len(options)+1)]:
			choix = int(input("Choisissez une option:"))
		if choix!=0:
			if choix==len(options):
				continuer = False
			else:
				lancement(*dico_choix_actions[choix])
	       
	

