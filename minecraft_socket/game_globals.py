import math

# Display the log messages on the terminal
DISPLAY_LOG = True

# The width and height of the game window (always square)
WINDOW_SIZE = 84

# The number of game frames before calling the agent's getDecision
DECISION_FREQUENCY = 4

# Number of intermediate features from the autoencoder
FEATURE_VECTOR_SIZE = 1250

# The number of possible actions the agent can perform each step
TOTAL_NUMBER_ACTIONS = 18

# Number of inputs and outputs in the reinforcement network
# (Actions are encoded and passed as input!)
# Single output is the Q value of performing the given action at the given sequence 
REINFORCEMENT_INPUT_SIZE = FEATURE_VECTOR_SIZE + TOTAL_NUMBER_ACTIONS
REINFORCEMENT_OUTPUT_SIZE = 1

#OUTPUT_VECTOR_SIZE = 1

TICKS_PER_SEC = 6000

# Number of Experiences to train on
TRAINING_BATCH_SIZE = 512

# Agent's turning speed (per tick)
AGENT_ROTATION_SPEED = 1.50

# Run each episode for this many game ticks
MAX_FRAMES_PER_GAME = 300  # equivalent to one minute of normal, 60fps play

# How often (in getDecision calls) to start a minibatch of training
BATCH_TRAINING_FREQUENCY = 4 * DECISION_FREQUENCY

# Number of iterations of training per minibatch (we think DeepMind is 1)
BATCH_TRAINING_ITERATIONS = 1

# How often to print the simulation progress to the terminal
WORLD_COUNTER_DISPLAY_FREQUENCY = 100

REINFORCEMENT_PROTO = 'protos/reinforcement_solver.prototxt'
REINFORCEMENT_MODEL = 'models/reinforcement/current.caffemodel'

AUTOENCODER_PROTO = 'protos/small_autoencoder_solver.prototxt'
AUTOENCODER_TEST_PROTO = 'protos/small_autoencoder_tester.prototxt'
AUTOENCODER_MODEL = 'models/small_autoencoder/current.caffemodel'

CNNPLAYER_SAVE_FILENAME = "cnnplayer.dat"
REPLAY_MEMORY_FILENAME = "replay.pick"

# Size of sectors used to ease block loading.
SECTOR_SIZE = 16

WALKING_SPEED = 5
FLYING_SPEED = 15

GRAVITY = 20.0
MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
# To derive the formula for calculating jump speed, first solve
#    v_t = v_0 + a * t
# for the time at which you achieve maximum height, where a is the acceleration
# due to gravity and v_t = 0. This gives:
#    t = - v_0 / a
# Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
#    s = s_0 + v_0 * t + (a * t^2) / 2
JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
TERMINAL_VELOCITY = 50

PLAYER_HEIGHT = 2

def cube_vertices(x, y, z, n):
    """ Return the vertices of the cube at position x, y, z with size 2*n.

    """
    return [
        x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
        x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
        x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
        x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
        x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
        x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
    ]


def tex_coord(x, y, n=4):
    """ Return the bounding vertices of the texture square.

    """
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """ Return a list of the texture squares for the top, bottom and side.

    """
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


TEXTURE_PATH = 'texture.png'

GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = tex_coords((1, 1), (1, 1), (1, 1))
BRICK = tex_coords((2, 0), (2, 0), (2, 0))
STONE = tex_coords((2, 1), (2, 1), (2, 1))

FACES = [
    ( 0, 1, 0),
    ( 0,-1, 0),
    (-1, 0, 0),
    ( 1, 0, 0),
    ( 0, 0, 1),
    ( 0, 0,-1),
]


def normalize(position):
    """ Accepts `position` of arbitrary precision and returns the block
    containing that position.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    block_position : tuple of ints of len 3

    """
    x, y, z = position
    x, y, z = (int(round(x)), int(round(y)), int(round(z)))
    return (x, y, z)


def sectorize(position):
    """ Returns a tuple representing the sector for the given `position`.

    Parameters
    ----------
    position : tuple of len 3

    Returns
    -------
    sector : tuple of len 3

    """
    x, y, z = normalize(position)
    x, y, z = x / SECTOR_SIZE, y / SECTOR_SIZE, z / SECTOR_SIZE
    return (x, 0, z)
