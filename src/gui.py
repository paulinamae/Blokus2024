import os
import sys
from typing import Any
from fakes import BlokusFake
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

import pygame
import pygame.gfxdraw
pygame.init()

Color = tuple[int, int, int]
sys_input: Any = sys.argv[1]
SCREEN_SIZE: int = 0
players: int = 0
start_positions: set[tuple[int, int]] = set()

if type(sys_input) is str:
    if sys_input == "duo":
        SCREEN_SIZE = 14
        players = 2
        start_positions.add((4, 4))
        start_positions.add((9,9))
    elif sys_input == "mono":
        SCREEN_SIZE = 11
        players = 1
        start_positions.add((5, 5))
    else:
        SCREEN_SIZE = int(sys.argv[1])
        players = 2
        start_positions.add((0,0))
        start_positions.add((SCREEN_SIZE, 0))
        start_positions.add((0, SCREEN_SIZE))
        start_positions.add((SCREEN_SIZE, SCREEN_SIZE))

SQUARE_SIZE: int = 36
SCREEN_COLOR: Color = (182, 240, 255)
SCREEN = pygame.display.set_mode((SCREEN_SIZE * SQUARE_SIZE, SCREEN_SIZE * SQUARE_SIZE))
SQUARE_COLOR: Color = (255, 255, 255)
START_POSITION_COLOR: Color = (175, 219, 193)
SCREEN.fill(SCREEN_COLOR)
pygame.display.set_caption("Blokus")

print(players)
board: BlokusFake = BlokusFake(players, SCREEN_SIZE, start_positions)

piece_colors: set[Color] = [(135, 81, 196), (156, 36, 54), (255, 255, 140)]
player_colors: dict[int, Color] = {}
for i in range(board.num_players):
    player_colors[i + 1] = piece_colors.pop(0)

shapes: dict[ShapeKind, Shape] = board.shapes

def draw_board():
    """
    draws the game grid based on given size with starting positions
    """
    for x in range(0, SCREEN_SIZE):
        for y in range(0, SCREEN_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE,  y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, SQUARE_COLOR, rect)
            pygame.gfxdraw.rectangle(SCREEN, rect, SCREEN_COLOR)

    for position in start_positions:
        x, y = position
        if x != 0 and y != 0:
            x = ((x - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
            y = ((y - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
        elif x == 0 and y != 0:
            x = (x * SQUARE_SIZE) + SQUARE_SIZE // 2
            y = ((y - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
        elif x != 0 and y ==0:
            x = ((x - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
            y = (y * SQUARE_SIZE) + SQUARE_SIZE // 2
        else:
            x = (x * SQUARE_SIZE) + SQUARE_SIZE // 2
            y = (y * SQUARE_SIZE) + SQUARE_SIZE // 2
        r = SQUARE_SIZE // 4
        pygame.gfxdraw.filled_circle(SCREEN, x, y, r, START_POSITION_COLOR)

def draw_pieces():
    for r in range(len(board._grid)):
        for c in range(len(board._grid)):
            if board._grid[r][c] is not None:
                player, kind = board._grid[r][c]
                piece_color = player_colors[player]
                piece_shape = shapes[kind]

                piece_rect = pygame.Rect(r * SQUARE_SIZE,  c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(SCREEN, piece_color, piece_rect)
        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            quit()
    
    draw_board()
    draw_pieces()
    pygame.display.update()