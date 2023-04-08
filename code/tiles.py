import pygame
from import_functions import import_folder

###
#classes Tile, StaticTile, Stump, Tree, Coin, AnimatedTile
##were used by the tutorial
# YouTube:

# https://www.youtube.com/watch?v=wJMDh9QGRgs

# GitHub (keep in mind we only took code from the 2nd folder, named “2 - Level“):

# https://github.com/clear-code-projects/2D-Mario-style-platformer
###
class Tile(pygame.sprite.Sprite):
	# Basic tile class
	# Note: Abstract method, but Python doesn't have abstract methods built in
	def __init__(self,size,x,y):
		super().__init__()
		# Attributes:
		# Image + Rect
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,x_shift):
		self.rect.x += x_shift


class StaticTile(Tile):
	# For tiles with static images
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface

class Stump(StaticTile):
	def __init__(self,size,x,y):
		super().__init__(size,x,y,pygame.image.load('../graphics/terrain/stump.png').convert_alpha())
		# Apply offset to y, such that stump sits right ontop of tile (otherwise stump would be floating)
		self.rect = self.image.get_rect(bottomleft = (x,y + size))

class Tree(StaticTile):
	def __init__(self, size, x, y, surface, offset):
		super().__init__(size, x, y, surface)
		# Apply offset, so palm is properly positioned
		self.rect.topleft = (x, y - offset)

class StaticCoin(StaticTile): # coin 32x32,  number 6x7
	def __init__(self,size,x,y,path):
		image = pygame.image.load(path).convert_alpha()
		if path == '../graphics/coins/gold/0.png':
			# Enlarge gold icon
			image = pygame.transform.scale(image, (46, 46))
		
		super().__init__(size,x,y,image)

	def update(self):
		# overwrite update() so it cannot scroll
		pass


class AnimatedTile(Tile):
	# For tiles with animated images
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y)
		# Animation
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
	
	def animate(self):
		# Increment frame index
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			# If at the end of animation, reset index back to 0
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]
	
	def update(self, x_shift):
		super().update(x_shift)
		self.animate()
		
class Coin(AnimatedTile):
	def __init__(self, size, x, y, path,is_gold):
		super().__init__(size, x, y, path)
		self.is_gold = is_gold
		# Center coins
		self.rect = self.image.get_rect(center = (x + (size//2), y + (size//2)))

class Heart(AnimatedTile): # 18px wide
	def __init__(self, size, x, y, path):
		super().__init__(size, x, y, path)

	# overwrite update() so it cannot scroll, but still animated (could just not call update() though)
	def update(self):
		self.animate()
