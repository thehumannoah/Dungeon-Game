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

import os
import sys
import random as Rand
import mode_gen as mg
import helper_functions as hf
from config import SECTION_LENGTH

VALID_MODES = {
    "EMPTY",
    "START",
    "BOSS",
    "CORRIDOR",
    "DUNGEON",
    "SECRET"
}

class Section():
    def __init__(self, mode = "EMPTY", entrances = None):
        """
        Sets Section variables and creates tilemap.
        Holds all info on a section.
        """
        # Check if mode is valid
        if mode not in VALID_MODES:
            raise ValueError(f"Unknown section mode: {mode}")
        
        # Set self variables
        self.mode = mode
        self.tilemap = [[0] * SECTION_LENGTH for _ in range(SECTION_LENGTH)]
        
        # Set entrances to none and update with passed entrances (False means no entrance, None means possible entrance)
        self.entrances = {'N': None, 'E': None, 'S': None, 'W': None}
        if entrances:
            self.entrances.update(entrances)
        
        # Execute corresponding function for each mode
        match self.mode:
            case "EMPTY":
                pass
            case "START":
                mg.start(self.tilemap, self.entrances)
            case "CORRIDOR":
                mg.corridor(self.tilemap, self.entrances)
            case "BOSS":
                pass
            case "DUNGEON":
                pass
            case "SECRET":
                pass
    
    def print_grid(self):
        """
        Display the section's tilemap in the terminal.
        Used for debugging the dungeon generator.
        """
        RED = "\033[31m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"
        RESET = "\033[0m"
        
        print("    ", end = "")
        for i in range(SECTION_LENGTH):
            if i <= 8: print(i, end = "  ")
            else: print(i, end = " ")
        print()

        i = 0
        for row in self.tilemap:
            if i <= 9: print(f" {i}", end = "  ")
            else: print(i, end = "  ")
            i += 1
            for cell in row:
                if cell == 1:
                    print(f"{BLUE}{cell}{RESET}", end="  ")
                elif cell == 2:
                    print(f"{GREEN}{cell}{RESET}", end="  ")
                else:
                    print(f"{RED}{cell}{RESET}", end="  ")
            print()

def rn():
    x = Rand.random()
    if x <= .5:
        return Rand.randint(3, SECTION_LENGTH - 4)
    elif .5 < x <= .75:
        return None
    elif .75 < x <= 1.0:
        return False

if __name__ == "__main__":
    choice = sys.argv[1]
    os.system("clear")
    print(f"\033[1m{choice}\033[0m", "\n")

    match choice:
        case "block_gen":
            test = Section("EMPTY")
            hf.block_gen(test.tilemap, [int(sys.argv[2]), int(sys.argv[3])], [int(sys.argv[4]), int(sys.argv[5])])
        case "empty":
            test = Section("EMPTY")
        case "start":
            test = Section("START")
        case "corridor":
            test = Section("CORRIDOR", {'N': rn(), 'E': rn(), 'S': rn(), 'W': rn()})
        case _:
            print("command not found.")
            exit()

    test.print_grid()
    print("\n", test.entrances)