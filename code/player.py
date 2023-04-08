import pygame 
from import_functions import import_folder

###
# all methods of the player class were used or adapted from the tutorial

# YouTube:

# https://www.youtube.com/watch?v=wJMDh9QGRgs

# GitHub (keep in mind we only took code from the 2nd folder, named “2 - Level“):

# https://github.com/clear-code-projects/2D-Mario-style-platformer
# ###

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,surface,create_jump_particles):
		super().__init__()
		# Attributes:
		# Animation
		self.import_character_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		
		# Image + Rect
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox_rect = pygame.Rect((pos), (54,self.rect.height)) # Constant rect attribute
		
		# Dust Particles 
		self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')
		self.dust_frame_index = 0
		self.dust_animation_speed = 0.15
		self.display_surface = surface
		self.create_jump_particles = create_jump_particles

		# Movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16

		# Status
		self.status = 'idle'
		self.invincible_until = 0  
		self.isAlive = True
		self.facing_right = True
		self.on_ground = False
		

	def import_character_assets(self):
		# Path to character assets folder
		character_path = '../graphics/character/'
		# Dictionary for animations
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

		for animation in self.animations.keys():
			# Full path to each animation folder
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path) # Import animations

	def animate(self):
		animation = self.animations[self.status]

		# Increment frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			# If at the end of animation, reset frame index back to 0
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		if self.facing_right:
			self.image = image
			self.rect.bottomleft = self.hitbox_rect.bottomleft
		else:
			# Flip sprite if facing left
			self.image = pygame.transform.flip(image,True,False)
			self.rect.bottomright = self.hitbox_rect.bottomright

		# So player isn't floating
		self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

		if (self.invincible_until > pygame.time.get_ticks()) and (pygame.time.get_ticks() % 2):
			# When invincible (after being hit) and on every other tick, make character invisible
			self.image.set_alpha(0)
		else:
			# Else, make character fully visible
			self.image.set_alpha(255)

	def run_dust_animation(self):
		# Animation for dust particles
		if self.status == 'run' and self.on_ground:
			# Increment frame index
			self.dust_frame_index += self.dust_animation_speed
			if self.dust_frame_index >= len(self.dust_run_particles):
				# If at the end of animation, reset frame index back to 0
				self.dust_frame_index = 0

			dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

			if self.facing_right:
				# If moving right, place particles on bottom left
				pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
				self.display_surface.blit(dust_particle,pos)
			else:
				# If moving left, place particles on bottom right
				pos = self.rect.bottomright - pygame.math.Vector2(6,10)
				flipped_dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.display_surface.blit(flipped_dust_particle,pos)

	def get_input(self):
		# Get keys pressed
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			# If moving right
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]:
			# If moving left
			self.direction.x = -1
			self.facing_right = False
		else:
			# Else, reduce direction to 0
			self.direction.x = 0

		if keys[pygame.K_UP] and self.on_ground:
			# If moving up
			self.jump()
			self.create_jump_particles(self.rect.midbottom)

	def jump(self):
		self.direction.y = self.jump_speed
		pygame.mixer.Channel(2).play(pygame.mixer.Sound("../sounds/jump.mp3"))


	def get_status(self):
		# Updates players status
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.run_dust_animation()
