import os
import sys
import random
from typing import Any
from fakes import BlokusFake
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

import pygame
import pygame.gfxdraw
pygame.init()

Color = tuple[int, int, int]
sys_input: Any = sys.argv[1]
SCREEN_SIZE: int = 0
SIDEBAR_SIZE: int = 0
PIECE_BANK_LENGTH: int = 0
SQUARE_SIZE: int = 36
FONT_SIZE: int = 0
FONT_SPACING: int = 0
players: int = 0
start_positions: set[tuple[int, int, int]] = set()

if type(sys_input) is str:
    if sys_input == "duo":
        SCREEN_SIZE = 14
        FONT_SIZE = 20
        players = 2
        start_positions.add((4, 4))
        start_positions.add((9,9))
    elif sys_input == "mono":
        SCREEN_SIZE = 11
        FONT_SIZE = 16
        players = 1
        start_positions.add((5, 5))
    else:
        SCREEN_SIZE = int(sys.argv[1])
        players = 2
        FONT_SIZE = int(SCREEN_SIZE * 1.3)
        start_positions.add((0,0))
        start_positions.add((SCREEN_SIZE - 1, 0))
        start_positions.add((0, SCREEN_SIZE - 1))
        start_positions.add((SCREEN_SIZE - 1, SCREEN_SIZE - 1))

FONT_SPACING = FONT_SIZE // 10
SIDEBAR_SIZE = SQUARE_SIZE * players
PIECE_BANK_LENGTH = int((SCREEN_SIZE * SQUARE_SIZE) - (SQUARE_SIZE * 1.5))
SCREEN_COLOR: Color = (189, 255, 248)
SCREEN = pygame.display.set_mode(((SCREEN_SIZE * SQUARE_SIZE)  + SIDEBAR_SIZE, SCREEN_SIZE * SQUARE_SIZE))
SQUARE_COLOR: Color = (255, 255, 255)
START_POSITION_COLOR: Color = (175, 219, 193)
SCREEN.fill(SCREEN_COLOR)
pieces_font = pygame.font.Font(None, size=FONT_SIZE)
player_font = pygame.font.Font(None, size=SQUARE_SIZE)
pygame.display.set_caption("Blokus")

board: BlokusFake = BlokusFake(players, SCREEN_SIZE, start_positions)

piece_colors: set[Color] = [(135, 81, 176), (156, 36, 54), (56, 177, 181)]
player_colors: dict[int, Color] = {}
for i in range(board.num_players):
    player_colors[i + 1] = piece_colors.pop(0)

def draw_piece_bank(selected_piece: Piece):
    for player in range(1, players + 1):
        pieces_left: list[ShapeKind] = board.remaining_shapes(player)

        text_x_coord: float = (SCREEN_SIZE * SQUARE_SIZE) + ((player - 1) * SQUARE_SIZE) + (SQUARE_SIZE // 2.5)
        text_y_coord: float = SQUARE_SIZE 
        player_color: Color = player_colors[player]

        y_counter: int = 0
        for shape in board.shapes:
            shape_string = shape.value
            text_y_coord = (SQUARE_SIZE * 1.3) + (y_counter * FONT_SPACING) + (y_counter * FONT_SIZE)
            if shape == selected_piece.shape.kind and player == board.curr_player:
                text = pieces_font.render(shape_string, False, (255, 252, 102))
            elif shape in pieces_left:
                text = pieces_font.render(shape_string, False, player_color)
            else:
                text = pieces_font.render(shape_string, False, (255,255,255))
            SCREEN.blit(text, (text_x_coord, text_y_coord))
            y_counter += 1

    current_player: int = board.curr_player
    current_player_color: Color = player_colors[current_player]
    text = player_font.render(str(current_player), False, current_player_color)
    pygame.draw.circle(SCREEN, START_POSITION_COLOR, ((SIDEBAR_SIZE // 2) + (SCREEN_SIZE * SQUARE_SIZE), SQUARE_SIZE // 1.7), SQUARE_SIZE // 2)
    SCREEN.blit(text, (((SCREEN_SIZE * SQUARE_SIZE) + (SIDEBAR_SIZE // 2)) - (SQUARE_SIZE // 5), SQUARE_SIZE // 4))

def update_board(selected_piece: Piece):
    draw_piece_bank((selected_piece))

    #draws the base squares  / start positions
    for x in range(0, SCREEN_SIZE):
        for y in range(0, SCREEN_SIZE):
            rect = pygame.Rect(x * SQUARE_SIZE,  y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(SCREEN, SQUARE_COLOR, rect)
            pygame.gfxdraw.rectangle(SCREEN, rect, SCREEN_COLOR)
    
    for position in start_positions:
        x, y = position
        x = (x * SQUARE_SIZE) + SQUARE_SIZE // 2
        y = (y * SQUARE_SIZE) + SQUARE_SIZE // 2
        r = SQUARE_SIZE // 4
        pygame.gfxdraw.filled_circle(SCREEN, x, y, r, START_POSITION_COLOR)
    
    #updates the already placed pieces
    for r in range(len(board._grid)):
        for c in range(len(board._grid)):
            if board._grid[r][c] is not None:
                player, kind = board._grid[r][c]
                piece_color = player_colors[player]
                piece_rect = pygame.Rect(r * SQUARE_SIZE,  c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(SCREEN, piece_color, piece_rect)

    #manages the selected piece
    selected_piece_coords = selected_piece.squares()
    r, g, b = player_colors[board.curr_player]
    selected_piece_color = (r + 70, g + 70, b + 70)

    #draws selected piece
    for r, c in selected_piece_coords:
        piece_rect = pygame.Rect(r * SQUARE_SIZE,  c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(SCREEN, selected_piece_color, piece_rect)
    
    #updates surrounding cells
    for r in range(0, SCREEN_SIZE):
        for c in range(0, SCREEN_SIZE):
            if (r, c) not in selected_piece_coords and (r, c) not in start_positions and board._grid[r][c] is None:
                rect = pygame.Rect(r * SQUARE_SIZE,  c * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(SCREEN, SQUARE_COLOR, rect)
                pygame.gfxdraw.rectangle(SCREEN, rect, SCREEN_COLOR)

def game_loop():
    run = True
    current_player = board.curr_player
    pieces_left: list[ShapeKind] = board.remaining_shapes(current_player)
    random_shapekind: ShapeKind = random.choice(pieces_left)
    current_piece: Piece = Piece(Shape.from_string(random_shapekind, definitions[random_shapekind]))
    current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    x, y = current_piece.anchor
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                if event.key == pygame.K_UP:
                    current_piece.set_anchor((x, y - 1))
                    if not board.any_wall_collisions(current_piece):
                        x, y = current_piece.anchor
                    else:
                        current_piece.set_anchor((x, y))
                        x, y = current_piece.anchor
                if event.key == pygame.K_DOWN:
                    current_piece.set_anchor((x, y + 1))
                    if not board.any_wall_collisions(current_piece):
                       x, y = current_piece.anchor
                    else:
                        current_piece.set_anchor((x, y))
                        x, y = current_piece.anchor
                if event.key == pygame.K_LEFT:
                    current_piece.set_anchor((x - 1, y))
                    if not board.any_wall_collisions(current_piece):
                        x, y = current_piece.anchor
                    else:
                        current_piece.set_anchor((x, y))
                        x, y = current_piece.anchor
                if event.key == pygame.K_RIGHT:
                    current_piece.set_anchor((x + 1, y))
                    if not board.any_wall_collisions(current_piece):
                        x, y = current_piece.anchor
                    else:
                        current_piece.set_anchor((x, y))
                        x, y = current_piece.anchor
                if event.key == pygame.K_RETURN:
                    board.maybe_place(current_piece)
                    run = False
                    break
        update_board(current_piece)
        pygame.display.update()

    game_loop()

game_loop()