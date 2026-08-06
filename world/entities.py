import config

class Player():
    def __init__(self, surface, rect):
        self.surface = surface
        self.rect = rect
        self.tile_x = rect.x // config.TILE_SIZE
        self.tile_y = rect.y // config.TILE_SIZE