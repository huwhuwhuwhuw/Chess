#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 12:55:25 2025

@author: huwtebbutt
"""
import pygame
from Make_Move import Make_Move
from Board import Board

def Transform_Coords(x,y=None):
    #Transform from pygame coords to board coords
    if (type(x)==list or type(x)==tuple) and y==None:
        y=x[1]
        x=x[0]
    return y,17-x
    

def render_board(Board, screen, Highlight=[None,None], square_size=80):
    import numpy as np
    """
    Renders a chess board to the given Pygame screen.
    
    Parameters:
    - board: 2D array (e.g., 8x8) containing piece objects or None
    - screen: Pygame display surface
    - square_size: size of each square in pixels
    """
    colors = [(240, 217, 181), (181, 136, 99),(135, 206, 235)]  # light and dark squares
    new_Board=np.flipud(Board.Board.T)
    for i,row in enumerate(new_Board):
        for j,square in enumerate(row):
            # Draw square
            if (i,j) in Highlight:
                color=colors[-1]
            else:
                color = colors[(i + j) % 2]
            pygame.draw.rect(screen, color, (j * square_size, i * square_size, square_size, square_size))

            # Draw piece if present
            if square!='Empty':
                font = pygame.font.SysFont(None, square_size)
                text = font.render(square.display(), True, (0, 0, 0))
                screen.blit(text, (j * square_size + square_size//4, i * square_size + square_size//4))

def get_square_from_click(pos,SQUARE_SIZE):
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return row, col


#Initialise board
Board=Board()



# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Constants
WIDTH, HEIGHT = 640, 640
ROWS, COLS = Board.X_Size, Board.Y_Size
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Chess Game")

# Main loop
running = True
Coords=[]
Relative_x=0
Relative_y=0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x, y = get_square_from_click(pos,SQUARE_SIZE)
            if x>=0 and x<=17 and y>=0 and y<=17:
                if Coords and Coords[-1]==(x,y):
                    Coords=[]
                else:
                    Coords.append((x,y))
        elif event.type == pygame.KEYDOWN and len(Coords)==1:
            if event.key == pygame.K_LEFT:
                Relative_y-=1
            elif event.key == pygame.K_RIGHT:
                Relative_y+=1
            elif event.key == pygame.K_UP:
                Relative_x-=1
            elif event.key == pygame.K_DOWN:
                Relative_x+=1
            elif event.key == pygame.K_RETURN:
                Coords.append((Coords[0][0]+Relative_x,Coords[0][1]+Relative_y))
    if len(Coords)==0:
        Relative_x=0
        Relative_y=0
        render_board(Board,screen,square_size=SQUARE_SIZE)
    elif len(Coords)==1:
        Highlight=[]
        Highlight.append(Coords[0])
        Highlight.append((Coords[0][0]+Relative_x,Coords[0][1]+Relative_y))
        render_board(Board,screen,Highlight=Highlight,square_size=SQUARE_SIZE)
    elif len(Coords)==2:
        Relative_x=0
        Relative_y=0
        Piece_Coords=Transform_Coords(Coords[0])
        Target_Coords=Transform_Coords(Coords[1])
        Make_Move(Board,Piece_Coords,Target_Coords)
        render_board(Board,screen,square_size=SQUARE_SIZE)
        Coords=[]
    pygame.display.flip()
    clock.tick(5)

pygame.quit()

