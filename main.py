import math
import pygame
import config
from world import *

"""
Config Initialization
"""

SECTION_LENGTH = config.SECTION_LENGTH
TILE_SIZE = config.TILE_SIZE
SCREEN_SIZE = config.SCREEN_SIZE
SCREEN_CENTER = config.SCREEN_CENTER
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

"""
Pygame & Variable Initialization
"""

pygame.init()

# Screen
pygame.display.set_caption('Dungeon Game')
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()

# Player
player = entities.Player(pygame.Surface((TILE_SIZE, TILE_SIZE)),
                        pygame.Rect(SCREEN_CENTER, SCREEN_CENTER, TILE_SIZE, TILE_SIZE)
                    )
player.surface.fill(RED)

# Grid and Start Room generation
start = room.Room((0,0), "START")
main_grid = grid.Grid()
main_grid.rooms[(0,0)] = start
active_room = start

# Current tile text display
font = pygame.font.Font(None, 32)

speed = 5
running = True

"""
Functions for Room Handling
"""

def render_tilemap(section):
    screen.fill(BLACK)
    for i in range(SECTION_LENGTH):
        for j in range(SECTION_LENGTH):
            if section.tilemap[i][j] == 1:
                pygame.draw.rect(screen, BLUE, (j*TILE_SIZE, i*TILE_SIZE, 32, 32))
            else:
                pygame.draw.rect(screen, BLACK, (j*TILE_SIZE, i*TILE_SIZE, 32, 32))

def tilemap_collision(player, room):
    left = player.rect.left // TILE_SIZE
    right = (player.rect.right - 1) // TILE_SIZE
    top = player.rect.top // TILE_SIZE
    bottom = (player.rect.bottom - 1) // TILE_SIZE
    
    return (
        room.tilemap[top][left] == 0 or
        room.tilemap[top][right] == 0 or
        room.tilemap[bottom][left] == 0 or
        room.tilemap[bottom][right] == 0
    )

def room_transfer(player, room):
    left = player.rect.left // TILE_SIZE
    right = (player.rect.right - 1) // TILE_SIZE
    top = player.rect.top // TILE_SIZE
    bottom = (player.rect.bottom - 1) // TILE_SIZE
    
    if top < 0:
        return new_room(player, room, 'N')
    if right > SECTION_LENGTH-1:
        return new_room(player, room, 'E')
    if bottom > SECTION_LENGTH-1:
        return new_room(player, room, 'S')
    if left < 0:
        return new_room(player, room, 'W')
    
    return False

def new_room(player, curr_room, direction = str):
    grid_x = curr_room.position[0]
    grid_y = curr_room.position[1]
    
    n_ent = None
    e_ent = None
    s_ent = None
    w_ent = None
    
    match direction:
        case 'N':
            grid_y += 1
            s_ent = player.tile_x
            if curr_room.tilemap[0][player.tile_x - 1] == 0:
                s_ent += 1
            elif curr_room.tilemap[0][player.tile_x + 1] == 0:
                s_ent -= 1
        case 'E':
            grid_x += 1
            w_ent = player.tile_y
            if curr_room.tilemap[player.tile_y - 1][SECTION_LENGTH-1] == 0:
                w_ent += 1
            elif curr_room.tilemap[player.tile_y + 1][SECTION_LENGTH-1] == 0:
                w_ent -= 1
        case 'S':
            grid_y -= 1
            n_ent = player.tile_x
            if curr_room.tilemap[SECTION_LENGTH-1][player.tile_x - 1] == 0:
                n_ent += 1
            elif curr_room.tilemap[SECTION_LENGTH-1][player.tile_x + 1] == 0:
                n_ent -= 1 
        case 'W':
            grid_x -= 1
            e_ent = player.tile_y
            if curr_room.tilemap[player.tile_y - 1][0] == 0:
                e_ent += 1
            elif curr_room.tilemap[player.tile_y + 1][0] == 0:
                e_ent -= 1
    
    if (grid_x, grid_y) in main_grid.rooms:
        return main_grid.rooms[grid_x, grid_y]
    else:
        new_room = main_grid.generate_room((grid_x, grid_y),
                                            "CORRIDOR",
                                            {'N': n_ent, 'E': e_ent, 'S': s_ent, 'W': w_ent})
        return new_room

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    """
    Movement Tracking
    """
    
    move_x = 0
    move_y = 0
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_y -= speed
    if keys[pygame.K_s]:
        move_y += speed
    if keys[pygame.K_a]:
        move_x -= speed
    if keys[pygame.K_d]:
        move_x += speed
    
    if move_x != 0 and move_y != 0:
        move_x /= math.sqrt(2)
        move_y /= math.sqrt(2)
    
    for i in range(abs(int(move_x))):
        player.rect.x += 1 if move_x > 0 else -1
        result = room_transfer(player, active_room)
        
        if not result:
            collision_check = tilemap_collision(player, active_room)
            if collision_check == True:
                player.rect.x += -1 if move_x > 0 else 1
            else:
                pass
        else:
            active_room = result
            if move_x <= 0:
                player.rect.x = SCREEN_SIZE - TILE_SIZE
            else:
                player.rect.x = 0
    
    for i in range(abs(int(move_y))):
        player.rect.y += 1 if move_y > 0 else -1
        result = room_transfer(player, active_room)
        
        if not result:
            collision_check = tilemap_collision(player, active_room)
            if collision_check == True:
                player.rect.y += -1 if move_y > 0 else 1
            else:
                pass
        else:
            active_room = result
            if move_y <= 0:
                player.rect.y = SCREEN_SIZE - TILE_SIZE
            else:
                player.rect.y = 0
    
    """
    Player Value Updates
    """
    
    player.tile_x = player.rect.x // TILE_SIZE
    player.tile_y = player.rect.y // TILE_SIZE
    
    """
    Rendering
    """
    
    render_tilemap(active_room)
    screen.blit(player.surface, player.rect)
    
    text = font.render(f"({active_room.position[0]}, {active_room.position[1]})", True, (255, 255, 255))
    screen.blit(text, (32, 32))
    
    """
    Pygame Screen Update & Clock Tick
    """
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()