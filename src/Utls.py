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

#-------------------------------
# Fonctions definissant les positions legales et placement de mur aléatoire
#-------------------------------

def exist_route(g,initStates,objectifs,x1,y1,x2,y2):
	g[x1][y1]=False
	g[x2][y2]=False
	p0 = ProblemeGrid2D(initStates[0],objectifs[0],g,'manhattan')
	path0 = probleme.astar(p0,verbose=False)
	p1 = ProblemeGrid2D(initStates[1],objectifs[1],g,'manhattan')
	path1 = probleme.astar(p1,verbose=False)
	return path0[-1] == objectifs[0] and path1[-1] == objectifs[1]

def exist_route_allobj(g,initStates,allObjectifs,x1,y1,x2,y2):
	g[x1][y1]=False
	g[x2][y2]=False
	valid0, valid1 = False, False
	for o0 in allObjectifs[0]:
		prob_temp = ProblemeGrid2D(initStates[0],o0,g,'manhattan')
		if probleme.astar(prob_temp,verbose=False)[-1] == o0:
			valid0 = True
			break
	for o1 in allObjectifs[1]:
		prob_temp = ProblemeGrid2D(initStates[1],o1,g,'manhattan')
		if probleme.astar(prob_temp,verbose=False)[-1] == o1:
			valid1 = True
			break
	return valid0 and valid1

def step_rest_wall(g,initStates,allObjectifs,x1,y1,x2,y2):
	# return (player0 steps, player1 steps)
	g[x1][y1]=False
	g[x2][y2]=False
	min0, min1 = 255, 255
	for o0 in allObjectifs[0]:
		prob_temp = ProblemeGrid2D(initStates[0],o0,g,'manhattan')
		min0 = min([min0,len(probleme.astar(prob_temp,verbose=False))])
	for o1 in allObjectifs[1]:
		prob_temp = ProblemeGrid2D(initStates[1],o1,g,'manhattan')
		min1 = min([min1,len(probleme.astar(prob_temp,verbose=False))])
	return (min0,min1)

def step_rest(g,initStates,allObjectifs):
	# return (player0 steps, player1 steps)
	min0, min1 = 255, 255
	for o0 in allObjectifs[0]:
		prob_temp = ProblemeGrid2D(initStates[0],o0,g,'manhattan')
		min0 = min([min0,len(probleme.astar(prob_temp,verbose=False))])
	for o1 in allObjectifs[1]:
		prob_temp = ProblemeGrid2D(initStates[1],o1,g,'manhattan')
		min1 = min([min1,len(probleme.astar(prob_temp,verbose=False))])
	return (min0,min1)

