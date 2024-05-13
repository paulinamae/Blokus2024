import sys,random
from piece import Point, Piece, Shape, ShapeKind
from blokus import Blokus
import click

# Classes that represent players with different strategies

class Player:

    """
    A class that represents a Blokus player using either the N (needs improvement),
    S (satisfactory), or U (unsatisfactory) strategy.
    """

    _bot_gme: Blokus
    _player: int

    def __init__(self, bot_game: Blokus, player: int):
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
            avail_moves: set[Piece] = self._bot_game.fake_available_moves()
            if avail_moves == set():
                self._bot_game.retire()
            else:
                move: Piece = self.strategy(avail_moves)
                self._bot_game.maybe_place(move)

class NBot(Player):

    """
    A Blokus player that uses a "needs improvement" strategy by randomly selecting
    pieces to play.
    """

    def __init__(self, bot_game: Blokus, player: int):
        super().__init__(bot_game, player)

    def strategy(self, avail_moves: set[Piece]) -> Piece:
        rand: Piece = random.choice(list(avail_moves))
        return rand
    
    def make_move(self) -> None:
        super().make_move()
    

class SBot(Player):
    """
    A Blokus player that uses a "satisfactory" strategy by playing the largest
    piece possible.
    """

    def __init__(self, bot_game: Blokus, player: int):
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
        return shape_sizes[max_size]
    
    def make_move(self) -> None:
        super().make_move()

class UBot(Player):

    """
    A Blokus player that uses an "unsatisfactory" strategy by playing the smallest
    piece possible.
    """

    def __init__(self, bot_game: Blokus, player: int):
        super().__init__(bot_game, player)
    
    def strategy(self, avail_moves: set[Piece]) -> Piece:
        return self.smallest_piece(avail_moves)

    def smallest_piece(self, avail_moves: set[Piece]) -> Piece:
        """
        Find a piece with the smallest size out of the available pieces.
        """

        shape_sizes: dict[int,Piece] = {}
        for piece in avail_moves:
            shape_sizes[len(piece.shape.squares)] = piece
        min_size: int = min(shape_sizes)
        return shape_sizes[min_size]
    
    def make_move(self) -> None:
        super().make_move()

# Set up command line interface

@click.command()
@click.option("-n","--num-games",
              type=int,
              default=20)
@click.option("-1", "--player1",
              type=click.Choice(["S", "N", "U"]),
              default="N")
@click.option("-2", "--player2",
              type=click.Choice(["S", "N", "U"]),
              required=True)
def cmd(num_games: int, player1: str, player2: str) -> None:

    # Simulate games

    one_wins: int = 0
    two_wins: int = 0
    ties: int = 0

    for i in range(num_games):

        start_positions: set[Point] = set([(0,0),(10,10)])

        bot_game: Blokus = Blokus(2, 11, start_positions)

        if player1 == "S":
            bot1: SBot = SBot(bot_game, 1)
        elif player1 == "N":
            bot1: NBot = NBot(bot_game, 1)
        else:
            bot1: UBot = UBot(bot_game, 1)

        if player2 == "S":
            bot2: SBot = SBot(bot_game, 2)
        elif player2 == "N":
            bot2: NBot = NBot(bot_game, 2)
        else:
            bot2: UBot = UBot(bot_game, 2) 

        while not bot_game.game_over:
            bot1.make_move()
            bot2.make_move()
                
        if bot_game.winners is not None:
            if len(bot_game.winners) > 1:
                ties += 1
            elif bot_game.winners[0] == 1:
                one_wins += 1
            else:
                two_wins += 1

    print(f"Bot 1 ({player1}) Wins |  {one_wins/num_games*100:.2f} %")
    print(f"Bot 2 ({player2}) Wins |  {two_wins/num_games*100:.2f} %")
    print(f"Ties       |  {ties/num_games*100:.2f} %")

if __name__ == "__main__":
    cmd()


