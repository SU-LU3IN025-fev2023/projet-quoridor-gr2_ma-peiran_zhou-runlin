# <center>Rapport de projet : IA et Jeux </center>
<h4 style="text-align:right;">Stratégies dans Quoridor</h4>

<center> ZHOU runlin 28717281 </center>
<center> MA peiran 28717249 </center>

## Introduction 
Quoridor est un jeu de société stratégique pour deux ou quatre joueurs, où le but est de déplacer son pion d'un côté du plateau à l'autre tout en bloquant les adversaires à l'aide de murs. Le but de ce projet est d'explorer et d'analyser différentes stratégies de jeu pour améliorer le taux de victoire des joueurs dans Quoridor. 

Nous nous concentrerons sur le développement et la mise en œuvre de <u>*trois stratégies*</u> pour maximiser la chance de réussite:
- s
- s
- s

Les code principal est dans le ficher <u>*main.py*</u> et <u>*Utls.py*</u>. 
- main.py est le code du test 
- Utls.py contient certaines des fonctions nécessaires à main

## Description des stratégies proposées
#### Astar

#### Minimax

#### noName

## Description des résultats
Afin de comparer les différentes stratégies, nous générons le tableau suivant :
- Les lignes correspondent aux stratégies utilisées par le joueur 1
- Les colonnes sont les stratégies utilisées par le joueur 2.
- Le contenu du tableau est le pourcentage de gain du joueur 1 (sur 1000 match).

En outre, afin de comparer le degré de réussite, nous collecterons la distance restante de l'autre joueur lorsqu'un joueur atteint la ligne d'arrivée et stockerons ces données dans un histogramme. 
- les ordonnées représente la fréquence, 
- l'abscisse positive indique la distance restante du joueur2 lorsque le joueur1 gagne
- l'abscisse négative indique la distance restante du joueur1 lorsque le joueur2 atteint la ligne d'arrivée

