import sys,random
from base import Cell, BlokusBase
from fakes import BlokusStub
from piece import Point, Piece

num_games: int = int(sys.argv[1])

zero_wins: int = 0
one_wins: int = 0
ties: int = 0

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

print(f"Bot 0 Wins |  {zero_wins/num_games*100:.2f} %")
print(f"Bot 1 Wins |  {one_wins/num_games*100:.2f} %")
print(f"Ties       |  {ties/num_games*100:.2f} %")
