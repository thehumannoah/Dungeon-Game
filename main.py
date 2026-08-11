import math
import pygame
import config
from world import *

SECTION_LENGTH = config.SECTION_LENGTH
TILE_SIZE = config.TILE_SIZE
SCREEN_SIZE = config.SCREEN_SIZE
SCREEN_CENTER = config.SCREEN_CENTER
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

def render_tilemap(section):
    screen.fill(BLACK)
    for i in range(SECTION_LENGTH):
        for j in range(SECTION_LENGTH):
            if section.tilemap[i][j] == 1:
                pygame.draw.rect(screen, BLUE, (j*TILE_SIZE, i*TILE_SIZE, 32, 32))
            else:
                pygame.draw.rect(screen, BLACK, (j*TILE_SIZE, i*TILE_SIZE, 32, 32))

def tilemap_collision(player_rect, tilemap):
    left = player_rect.left // TILE_SIZE
    right = (player_rect.right - 1) // TILE_SIZE
    top = player_rect.top // TILE_SIZE
    bottom = (player_rect.bottom - 1) // TILE_SIZE
    
    if top < 0: return True
    if right > SECTION_LENGTH-1: return True
    if bottom > SECTION_LENGTH-1: return True
    if left < 0: return True
    
    return (
        tilemap[top][left] == 0 or
        tilemap[top][right] == 0 or
        tilemap[bottom][left] == 0 or
        tilemap[bottom][right] == 0
    )

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

# Current tile text display
font = pygame.font.Font(None, 32)

# Start Room generation
start = room.Room(mode = "START")
active_room = start

speed = 5
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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
        
        if tilemap_collision(player.rect, active_room.tilemap):
            player.rect.x += -1 if move_x > 0 else 1
    
    for i in range(abs(int(move_y))):
        player.rect.y += 1 if move_y > 0 else -1
        
        if tilemap_collision(player.rect, active_room.tilemap):
            player.rect.y += -1 if move_y > 0 else 1
    
    player.tile_x = player.rect.x // TILE_SIZE
    player.tile_y = player.rect.y // TILE_SIZE
    
    render_tilemap(active_room)
    screen.blit(player.surface, player.rect)
    
    text = font.render(f"({player.tile_x}, {player.tile_y})", True, (255, 255, 255))
    screen.blit(text, (32, 32))
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()