[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-8d59dc4de5201274e310e4c54b9627a8934c3b88527886e3b421487c677d23eb.svg)](https://classroom.github.com/a/qbyu_KOJ)
# projet-quoridor
Projet IA et Jeux 2022-2023, L3 Sorbonne Université

## Présentation générale du projet

On propose dans ce projet d'implémenter une version librement inspirée du jeu Quoridor.
Le principe général du jeu est le suivant: chaque joueur cherche à être le premier à traverser le terrain.
Chaque joueur jour à tour de rôle. Les coups possibles sont:
* le déplacement de son joueur,
* le dépôt d'un mur de 2 cases sur le plateau.

Les règles de déplacement sont les suivantes:
* il est possible de se déplacer de une case, dans toutes les directions sauf les diagonales. On suppose ici que les joueurs ne se bloquent pas entre eux, et qu'ils peuvent éventuellement être sur la même case à un moment donné.

Les règles de placement sont les suivantes:
* les murs sont constitués de 2 "briques" (2 cases) qui doivent posés côte-à-côte horizontalement ou verticalement
* les murs sont ici posés sur les cases (et non entre elles comme c'est le cas dans le jeu de Quridor classique),
* il est interdit de poser des murs sur les lignes où sont placés initialement les joueurs
* il est interdit de déposer un mur à un endroit qui fermerait tout chemin d'un des autres joueurs vers ses objectifs.


Note: bien que présenté ici pour 2 joueurs, le jeu peut être joué à 4 joueurs. Nous laissons cette perspective comme extension possible de votre projet.

### Bibilographie
Article Wikipedia [Quoridor](https://en.wikipedia.org/wiki/Quoridor)

## Modules disponibles

### Module pySpriteWorld

Pour la partie graphique, vous utiliserez le module `pySpriteWorld` (développé par Yann Chevaleyre) qui s'appuie sur `pygame` et permet de manipuler simplement des personnages (sprites), cartes, et autres objets à l'écran.

Une carte par défaut vous est proposée pour ce projet (`quoridorMap`): elle comporte 2 joueurs.
Les murs de chaque joueur sont initialement placés derrière lui. Dans cette carte, chaque joueur dispose de 15 murs, mais cela peut facilement être modifié.

La gestion de la carte s'opère grâce à des calques:
* un calque `joueur`, où seront présents les joueurs
* un calque `ramassable`, qui contient ici les murs


Les joueurs et les ramassables sont des objets Python sur lesquels vous pouvez effectuer des opérations classiques.
Par exemple, il est possible récupérer leurs coordonnées sur la carte avec `o.get_rowcol(x,y)` ou à l'inverse fixer leurs coordonnées avec `o.set_rowcol(x,y)`.
La mise à jour sur l'affichage est effective lorsque `mainiteration()` est appelé.


Notez que vous pourrez ensuite éditer vos propres cartes à l'aide de l'éditeur [Tiled](https://www.mapeditor.org/), et exporter ces cartes au format `.json`. Vous pourrez alors modifier le nombre de joueurs ou de murs disponibles, par exemple.

Il est ensuite possible de changer la carte utilisée en modifiant le nom de la carte utilisée dans la fonction `init` du `main`:
`name = _boardname if _boardname is not None else 'quoridorMap'``
Une carte miniature vous est aussi proposée, pour plus de facilité pour les premiers tests.  

:warning: Vous n'avez pas à modifier le code de `pySpriteWorld`

### Module search

Le module `search` qui accompagne le cours est également disponible. Il permet en particulier de créer des problèmes de type grille et donc d'appeler directement certains algorithmes de recherche à base d'heuristiques vus en cours, comme A:star: pour la recherche de chemin.

## Travail demandé

### Semaine 1
**Prise en main**. A l'éxécution du fichier `main.py`, vous devez observer le comportement suivant: le joueur 0 (en haut du plateau) place tous ses murs les uns après les autres (avant que le joueur 1 ne joue). Puis le joueur 1 choisit un objectif au hasard sur la ligne qu'il doit atteindre et calcule le plus court chemin pour atteindre cette case, avant d'effectuer tous les déplacements nécessaire.

Evidemment tout ceci ne respecte pas du tout les règles du jeu.

:point_right: Modifiez le code de manière à ce que les deux joueurs jouent à tour de rôle de manière **aléatoire**, en suivant le principe suivant:
* s'il reste au moins un mur à placer, le joueur choisit au hasard entre se déplacer et placer un mur.
  * s'il choisit de poser un mur celui-ci sera déposé au hasard sur une position légale
  * s'il choisit de se déplacer le joueur choisit le plus court chemin à un de ses objectifs (n'importe quelle position sur la ligne qui lui permet de gagner)

:warning: il faudra bien tenir compte du fait que les joueurs ont pour objectif d'atteindre n'importe quelle case sur la ligne de départ adverse, et que les murs ne doivent pas couper tous les chemins qui mènent aux objectifs pour l'adversaire. Ceci n'est pas géré dans le code fourni qui est juste une base illustrative.


### Semaine 2 et 3
**Mise en place et test de différentes stratégies**. Vous vous inspirerez des méthodes vues en cours pour proposer au moins 3 stratégies en plus de la stratégie aléatoire élaborée en première semaine.
Il peut être utile de distinguer plusieurs phases de jeux (ouverture, milieu de jeu, fin de jeu).
Vous comparerez chacune de ces stratégies en les faisant jouer les unes contre les autres.


### Semaine 4
**Soutenances**. Celles-ci ont lieu en binôme. Vous présenterez les principaux résultats de votre projet.
Le rapport doit être rédigé en markdown dans le fichier prévu à cet effet dans le répertoire `docs` (voir le template `rapport.md`).
