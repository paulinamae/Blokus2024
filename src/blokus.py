from typing import Optional
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid

import shape_definitions
import piece

class Blokus(BlokusBase):
    """
    Blokus class for Blokus game logic.
    """

    _num_players: int
    _size: int
    _start_positions: set[Point]
    _shapes_placed: dict[int, set[ShapeKind]]
    _retired_players: set[int]
    _shapes_left: dict[int,set[ShapeKind]]
    _grid: Grid
    _curr_player: int
    _num_moves: int
    _last_moves: dict[int, ShapeKind|None]

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Arguments:

            num_players: Number of players
            size: Number of squares on each side of the board
            start_positions: Positions for players' first moves

        Raises ValueError...
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players.
        """

        super().__init__(num_players,size,start_positions)
        if self._num_players not in range(1,5):
            raise ValueError("Must have one or two players.")
        if self._size < 5:
            raise ValueError("Size must be greater than 5.")
        for position in self._start_positions:
            if not self.valid_coordinate(position):
                raise ValueError("Choose valid start position.")
        if len(self._start_positions) < self._num_players:
            raise ValueError("Not enough start positions.")  

        self._shapes_placed = {}
        for i in range(self._num_players):
            self._shapes_placed[i+1] = set()
            
        self._retired_players = set()
        self._grid = [[None] * size for _ in range(size)]

        self._curr_player = 1

        self._num_moves = 0

        self._shapes_left = {}
        self._last_moves = {}
        for player in range(1, self._num_players + 1):
            self._shapes_left[player] = set(self.shapes.keys())
            self._last_moves[player] = None

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all 21 Blokus shapes, as named and defined by
        the string representations in shape_definitions.py.

        The squares and origin, if any, of each shape should
        correspond to the locations and orientations defined
        in shape_definitions. For example, the five-square
        straight piece is called ShapeKind.FIVE, defined as a
        vertical line (as opposed to horizontal), and has its
        origin at the middle (third) square.

        See shape_definitions.py for more details.
        """
        shapes = {}
        for kind, string in shape_definitions.definitions.items():
            working_shape = Shape.from_string(kind, string)
            shapes[kind] = working_shape
        return shapes

    @property
    def size(self) -> int:
        """
        Returns the board size (the number of squares per side).
        """
        return self._size
    
    @property
    def start_positions(self) -> set[Point]:
        """
        Returns the start positions.
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        Returns the number of players. Players are numbered
        consecutively, starting from 1.
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "Whose turn is it?"). While the
        game is ongoing, this property never refers to a player
        that has played all of their pieces or that retired
        before playing all of their pieces. If the game is over,
        this property will not return a meaningful value.
        """
        if self.game_over:
            return 0
        
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        Returns the set of players who have retired. These
        players do not get any more turns; they are skipped
        over during subsequent gameplay.
        """
        return self._retired_players

    @property
    def grid(self) -> Grid:
        """
        Returns the current state of the board (i.e. Grid).
        There are two values tracked for each square (i.e. Cell)
        in the grid: the player number (an int) who has played
        a piece that occupies this square; and the shape kind
        of that piece. If no played piece occupies this square,
        then the Cell is None.
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        Returns whether or not the game is over. A game is over
        when every player is either retired or has played all
        their pieces.
        """
        leftovers = set()
        players_done: list[int] = []
        players_done += list(self._retired_players)

        for i in range(1,self.num_players+1):
            if i not in self._retired_players:
                leftovers.add(i)
            
        for leftover in leftovers:
            if self._shapes_left[leftover]:
                return False
            else:
                players_done.append(leftover)
        if len(players_done) == self.num_players:
            return True
        
        return False

    @property
    def winners(self) -> Optional[list[int]]:
        """
        Returns the (one or more) players who have the highest
        score. Returns None if the game is not over.
        """
        win: list[int] = []
        for player in range(1, self.num_players + 1):
            check_score = self.get_score(player)
            if win == []:
                win.append(player)
            elif check_score > self.get_score(win[0]):
                win.pop(0)
                win.append(player)
            elif check_score == self.get_score(win[0]):
                win.append(player)
        return win
    #
    # METHODS
    #
    def valid_coordinate(self, coord):
        """
        Check if a coordinate is on the board. Return True if so and False otherwise.
        Inputs:
            coord [tuple[int,int]]: coordinate that is being checked
        Returns [bool]
        """
        x,y = coord
        return (0 <= x <= self._size and 0 <= y <= self._size)  
    
    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns a list of shape kinds that a particular
        player has not yet played.
        """
        return list(self._shapes_left[player])

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall. For the purposes of this
        predicate, a "wall collision" occurs when at
        least one square of the piece would be located
        beyond the bounds of the (size x size) board.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        piece_shape: Shape = piece.shape
        if piece_shape in self._shapes_placed[self.curr_player]:
            raise ValueError("Piece already placed")

        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None.")

        for coord in piece.squares():
            x, y = coord
            if x < 0 or y < 0 or x >= self._size or y >= self._size:
                return True
        
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall or with any played pieces.
        A "collision" between pieces occurs when they
        overlap.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        piece_shape: Shape = piece.shape
        if piece_shape in self._shapes_placed[self.curr_player]:
            raise ValueError("Piece already placed")

        if piece.anchor is None:
            raise ValueError("Anchor of the piece is None") 

        if self.any_wall_collisions(piece):
            return True
        
        for r, c in piece.squares():
            if self._grid[r][c] is not None:
                return True
        
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        If the current player has not already played
        this shape, this method returns a boolean
        indicating whether or not the given piece is
        legal to place. This requires that:

         - if the player has not yet played any pieces,
           this piece would cover a start position;
         - the piece would not collide with a wall or any
           previously played pieces; and
         - the piece shares one or more corners but no edges
           with the player's previously played pieces.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        
        if piece.shape.kind in self._shapes_placed[self.curr_player]:
            raise ValueError("Piece already placed")

        if piece.anchor is None:
            raise ValueError("Anchor is None.")
        
        if self.any_collisions(piece):
            return False
        
        if self._shapes_placed[self._curr_player] == set(): # checks start pos
            in_start: bool = False
            for square in piece.squares():
                if square in self.start_positions:
                    return True
            if not in_start:
                return False        

        piece_cardinals: set[Point] = piece.cardinal_neighbors(self.size)
        piece_intercardinals: set[Point] = piece.intercardinal_neighbors(self.size)

        # piece can't have adjacent edge with piece already played by current player
        for point in piece_cardinals: 
            r, c = point
            if self._grid[r][c]:
                if self._grid[r][c]:
                    if self._grid[r][c][0] == self.curr_player:
                        return False
        
        # piece has to share corner with previously placed piece
        for point in piece_intercardinals: 
            r, c = point
            if self._grid[r][c]:
                if self._grid[r][c][0] == self.curr_player:
                    return True
    
        return False

    def maybe_place(self, piece: Piece) -> bool:
        """
        If the piece is legal to place, this method
        places the piece on the board, updates the
        current player and other relevant game state,
        and returns True.

        If not, this method leaves the board and current
        game state unmodified, and returns False.

        Note that the game does not necessarily end right
        away when a player places their last piece; players
        who have not retired and have remaining pieces
        should still get their turns.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        
        if piece.shape.kind in self._shapes_placed[self.curr_player]:
            raise ValueError("Piece already placed")

        if piece.anchor is None:
            raise ValueError("Anchor is None.")

        if not self.legal_to_place(piece):
            return False
        
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        
        # Update current player status and board
        self._num_moves += 1
        self._shapes_placed[self.curr_player].add(piece.shape.kind)
        self._last_moves[self.curr_player] = piece.shape.kind
        self._shapes_left[self.curr_player].remove(piece.shape.kind)

        # Move to next player
        if ((self._curr_player % self.num_players) + 1) not in self._retired_players:
            self._curr_player = (self._curr_player % self.num_players) + 1
        
        return True

    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        self._retired_players.add(self.curr_player)
        
        if self._num_players - len(self.retired_players) > 0:
            self._curr_player = (self.curr_player % self.num_players) + 1

    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        score: int = 0
        for shape in self._shapes_left[player]:
            str = shape_definitions.definitions[shape]
            working_shape = Shape.from_string(shape, str)
            score -= len(working_shape.squares)
        
        if not self._shapes_left[player]:
            score += 15
            if self._last_moves[player] == ShapeKind.ONE:
                score += 5

        return score

    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Notice there may be many different Pieces corresponding
        to a single Shape that are considered available moves
        (because they may differ in location and orientation).
        """
        
        avail_moves: set[Piece] = set()
 
        for shapekind in self._shapes_left[self._curr_player]:
            for x in range(self._size):
                for y in range(self._size):
                    one = Piece(self.shapes[shapekind])
                    one.set_anchor((y, x))
                    if self.legal_to_place(one):
                        avail_moves.add(one)

                    if self.shapes[shapekind].can_be_transformed: # does transforming change the squares?
                        two = Piece(self.shapes[shapekind])
                        two.set_anchor((y, x))
                        two.flip_horizontally()
                        two1 = Piece(self.shapes[shapekind])
                        two1.set_anchor((y, x))
                        if set(two.squares()) != set(two1.squares()): # does flipping horizontally change the squares?
                            if self.legal_to_place(two):
                                avail_moves.add(two)

                        three = Piece(self.shapes[shapekind])
                        three.set_anchor((y, x))
                        three.rotate_right()
                        three1 = Piece(self.shapes[shapekind])
                        three1.set_anchor((y, x))
                        if set(three.squares()) != set(three1.squares()): # does rotating right change the squares?
                            if self.legal_to_place(three):
                                avail_moves.add(three)

                        four = Piece(self.shapes[shapekind])
                        four.set_anchor((y, x))
                        four.rotate_left()
                        four1 = Piece(self.shapes[shapekind])
                        four1.set_anchor((y, x))
                        if set(four.squares()) != set(four1.squares()): # does rotating left change the squares?
                            if self.legal_to_place(four):
                                avail_moves.add(four)
        return avail_moves
    
    def fake_available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Does not consider any horizontal flips, left rotations, or right rotations.
        This method is used in bot.py to ensure a faster runtime.
        """

        empty_squares: set[tuple[int,int]] = set()
        i: int = -1
        for row in self.grid:
            i += 1
            for j in range(len(row)):
                if self.grid[i][j] == None:
                    empty_squares.add((i,j))

        avail_moves: set[Piece] = set()
 
        for shapekind in self._shapes_left[self._curr_player]:
            for empty_square in empty_squares:
                maybe_piece: Piece = Piece(self.shapes[shapekind])
                maybe_piece.set_anchor(empty_square)
                if self.legal_to_place(maybe_piece) and piece not in avail_moves:
                    avail_moves.add(maybe_piece)

        return avail_moves
