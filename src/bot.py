import sys,random
from base import Cell, BlokusBase
from fakes import BlokusStub
from piece import Point, Piece, Shape

num_games: int = int(sys.argv[1])

# pass in either n_bot or s_bot as a parameter to make_move in order to keep 
# drawing pieces

def make_move(bot_game: BlokusStub, avail_moves: set[Piece], move: Piece) -> None:
    """
    Make a move using a piece that was determined by either the n_bot or s_bot
    strategy.
    """
    avail_moves.remove(move)
    bot_game.maybe_place(move)
    while not bot_game.maybe_place(move) and avail_moves != set():
        move: Piece = random.choice(list(avail_moves)) 
        avail_moves.remove(move)
        bot_game.maybe_place(move)

def n_bot(bot_game: BlokusStub) -> Piece:
    """
    Make a move using the "needs-improvement" bot strategy of selecting from all
    available moves.
    """
    if bot_game.available_moves() == set():
        bot_game.retire()
    avail_moves: set[Piece] = bot_game.available_moves()
    move: Piece = random.choice(list(avail_moves)) 
    avail_moves.remove(move)
    bot_game.maybe_place(move)
    while not bot_game.maybe_place(move) and avail_moves != set():
        move: Piece = random.choice(list(avail_moves)) 
        avail_moves.remove(move)
        bot_game.maybe_place(move)

def s_bot(bot_game: BlokusStub) -> None:
    """
    Make a move using the "satisfactory" bot strategy of selecting from all
    available moves.
    """
    if bot_game.available_moves() == set():
        bot_game.retire()
    avail_moves: set[Piece] = bot_game.available_moves()
    move: Piece = random.choice(list(avail_moves)) 
    avail_moves.remove(move)
    bot_game.maybe_place(move)
    while not bot_game.maybe_place(move) and avail_moves != set():
        move: Piece = random.choice(list(avail_moves)) 
        avail_moves.remove(move)
        bot_game.maybe_place(move)

def calc_shape_sizes(bot_game: BlokusStub) -> dict[int,Shape]:
    """
    Create a dictionary where the key is the size of the shape (in squares) and
    the value is the Shape that it corresponds to.
    Inputs:
        bot_game[BlokusStub]
    Returns [dict[int,Shape]]
    """

    shape_sizes: dict[int,Shape] = {}
    for _, shape in bot_game.shapes.items():
        shape_sizes[len(shape.squares)] = shape
    return shape_sizes


for i in range(num_games):

    one_wins: int = 0
    two_wins: int = 0
    ties: int = 0

    bot_game: BlokusStub = BlokusStub(2, 11, set())


        
    win_square: Cell = bot_game.grid[0][13]
    if win_square is not None:
        player,shape = win_square
        if player == 1:
            one_wins += 1
        else:
            two_wins += 1
    else:
        ties += 1

print(f"Bot 1 Wins |  {one_wins/num_games*100:.2f} %")
print(f"Bot 2 Wins |  {two_wins/num_games*100:.2f} %")
print(f"Ties       |  {ties/num_games*100:.2f} %")

"""
# MILESTONE 1 IMPLEMENTATION OF BOT.PY

for i in range(num_games):

    bot_game: BlokusStub = BlokusStub(2, 14, set())

    while not bot_game.game_over:
        bot1_move: Point = (random.randint(0,13),random.randint(0,13))
        bot2_move: Point = (random.randint(0,13),random.randint(0,13))
        if bot_game.available_moves() == set():
            bot_game.retire()
        for piece in bot_game.available_moves():
            check_anchor: Point|None = piece.anchor
            if bot1_move == check_anchor:
                bot_game.maybe_place(piece)
            if bot2_move == check_anchor:
                bot_game.maybe_place(piece)
    
    win_square: Cell = bot_game.grid[0][13]
    if win_square is not None:
        player,shape = win_square
        if player == 1:
            zero_wins += 1
        else:
            one_wins += 1
    else:
        ties += 1
"""
