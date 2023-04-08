import pygame
from import_functions import import_csv_layout,import_cut_graphics
from game_data import TILE_SIZE,SCREEN_HEIGHT,SCREEN_WIDTH
from tiles import StaticTile,Stump,Coin,Tree,Heart,StaticCoin
from enemy import Enemy
from background import Sky,Clouds,Water
from player import Player
from particles import ParticleEffect
from testing import Test
import time
from leaderboard import update_coins

###
# of the Level class:
	# update_coin_sprites, 
	# update_heart_sprites
	# is_player_on_ground
	# hat_collision
	# player_fell_off_map
	# show_death_screen
	# completed_level_screen
# are unique
# methods:
	# horizontal_movement_collision, 
	# vertical_movement_collision, 
	# create_landing_dust, 
	# run, 
	# create_jump_particles
	# __init__
	# scroll_x
	# enemy_collision_reverse
	# create_tile_group
# were used from the tutorial

# methods:
	# coin_collision
	# enemy_collision
# are heavily modified, but from the tutorial

# (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs


# Level class handles all sprites and game logic, within a given level
class Level:
	def __init__(self,level_data,screen,level_num):
		# Sound:
		pygame.mixer.Channel(1).play(pygame.mixer.Sound("../sounds/background.mp3"),-1)

		# Attributes:
		# World
		self.screen = screen
		self.world_shift = 0
		
		# Dust 
		self.particle_sprite = pygame.sprite.GroupSingle()
		self.prev_on_ground = False

		#status          #before create_tile_group() or status undefined
		self.coins_taken = 0
		self.lives_left = 5
		self.gameOver = False

		# Level info
		self.completed_current_level = False
		self.level_num = level_num

		# Setup Tiles/Sprites
		self.bg_trees_sprites = pygame.sprite.Group()
		self.terrain_sprites = pygame.sprite.Group()
		self.enemies_sprites = pygame.sprite.Group()
		self.constraints_sprites = pygame.sprite.Group()
		self.stumps_sprites = pygame.sprite.Group()
		self.coins_sprites = pygame.sprite.Group()
		self.heart_sprites = pygame.sprite.Group()
		self.numbers_sprites = pygame.sprite.Group()
		self.fg_trees_sprites = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.create_tile_group(level_data)
		self.update_heart_sprites()
		self.update_coin_sprites()

		# Background Layout
		self.sky = Sky(8)
		terrain_layout = import_csv_layout(level_data["terrain"])
		level_width = len(terrain_layout[0]) * TILE_SIZE
		self.water = Water(SCREEN_HEIGHT - 20,level_width)
		self.clouds = Clouds(400,level_width,30)

		# Font used
		font_path = "../graphics/menu/font/font.ttf"  
		self.font = pygame.font.Font(font_path, 70)

	# ----- Add Tiles/Sprites -----
	def create_tile_group(self,level_data):
		for key in level_data:
			# For each tile type in level_data

			# Layout for each tile type
			layout = import_csv_layout(level_data[key])
			for row_index, row in enumerate(layout):
				for col_index, val in enumerate(row):
					if val != '-1':
						# If tile needs to be placed
						x = col_index * TILE_SIZE
						y = row_index * TILE_SIZE

						match key:
							# Match tile type, and add appropriate tile
							case 'bg_trees':
								tree_surface = pygame.image.load('../graphics/terrain/tree_bg.png').convert_alpha()	
								tile = Tree(TILE_SIZE, x, y, tree_surface, 64)
								self.bg_trees_sprites.add(tile)
							case 'terrain':
								terrain_tile_list = import_cut_graphics('../graphics/terrain/terrain_tiles.png')
								tile_surface = terrain_tile_list[int(val)]
								tile = StaticTile(TILE_SIZE, x, y,tile_surface)
								self.terrain_sprites.add(tile)
							case 'enemies':
								tile = Enemy(TILE_SIZE, x, y)
								self.enemies_sprites.add(tile)
							case 'constraints':
								constraint_tile_list = import_cut_graphics('../graphics/enemy/setup_tiles.png')
								tile_surface = constraint_tile_list[int(val)]
								tile = StaticTile(TILE_SIZE, x, y,tile_surface)
								self.constraints_sprites.add(tile)
							case 'stumps':
								tile = Stump(TILE_SIZE,x,y)
								self.stumps_sprites.add(tile)
							case 'coins':
								if val == '0': tile = Coin(TILE_SIZE, x, y, '../graphics/coins/gold',True)
								else: tile = Coin(TILE_SIZE, x, y, '../graphics/coins/silver',False)
								self.coins_sprites.add(tile)
							case 'fg_trees':
								if val == '0': 
									tree_surface = pygame.image.load('../graphics/terrain/tree_small.png').convert_alpha()
									tile = Tree(TILE_SIZE, x, y, tree_surface, 38)
								elif val == '1':
									tree_surface = pygame.image.load('../graphics/terrain/tree_large.png').convert_alpha()
									tile = Tree(TILE_SIZE, x, y, tree_surface, 72)
								self.fg_trees_sprites.add(tile)
							case "player":
								if val == '0':
									# Places character
									character = Player((x,y),self.screen,self.create_jump_particles)
									self.player.add(character)
								if val == '1':
									# Places end of level ("goal")
									hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
									character = StaticTile(TILE_SIZE, x, y, hat_surface)
									self.goal.add(character)


	# ----- Scroll screen right and left -----
	def scroll_x(self):
		# Variables
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < SCREEN_WIDTH / 4 and direction_x < 0:
			# If player is at right, move screen to right and keep player still
			self.world_shift = 8
			player.speed = 0
		elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_x > 0:
			# If player is at left, move screen to left and keep player still
			self.world_shift = -8
			player.speed = 0
		else:
			# Else, keep screen still and return player speed to normal
			self.world_shift = 0
			player.speed = 8

	# ----- Player collision (with tiles and enemies) -----
	def horizontal_movement_collision(self):
		# Moves player horizontally then checks for horizontal collisions
		# Move player horizontally
		player = self.player.sprite
		# player.rect.x += player.direction.x * player.speed
		player.hitbox_rect.x += player.direction.x * player.speed
		
		collidable_sprites = self.terrain_sprites.sprites() + self.stumps_sprites.sprites() + self.fg_trees_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.hitbox_rect):
				# If collision detected with tile
				if player.direction.x < 0:
					# If moving left
					player.hitbox_rect.left = sprite.rect.right
					# player.rect.right = player.hitbox_rect.right
					self.current_x = player.hitbox_rect.left
				elif player.direction.x > 0:
					# If moving right
					player.hitbox_rect.right = sprite.rect.left
					# player.rect.left = player.hitbox_rect.left
					self.current_x = player.hitbox_rect.right

	def vertical_movement_collision(self):
		# Moves player vertically then checks for vertical collisions
		# Move player vertically
		player = self.player.sprite
		player.direction.y += player.gravity # Apply gravity to direction
		# player.rect.y += player.direction.y # Update rectangle
		player.hitbox_rect.y += player.direction.y # Update rectangle
		
		collidable_sprites = self.terrain_sprites.sprites() + self.stumps_sprites.sprites() + self.fg_trees_sprites.sprites()
		for sprite in collidable_sprites:
			if sprite.rect.colliderect(player.hitbox_rect):
				# If collision detected with tile
				if player.direction.y > 0: 
					# If moving down
					# player.rect.bottom = sprite.rect.top
					player.hitbox_rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					# If moving up
					# player.rect.top = sprite.rect.bottom
					player.hitbox_rect.top = sprite.rect.bottom
					player.direction.y = 0

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False

	def hat_collision(self):
		player = self.player.sprite
		if self.goal.sprite.rect.colliderect(player.hitbox_rect):
			self.completed_current_level = True

	def coin_collision(self):
		# List of coins that have collided with player
		coins_collided = pygame.sprite.spritecollide(self.player.sprite,self.coins_sprites,True)
		for coins in coins_collided:
			if coins.is_gold:
				# If gold, add 5 points
				self.coins_taken += 5
			else:
				# Else, add 1
				self.coins_taken += 1

			self.update_coin_sprites()

	def enemy_collision(self):
		player = self.player.sprite
		hitbox_width = 20
		invincibility_duration = 1000  # In milliseconds (1 second)

		for enemy in self.enemies_sprites.sprites():
			if enemy.rect.colliderect(player.hitbox_rect):
				if enemy.rect.top - hitbox_width <= player.rect.bottom <= enemy.rect.top + hitbox_width:
					if player.direction.y > 0 and player.status == 'fall': #If player is falling
						# Explosion animation
						explosion_dust_particle = ParticleEffect(enemy.rect.center,'explosion')
						self.particle_sprite.add(explosion_dust_particle)
						player.jump()
						enemy.kill()
				elif player.invincible_until <= pygame.time.get_ticks():  # Player is not invincible
					self.lives_left -= 1 
					for heart in self.heart_sprites:
						heart_hit_particle = ParticleEffect(heart.rect.center,'heart_hit')
						self.particle_sprite.add(heart_hit_particle)
					self.update_heart_sprites()
					player.invincible_until = pygame.time.get_ticks() + invincibility_duration  # Set invincibility timer
	
	def player_fell_off_map(self):
		player = self.player.sprite
		
		if player.rect.top > SCREEN_HEIGHT:
			self.lives_left = 0

	# ----- Enemy collision (with constraints) -----
	def enemy_collision_reverse(self):
		for enemy in self.enemies_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
				# If enemy collides with a constraints sprite, reverse direction
				enemy.reverse()

	# ----- Add Dust Particles -----
	def create_jump_particles(self,pos):
		# Apply offet depending on way player is facing
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,15)
		else:
			pos += pygame.math.Vector2(10,-15)
		# Add jump particle
		jump_particle_sprite = ParticleEffect(pos,'jump')
		self.particle_sprite.add(jump_particle_sprite)

	def is_player_on_ground(self):
		# Check if player is on ground
		if self.player.sprite.on_ground:
			self.prev_on_ground = True
		else:
			self.prev_on_ground = False

	def create_landing_dust(self):
		# If player wasn't on ground before but is after running vertical_collision
		if not self.prev_on_ground and self.player.sprite.on_ground and not self.particle_sprite.sprites():
			# Apply offset depending on way character is facing
			if self.player.sprite.facing_right:
				offset = pygame.math.Vector2(10,15)
			else:
				offset = pygame.math.Vector2(-10,15)
			# Add landing particle
			land_particle_sprite = ParticleEffect(self.player.sprite.rect.midbottom - offset,'land')
			self.particle_sprite.add(land_particle_sprite)

	# ----- Update UI -----
	def update_heart_sprites(self):
		self.heart_sprites.empty()
		# place hearts
		for i in range(self.lives_left):
			x = i * 70
			tile = Heart(TILE_SIZE, x, 10, '../graphics/lives/idle')

			self.heart_sprites.add(tile)

		# re-runs to update sprites
		self.run

	def show_death_screen(self):
		pygame.mixer.Channel(1).stop()
		time.sleep(0.25)
		self.screen.fill((0,0,0))
		death_label = self.font.render('You Died', True, (255, 255, 255))
		death_label_rect = death_label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.screen.blit(death_label, death_label_rect)
		
		pygame.display.update()
		time.sleep(2.5)
	
	def completed_level_screen(self):
		time.sleep(0.75)
		self.screen.fill((0,0,0))
		if self.level_num != 5: 
			completed_level_label = self.font.render('Completed Level ' + str(self.level_num), True, (255, 255, 255))
		else:
			pygame.mixer.Channel(1).stop()
			completed_level_label = self.font.render('You won!', True, (255, 255, 255))
		completed_level_label_rect = completed_level_label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.screen.blit(completed_level_label, completed_level_label_rect)
		pygame.display.update()
		time.sleep(2)
		

	def update_coin_sprites(self):
		self.numbers_sprites.empty()
		for i in range(len(str(self.coins_taken)) + 1):
			x = 400 + (i* 40)			
			if i == 0:
				# places coin icon
				tile = StaticCoin(TILE_SIZE, x, 12,'../graphics/coins/gold/0.png')
			else:
				# places numbers
				number = str(self.coins_taken)[i - 1]
				tile = StaticCoin(TILE_SIZE, x, 10,'../graphics/coins/numbers/'+number+'.png')
			
			self.numbers_sprites.add(tile)
		# re runs so numbers are deleted then added
		self.run

	# ----- Draws sprites/tiles -----
	def run(self):
		# If player dies, show the death screen
		if self.lives_left == 0:
			self.gameOver = True
			self.show_death_screen()
			return
	
		# Note: Order matters
		# Sky
		self.sky.draw(self.screen)
		self.clouds.draw(self.screen,self.world_shift)

		# Background trees
		self.bg_trees_sprites.update(self.world_shift)
		self.bg_trees_sprites.draw(self.screen)

		# Terrain
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.screen)
		
		# Enemies
		self.enemies_sprites.update(self.world_shift)
		self.constraints_sprites.update(self.world_shift)
		self.enemy_collision_reverse()
		self.enemies_sprites.draw(self.screen)

		# Stumps
		self.stumps_sprites.update(self.world_shift)
		self.stumps_sprites.draw(self.screen)

		# Coins
		self.coins_sprites.update(self.world_shift)
		self.coins_sprites.draw(self.screen)
		self.coin_collision()

		# Hearts
		self.heart_sprites.update()
		self.heart_sprites.draw(self.screen)

		# Coin count
		self.numbers_sprites.draw(self.screen)

		# Foreground trees
		self.fg_trees_sprites.update(self.world_shift)
		self.fg_trees_sprites.draw(self.screen)

		# Dust Particles
		self.particle_sprite.update(self.world_shift)
		self.particle_sprite.draw(self.screen)

		# Player
		self.player.update()
		self.horizontal_movement_collision()
		self.hat_collision()

		# Check if player has won by colliding with the hat
		if self.completed_current_level: 
			update_coins(1,self.level_num,self.coins_taken) #update coin data in the leaderboard
			self.completed_level_screen() 
			return
		
		self.is_player_on_ground()
		self.vertical_movement_collision()
		self.create_landing_dust()
		
		self.scroll_x()
		self.player.draw(self.screen)
		
		self.goal.update(self.world_shift)
		self.goal.draw(self.screen)

		self.enemy_collision()
		self.player_fell_off_map()

		# Water
		self.water.draw(self.screen,self.world_shift)


		# Testing (comment out of not needed)
		# self.constraints_sprites.draw(self.screen) # Realisticly, draw_hitboxes would be more useful
		# Test.draw_hitboxes(self.screen, self.enemies_sprites)
		# Test.draw_hitboxes(self.screen, self.player)
		# Test.draw_hitboxes(self.screen, self.player, True)
