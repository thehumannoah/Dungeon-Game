import random as Rand
from config import SECTION_LENGTH

# Helper function for block_gen, condenses filling in each line on x axis
def x_line(tilemap, x_start, x_end, y):
    if x_start < x_end:
        for j in range(x_start, x_end + 1):
            tilemap[y][j] = 1
    elif x_start > x_end:
        for j in range(x_end, x_start + 1):
            tilemap[y][j] = 1

# Draws a box from the start position to the end position, doesn't matter which position is smaller or larger
def block_gen(tilemap, start_pos, end_pos):
    y_start, x_start = start_pos
    y_end, x_end = end_pos
    
    if y_start < y_end:
        for i in range(y_start, y_end + 1):
            x_line(tilemap, x_start, x_end, i)
    elif y_start > y_end:
        for i in range(y_end, y_start + 1):
            x_line(tilemap, x_start, x_end, i)

# Helper function for entrance_connect, carves a 3x3 block radius around every point
def carve_radius(tilemap, y, x):
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            ny = y + dy
            nx = x + dx

            if 0 <= ny < SECTION_LENGTH and 0 <= nx < SECTION_LENGTH:
                tilemap[ny][nx] = 1

# Connects 2 points: start being the entrance from a direction, and end being a hub
# Sloppy, curves randomly
# OPTIONAL: WORK ON LATER
def entrance_connect(tilemap, start, end):
    y, x = start
    end_y, end_x = end
    
    while (y, x) != (end_y, end_x):
        moves = []
        
        if 2 < x < SECTION_LENGTH - 3:
            if y < end_y:
                moves.append((1, 0))
            elif y > end_y:
                moves.append((-1, 0))
        
        if 2 < y < SECTION_LENGTH - 3:
            if x < end_x:
                moves.append((0, 1))
            elif x > end_x:
                moves.append((0, -1))

        dy, dx = Rand.choice(moves)
        y += dy
        x += dx

        carve_radius(tilemap, y, x)
    
    tilemap[end_y][end_x] = 2

# Connects two points with straight perpendicular lines as opposed to fluid design of entrance_connect
def sharp_connect(tilemap, start, end):
    y, x = start
    end_y, end_x = end
    
    if x == 0: # WEST
        block_gen(tilemap, [y - 1, x], [y + 1, end_x + 1])
        block_gen(tilemap, [end_y - 1, end_x - 1], [y + 1, end_x + 1])
    elif x == SECTION_LENGTH - 1: # EAST
        block_gen(tilemap, [y - 1, x], [y + 1, end_x - 1])
        block_gen(tilemap, [end_y - 1, end_x + 1], [y + 1, end_x - 1])
    elif y == 0: # NORTH
        block_gen(tilemap, [y, x - 1], [end_y + 1, x + 1])
        block_gen(tilemap, [end_y - 1, x - 1], [end_y + 1, end_x + 1])
    elif y == SECTION_LENGTH - 1: # SOUTH
        block_gen(tilemap, [y, x - 1], [end_y - 1, x + 1])
        block_gen(tilemap, [end_y - 1, x + 1], [end_y + 1, end_x - 1])
    
    carve_radius(tilemap, end_y, end_x)
    
    for i in range(4):
        for i in range(3, SECTION_LENGTH - 4, 1):
            for j in range(3, SECTION_LENGTH - 4, 1):
                adjacent = []
                if tilemap[i+1][j] == 1: adjacent.append(1)
                if tilemap[i-1][j] == 1: adjacent.append(1)
                if tilemap[i][j+1] == 1: adjacent.append(1)
                if tilemap[i][j-1] == 1: adjacent.append(1)
                if len(adjacent) == 3: tilemap[i][j] = 1