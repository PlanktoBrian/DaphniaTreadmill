# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 20:47:53 2023

@author: brian
"""

import pygame
from datetime import datetime


# define button class
class col_button:
    def __init__(self, pos, size, col, which):
        # pos: touple with top left coordinates
        # size: touple with width and height
        # what color does the button stand for (and also sets)
        # which color is set by it (background [0] or object [1])
        self.rect = pygame.Rect(pos,size)
        self.col = col
        self.which = which
    
    def show(self,surface):
        pygame.draw.rect(surface, self.col, self.rect)
        

# predefine colors
BLACK = (   0,   0,   0)
WHITE = ( 255, 255, 255)
BLUE  = (   0,   0, 255)
GREEN = (   0, 255,   0)
RED   = ( 255,   0,   0)
PURPLE = (255,   0, 255)
YELLOW = (255, 255,   0)
CYAN = (    0, 255, 255)
GRAY  = ( 128, 128, 128)
DGRAY = (  64,  64,  64)

# initial colors used
left_color = BLACK
right_color = BLUE

# initialize pygame objects
pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Daphnia TwoSides")
font = pygame.font.SysFont('Arial', 24)
clock = pygame.time.Clock()


# define buttons for background color
r_b = col_button((10,50),(20,20),RED,0)
g_b = col_button((10,80),(20,20),GREEN,0)
b_b = col_button((10,110),(20,20),BLUE,0)
p_b = col_button((10,140),(20,20),PURPLE,0)
y_b = col_button((10,170),(20,20),YELLOW,0)
c_b = col_button((10,200),(20,20),CYAN,0)
s_b = col_button((10,230),(20,20),BLACK,0)
w_b = col_button((10,260),(20,20),WHITE,0)

# define buttons for object color
r_o = col_button((40,50),(20,20),RED,1)
g_o = col_button((40,80),(20,20),GREEN,1)
b_o = col_button((40,110),(20,20),BLUE,1)
p_o = col_button((40,140),(20,20),PURPLE,1)
y_o = col_button((40,170),(20,20),YELLOW,1)
c_o = col_button((40,200),(20,20),CYAN,1)
s_o = col_button((40,230),(20,20),BLACK,1)
w_o = col_button((40,260),(20,20),WHITE,1)

col_buttons = [r_b,g_b,b_b,p_b,y_b,c_b,s_b,w_b,
               r_o,g_o,b_o,p_o,y_o,c_o,s_o,w_o]

right_side = pygame.Rect((screen.get_size()[0]/2,0),(screen.get_size()[0]/2,screen.get_size()[1]))

# main loop
run = True
while run:

    clock.tick(30) # set maximum fps

    # check events since last iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
          
        # check key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            
        # check if one of the color buttons is clicked
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = event.pos
            for button in col_buttons:
                if button.rect.collidepoint(x,y):
                    if button.which == 0:
                        left_color = button.col
                    elif button.which == 1:
                        right_color = button.col
    
    screen.fill(left_color) # fill screen with color for left side
    pygame.draw.rect(screen,right_color,right_side) # plot rectangle with color on right halve of the screen

    # show col buttons with panel
    col_option_box = pygame.Rect((0,20),(70,270))
    pygame.draw.rect(screen, GRAY, col_option_box)
    screen.blit(font.render("L", False, WHITE), (12, 20))
    screen.blit(font.render("R", False, WHITE), (42, 20))
    for button in col_buttons:
        button.show(screen)
    
    # show display
    pygame.display.flip()

pygame.quit()