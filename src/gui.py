import os
import sys
import random
import click
from typing import Any
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from blokus import Blokus

import pygame
import pygame.gfxdraw
pygame.init()

Color = tuple[int, int, int]
SCREEN_SIZE: int = 0
SIDEBAR_SIZE: int = 0
PIECE_BANK_LENGTH: int = 0
SQUARE_SIZE: int = 36
FONT_SIZE: int = 0
FONT_SPACING: int = 0
players: int = 0
start_positions: set[tuple[int, int]] = set()

@click.command()
@click.option('--game')
@click.option('--num-players', '-n', default=2, type=int)
@click.option('--size', '-s', default=14, type=int)
@click.option('--start-position', '-p', multiple=True, nargs=2, type=(int, int))
def assign_specs(game, num_players, size, start_position) -> None:
    global SCREEN_SIZE, FONT_SIZE, players, start_positions
    if game == "duo":
        SCREEN_SIZE = 14
        FONT_SIZE = 20
        players = 2
        start_positions.add((3, 3))
        start_positions.add((8,8))
    elif game == "mono":
        SCREEN_SIZE = 11
        FONT_SIZE = 16
        players = 1
        start_positions.add((4, 4))
    elif game == "classic-2":
        SCREEN_SIZE = 20
        FONT_SIZE = 25
        players = 2
        start_positions.add((0, 0))
        start_positions.add((19, 19))
        start_positions.add((0, 19))
        start_positions.add((19, 0))
    elif game == "classic-3":
        SCREEN_SIZE = 20
        FONT_SIZE = 25
        players = 3
        start_positions.add((0, 0))
        start_positions.add((19, 19))
        start_positions.add((0, 19))
        start_positions.add((19, 0))
    elif game == "classic-4":
        SCREEN_SIZE = 20
        FONT_SIZE = 25
        players = 4
        start_positions.add((0, 0))
        start_positions.add((19, 19))
        start_positions.add((0, 19))
        start_positions.add((19, 0))
    else:
        print("here")
        SCREEN_SIZE = size
        players = num_players
        FONT_SIZE = int(SCREEN_SIZE * 1.4)
        for pos in start_position:
            x, y = pos
            start_positions.add((x - 1, y - 1))

    click.echo(f"Game: {game}")
    click.echo(f"Screen Size: {SCREEN_SIZE}")
    click.echo(f"Font Size: {FONT_SIZE}")
    click.echo(f"Number of Players: {players}")
    click.echo(f"Start Positions: {start_positions}")

if __name__ == '__main__':
    assign_specs.main(standalone_mode=False)

FONT_SPACING = FONT_SIZE // 10
SIDEBAR_SIZE = SQUARE_SIZE * players
PIECE_BANK_LENGTH = int((SCREEN_SIZE * SQUARE_SIZE) - (SQUARE_SIZE * 1.5))
SCREEN_COLOR: Color = (189, 255, 248)
SCREEN = pygame.display.set_mode(((SCREEN_SIZE * SQUARE_SIZE)  + SIDEBAR_SIZE, (SCREEN_SIZE * SQUARE_SIZE) + SIDEBAR_SIZE))
SQUARE_COLOR: Color = (255, 255, 255)
START_POSITION_COLOR: Color = (175, 219, 193)
SCREEN.fill(SCREEN_COLOR)
pieces_font = pygame.font.Font(None, size=FONT_SIZE)
player_font = pygame.font.Font(None, size=SQUARE_SIZE)
pygame.display.set_caption("Blokus")

board: Blokus = Blokus(players, SCREEN_SIZE, start_positions)

piece_colors: list[Color] = [(135, 81, 176), (156, 36, 54), (56, 177, 181)]
player_colors: dict[int, Color] = {}
for i in range(board.num_players):
    player_colors[i + 1] = piece_colors.pop(0)

def draw_piece_bank(selected_piece: Piece) -> None:
    blank_bank = pygame.Rect(SCREEN_SIZE * SQUARE_SIZE, 0, SIDEBAR_SIZE, PIECE_BANK_LENGTH)
    pygame.draw.rect(SCREEN, SCREEN_COLOR, blank_bank)
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

    print(board.curr_player)
    current_player: int = board.curr_player
    current_player_color: Color = player_colors[current_player]
    text = player_font.render(str(current_player), False, current_player_color)
    pygame.draw.circle(SCREEN, START_POSITION_COLOR, ((SIDEBAR_SIZE // 2) + (SCREEN_SIZE * SQUARE_SIZE), SQUARE_SIZE // 1.7), SQUARE_SIZE // 2)
    SCREEN.blit(text, (((SCREEN_SIZE * SQUARE_SIZE) + (SIDEBAR_SIZE // 2)) - (SQUARE_SIZE // 5), SQUARE_SIZE // 4))

def draw_score_bank() -> None:
    blank_bank = pygame.Rect(0, SCREEN_SIZE * SQUARE_SIZE, PIECE_BANK_LENGTH, SIDEBAR_SIZE)
    pygame.draw.rect(SCREEN, SCREEN_COLOR, blank_bank)
    for player in range(1, players + 1):
        player_color: Color = player_colors[player]
        player_score: int = board.get_score(player)
        score_text = player_font.render(f'Player {player}: {player_score}', False, player_color)
        if player in board.retired_players:
            status_text = player_font.render(f'RETIRED', False, (232, 7, 29))
        else:
            status_text = player_font.render(f'ACTIVE', False, (62, 181, 62))
        SCREEN.blit(score_text, (FONT_SPACING, (SCREEN_SIZE * SQUARE_SIZE) + ((player - 1) * SQUARE_SIZE) + FONT_SPACING))
        SCREEN.blit(status_text, ((((SCREEN_SIZE * SQUARE_SIZE) + SIDEBAR_SIZE) // 3) + (((SCREEN_SIZE * SQUARE_SIZE) + SIDEBAR_SIZE) // 4), (SCREEN_SIZE * SQUARE_SIZE) + ((player - 1) * SQUARE_SIZE) + FONT_SPACING))

def update_board(selected_piece: Piece) -> None:
    draw_piece_bank((selected_piece))
    draw_score_bank()

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

def game_loop() -> None:
    run: bool = True
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
                if event.key == pygame.K_1:
                    if ShapeKind.ONE in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.ONE, definitions[ShapeKind.ONE]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_2:
                    if ShapeKind.TWO in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.TWO, definitions[ShapeKind.TWO]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_3:
                    if ShapeKind.THREE in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.THREE, definitions[ShapeKind.THREE]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_4:
                    if ShapeKind.FOUR in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.FOUR, definitions[ShapeKind.FOUR]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_5:
                    if ShapeKind.FIVE in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.FIVE, definitions[ShapeKind.FIVE]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_7:
                    if ShapeKind.SEVEN in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.SEVEN, definitions[ShapeKind.SEVEN]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_a:
                    if ShapeKind.A in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.A, definitions[ShapeKind.A]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2)) 
                if event.key == pygame.K_c:
                    if ShapeKind.C in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.C, definitions[ShapeKind.C]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_f:
                    if ShapeKind.F in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.F, definitions[ShapeKind.F]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_s:
                    if ShapeKind.S in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.S, definitions[ShapeKind.S]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_l: 
                    if ShapeKind.L in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.L, definitions[ShapeKind.L]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_n: 
                    if ShapeKind.N in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.N, definitions[ShapeKind.N]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_o: 
                    if ShapeKind.LETTER_O in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.LETTER_O, definitions[ShapeKind.LETTER_O]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_p: 
                    if ShapeKind.P in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.P, definitions[ShapeKind.P]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_t: 
                    if ShapeKind.T in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.T, definitions[ShapeKind.T]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_u: 
                    if ShapeKind.U in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.U, definitions[ShapeKind.U]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2)) 
                if event.key == pygame.K_v: 
                    if ShapeKind.V in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.V, definitions[ShapeKind.V]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_w: 
                    if ShapeKind.W in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.W, definitions[ShapeKind.W]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                if event.key == pygame.K_x: 
                    if ShapeKind.X in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.X, definitions[ShapeKind.X]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2)) 
                if event.key == pygame.K_y: 
                    if ShapeKind.Y in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.Y, definitions[ShapeKind.Y]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2)) 
                if event.key == pygame.K_z: 
                    if ShapeKind.Z in board.remaining_shapes(current_player):
                        current_piece = Piece(Shape.from_string(ShapeKind.Z, definitions[ShapeKind.Z]))
                        current_piece.set_anchor((SCREEN_SIZE // 2, SCREEN_SIZE // 2))
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
                if event.key == pygame.K_r:
                    current_piece.rotate_right()
                if event.key == pygame.K_e:
                    current_piece.rotate_left()
                if event.key == pygame.K_SPACE:
                    current_piece.flip_horizontally()
                if event.key == pygame.K_q:
                    board.retire()
                if event.key == pygame.K_RETURN:
                    board.maybe_place(current_piece)
                    run = False
                    if not board.game_over:
                        break
        
        if board.game_over:
            run = False
            winners = board.winners
            if len(winners) > 1:
                winners_text = player_font.render(f'the winners are players {winners}!!', False, (0, 0, 0))
            else:
                winners_text = player_font.render(f'the winner is player {winners}!!', False, (0, 0, 0))
            SCREEN.blit(winners_text, (((SCREEN_SIZE * SQUARE_SIZE) + SIDEBAR_SIZE) // 2, (((SCREEN_SIZE * SQUARE_SIZE) + SIDEBAR_SIZE) // 2) - winners_text.get_width()))

        if board.curr_player > 0:
            update_board(current_piece)
            pygame.display.update()

    game_loop()

game_loop()