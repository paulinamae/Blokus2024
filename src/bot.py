import sys,random
from base import Cell, BlokusBase
from fakes import BlokusFake
from piece import Point, Piece, Shape

# Classes that represent players with different strategies

class Player:

    def __init__(self, bot_game: BlokusFake, player: int):
        self._bot_game = bot_game
        self._player = player

    @ property
    def retired(self) -> bool:
        """
        Check if player has retired from the game.
        """
        if self._player in self._bot_game._retired_players:
            return True
        return False
    
    def strategy(self, avail_moves: set[Piece])-> Piece:
        """
        Choose a piece to place based on a given strategy.
        """
        raise NotImplementedError

    def make_move(self) -> None:
        """
        Make a move using a piece that was determined by a specific strategy.
        """
        if not self.retired:
            avail_moves: set[Piece] = self._bot_game.available_moves()
            if avail_moves == set():
                self._bot_game.retire()
            else:
                move: Piece = self.strategy(avail_moves)
                self._bot_game.maybe_place(move)

class NBot(Player):

    def __init__(self, bot_game: BlokusFake, player: int):
        super().__init__(bot_game, player)

    def strategy(self, avail_moves: set[Piece]) -> Piece:
        rand: Piece = random.choice(list(avail_moves))
        #print("N:",rand.shape.kind)
        return rand
    

class SBot(Player):

    def __init__(self, bot_game: BlokusFake, player: int):
        super().__init__(bot_game, player)
    
    def strategy(self, avail_moves: set[Piece]) -> Piece:
        return self.biggest_piece(avail_moves)

    def biggest_piece(self, avail_moves: set[Piece]) -> Piece:
        """
        Find a piece with the largest size out of the available pieces.
        """

        shape_sizes: dict[int,Piece] = {}
        for piece in avail_moves:
            shape_sizes[len(piece.shape.squares)] = piece
        max_size: int = max(shape_sizes)
        #print("S:",shape_sizes[max_size].shape.kind)
        return shape_sizes[max_size]

# Simulate games

num_games: int = int(sys.argv[1])

one_wins: int = 0
two_wins: int = 0
ties: int = 0

for i in range(num_games):

    start_positions: set[Point] = set([(0,0),(10,10)])

    bot_game: BlokusFake = BlokusFake(2, 11, start_positions)

    bot1: NBot = NBot(bot_game, 1)
    bot2: SBot = SBot(bot_game,2)

    while not bot_game.game_over:
        #print("first:", bot_game._curr_player)
        bot2.make_move()
        #print("Bot 1:", bot_game._shapes_placed[1])
        #print("second:",bot_game._curr_player)
        bot1.make_move()
        #print("Bot 2:", bot_game._shapes_placed[2])
               
    print("N-bot:",bot_game.get_score(1))
    print("S-bot:",bot_game.get_score(2))
    if bot_game.winners is not None:
        if len(bot_game.winners) > 1:
            ties += 1
        elif bot_game.winners[0] == 1:
            one_wins += 1
        else:
            two_wins += 1

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
