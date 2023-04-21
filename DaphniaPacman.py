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
        
# define class for rezising buttons        
class size_button:
    def __init__(self, pos, size, col, step):
        self.rect = pygame.Rect(pos,size)
        self.col = col
        self.step = step
    
    def show(self, surface):
        pygame.draw.rect(surface, self.col, self.rect)
        
    def click(self, size):
        size += self.step
        if size < 2:
            size = 2
        return size
    

pacman_radius = 20

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
background_color = BLACK
object_color = BLUE

# initialize pygame objects
pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Daphnia Treadmill")
font = pygame.font.SysFont('Arial', 24)
clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

# setup recording
recording = False
blink = 0

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

add_b = size_button((10,340),(20,20),DGRAY,2)
sub_b = size_button((40,340),(20,20),DGRAY,-2)

size_buttons = [add_b,sub_b]

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
            # recording
            if event.key == pygame.K_r:
                if recording:
                    print("End of recording")
                    print(record)
                    recording = False
                else:
                    print("Start recording")
                    record = []
                    recording = True
                    last = -1
                    start = datetime.now()
            
        # check if one of the color buttons is clicked
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = event.pos
            for button in col_buttons:
                if button.rect.collidepoint(x,y):
                    if button.which == 0:
                        background_color = button.col
                    elif button.which == 1:
                        object_color = button.col
            for button in size_buttons:
                if button.rect.collidepoint(x,y):
                    pacman_radius = button.click(pacman_radius)
                    print("Radius is now: " + str(pacman_radius))
                 
    # get position of mouse
    mouse_pos = pygame.mouse.get_pos()
    
    #log mouse position (one entry per second)
    if recording:
        curr = datetime.now()
        diff = curr - start
        if diff.seconds != last:
            last = diff.seconds
            record.append(mouse_pos)
    
    screen.fill(background_color) # fill screen with background color
    
    #recording blinker
    if recording:
        blink = (blink+1)%30
        if blink < 10:
            pygame.draw.circle(screen,GRAY,(15,10),8)
            pygame.draw.circle(screen,RED,(15,10),5)

    # show col buttons with panel
    col_option_box = pygame.Rect((0,20),(70,270))
    pygame.draw.rect(screen, GRAY, col_option_box)
    screen.blit(font.render("B", False, WHITE), (12, 20))
    screen.blit(font.render("O", False, WHITE), (42, 20))
    for button in col_buttons:
        button.show(screen)
        
    # show size buttons
    size_option_box = pygame.Rect((0,310),(70,60))
    pygame.draw.rect(screen, GRAY, size_option_box)
    screen.blit(font.render("+", False, WHITE), (14, 310))
    screen.blit(font.render("-", False, WHITE), (47, 310))
    for button in size_buttons:
        button.show(screen)
        
    #show pacman at mouse position 
    pygame.draw.circle(screen,object_color,mouse_pos,pacman_radius)

    # display controls
    screen.blit(font.render("R: Start/Stop recording",False, GRAY), (12, screen.get_size()[1]-30))
    
    # show display
    pygame.display.flip()

pygame.quit()