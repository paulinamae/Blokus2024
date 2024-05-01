import os
import sys
from fakes import BlokusStub
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

import pygame
import pygame.gfxdraw
pygame.init()

Color = tuple[int, int, int]

SCREEN_SIZE: int = int(sys.argv[1])
SQUARE_SIZE: int = 36
SCREEN_COLOR: Color = (182, 240, 255)
SCREEN = pygame.display.set_mode((SCREEN_SIZE * SQUARE_SIZE, SCREEN_SIZE * SQUARE_SIZE))
SQUARE_COLOR: Color = (255, 255, 255)
START_POSITION_COLOR: Color = (175, 219, 193)
SCREEN.fill(SCREEN_COLOR)
pygame.display.set_caption("Blokus")

start_positions: set[tuple[int, int]] = set()
start_positions.add((0,0))
start_positions.add((SCREEN_SIZE, SCREEN_SIZE))

board: BlokusStub = BlokusStub(2, SCREEN_SIZE, start_positions)
piece_colors: set[Color] = [(135, 81, 196), (156, 36, 54), (255, 255, 140)]
player_colors: dict[int, Color] = {}
for i in range(board.num_players):
    player_colors[i + 1] = piece_colors.pop(0)

shapes: dict[ShapeKind, Shape] = board._load_shapes()

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
        if position is not (0,0):
            x = ((x - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
            y = ((y - 1) * SQUARE_SIZE) + SQUARE_SIZE // 2
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