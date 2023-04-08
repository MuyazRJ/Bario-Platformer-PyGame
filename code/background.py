import pygame
from game_data import VERTICAL_TILE_NUMBER, TILE_SIZE, SCREEN_WIDTH
from import_functions import import_folder
from random import choice, randint
from tiles import StaticTile, AnimatedTile

# all methods from Sky, Clouds and Water classes was taken from this video (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs

class Sky:
	# Note: Not a tile since it doesn't shift, practically like a background image 
    def __init__(self, field):
    	# Attributes:
    	# Images
        self.upper = pygame.image.load(
            '../graphics/decoration/sky/sky_top.png').convert_alpha()
        self.lower = pygame.image.load(
            '../graphics/decoration/sky/sky_bottom.png').convert_alpha()
        self.middle = pygame.image.load(
            '../graphics/decoration/sky/sky_middle.png').convert_alpha()
        self.field = field

		# Scaling the sky image
        self.upper = pygame.transform.scale(
            self.upper, (SCREEN_WIDTH, TILE_SIZE))
        self.lower = pygame.transform.scale(
            self.lower, (SCREEN_WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(
            self.middle, (SCREEN_WIDTH, TILE_SIZE))

    def draw(self,space):
        for line in range(VERTICAL_TILE_NUMBER):
            # For each row
            y = line * TILE_SIZE

            if line < self.field:
            	# If row is below horizon, display top tile
            	space.blit(self.upper,(0,y))
            elif line == self.field:
				# If row is at horizon, display middle tile
                space.blit(self.middle,(0,y))
            else:
				# If row is below horizon, display bottom tile
                space.blit(self.lower,(0,y))

class Clouds:
	def __init__(self,field,level_width,cloud_number):
		cloud_surf_list = import_folder('../graphics/decoration/clouds') # Holds list of different cloud images
		min_x = -SCREEN_WIDTH
		max_x = level_width + SCREEN_WIDTH
		min_y = 0
		max_y = field
		
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			# For each cloud, randomly select image and location
			cloud = choice(cloud_surf_list)
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	def draw(self,screen,x_shift):
		self.cloud_sprites.update(x_shift * 0.5) # Multiply by 0.5 to add parallax effect
		self.cloud_sprites.draw(screen)

                                
class Water:
	# Note: Water sits ontop of everything, though not collidable
	def __init__(self,top,level_width):
		water_start = -SCREEN_WIDTH # Water starts before level
		water_tile_width = 192
		tile_amount = (level_width + (SCREEN_WIDTH * 2)) // water_tile_width
		self.water_sprites = pygame.sprite.Group()

		for tile in range(tile_amount):
			# For each tile:
			x = (tile * water_tile_width) + water_start
			y = top
			sprite = AnimatedTile(water_tile_width,x,y,'../graphics/decoration/water')
			self.water_sprites.add(sprite)

	def draw(self,screen,x_shift):
		self.water_sprites.update(x_shift)
		self.water_sprites.draw(screen)
