import random as Rand
import config
from world import room

def rn():
    x = Rand.random()
    if x <= .5:
        return Rand.randint(3, config.SECTION_LENGTH - 4)
    elif .5 < x <= .75:
        return None
    elif .75 < x <= 1.0:
        return False

class Grid():
    def __init__(self):
        self.rooms = {}
        self.open_paths = 3
        self.minimap = {}
    
    def generate_corridor_room(self, pos = tuple, mode = str, entrances = None):
        for key, value in entrances.items():
            if value is None:
                match key:
                    case 'N':
                        pos_check = (pos[0], pos[1] + 1)
                        direction_check = 'S'
                    case 'E':
                        if pos[0] < 10:
                            pos_check = (pos[0] + 1, pos[1])
                            direction_check = 'W'
                        else:
                            entrances[key] = False
                            continue
                    case 'S':
                        if pos[1] > 0:
                            pos_check = (pos[0], pos[1] - 1)
                            direction_check = 'N'
                        else:
                            entrances[key] = False
                            continue
                    case 'W':
                        if pos[0] > -10:
                            pos_check = (pos[0] - 1, pos[1])
                            direction_check = 'E'
                        else:
                            entrances[key] = False
                            continue
                
                if pos_check in self.rooms:
                    entrances[key] = self.rooms[pos_check].entrances[direction_check]
                else:
                    entrances[key] = Rand.randint(3, config.SECTION_LENGTH - 4) if self.open_paths < 3 else rn()
        
        self.rooms[pos] = room.Room(pos, mode, entrances)

        for i in self.rooms[pos].entrances:
            pass
        return self.rooms[pos]