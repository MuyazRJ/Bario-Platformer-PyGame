import pygame
from tiles import AnimatedTile
from random import randint

# all methods from Enemy class was taken from this video (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, '../graphics/enemy/run')
        # Offset image such that it's right above tile
        # Note: Only a problem if enemy is smaller than TILESIZE
        self.rect = self.image.get_rect(topleft = self.rect.topleft)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(3, 5)
    
    def move(self):
        self.rect.x += self.speed
    
    def reverse(self):
        # Reverse direction
        self.speed *= -1
    
    def update(self, x_shift):
        super().update(x_shift)
        self.move()
        if self.speed > 0:
            # If moving right, flip image
            self.image = pygame.transform.flip(self.image, True, False)
