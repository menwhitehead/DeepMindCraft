import Action
import random
import os
from game_globals import *
from string import Template
import stat

##############################
# Frequently Changed Globals #
##############################

# The width and height of the viewable game window (always square)
# For maximum speed, set this to 84 to match the scaled size (no scaling is required!)
VIEW_WINDOW_SIZE = 84

# The width and height of the image sent to DeepMind
SCALED_WINDOW_SIZE = 84

# The number of possible actions the agent can perform each step
TOTAL_NUMBER_ACTIONS = 18

# Host and port number for Lua DeepMind connection
TCP_HOST = "localhost"
TCP_PORT = 9999

TICKS_PER_SEC = 6000

# Total number of game frames per episode
MAXIMUM_GAME_FRAMES = 300

# Agent's turning speed (per tick)
AGENT_ROTATION_SPEED = 1.50
WALKING_SPEED = 1.0

# World generation parameters
WORLD_WIDTH = 5  # width in both directions from start
WORLD_DEPTH = 5  # depth in both directions from start
NUMBER_GRASS_BLOCKS = 8  # number of dirt blocks to add randomly through world
NUMBER_BRICK_BLOCKS = 7 # number of brick blocks to add randomly through world
MAX_BLOCK_HEIGHT = 5 # The maximum height of blocks placed in the world

# How often to print out the total number of frames 
COUNTER_DISPLAY_FREQUENCY = 1000

##############
# Game rules #
##############
# Rewards and penalties must fit into one byte!
# All accumulated rewards also must be non-negative!!!

# Rewards (these are added to reward)

# How much do you get for breaking different blocks?
BLOCK_BREAK_REWARDS = {
    "GRASS":100,
    "STONE":0,
    "BRICK":0
}

# Penalties (these are subtracted from reward)
SWING_PENALTY = 0
EXISTENCE_PENALTY = 0

# If you get all the penalties, then you get zero
STARTING_REWARD = SWING_PENALTY + EXISTENCE_PENALTY

################
# Game Actions #
################
GAME_ACTIONS = [
    # (break_block, updown_rot, leftright_rot, forwardback, leftright)
    
    # Do nothing
    Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=0),
    
    # Go forward
    Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=WALKING_SPEED, leftright=0),
    
    # Go backward
    Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=-WALKING_SPEED, leftright=0),
    
    # Rotate right
    Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=0, leftright=0),
    # Rotate right and go forward
    #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=1, leftright=0))
    
    # Rotate right and go backward
    #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))
    
    # Rotate left
    Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=0, leftright=0),

    # Rotate left and go forward
    #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=1, leftright=0))
    
    # Rotate left and go backward
    #self.actions.append(Action.Action(False, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=-1, leftright=0))    
    
    # Click
    Action.Action(True, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=0),
    
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
    #Action.Action(True, updown_rot=0.0, leftright_rot=-AGENT_ROTATION_SPEED, forwardback=-1, leftright=0),

    # Go right
    Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=WALKING_SPEED),
    
    # Go left
    Action.Action(False, updown_rot=0.0, leftright_rot=0.0, forwardback=0, leftright=-WALKING_SPEED),

    # Rotate up
    Action.Action(False, updown_rot=AGENT_ROTATION_SPEED, leftright_rot=0.0, forwardback=0, leftright=0),
    
    # Rotate down
    Action.Action(False, updown_rot=-AGENT_ROTATION_SPEED, leftright_rot=0.0, forwardback=0, leftright=0)
]

###############
# Build World #
###############

GROUND = -2
WALL_HEIGHT = 2

def saveWorld(locations, filename):
    o = open("maps" + os.sep + filename, 'w')
    for location in locations:
        o.write("%d %d %d %s\n" % location)
    o.close()
    
def generateTower(locations, texture):
    randomX = random.randrange(-WORLD_WIDTH+1, WORLD_WIDTH-1)
    randomZ = random.randrange(-WORLD_DEPTH+1, WORLD_DEPTH-1)
    # Don't make it the ground or the agent could fall through if it breaks it...
    randomY = GROUND + 1 + random.randrange(MAX_BLOCK_HEIGHT)
    
    locations.append((randomX, randomY, randomZ, texture))
    
    return locations
    
def generateFlatWorld(locations):
    
    # Make the flat ground
    for i in range(-WORLD_WIDTH, WORLD_WIDTH):
        for j in range(-WORLD_DEPTH, WORLD_DEPTH):
            locations.append((i, GROUND, j, "STONE"))

    # Put walls around the outside
    for i in range(-2, WALL_HEIGHT):
        for j in range(-WORLD_DEPTH, WORLD_DEPTH):
            locations.append((-WORLD_WIDTH, i, j, "STONE"))
            locations.append((WORLD_WIDTH, i, j, "STONE"))
        for j in range(-WORLD_WIDTH, WORLD_WIDTH):
            locations.append((j, i, -WORLD_DEPTH, "STONE"))
            locations.append((j, i, WORLD_DEPTH, "STONE"))
    return locations

def generateGameWorld(filename):
    locs = []
    locs = generateFlatWorld(locs)
    for i in range(NUMBER_GRASS_BLOCKS):
        locs = generateTower(locs, "GRASS")
    for i in range(NUMBER_BRICK_BLOCKS):
        locs = generateTower(locs, "BRICK")
    saveWorld(locs, filename)

#################
# Write Scripts #
#################
# These functions write the custom lua scripts according to the specifications in this config file 
#TODO: Check run_cpu/run_gpu to see if it's necessary to script them
#TODO: Make this run automatically?
#TODO: Figure out why the game runs with incorrect number of actions in GameEnvironment.lua
#TODO: Check and warn if configs don't match

# Verify the necessary files conform to the configurations in this file
def verify_files():
    GAME_ENVIRONMENT_TEMPLATE = "templates/GameEnvironment_template"
    GAME_ENVIRONMENT_LOCATION = "../../DeepMind-Atari-Deep-Q-Learner/torch/share/lua/5.1/minecraft/GameEnvironment.lua"
    GAME_ENVIRONMENT_REPLACEMENTS = {"ACTION_NUMBER" :len(GAME_ACTIONS)}

    template = open(GAME_ENVIRONMENT_TEMPLATE, "r")
    compare_file = open(GAME_ENVIRONMENT_LOCATION, "r")
    filled_template = Template(template.read()).substitute(GAME_ENVIRONMENT_REPLACEMENTS)
    compare_contents = compare_file.read()
    if compare_contents != filled_template:
        print("WARNING: The current GameEnvironment.lua file does not match the current configurations...\n")
        option = raw_input("Would you like to replace the current GameEnvironment.lua file with one that matches the current configurations? [Y/N]: ")
        if option.upper() == "Y" or option.upper() == "YES":
            print("Replacing current GameEnvironment.lua file...\n")
            write_script(GAME_ENVIRONMENT_TEMPLATE, GAME_ENVIRONMENT_LOCATION, GAME_ENVIRONMENT_REPLACEMENTS)
    template.close()
    compare_file.close()
    
        
def write_script(template_name, new_file_name, replacements, executable = 0):
    template = open(template_name, "r")
    new_file = open(new_file_name, "w")
    filled_template = Template(template.read()).substitute(replacements)
    new_file.write(filled_template)
    template.close()
    new_file.close()
    st = os.stat(new_file_name)
    if executable:
        os.chmod(new_file_name, st.st_mode | stat.S_IEXEC)

if __name__ == "__main__":
    GAME_ENVIRONMENT_TEMPLATE = "templates/GameEnvironment_template"
    GAME_ENVIRONMENT_LOCATION = "../DeepMind-Atari-Deep-Q-Learner/torch/share/lua/5.1/minecraft/GameEnvironment.lua"
    GAME_ENVIRONMENT_REPLACEMENTS = {"ACTION_NUMBER" :len(GAME_ACTIONS)}
    
    write_script(GAME_ENVIRONMENT_TEMPLATE, GAME_ENVIRONMENT_LOCATION, GAME_ENVIRONMENT_REPLACEMENTS)
