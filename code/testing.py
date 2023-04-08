import pygame

class Test():
	# Class to help with testing
	def draw_hitboxes(screen,sprites_group, is_hitbox = False):
		# Draws hitboxes around all sprites in a group
		for i in range(len(sprites_group)):
			# Draws box using rect attribute, from each sprite (same attribute typically used in collide functions)
			if is_hitbox:
				pygame.draw.rect(screen, "blue", sprites_group.sprites()[i].hitbox_rect,3)
			else:
				pygame.draw.rect(screen, "red", sprites_group.sprites()[i].rect,3)