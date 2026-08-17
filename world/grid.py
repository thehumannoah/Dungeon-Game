from world import room

class Grid():
    def __init__(self):
        self.rooms = {}
        self.open_paths = 3
    
    def generate_room(self, pos = tuple, mode = str, entrances = None):
        self.rooms[pos] = room.Room(pos, mode, entrances)
        self.open_paths -= 1
        for i in self.rooms[pos].entrances:
            if i != False:
                self.open_paths += 1
        return self.rooms[pos]