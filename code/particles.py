import pygame
from import_functions import import_folder


# all methods in the ParticleEffect class was taken from this video (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type):
		super().__init__()
		# Animation
		self.frame_index = 0
		self.animation_speed = 0.5
		
		if type == 'jump':
			# If jump , import jump particles
			self.frames = import_folder('../graphics/character/dust_particles/jump')
		elif type == 'land':
			# If land , import land particles
			self.frames = import_folder('../graphics/character/dust_particles/land')
		elif type == 'explosion':
			# If explosion , import explosion particles
			self.frames = import_folder('../graphics/enemy/explosion')
		elif type == 'heart_hit':
			self.frames = import_folder('../graphics/lives/hit')
		
		# Image + Rect
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		# Increment frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			# If at the end of animation, remove particles
			self.kill()
		else:
			# Else, update image
			self.image = self.frames[int(self.frame_index)]

	def update(self,x_shift):
		self.animate()
		self.rect.x += x_shift
