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

# Host and port number for Lua DeepMind connection
TCP_HOST = "localhost"
TCP_PORT = 9988

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

# GPU Training, -1 is CPU and 0 is GPU
GPU = 0

###################################
# Directory Structure Information #
###################################

# Experiments Directory Information
EXPERIMENT_NAME = "test" # Current Experiment Name
EXPERIMENT_DIRECTORY_PATH = "/home/alan/Capstone/DeepMindCraft_Experiments/"
EXPERIMENT_WRITE_LOCATION = EXPERIMENT_DIRECTORY_PATH + EXPERIMENT_NAME # Experiment write location

# Qlua directory path
QLUA_DIRECTORY = "/home/alan/Capstone/DeepMind-Atari-Deep-Q-Learner/torch/bin/qlua"

# DQN directory path
DQN_DIRECTORY = "/home/alan/Capstone/DeepMind-Atari-Deep-Q-Learner/dqn"

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
#TODO: Check and warn if configs don't match

# Verify the necessary directories exist and conform to the configurations in this file
def verify_directories():
    if os.path.isdir(EXPERIMENT_WRITE_LOCATION):
        print("WARNING: The current directory {0} exists!...\n".format(EXPERIMENT_WRITE_LOCATION))
        option = raw_input("Would you like to continue and possibly overwrite files? [Y/N]: ".format(EXPERIMENT_WRITE_LOCATION))
        if option.upper() == "N" or option.upper() == "NO":
            exit(0)
    else:
        print("WARNING: The current directory {0} does not exist as specified in the current configurations...\n".format(EXPERIMENT_WRITE_LOCATION))
        option = raw_input("Would you like to create the directory {0} (if no then you cannot continue)? [Y/N]: ".format(EXPERIMENT_WRITE_LOCATION))
        if option.upper() == "Y" or option.upper() == "YES":
            print("Creating directory {0}...\n".format(EXPERIMENT_WRITE_LOCATION))
            os.makedirs(EXPERIMENT_WRITE_LOCATION)
    
# Verify the necessary files conform to the configurations in this file
def verify_files():
    RUN_TEMPLATE = "templates/run_template"
    RUN_FILE_PATH = EXPERIMENT_WRITE_LOCATION + "/run_" + EXPERIMENT_NAME
    RUN_FILE_REPLACEMENTS = {"EXPERIMENTS_DIRECTORY" : EXPERIMENT_WRITE_LOCATION + "/", "HOST" : TCP_HOST, "PORT" : TCP_PORT, "ACTION_NUMBER" : len(GAME_ACTIONS),
                             "GPU" : GPU, "QLUA_DIRECTORY" : QLUA_DIRECTORY, "DQN_DIRECTORY" : DQN_DIRECTORY}
    GAME_ENVIRONMENT_TEMPLATE = "templates/GameEnvironment_template"
    GAME_ENVIRONMENT_PATH = "../../DeepMind-Atari-Deep-Q-Learner/torch/share/lua/5.1/minecraft/GameEnvironment.lua"
    TRAIN_AGENT_TEMPLATE = "templates/train_agent_template"
    TRAIN_AGENT_PATH = "../../DeepMind-Atari-Deep-Q-Learner/dqn/train_agent.lua"
    replace_file(RUN_TEMPLATE, RUN_FILE_PATH, RUN_FILE_REPLACEMENTS, executable = True)
    replace_file(GAME_ENVIRONMENT_TEMPLATE, GAME_ENVIRONMENT_PATH)
    replace_file(TRAIN_AGENT_TEMPLATE, TRAIN_AGENT_PATH)

# Replace files if necessary
def replace_file(file_template, file_path, template_replacements = None, executable = False):
    template = open(file_template, "r")
    filled_template = template.read()
    compare_contents = None
    if os.path.exists(file_path):
        compare_file = open(file_path, "r")
        compare_contents = compare_file.read()
        compare_file.close()
    if template_replacements != None:
        filled_template = Template(filled_template).safe_substitute(template_replacements)
    if compare_contents != filled_template:
        print("WARNING: The current {0} file does not match the current configurations...\n".format(file_path))
        option = raw_input("Would you like to replace the current {0} file with one that matches the current configurations? [Y/N]: ".format(file_path))
        if option.upper() == "Y" or option.upper() == "YES":
            print("Replacing current {0} file...\n".format(file_path))
            write_script(filled_template, file_path, executable)
    template.close()
        
def write_script(filled_template, new_file_name, executable = False):
    new_file = open(new_file_name, "w")
    new_file.write(filled_template)
    new_file.close()
    st = os.stat(new_file_name)
    if executable:
        os.chmod(new_file_name, st.st_mode | stat.S_IEXEC)
