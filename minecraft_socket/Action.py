import random


def getRandomAction():
    a = Action()
    a.leftright_rotation = 1 - 2 * random.random()
    #a.updown_rotation = 1 - 2 * random.random()
    a.forwardbackward_walk = random.choice([1, 0, -1])
    #a.leftright_walk = random.choice([1, 0, -1])
    #a.break_block = random.choice([True, False])
    a.break_block = random.choice([False, False])

    
    return a

class Action(object):

    def __init__(self, break_block=False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=0):
        
        # Pressing left button to break block
        self.break_block = break_block
        
        # Looking up or down
        self.updown_rotation = updown_rot
        
        # Looking right or left
        self.leftright_rotation = leftright_rot
        
        # Walking forward or backward (-1 is backward, 1 is forward, 0 is neither)
        self.forwardbackward_walk = forwardback
        
        # Strafing left or right
        self.leftright_walk = leftright
 
    def __eq__(self, other):
        return self.break_block == other.break_block and \
                abs(self.updown_rotation - other.updown_rotation) < 0.01 and \
                abs(self.leftright_rotation - other.leftright_rotation) < 0.01 and \
                self.forwardbackward_walk == other.forwardbackward_walk and \
                self.leftright_walk == other.leftright_walk
 

    def __str__(self):
        return "Action: " + str(self.break_block) + " %.4f %.4f %d %d" % (self.updown_rotation, self.leftright_rotation, self.forwardbackward_walk, self.leftright_walk)
