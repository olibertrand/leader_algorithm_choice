from configurations import *
import random, time, os
import numpy as np


#Les lignes ci-dessous donnent des exemples d'appel aux fonctions de création de séries


######### Création de séries de configurations classées et de leurs représentations graphiques

# print(stats(10000, 100,'uniforme', ['centreGeom','kBFS'], '10000_gaussiennes','train','0',43, aretes = False, couleurs = True))
# print(stats(2500, 100,'uniforme', ['centreGeom','kBFS'], '10000_gaussiennes','validation','v0',43, aretes = False, couleurs = True))
# print(stats(2500, 100,'uniforme', ['centreGeom','kBFS'], '10000_gaussiennes','test','t0',43, aretes = False, couleurs = True))
  
    
######## Reconstruction de représentations graphiques pour une série 
########(permet de tester un nouveau type de représentation pour la même série de données)

# redessine("10_a_200_geom_kBFS", "mixte", 43, True, False, True)


######## (ré)analyse d'une série de configurations pour reconstruction et reclassement de représentations graphiques

# analyse_et_redessine(['centreGrav', 'kBFS'], '10000_geom_kBFS', 'centreGrav_ou_kBFS_tresepaisses', 5, True, False, True)
 
 
######### étude de la taille moyenne de la composante connexe principale
# rep1 = tailleMoyenne("5000_donnees/csv/train/centreGeom")
# rep2 = tailleMoyenne("5000_donnees/csv/train/centreGrav")
# rep3 =  tailleMoyenne("5000_donnees/csv/train/kBFS")
# print(rep1,rep2,rep3, (rep1+rep2+rep3)/3)



#excentriciteCentre("10000_geom_kBFS", "train")
 

#print(stabilite(10000, 30, 'stabilite_50_30_geom', 'train',''))
#print(stabilite(2500, 30,'stabilite_50_30', 'validation','v'))
# print("50_10 instable")
# print(analyse(['centreGrav', 'exact'], 'stabilite_50_10', 'train', 'instable', False, False))
# print("50_10 stable")
# print(analyse(['centreGrav', 'exact'], 'stabilite_50_10', 'train', 'stable', False, False))

#['centreGeom', 'centreGrav', 'ABC', 'slowABC', 'kBFS', 'tree', 'exact']

