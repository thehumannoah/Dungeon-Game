import random as Rand

SECTION_LENGTH = 25 # Must be odd
CENT = SECTION_LENGTH // 2



def start(tilemap):
    # Middle square
    with open("section_templates/start.txt", "r") as f:
        file_text = f.read().split()
        for i in range(len(file_text)):
            tilemap[i] = [int(c) for c in file_text[i]]
    
    return {'N': CENT, 'E': CENT, 'W': CENT}

def corridor(tilemap, entrances):
    hub_y = CENT #Rand.randint(CENT - 4, CENT + 4)
    hub_x = CENT #Rand.randint(CENT - 4, CENT + 4)
    
    tilemap[hub_y][hub_x] = 2
    
    for i in entrances:
        if entrances[i] != False:
            if entrances[i] == None and Rand.random() <= .5: entrances[i] = Rand.randint(3, SECTION_LENGTH - 4)
            
            if entrances[i] != None:
                match i:
                    case 'N':
                        tilemap[0][entrances[i]] = 1
                    case 'E':
                        tilemap[entrances[i]][SECTION_LENGTH - 1] = 1
                    case 'S':
                        tilemap[SECTION_LENGTH - 1][entrances[i]] = 1
                    case 'W':
                        tilemap[entrances[i]][0] = 1