import pygame
from pygame.locals import *
from game_data import SCREEN_HEIGHT, SCREEN_WIDTH
from leaderboard import show_leaderBoard


###
# credits code modified from https://stackoverflow.com/questions/36164524/python-pygame-create-end-credits-like-the-ones-at-the-end-of-a-movie
###


class Menu:
    def __init__(self, screen):
        pygame.init()

        # set up the window
        background_image_path = "../graphics/menu/background/background.png"
        self.background_image = pygame.image.load(background_image_path)
        self.screen = screen

        # set up the font
        font_path = "../graphics/menu/font/font.ttf"  
        font_size = 50
        title_size = 70
        self.font = pygame.font.Font(font_path, font_size)
        self.title_font = pygame.font.Font(font_path, title_size)
        
        # initialize button colours
        self.button_colour = (255, 255, 255) # White
        self.hover_button_colour = (0, 200, 200) # Blue
        self.inactive_button_colour = (169, 169, 169) # Grey

        self.play_button_colour = self.button_colour
        self.leaderboard_button_colour = self.button_colour
        self.credits_button_colour = self.button_colour
        self.level_1_button_colour = self.button_colour
        self.level_2_button_colour = self.button_colour
        self.level_3_button_colour = self.button_colour
        self.level_4_button_colour = self.button_colour
        self.level_5_button_colour = self.button_colour
        self.back_button_colour = self.button_colour

        # set up the buttons and button positions
        self.bario_label = self.title_font.render('Bario', True, self.button_colour)
        self.bario_label_rect = self.bario_label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 250))

        self.play_button = self.font.render('Play', True, self.play_button_colour)
        self.play_button_rect = self.play_button.get_rect(center=(SCREEN_WIDTH / 2, 250))

        self.back_button = self.font.render('Back', True, self.back_button_colour)
        self.back_button_rect = self.play_button.get_rect(center=(110, 40))

        self.leaderboard_button = self.font.render('Leaderboard', True, self.leaderboard_button_colour)
        self.leaderboard_button_rect = self.leaderboard_button.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.credits_button = self.font.render('Credits', True, self.credits_button_colour)
        self.credits_button_rect = self.credits_button.get_rect(center=(SCREEN_WIDTH / 2, 455))

        self.select_level_label = self.font.render('Select Level', True, self.button_colour)
        self.select_level_label_rect = self.select_level_label.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 250))

        self.level_1_button = self.font.render('Level 1', True, self.level_1_button_colour)
        self.level_1_button_rect = self.level_1_button.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150))

        self.level_2_button = self.font.render('Level 2', True, self.level_2_button_colour)
        self.level_2_button_rect = self.level_2_button.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))

        self.level_3_button = self.font.render('Level 3', True, self.level_3_button_colour)
        self.level_3_button_rect = self.level_3_button.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        
        self.level_4_button = self.font.render('Level 4', True, self.level_4_button_colour)
        self.level_4_button_rect = self.level_4_button.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))

        self.level_5_button = self.font.render('Level 5', True, self.level_5_button_colour)
        self.level_5_button_rect = self.level_5_button.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 250))

    def handle_events(self):
        self.screen.blit(self.background_image, (0, 0))

        for event in pygame.event.get():
            # Get the current position of the mouse
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif self.on_select_level_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Set the selected level based on which button was clicked
                    if self.level_1_button_rect.collidepoint(mouse_pos):
                        self.selected_level = 1
                    elif self.level_2_button_rect.collidepoint(mouse_pos) and self.level_2_button_colour != self.inactive_button_colour:
                        self.selected_level = 2
                    elif self.level_3_button_rect.collidepoint(mouse_pos) and self.level_3_button_colour != self.inactive_button_colour:
                        self.selected_level = 3
                    elif self.level_4_button_rect.collidepoint(mouse_pos) and self.level_4_button_colour != self.inactive_button_colour:
                        self.selected_level = 4
                    elif self.level_5_button_rect.collidepoint(mouse_pos) and self.level_5_button_colour != self.inactive_button_colour:
                        self.selected_level = 5
                    # If the back button is clicked, go back to the main menu screen
                    elif self.back_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = True
                        self.on_select_level_screen = False
            elif self.on_credits_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the back button is clicked, go back to the main menu screen
                    if self.back_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = True
                        self.on_credits_screen = False
            elif self.on_leaderboard_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the back button is clicked, go back to the main menu screen
                    if self.back_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = True
                        self.on_leaderboard_screen = False
            elif self.on_main_menu_screen:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the play button is clicked, go to the level selection screen
                    if self.play_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = False
                        self.on_select_level_screen = True
                    # If the leaderboard button is clicked, go to the leaderboard screen
                    elif self.leaderboard_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = False
                        self.on_leaderboard_screen = True
                    # If the credits button is clicked, go to the credits screen
                    elif self.credits_button_rect.collidepoint(mouse_pos):
                        self.on_main_menu_screen = False
                        self.on_credits_screen = True

    def update_button_colours(self, mouse_pos):
        if self.on_main_menu_screen:
            # create a list of button rects and colours
            button_list = [(self.play_button_rect, "play_button_colour"),
                        (self.leaderboard_button_rect, "leaderboard_button_colour"),
                        (self.credits_button_rect, "credits_button_colour")]

            # loop through the list and check if the mouse is over each button
            for button_rect, colour_attr in button_list:
                if button_rect.collidepoint(mouse_pos):
                    setattr(self, colour_attr, self.hover_button_colour) # set button colour to blue
                else:
                    setattr(self, colour_attr, self.button_colour) # set button colour to white
        elif self.on_select_level_screen:
            button_rects = [self.level_1_button_rect, self.level_2_button_rect, self.level_3_button_rect, self.level_4_button_rect, self.level_5_button_rect, self.back_button_rect]
            button_colours = [self.level_1_button_colour, self.level_2_button_colour, self.level_3_button_colour, self.level_4_button_colour, self.level_5_button_colour, self.back_button_colour]

            for i in range(len(button_rects)):
                # If the player hasn't reached the level yet, it is greyed out
                if i > self.highest_level_achieved - 1 and i < 5:
                    button_colours[i] = self.inactive_button_colour
                elif button_rects[i].collidepoint(mouse_pos):
                    button_colours[i] = self.hover_button_colour   # set button colour to blue
                else:
                    button_colours[i] = self.button_colour  # set button colour to white

            # update the self variables with the new button colours
            self.level_1_button_colour, self.level_2_button_colour, self.level_3_button_colour, self.level_4_button_colour, self.level_5_button_colour, self.back_button_colour = button_colours

        elif self.on_credits_screen or self.on_leaderboard_screen:
            if self.back_button_rect.collidepoint(mouse_pos):
                self.back_button_colour = self.hover_button_colour   # set button colour to blue
                
            else:
                self.back_button_colour = self.button_colour  # set button colour to white

    # draw the buttons and labels needed for each menu screen
    def draw(self):
        if self.on_main_menu_screen:
            # update button colour 
            self.play_button = self.font.render('Play', True, self.play_button_colour)
            self.leaderboard_button = self.font.render('Leaderboard', True, self.leaderboard_button_colour)
            self.credits_button = self.font.render('Credits', True, self.credits_button_colour)

            # draw the buttons
            self.screen.blit(self.background_image, (0, 0))
            self.screen.blit(self.play_button, self.play_button_rect)
            self.screen.blit(self.leaderboard_button, self.leaderboard_button_rect)
            self.screen.blit(self.credits_button, self.credits_button_rect)
            self.screen.blit(self.bario_label, self.bario_label_rect)
        elif self.on_select_level_screen:
            # Create lists for the button texts, colours, buttons, and rects
            self.back_button = self.font.render('back', True, self.back_button_colour)
            level_button_texts = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
            level_button_colours = [self.level_1_button_colour, self.level_2_button_colour, self.level_3_button_colour, self.level_4_button_colour, self.level_5_button_colour]
            level_buttons = [self.level_1_button, self.level_2_button, self.level_3_button, self.level_4_button, self.level_5_button]
            level_button_rects = [self.level_1_button_rect, self.level_2_button_rect, self.level_3_button_rect, self.level_4_button_rect, self.level_5_button_rect]

            # Update the level button text and colour for each button
            self.screen.blit(self.background_image, (0, 0))
            for i in range(len(level_button_texts)):
                level_buttons[i] = self.font.render(level_button_texts[i], True, level_button_colours[i])
                self.screen.blit(level_buttons[i], level_button_rects[i])

            # Blit the select level label to the screen
            self.screen.blit(self.select_level_label, self.select_level_label_rect)
            self.screen.blit(self.back_button, self.back_button_rect)
        elif self.on_leaderboard_screen:
            # Draw back button
            show_leaderBoard(self.screen)
            self.back_button = self.font.render('back', True, self.back_button_colour)
            self.screen.blit(self.back_button, self.back_button_rect)
        elif self.on_credits_screen:


           

            credits_text = [
            "Credits","",
            "Roles:",
            "Muyaz - Main code, Team discussions",
            "Rehan - Main code, Organisation",
            "Matt - Main code",
            "Yousef - Main code",
            "Minjun - Graphics",
            "Dennis - Sounds"," ",
            "Code:",
            "Code modified from the below tutorial (CC0) (exact functions listed in each file)","",
            "YouTube: https://www.youtube.com/watch?v=wJMDh9QGRgs","",
            "Github (keep in mind we only took code from the 2nd folder, named “2 - Level“):",
            "https://github.com/clear-code-projects/2D-Mario-style-platformer","",
            "Images:",
            "Character, Trees modified from Treasure Hunters (CC0) - https://pixelfrog-assets.itch.io/treasure-hunters",
            "Dust particles, Clouds, Water copied from Treasure Hunters (CC0) - https://pixelfrog-assets.itch.io/treasure-hunters",
            "Coins modified from Rocky Roads (CC0) - https://essssam.itch.io/rocky-roads",
            "Enemy explosion copied from Rocky Roads (CC0) - https://essssam.itch.io/rocky-roads",
            "Hearts copied from Kings and Pigs (CC0) - https://pixelfrog-assets.itch.io/kings-and-pigs",
            "Terrain tiles copied from Sunny Land - https://ansimuz.itch.io/sunny-land-pixel-game-art",
            "Font used is Press Start 2P - https://fonts.google.com/specimen/Press+Start+2P","",
            "Sounds:",
            "All sounds were used from https://uppbeat.io "]


            # Create a Pygame surface to display the credits
            font_path = "../graphics/menu/font/font.ttf"
            credits_font = pygame.font.Font(font_path, 10)
            clock = pygame.time.Clock()

            screen_r = self.screen.get_rect()
            texts = []
            # we render the text once, since it's easier to work with surfaces
            # also, font rendering is a performance killer
            for i, line in enumerate(credits_text):
                s = credits_font.render(line, 1, (255, 255, 255))
                # we also create a Rect for each Surface. 
                # whenever you use rects with surfaces, it may be a good idea to use sprites instead
                # we give each rect the correct starting position 
                r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * 45)
                texts.append((r, s))


            # while some rects are on screen
            while self.on_credits_screen == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                self.screen.blit(self.background_image, (0, 0))

                for r, s in texts:
                    # now we just move each rect by one pixel each frame
                    r.move_ip(0, -2)
                    # and drawing is as simple as this
                    self.screen.blit(s, r)
                

                # if all rects have left the screen, we exit
                if not screen_r.collidelistall([r for (r, _) in texts]):
                    self.on_main_menu_screen = True
                    self.on_credits_screen = False
                    
                # only call this once so the screen does not flicker
                pygame.display.flip()

                # cap framerate at 60 FPS
                clock.tick(60)





    def run(self, highest_level_achieved):
        # Initially on main menu screen
        self.on_main_menu_screen = True
        self.on_select_level_screen = False
        self.on_leaderboard_screen = False
        self.on_credits_screen = False
        self.highest_level_achieved = highest_level_achieved

        # Selected level chosen by player after closing the menu
        self.selected_level = None

        while self.selected_level == None:
            # handle events
            self.handle_events()

            # get the mouse position
            mouse_pos = pygame.mouse.get_pos()

            # update button colours
            self.update_button_colours(mouse_pos)

            # draw the buttons and labels
            self.draw()

            # update the screen
            pygame.display.update()

