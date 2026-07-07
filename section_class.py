"""
Defines Section class which is assigned to each new section entered by player
Modes:
    1. Empty
    2. Start
    3. Intersection
    4. Boss
    5. Corridor
    6. Dungeon (enemies and loot)
    7. Secret (good loot or lore)
"""

import mode_gen as mg
SECTION_LENGTH = mg.SECTION_LENGTH
CENT = SECTION_LENGTH // 2

VALID_MODES = {
    "EMPTY",
    "START",
    "INTERSECTION",
    "BOSS",
    "CORRIDOR",
    "DUNGEON",
    "SECRET"
}

class Section():
    def __init__(self, mode = "EMPTY", entrances = None):
        
        if mode not in VALID_MODES:
            raise ValueError(f"Unknown section mode: {mode}")
        
        self.mode = mode
        self.tilemap = [[0] * SECTION_LENGTH for _ in range(SECTION_LENGTH)]
        
        self.entrances = {'N': None, 'E': None, 'S': None, 'W': None}
        if entrances:
            self.entrances.update(entrances)
        
        match self.mode:
            case "EMPTY":
                pass
            case "START":
                self.entrances.update(mg.start(self.tilemap))
            case "CORRIDOR":
                mg.corridor(self.tilemap, self.entrances)
            case "INTERSECTION":
                pass
            case "BOSS":
                pass
            case "DUNGEON":
                pass
            case "SECRET":
                pass
    
    def print_grid(self):
        RED = "\033[31m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"
        RESET = "\033[0m"

        for row in self.tilemap:
            for cell in row:
                if cell == 1:
                    print(f"{BLUE}{cell}{RESET}", end="  ")
                elif cell == 2:
                    print(f"{GREEN}{cell}{RESET}", end="  ")
                else:
                    print(f"{RED}{cell}{RESET}", end="  ")
            print()

if __name__ == "__main__":
    test = Section(mode = "CORRIDOR", entrances = {'N': False, 'E': None, 'S': None, 'W': None})
    test.print_grid()
    print(test.entrances)