import time
import pyglet
import math
import random

from game_globals import *

import Action
from Player import Player

class DeepMindPlayer(Player):

    def __init__(self, agent_filename=""):
        Player.__init__(self)

        self.actions = []
        
        # Populate list of actions 
        # (break_block, updown_rot, leftright_rot, forwardback, leftright)
        
        # Do nothing
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=0))
        
        # Go forward
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=WALKING_SPEED, leftright=0))
        
        # Go backward
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=-WALKING_SPEED, leftright=0))  
        
        # Rotate right
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=0, leftright=0))
        
        # Rotate right and go forward
        #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=1, leftright=0))
        
        # Rotate right and go backward
        #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))

        # Rotate left
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=0, leftright=0))
        
        # Rotate left and go forward
        #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=1, leftright=0))
        
        # Rotate left and go backward
        #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))    

        # Click
        self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=0))
        
        # Click and go forward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=0.0, forwardback=1, leftright=0))
        
        # Click and go backward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=0.0, forwardback=-1, leftright=0))  
        
        # Click and rotate right
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=0, leftright=0))
        
        # Click and rotate right and go forward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=1, leftright=0))
        
        # Click and rotate right and go backward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))

        # Click and rotate left
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=0, leftright=0))
        
        # Click and rotate left and go forward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=1, leftright=0))

        # Click and rotate left and go backward
        #self.actions.append(Action.Action(True, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))

        # Go right
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=WALKING_SPEED))
        
        # Go left
        self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=-WALKING_SPEED))



    def doAction(self, actionString):
        #print("PERFORMING ACTION %s" % actionString)

        actionIndex = int(actionString) - 1   # Because LUA is 1-indexed!!!!!
        
        # create an action object from the actionString
        act = self.actions[actionIndex]

        # carry out the action
        self.performAction(act)   
            




