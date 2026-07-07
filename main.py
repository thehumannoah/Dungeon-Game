import pygame

pygame.init()

pygame.display.set_caption('Dungeon Game')
screen_size = 700
player_size = 50
player_pos = (screen_size/2)-(player_size/2)
screen = pygame.display.set_mode((screen_size, screen_size))
player = pygame.Surface((player_size, player_size))
player.fill((255, 0, 0))
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(player, (player_pos, player_pos))
    
    pygame.display.update()
    clock.tick(60)