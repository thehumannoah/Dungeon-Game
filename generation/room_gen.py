import random as Rand
from generation import gen_utils as gu
from config import SECTION_LENGTH, CENT

# Creates starting room based on template
def start(tilemap, entrances):
    # Middle square
    with open("generation/section_templates/start.txt", "r") as f:
        file_text = f.read().split()
        for i in range(len(file_text)):
            tilemap[i] = [int(c) for c in file_text[i]]
    
    entrances.update({'N': CENT, 'E': CENT, 'W': CENT})

# Creates corridor room
def corridor(tilemap, entrances):
    hub_x = Rand.randint(3, SECTION_LENGTH - 4)
    hub_y = Rand.randint(3, SECTION_LENGTH - 4)
    
    tilemap[hub_y][hub_x] = 2
    
    valid_entrances = []
    
    for i in entrances:
        if entrances[i] != False:
            chance = Rand.random()
            if entrances[i] == None and chance <= .5: entrances[i] = Rand.randint(3, SECTION_LENGTH - 4)
            
            if entrances[i] != None:
                match i:
                    case 'N':
                        tilemap[0][entrances[i]] = 1
                        valid_entrances.append([0, entrances[i]])
                    case 'E':
                        tilemap[entrances[i]][SECTION_LENGTH - 1] = 1
                        valid_entrances.append([entrances[i], SECTION_LENGTH - 1])
                    case 'S':
                        tilemap[SECTION_LENGTH - 1][entrances[i]] = 1
                        valid_entrances.append([SECTION_LENGTH - 1, entrances[i]])
                    case 'W':
                        tilemap[entrances[i]][0] = 1
                        valid_entrances.append([entrances[i], 0])
            else:
                entrances[i] = False
    
    for i in valid_entrances:
        #gu.entrance_connect(tilemap, i, [hub_y, hub_x])
        gu.sharp_connect(tilemap, i, [hub_y, hub_x])