import random
import os

GROUND = -2
WALL_HEIGHT = 2
WORLD_WIDTH = 5  # width in both directions from start
WORLD_DEPTH = 5  # depth in both directions from start
NUMBER_TOWERS = 8

def saveWorld(locations, filename):
    o = open("maps" + os.sep + filename, 'w')
    for location in locations:
        o.write("%d %d %d %s\n" % location)
    o.close()
    

def generateGrassTower(locations):
    randomX = random.randrange(-WORLD_WIDTH+1, WORLD_WIDTH-1)
    randomZ = random.randrange(-WORLD_DEPTH+1, WORLD_DEPTH-1)
    
    for i in range(1, 2):
        locations.append((randomX, GROUND+i+1, randomZ, "GRASS"))
    
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
    for i in range(NUMBER_TOWERS):
        locs = generateGrassTower(locs)
    saveWorld(locs, filename)


if __name__=="__main__":
    generateGameWorld("world.txt")