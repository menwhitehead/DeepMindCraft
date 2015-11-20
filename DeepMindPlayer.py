import time
import pyglet
import math
import random

import game_config

import Action
from Player import Player

class DeepMindPlayer(Player):

    def __init__(self, agent_filename=""):
        Player.__init__(self)

        self.actions = game_config.GAME_ACTIONS

    def doAction(self, actionString):
        #print("PERFORMING ACTION %s" % actionString)

        actionIndex = int(actionString) - 1   # Because LUA is 1-indexed!!!!!
        # create an action object from the actionString
        act = self.actions[actionIndex]

        # carry out the action
        self.performAction(act)   
            




