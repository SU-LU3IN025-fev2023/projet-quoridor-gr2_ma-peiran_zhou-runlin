# <center>Rapport de projet : IA et Jeux </center>
<h4 style="text-align:right;">Stratégies dans Quoridor</h4>

<center> ZHOU runlin 28717281 </center>
<center> MA peiran 28717249 </center>

## Introduction 
Quoridor est un jeu de société stratégique pour deux ou quatre joueurs, où le but est de déplacer son pion d'un côté du plateau à l'autre tout en bloquant les adversaires à l'aide de murs. Le but de ce projet est d'explorer et d'analyser différentes stratégies de jeu pour améliorer le taux de victoire des joueurs dans Quoridor. 

Nous nous concentrerons sur le développement et la mise en œuvre de <u>*trois stratégies*</u> pour maximiser la chance de réussite:
- astar
- minimax
- start trap

Les code principal est dans le ficher <u>*main.py*</u> et <u>*Utls.py*</u>. 
- main.py est le code du test 
- Utls.py contient certaines des fonctions nécessaires à main

## Description des stratégies proposées
#### Astar:
Avant que le joueur ne choisisse de placer un mur ou de se déplacer, nous effectuons les vérifications suivantes :
- Vérifier s'il reste des murs disponibles pour être placés. Si oui, passer à l'étape suivante, sinon le jouer se déplace.
- Parcourir toutes les positions possibles pour placer un mur. Après on calcule la distance du chemin le plus court pour les deux joueur. Si la différence des deux valeurs est supérieure à 2 après avoir placé un mur, placer le mur à la position correspondante. Sinon, le joueur se déplace.
- Tous les dépalcement des joueurs se font sur le chemin le plus court.

#### Minimax et ses versions améliorées
L'algorithme Minimax est une méthode courante de recherche d'arbre de jeu utilisée pour prendre des décisions entre deux adversaires. L'algorithme suppose que les adversaires sont tous rationnels et choisiront la meilleure stratégie. Par conséquent, l'objectif de l'algorithme est de trouver une stratégie qui minimise les pertes potentielles.

Pendant le processus de recherche, l'algorithme Minimax considère les stratégies des deux adversaires, maximisant ses propres avantages tout en minimisant les avantages de l'adversaire. 
L'algorithme effectue deux opérations en alternance : 
- maximisation : choisit la valeur maximale parmi les nœuds fils
- minimisation : choisit la valeur minimale

Dans le cas réel (sur le Quoridor), on peut présenter l'algorithme comme un automate suivant:
![](https://i.imgur.com/GHn4ziM.jpg)
- déplacement : car on a 4 directions, nous choisirons la direction le plus défavorable ou le plus favorable
- placer un mur : choisir 200 places vailde aléatoirement (Simuler une traversée avec un grand nombre de placement)

L'espace de recherche de l'algorithme Minimax est très grand, donc pour les jeux complexes, son temps de recherche sera très long. Par conséquent, l'algorithme Minimax est généralement utilisé avec des techniques de taille pour réduire l'espace de recherche. 
Ici, nous utilisons l'algorithme **Alpha-Beta**.
![](https://i.imgur.com/W3MaxUx.jpg)
la valeur de n peut modifier, si n est plus grand, la capacité de l'algorithme est plus puissance, mais il a besoin de plus de temps (plus proche que la traversée)
NB : dans le programme, on met n = 3 (le temps et la capacité de l'algorithme sont équilibrés)

Mais le temps d'exécution est 30min pour Alpha-Beta, donc on a besoin de faire une autre amélioration
![](https://i.imgur.com/gXrc6mO.jpg)


#### Start Trap
Cette stratégie met davantage l'accent sur l'utilisation de murs pour bloquer l'adversaire.

Tout d'abord, le joueur place un mur verticalement sur l'axe central de la grille, ce qui divise la grille en deux parties. (comme le shéma suivant)
![](https://i.imgur.com/Heeggo5.jpg)

Par conséquent, l'adversaire ne peut se trouver que dans deux situations : 
- soit il reste sur l'axe central, 
- soit il se trouve dans la partie gauche ou droite de la grille.

Si l'adversaire est sur l'axe central, le joueur doit avancer d'une case dans la direction opposée (stratégie du miroir). 
Si l'adversaire se trouve dans l'une des parties de la grille, le joueur doit placer un mur dans la zone correspondante pour le bloquer.

## Description des résultats
En aide de sript du bash, on exécute le ficher main.py plusieur fois. Nous plaçons les données dans un fichier txt, chaque ligne ne contenant qu'un seul chiffre, 0 ou 1. 0 signifie que le joueur 1 gagne, 1 signifie que le joueur 2 gagne.
En fin, on calcule le nombre de 0 par les commande de Linux 
```
./evaluerStrategie.sh
cat nom_ficher | grep -o "0" | wc -l
```

Afin de comparer les différentes stratégies, nous générons le tableau suivant :
- Les lignes correspondent aux stratégies utilisées par le joueur 1
- Les colonnes sont les stratégies utilisées par le joueur 2.
- Le contenu du tableau est le pourcentage de gain du joueur 1 (sur 100 match).
    
    |nom de strategie |  AStar   | Minimax | Start Trap|
    | ---             | ----     |  ----   | ----      | 
    | AStar           | nan      | 0.32    | 0.68
    | Minimax         | 0.68     | nan     | 0.78
    | Start Trap      | 0.32     | 0.21    | nan


