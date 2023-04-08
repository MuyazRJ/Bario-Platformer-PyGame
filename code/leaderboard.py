import csv
from import_functions import import_csv_layout
import pygame
from game_data import SCREEN_HEIGHT, SCREEN_WIDTH


path = "..\levels\LeaderBoard.csv" #the path for the leaderboard csv file





def update_coins(player_num,level,coins):
    """update the coins of the player in the leaderboard """
    data = import_csv_layout(path)

    if int(data[player_num][level]) < coins: data[player_num][level] = coins 

    

    with open(path,'w') as leader_board:
        lBFile= csv.writer(leader_board,lineterminator="\n")

        lBFile.writerows(data)

    

def add_player(player_name):
    """add new player to the leader Board"""
    with open(path,'a') as leader_board:
        lBFile= csv.writer(leader_board,lineterminator="\n")

        lBFile.writerow([player_name,0,0,0,0,0])

    


def change_player_name(player_num,player_name):
    data = import_csv_layout(path)

    data[player_num][0] = player_name

    with open(path,'w') as leader_board:
        lBFile= csv.writer(leader_board,lineterminator="\n")

        lBFile.writerows(data)


def show_leaderBoard(screen):
    # set up the font
    font_path = "../Graphics/menu/font/font.ttf"  
    title_size = 70
    data_font = pygame.font.Font(font_path,20)
    title_font = pygame.font.Font(font_path, title_size)
   

    text_colour = (255, 255, 255) # White

    #title position
    title = title_font.render('Leaderboard', True, text_colour)
    title_rect = title.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 250))

    screen.blit(title, title_rect)

    #import the data from 
    data = import_csv_layout(path)

    x_pos = SCREEN_WIDTH/15
    y_pos = SCREEN_HEIGHT/2 -180

    # Iterate through the data list and display on the screen
    for row in data:
        name_text = data_font.render(row[0], True, text_colour)
        score_text = [data_font.render(row[x], True, text_colour) for x in range(1,6)]
        
        screen.blit(name_text, (x_pos, y_pos))
        for i ,col in enumerate(score_text):
            screen.blit(col, (x_pos + 200*(i+1) , y_pos ))


        y_pos +=50
    

    

        