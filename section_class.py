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
            case "INTERSECTION":
                pass
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

if __name__ == "__main__":
    
    print("Select a mode:"
        "\n\t1. room_gen"
        "\n\t2. start"
        "\n\t3. corridor")
    choice = input()
    print()

    match choice:
        case "1":
            test = Section("EMPTY")
            mg.room_gen(test.tilemap, 2, 2, 3, 3)
        case "2":
            test = Section("START")
        case "3":
            test = Section("CORRIDOR", {'N': CENT, 'E': False, 'S': CENT, 'W': False})
        case _:
            print("command not found.")
            exit()
    
    test.print_grid()
    print("\n", test.entrances, "\n")