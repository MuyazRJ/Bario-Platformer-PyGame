from csv import reader
from game_data import TILE_SIZE
from os import walk
import pygame


###
# all functions were taken from this video (Github files are linked in description):
# https://www.youtube.com/watch?v=wJMDh9QGRgs
###
def import_folder(path):
	# Imports all images from a folder
	surface_list = []

	for folder_name, subfolders, image_files in walk(path):
		# Note: folder_name and subfolders not used
		for image in image_files:
			full_path = path + '/' + image
			image_surface = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surface)
	
	return surface_list

def import_csv_layout(path):
	# Import (layout) CSV file and return contents as a list
	layout = []

	with open(path) as map_file:
		# Holds CSV file
		level = reader(map_file,delimiter = ",")
		for row in level:
			# For each row in the file
			# Convert to list and append to layout
			layout.append(list(row))

	return layout


def import_cut_graphics(path):
	# Loads uncut graphic
	uncut_image = pygame.image.load(path).convert_alpha()
	
	tile_num_x = uncut_image.get_size()[0] // TILE_SIZE
	tile_num_y = uncut_image.get_size()[1] // TILE_SIZE

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * TILE_SIZE
			y = row * TILE_SIZE
			# New surface/image object (with dimensions TILE_SIZE)
			new_image = pygame.Surface((TILE_SIZE,TILE_SIZE), flags = pygame.SRCALPHA)
			# Cut image
			new_image.blit(uncut_image, (0,0), pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
			cut_tiles.append(new_image) # Append image to cut_tiles

	return cut_tiles
