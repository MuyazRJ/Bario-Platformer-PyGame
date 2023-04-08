# ___ function, ___ class was taken from this video (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs
# [Fill in the blanks when we finish the code]

import pygame
from game_data import SCREEN_WIDTH,SCREEN_HEIGHT,level_1,level_2,level_3,level_4,level_5
from level import Level
from menu import Menu

# Pygame Setup
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
hat_surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
pygame.display.set_icon(hat_surface)
pygame.display.set_caption("Bario")
clock = pygame.time.Clock()

# Run menu
highest_level_achieved = 1 # Variable to check which levels should be interactable on the menu
menu = Menu(screen)
menu.run(highest_level_achieved)

# All the code below runs the level
# Change level_1 to level_2 to run level 2, etc.

def getLevel(level_num = None):
	level_files = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5}
	if level_num != None: level_file = level_files.get(level_num, level_1)
	else: level_file = level_files.get(menu.selected_level, level_1)
	return level_file

# Update highest_level_achieved
def check_if_achieved_new_level(level):
	global highest_level_achieved
	if level.level_num > highest_level_achieved: highest_level_achieved = level.level_num

level = Level(getLevel(), screen, menu.selected_level)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# If user crosses out window, stop running
			running = False

	# Reset level and health and exit to main menu if the player dies
	if level.gameOver:
		level.gameOver = False
		level.lives_left = 5
		check_if_achieved_new_level(level)
		menu.run(highest_level_achieved)
		level = Level(getLevel(), screen, menu.selected_level)
	elif level.completed_current_level:
		level.completed_current_level = False
		# If the player has completed the last level, they are taken back to the menu
		if level.level_num == 5: 
			menu.run(highest_level_achieved)
			level = Level(getLevel(), screen, menu.selected_level)
		else:
			# Else, the next level is loaded
			level.level_num += 1
			check_if_achieved_new_level(level)
			level = Level(getLevel(level.level_num), screen, level.level_num)
	else:
		# Redraw Background + Sprites
		level.run()

	pygame.display.update()
	clock.tick(60)

# Quit pygame
pygame.quit()