# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 20:47:53 2023

@author: brian
"""

import pygame
from PIL import Image, ImageDraw
from datetime import datetime

# define button class
class col_button:
    def __init__(self,pos,size,col,which):
        # pos: touple with top left coordinates
        # size: touple with width and height
        # what color does the button stand for (and also sets)
        # which color is set by it (background [0] or object [1])
        self.rect = pygame.Rect(pos,size)
        self.col = col
        self.which = which
    
    def show(self,surface):
        pygame.draw.rect(surface, self.col, self.rect)

# function to create pie_slice with pil and convert to pygame
def create_slice(circle_size, a_start, a_stop, object_color):
    # create pil
    pil_image = Image.new("RGBA", (circle_size, circle_size))
    pil_draw = ImageDraw.Draw(pil_image)
    pil_draw.pieslice((0, 0, circle_size-1, circle_size-1), int(a_start), int(a_stop), fill=object_color)
    
    # prepare conversion from pil to pygame
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    
    # return converted image
    return pygame.image.fromstring(data, size, mode)

# defining circles
circle_size = 430
ring_width = 110 # with ring_width < circle_size

# definde angles of pie slice
a_start = 0 # start angle at initialization
a_width = 30 # angular size of slice
a_stop = (a_start+a_width) % 360 # end angle at inilialization
a_speed = 2 # angular speed per frame

a_auto = 0 # initial automatic angular speed per frame

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

# initial colors used
background_color = BLACK
object_color = BLUE

# initialize pygame objects
pygame.init()
screen = pygame.display.set_mode((1200,800))
pygame.display.set_caption("Daphnia Threadmill")
font = pygame.font.SysFont('Arial', 24)
clock = pygame.time.Clock()

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
            if event.key == pygame.K_d:
                a_auto += 0.5
                print("Auto speed: "+str(a_auto))
            if event.key == pygame.K_a:
                a_auto -= 0.5
                print("Auto speed: "+str(a_auto))
            if event.key == pygame.K_s:
                a_auto = 0
                print("Auto speed set to zero")
            
        # check if one of the color buttons is clicked
        if event.type == pygame.MOUSEBUTTONDOWN :
            x, y = event.pos
            for button in col_buttons:
                if button.rect.collidepoint(x, y):
                    if button.which == 0:
                        background_color = button.col
                    elif button.which == 1:
                        object_color = button.col
                
    # automatic movement
    a_start = (a_start + a_auto) % 360
    a_stop = (a_stop + a_auto) % 360
    
    # get keypresses for manual movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        a_start = (a_start - a_speed) % 360
        a_stop = (a_stop - a_speed) % 360
    if keys[pygame.K_RIGHT]:
        a_start = (a_start + a_speed) % 360
        a_stop = (a_stop + a_speed) % 360              
    
    #log angle (one entry per second)
    if recording:
        curr = datetime.now()
        diff = curr - start
        if diff.seconds != last:
            last = diff.seconds
            record.append(a_start)
    
    screen.fill(background_color) # fill screen with background color
    
    # create and show pie slice
    pie_slice = create_slice(circle_size, a_start, a_stop, object_color)
    pie_slice_rect = pie_slice.get_rect(center=screen.get_rect().center)
    screen.blit(pie_slice, pie_slice_rect) # display at center of screen
    # paint over center of pie slice to create a ring slice
    pygame.draw.circle(screen,background_color,screen.get_rect().center,int((circle_size-ring_width)/2))
    
    #center finder
    pygame.draw.circle(screen,GRAY,screen.get_rect().center,10)
    
    #recording blinker
    if recording:
        blink = (blink+1)%30
        if blink < 10:
            pygame.draw.circle(screen,GRAY,(15,10),8)
            pygame.draw.circle(screen,RED,(15,10),5)

    # show buttons with panel
    pygame.draw.rect(screen, GRAY, pygame.Rect((0,20),(70,270)))
    screen.blit(font.render("B", False, WHITE), (12, 20))
    screen.blit(font.render("O", False, WHITE), (42, 20))
    for button in col_buttons:
        button.show(screen)

    # display controls
    screen.blit(font.render("R: Start/Stop recording",False, GRAY), (12, screen.get_size()[1]-100))
    screen.blit(font.render("Arrow Keys: manually rotate slice",False, GRAY), (12, screen.get_size()[1]-70))
    screen.blit(font.render("A,S,D: auto-rotate/stop slice",False, GRAY), (12, screen.get_size()[1]-40))
    
    # show display
    pygame.display.flip()

pygame.quit()