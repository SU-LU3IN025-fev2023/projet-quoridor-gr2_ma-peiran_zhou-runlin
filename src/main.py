# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
import copy
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme
import Utls
STRATEGY_MODE = (0,4)
# 0 -> random strategy
# 1 -> astar
# 2 -> minimax original
# 3 -> minimax Alpha-beta
# 4 -> minimax reduced




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'mini-quoridorMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    assert nbLignes == nbCols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les murs)
    lMax=nbLignes-2 
    cMin=2
    cMax=nbCols-2
   
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    ligneObjectif = (initStates[1][0],initStates[0][0]) # chaque joueur cherche a atteindre la ligne ou est place l'autre 
    print(ligneObjectif)
    
    # on localise tous les murs
    # sur le layer ramassable    
    walls = [[],[]]
    walls[0] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]  
    walls[1] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == nbLignes-2 or o.get_rowcol()[0] == nbLignes-1)]  
    allWalls = walls[0]+walls[1]
    nbWalls = len(walls[0])
    assert len(walls[0])==len(walls[1]) # les 2 joueurs doivent avoir le mm nombre de murs
    
    def legal_wall_position(pos):
        row,col = pos
        # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
        # attention: pas de test ici qu'il reste un chemin vers l'objectif
        return ((pos not in wallStates(allWalls)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax)
    
    def legal_player_position(pos):
        row,col = pos
        return ((pos not in wallStates(allWalls)) and row>=lMin and row<=lMax-1 and col>=cMin and col<cMax)

    def draw_random_wall_location():
    # tire au hasard un couple de position permettant de placer un mur
        while True:
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_wall_position(random_loc):  
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis):
                        return(random_loc,random_loc_bis)
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets murs ou joueurs
    #-------------------------------

    def wallStates(walls): 
        # donne la liste des coordonnees dez murs
        return [w.get_rowcol() for w in walls]

    def playerStates(players):
       # donne la liste des coordonnees dez joueurs
       return [p.get_rowcol() for p in players]
    
    def minimax(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,max_iter=6,branch_border=(3,-3)):
        """
	    Maximizer enemy_steps - self_steps
	    """
        return maxValue(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,max_iter,branch_border)

    def maxValue(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,iter,branch_border):
        option = -1 # -1 noeud feuille ; 0 : se déplacer ; 1 : placer mur
        pos_list = [] # [] noeud feuille ; [(x,y)] : coordonnées de la prochaine étape (se déplacer) ; [(x1,y1),(x2,y2)] : coordonnées du mur placé (placer mur)
        tmp = Utls.step_rest(g,initStates,allObjectifs)
        if iter==0: # si limite de récurrence atteinte
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        if tmp[0]==1 or tmp[1]==1: # si feuille (quelqu'un gagne) on renvoie la valeur
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        v = -255

        for step in [(-1,0),(1,0),(0,1),(0,-1)]:
            if playernum==0:
                nextInitStates = ((initStates[0][0]+step[0],initStates[0][1]+step[1]),initStates[1])
            else:
                nextInitStates = (initStates[0],(initStates[1][0]+step[0],initStates[1][1]+step[1]))
            if not (legal_player_position(nextInitStates[0]) and legal_player_position(nextInitStates[1])):
                continue
            #print ("étendu noeud - ",playernum," se déplacer ", nextInitStates[playernum]," ; iter= ",iter)
            minval,_,_ = minValue(copy.deepcopy(g),nextInitStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,iter-1,branch_border)
            if v < minval:
                v = minval
                option = 0
                pos_list = [nextInitStates[playernum]]
                if modeAB and v >= branch_border[0]:
                    return v,option,pos_list
            
        if num_wall_used[playernum] < nbWalls//2:
            analysed_pos = []
            for wall_attempt in range(200):
                ((x1,y1),(x2,y2)) = draw_random_wall_location()
                if (x1,y1,x2,y2) not in analysed_pos and Utls.exist_route_allobj(copy.deepcopy(g),initStates,allObjectifs,x1,y1,x2,y2):
                    analysed_pos.append((x1,y1,x2,y2))
                    #print ("étendu noeud - ",playernum," placer mur ", (x1,y1),(x2,y2)," ; iter= ",iter)
                    nextG = copy.deepcopy(g)
                    nextG[x1][y1]=False
                    nextG[x2][y2]=False
                    new_num_wall_used = num_wall_used[:]
                    new_num_wall_used[playernum] += 1
                    minval,_,_ = minValue(nextG,initStates,allObjectifs,playernum,new_num_wall_used,nbWalls,modeAB,iter-1,branch_border)
                    if v < minval:
                        v = minval
                        option = 1
                        pos_list = [(x1,y1),(x2,y2)]
                        if modeAB and v >= branch_border[0]:
                            return v,option,pos_list
        return v,option,pos_list

    def minValue(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,iter,branch_border):
        option = -1 # -1 noeud feuille ; 0 : se déplacer ; 1 : placer mur
        pos_list = [] # [] noeud feuille ; [(x,y)] : coordonnées de la prochaine étape (se déplacer) ; [(x1,y1),(x2,y2)] : coordonnées du mur placé (placer mur)
        tmp = Utls.step_rest(g,initStates,allObjectifs)
        if iter==0: # si limite de récurrence atteinte
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        if tmp[0]==1 or tmp[1]==1: # si feuille (quelqu'un gagne) on renvoie la valeur
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        v = 255

        for step in [(-1,0),(1,0),(0,1),(0,-1)]:
            if playernum==1:
                nextInitStates = ((initStates[0][0]+step[0],initStates[0][1]+step[1]),initStates[1])
            else:
                nextInitStates = (initStates[0],(initStates[1][0]+step[0],initStates[1][1]+step[1]))
            if not (legal_player_position(nextInitStates[0]) and legal_player_position(nextInitStates[1])):
                continue
            #print ("étendu noeud - ",1-playernum," se déplacer ", nextInitStates[1-playernum]," ; iter= ",iter)
            maxval,_,_ = maxValue(copy.deepcopy(g),nextInitStates,allObjectifs,playernum,num_wall_used,nbWalls,modeAB,iter-1,branch_border)
            if v > maxval:
                v = maxval
                option = 0
                pos_list = [nextInitStates[playernum]]
                if modeAB and v <= branch_border[1]:
                    return v,option,pos_list
            
        if num_wall_used[1-playernum] < nbWalls//2:
            analysed_pos = []
            for wall_attempt in range(200):
                ((x1,y1),(x2,y2)) = draw_random_wall_location()
                if (x1,y1,x2,y2) not in analysed_pos and Utls.exist_route_allobj(copy.deepcopy(g),initStates,allObjectifs,x1,y1,x2,y2):
                    analysed_pos.append((x1,y1,x2,y2))
                    #print ("étendu noeud - ",playernum," placer mur ", (x1,y1),(x2,y2)," ; iter= ",iter)
                    nextG = copy.deepcopy(g)
                    nextG[x1][y1]=False
                    nextG[x2][y2]=False
                    new_num_wall_used = num_wall_used[:]
                    new_num_wall_used[1-playernum] += 1
                    maxval,_,_ = maxValue(nextG,initStates,allObjectifs,playernum,new_num_wall_used,nbWalls,modeAB,iter-1,branch_border)
                    if v > maxval:
                        v = maxval
                        option = 1
                        pos_list = [(x1,y1),(x2,y2)]
                        if modeAB and v <= branch_border[1]:
                            return v,option,pos_list
        return v,option,pos_list

    def minimax_ab_reduced(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,max_iter=4,branch_border=(1,-1)):
        """
	    Maximizer enemy_steps - self_steps
	    """
        print("!!!",playernum,initStates)
        return maxValue_ab_reduced(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,max_iter,branch_border)

    def maxValue_ab_reduced(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,iter,branch_border):
        option = -1 # -1 noeud feuille ; 0 : se déplacer ; 1 : placer mur
        pos_list = [] # [] noeud feuille ; [(x,y)] : coordonnées de la prochaine étape (se déplacer) ; [(x1,y1),(x2,y2)] : coordonnées du mur placé (placer mur)
        tmp = Utls.step_rest(g,initStates,allObjectifs)
        if iter==0: # si limite de récurrence atteinte
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        if tmp[0]==1 or tmp[1]==1: # si feuille (quelqu'un gagne) on renvoie la valeur
            return tmp[1-playernum]-tmp[playernum], option, pos_list
        v = -255

        for step in [(-1,0),(1,0),(0,1),(0,-1)]:
            if playernum==0:
                nextInitStates = ((initStates[0][0]+step[0],initStates[0][1]+step[1]),initStates[1])
            else:
                nextInitStates = (initStates[0],(initStates[1][0]+step[0],initStates[1][1]+step[1]))
            if not (legal_player_position(nextInitStates[0]) and legal_player_position(nextInitStates[1])):
                continue
            #print ("étendu noeud - ",playernum," se déplacer ", nextInitStates[playernum]," ; iter= ",iter)
            minval,_,_ = minValue_ab_reduced(copy.deepcopy(g),nextInitStates,allObjectifs,playernum,num_wall_used,nbWalls,iter-1,branch_border)
            if v < minval:
                v = minval
                option = 0
                pos_list = [nextInitStates[playernum]]
                if v >= branch_border[0]:
                    return v,option,pos_list
            
        if num_wall_used[playernum] < nbWalls//2:
            analysed_pos = []
            for wall_attempt in range(200):
                ((x1,y1),(x2,y2)) = draw_random_wall_location()
                if (x1,y1,x2,y2) not in analysed_pos and Utls.exist_route_allobj(copy.deepcopy(g),initStates,allObjectifs,x1,y1,x2,y2):
                    analysed_pos.append((x1,y1,x2,y2))
                    #print ("étendu noeud - ",playernum," placer mur ", (x1,y1),(x2,y2)," ; iter= ",iter)
                    nextG = copy.deepcopy(g)
                    nextG[x1][y1]=False
                    nextG[x2][y2]=False
                    new_num_wall_used = num_wall_used[:]
                    new_num_wall_used[playernum] += 1
                    minval,_,_ = minValue_ab_reduced(nextG,initStates,allObjectifs,playernum,new_num_wall_used,nbWalls,iter-1,branch_border)
                    if v < minval:
                        v = minval
                        option = 1
                        pos_list = [(x1,y1),(x2,y2)]
                        if v >= branch_border[0]:
                            print(v,"!",branch_border[0])
                            return v,option,pos_list
        return v,option,pos_list

    def minValue_ab_reduced(g,initStates,allObjectifs,playernum,num_wall_used,nbWalls,iter,branch_border):
        tmp = Utls.step_rest(g,initStates,allObjectifs)
        if iter==0: # si limite de récurrence atteinte
            return tmp[1-playernum]-tmp[playernum], -1, []
        if tmp[0]==1 or tmp[1]==1: # si feuille (quelqu'un gagne) on renvoie la valeur
            return tmp[1-playernum]-tmp[playernum], -1, []
        
        best_step = 255
        best_pos = None
        for o in allObjectifs[1-player_num]:
            p = ProblemeGrid2D(initStates[1-player_num],o,g,'manhattan')
            path = probleme.astar(p,verbose=False)
            if path[-1] == o and best_step > len(path):
                best_step = len(path)
                best_pos = path[1]
        if playernum==1:
            nextInitStates = (best_pos,initStates[1])
        else:
            nextInitStates = (initStates[0],best_pos)
        v,_,_ = maxValue_ab_reduced(copy.deepcopy(g),nextInitStates,allObjectifs,playernum,num_wall_used,nbWalls,iter-1,branch_border)
        return v,0,[best_pos]
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    print("Trouvé ", nbPlayers, " joueurs avec ", int(nbWalls/2), " murs chacun" )
    print ("Init states:", initStates)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: place au hasard
    # Joueur 1: A*
    #-------------------------------
    
        
    #-------------------------------
    # On choisit une case objectif au hasard pour chaque joueur
    #-------------------------------
    
    allObjectifs = ([(ligneObjectif[0],i) for i in range(cMin,cMax)],[(ligneObjectif[1],i) for i in range(cMin,cMax)])
    print("Tous les objectifs joueur 0", allObjectifs[0])
    print("Tous les objectifs joueur 1", allObjectifs[1])

    

    game_end = 0
    num_wall_used = [0,0]
    posPlayers = initStates
    g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True
    for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
        g[0][i]=False
        g[1][i]=False
        g[nbLignes-1][i]=False
        g[nbLignes-2][i]=False
        g[i][0]=False
        g[i][1]=False
        g[i][nbLignes-1]=False
        g[i][nbLignes-2]=False
        
# init part
    if STRATEGY_MODE[0] == 0 or STRATEGY_MODE[1] == 0:
        objectifs =  (allObjectifs[0][random.randint(cMin,cMax-3)], allObjectifs[1][random.randint(cMin,cMax-3)])
        print("Objectif joueur 0 choisi au hasard", objectifs[0])
        print("Objectif joueur 1 choisi au hasard", objectifs[1])
    
    while iterations > 0:
        for player_num in range(2): # Tour du joueurs 0/1
        # strategy random
            if STRATEGY_MODE[player_num] == 0:
                # décision de l'action
                action = 0 # 0 -> se déplacer ; 1 -> placer un mur
                if (num_wall_used[player_num] < nbWalls//2):
                    action = random.randint(0,1)
                if action == 1: # générer un mur
                    attemptnum = 0
                    while attemptnum<200:
                        ((x1,y1),(x2,y2)) = draw_random_wall_location()
                        if Utls.exist_route(copy.deepcopy(g),initStates,objectifs,x1,y1,x2,y2):
                            break
                        attemptnum+=1
                    if attemptnum>=200:
                        action = 0
                        num_wall_used[player_num] = nbWalls//2 #Ne plus essayer de placer des murs
                if action == 1: # placer un mur
                    walls[player_num][num_wall_used[player_num]].set_rowcol(x1,y1)
                    walls[player_num][num_wall_used[player_num]+nbWalls//2].set_rowcol(x2,y2)
                    g[walls[player_num][num_wall_used[player_num]].get_rowcol()]=False
                    g[walls[player_num][num_wall_used[player_num]+nbWalls//2].get_rowcol()]=False
                    num_wall_used[player_num] += 1
                
                if action == 0: # 0 -> se déplacer
                    # trouver une route
                    p = ProblemeGrid2D(initStates[player_num],objectifs[player_num],g,'manhattan')
                    path = probleme.astar(p,verbose=False)
                    # se déplacer
                    if path[-1] != objectifs[player_num]:
                        while True:
                            pass
                    row,col = path[1]
                    posPlayers[player_num]=(row,col)
                    players[player_num].set_rowcol(row,col)
                    print ("pos joueur ",player_num,":", row,col)
                    if (row,col) in allObjectifs[player_num]:
                        print("le joueur "+str(player_num)+" a atteint son but!")
                        game_end = 1
        #strategy astar
            if STRATEGY_MODE[player_num] == 1:
                self_min_step = 255
                enemy_min_step = 255
                for self_objective in allObjectifs[player_num]:
                    prob_temp = ProblemeGrid2D(initStates[player_num],self_objective,g,'manhattan')
                    self_min_step = min([self_min_step,len(probleme.astar(prob_temp,verbose=False))])
                for enemy_objective in allObjectifs[1-player_num]:
                    prob_temp = ProblemeGrid2D(initStates[1-player_num],enemy_objective,g,'manhattan')
                    enemy_min_step = min([enemy_min_step,len(probleme.astar(prob_temp,verbose=False))])
                    
                # Branche : si placer un mur peut mener l'ennemi de deux pas, alors placer le mur, sinon se bouger.
                x1b, y1b, x2b, y2b = -1, -1, -1, -1 #Emplacement optimal pour placer les murs
                action = 1 # 0 -> se déplacer ; 1 -> placer un mur
                max_diff = 1
                for attemptnum in range(200):
                    ((x1,y1),(x2,y2)) = draw_random_wall_location()
                    if Utls.exist_route_allobj(copy.deepcopy(g),initStates,allObjectifs,x1,y1,x2,y2):
                        tmp = Utls.step_rest_wall(copy.deepcopy(g),initStates,allObjectifs,x1,y1,x2,y2)
                        self_step_rest = tmp[player_num]
                        enemy_step_rest = tmp[1-player_num]
                        if enemy_step_rest - self_step_rest - (enemy_min_step - self_min_step) > max_diff:
                            max_diff = enemy_step_rest - self_step_rest - (enemy_min_step - self_min_step)
                            x1b, y1b, x2b, y2b = x1, y1, x2, y2
                if x1b == -1: # aucun emplacement approprié n'a été trouvé
                    action = 0
                    
                # placer un mur
                if action == 1:
                    walls[player_num][num_wall_used[player_num]].set_rowcol(x1b,y1b)
                    walls[player_num][num_wall_used[player_num]+nbWalls//2].set_rowcol(x2b,y2b)
                    g[walls[player_num][num_wall_used[player_num]].get_rowcol()]=False
                    g[walls[player_num][num_wall_used[player_num]+nbWalls//2].get_rowcol()]=False
                    num_wall_used[player_num] += 1
                # se déplacer
                if action == 0:
                    # trouver une route
                    best_step = 255
                    best_pos = None
                    for o in allObjectifs[player_num]:
                        p = ProblemeGrid2D(initStates[player_num],o,g,'manhattan')
                        path = probleme.astar(p,verbose=False)
                        if path[-1] == o and best_step > len(path):
                            best_step = len(path)
                            best_pos = path[1]
                    # se déplacer
                    if best_pos == None:
                        while True:
                            pass
                    row,col = best_pos
                    posPlayers[player_num]=(row,col)
                    players[player_num].set_rowcol(row,col)
                    print ("pos joueur ",player_num,":", row,col)
                    print(initStates)
                    if (row,col) in allObjectifs[player_num]:
                        print("le joueur "+str(player_num)+" a atteint son but!")
                        game_end = 1
        # strategy minimax & ab
            if STRATEGY_MODE[player_num] in [2,3,4]:
                # décision de l'action
                if STRATEGY_MODE[player_num] == 2:
                    v,action,pos_list = minimax(copy.deepcopy(g),initStates,allObjectifs,player_num,num_wall_used,nbWalls,False) # action 0 -> se déplacer ; 1 -> placer un mur
                elif STRATEGY_MODE[player_num] == 3:
                    v,action,pos_list = minimax(copy.deepcopy(g),initStates,allObjectifs,player_num,num_wall_used,nbWalls,True) # action 0 -> se déplacer ; 1 -> placer un mur
                elif STRATEGY_MODE[player_num] == 4:
                    v,action,pos_list = minimax_ab_reduced(copy.deepcopy(g),initStates,allObjectifs,player_num,num_wall_used,nbWalls) # action 0 -> se déplacer ; 1 -> placer un mur
                if action == 1: # placer un mur
                    x1,y1 = pos_list[0]
                    x2,y2 = pos_list[1]
                    walls[player_num][num_wall_used[player_num]].set_rowcol(x1,y1)
                    walls[player_num][num_wall_used[player_num]+nbWalls//2].set_rowcol(x2,y2)
                    g[walls[player_num][num_wall_used[player_num]].get_rowcol()]=False
                    g[walls[player_num][num_wall_used[player_num]+nbWalls//2].get_rowcol()]=False
                    num_wall_used[player_num] += 1
                
                if action == 0: # 0 -> se déplacer
                    # se déplacer
                    row,col = pos_list[0]
                    posPlayers[player_num]=(row,col)
                    players[player_num].set_rowcol(row,col)
                    print ("pos joueur ",player_num,":", row,col)
                    if (row,col) in allObjectifs[player_num]:
                        print("le joueur "+str(player_num)+" a atteint son but!")
                        game_end = 1
            game.mainiteration()
        if game_end==1:
            break
        iterations -= 1
        
            

    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
    
    
   

if __name__ == '__main__':
    main()
    


    