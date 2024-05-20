import pytest
from typing import Optional

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from blokus import Blokus
from fakes import BlokusFake

def test_inheritance() -> None:
    """Test that Blokus inherits from BlokusBase"""
    assert issubclass(
        Blokus, BlokusBase
    ), "Blokus should inherit from BlokusBase"

def test_init_blokus_mini_1() -> None:
    """Tests that the size, start_positions, num_players, 
    curr_player, and grid properties have been initialized 
    correctly for a 1-player Blokus Mini game configuration"""
    blokus_mini = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    assert blokus_mini.num_players == 1
    assert blokus_mini.size == 5
    assert blokus_mini.curr_player == 1
    assert blokus_mini.start_positions == {(0,0), (0, 4), (4,0), (4, 4), (2, 2)}
    assert blokus_mini.grid == [[None] * blokus_mini.size for _ in range(blokus_mini.size)]
    assert not blokus_mini.game_over

def test_init_blokus_mini_2() -> None:
    """Tests that the size, start_positions, num_players, 
    curr_player, and grid properties have been initialized 
    correctly for a 2-player Blokus Mini game configuration"""
    blokus_mini = Blokus(2, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    assert blokus_mini.num_players == 2
    assert blokus_mini.size == 5
    assert blokus_mini.curr_player == 1
    assert blokus_mini.start_positions == {(0,0), (0, 4), (4,0), (4, 4), (2, 2)}
    assert blokus_mini.grid == [[None] * blokus_mini.size for _ in range(blokus_mini.size)]
    assert not blokus_mini.game_over

def test_init_blokus_mono() -> None:
    """Tests that the size, start_positions, num_players, 
    curr_player, and grid properties have been initialized 
    correctly for a Blokus Mono game configuration"""
    blokus_mono = Blokus(1, 11, {(5, 5)})

    assert blokus_mono.num_players == 1
    assert blokus_mono.size == 11
    assert blokus_mono.curr_player == 1
    assert blokus_mono.start_positions == {(5, 5)}
    assert blokus_mono.grid == [[None] * blokus_mono.size for _ in range(blokus_mono.size)]
    assert not blokus_mono.game_over

def test_init_blokus_duo_2() -> None:
    """Tests that the size, start_positions, num_players, 
    curr_player, and grid properties have been initialized 
    correctly for a Blokus Duo game configuration"""
    blokus_duo = Blokus(2, 14, {(4, 4), (9, 9)})

    assert blokus_duo.num_players == 2
    assert blokus_duo.size == 14
    assert blokus_duo.curr_player == 1
    assert blokus_duo.start_positions == {(4, 4), (9, 9)}
    assert blokus_duo.grid == [[None] * blokus_duo.size for _ in range(blokus_duo.size)]
    assert not blokus_duo.game_over

def test_shapes_loaded() -> None:
    """Tests that the shapes dictionary has been correctly initialized 
    with all 21 Blokus shapes"""
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    shape = bk.shapes[ShapeKind.ONE]
    assert shape.kind == ShapeKind.ONE
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0)]

    shape = bk.shapes[ShapeKind.TWO]
    assert shape.kind == ShapeKind.TWO
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1)}

    shape = bk.shapes[ShapeKind.THREE]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1), (0, -1)}

    shape = bk.shapes[ShapeKind.C]
    assert shape.kind == ShapeKind.C
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1), (1, 0)}

    shape = bk.shapes[ShapeKind.FOUR]
    assert shape.kind == ShapeKind.FOUR
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1), (0, -1), (0, 2)}

    shape = bk.shapes[ShapeKind.SEVEN]
    assert shape.kind == ShapeKind.SEVEN
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(-1, -1), (-1, 0), (0, 0), (1, 0)}

    shape = bk.shapes[ShapeKind.S]
    assert shape.kind == ShapeKind.S
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1), (1, -1), (1, 0)}

    shape = bk.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, 1), (1, 0), (1, 1)}

    shape = bk.shapes[ShapeKind.A]
    assert shape.kind == ShapeKind.A
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 0), (0, -1), (0, 1)}

    shape = bk.shapes[ShapeKind.F]
    assert shape.kind == ShapeKind.F
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, -1), (-1, 0), (-1, 1), (1, 0)}

    shape = bk.shapes[ShapeKind.FIVE]
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0)}

    shape = bk.shapes[ShapeKind.L]
    assert shape.kind == ShapeKind.L
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 0), (-2, 0), (1, 0), (1, 1)}
    {(0, 0), (0, 1), (0, 2), (0, -1), (1, -1)}

    shape = bk.shapes[ShapeKind.N]
    assert shape.kind == ShapeKind.N
    assert shape.origin == (1, 0)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 1), (0, 1), (1, 0), (2, 0)}

    shape = bk.shapes[ShapeKind.P]
    assert shape.kind == ShapeKind.P
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, -1), (-1, -1), (-1, 0), (1, -1)}

    shape = bk.shapes[ShapeKind.T]
    assert shape.kind == ShapeKind.T
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)}

    shape = bk.shapes[ShapeKind.U]
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, -1), (-1, 1), (0, -1), (0, 1)}

    shape = bk.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)}

    shape = bk.shapes[ShapeKind.W]
    assert shape.kind == ShapeKind.W
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 1), (0, 1), (1, -1), (1, 0)}

    shape = bk.shapes[ShapeKind.X]
    assert shape.kind == ShapeKind.X
    assert shape.origin == (1, 1)
    assert not shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)}

    shape = bk.shapes[ShapeKind.Y]
    assert shape.kind == ShapeKind.Y
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(0, 0), (0, -1), (-1, 0), (1, 0), (2, 0)}

    shape = bk.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert set(shape.squares) == {(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)}

def test_some_flipped_shapes() -> None:
    """Tests that at least three kinds of shapes can be flipped correctly 
    via the Shape.flip_horizontally method."""
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.flip_horizontally()
    assert set(z_shape.squares) == {(-1, 1), (-1, 0), (0, 0), (1, 0), (1, -1)}

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.flip_horizontally()
    assert set(f_shape.squares) == {(0, 0), (0, 1), (-1, 0), (-1, -1), (1, 0)}

    w_shape = bk.shapes[ShapeKind.W]
    w_shape.flip_horizontally()
    assert set(w_shape.squares) == {(0, 0), (0, -1), (-1, -1), (1, 0), (1, 1)}

def test_some_left_rotated_shapes() -> None:
    """Tests that at least three kinds of shapes can be flipped correctly 
    via the Shape.rotate_left method."""
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.rotate_left()
    assert set(z_shape.squares) == {(0, 0), (0, 1), (0, -1), (1, -1), (-1, 1)}

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.rotate_left()
    assert set(f_shape.squares) == {(0, 0), (0, 1), (0, -1), (-1, -1), (1, 0)}

    w_shape = bk.shapes[ShapeKind.W]
    w_shape.rotate_left()
    assert set(w_shape.squares) == {(0, 0), (0, 1), (1, 1), (-1, 0), (-1, -1)}

def test_some_right_rotated_shapes() -> None:
    """Tests that at least three kinds of shapes can be flipped correctly 
    via the Shape.rotate_right method."""
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.rotate_right()
    assert set(z_shape.squares) == {(0, 0), (0, 1), (0, -1), (1, -1), (-1, 1)}

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.rotate_right()
    assert set(f_shape.squares) == {(0, 0), (0, 1), (0, -1), (-1, 0), (1, 1)}

    w_shape = bk.shapes[ShapeKind.W]
    w_shape.rotate_right()
    assert set(w_shape.squares) == {(0, 0), (0, -1), (1, 0), (-1, -1), (1, 1)}

def test_some_cardinal_neighbors() -> None:
    """Tests that Piece.cardinal_neighbors correctly computes the cardinal 
    neighbors of at least three kinds of pieces"""
    bk1 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    f_piece = Piece(bk1.shapes[ShapeKind.F])
    f_piece.set_anchor((1, 1))
    assert f_piece.cardinal_neighbors(bk1.size) == {(0, 0), (0, 3), (1, 2), (2, 0), (2, 2), (3, 1)}

    bk2 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    z_piece = Piece(bk2.shapes[ShapeKind.Z])
    z_piece.set_anchor((1, 1))
    assert z_piece.cardinal_neighbors(bk2.size) == {(1, 0), (2, 0), (0, 2), (1, 2), (2, 3), (3, 1), (3, 2)}

    bk3 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    w_piece = Piece(bk3.shapes[ShapeKind.W])
    w_piece.set_anchor((1, 1))
    assert w_piece.cardinal_neighbors(bk3.size) == {(1, 0), (0, 1), (3, 0), (3, 1), (2, 2), (1, 3), (0, 3)}

def test_some_intercardinal_neighbors() -> None:
    """Tests that Piece.intercardinal_neighbors correctly computes the cardinal 
    neighbors of at least three kinds of pieces"""
    bk1 = Blokus(1, 5, {(1, 1), (0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    f_piece = Piece(bk1.shapes[ShapeKind.F])
    f_piece.set_anchor((1, 1))
    assert f_piece.intercardinal_neighbors(bk1.size) == {(3, 0), (3, 2), (1, 3)}

    bk2 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    z_piece = Piece(bk2.shapes[ShapeKind.Z])
    z_piece.set_anchor((1, 1))
    assert z_piece.intercardinal_neighbors(bk2.size) == {(3, 0), (3, 3), (1, 3)}

    bk3 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    w_piece = Piece(bk3.shapes[ShapeKind.W])
    w_piece.set_anchor((1, 1))
    assert w_piece.intercardinal_neighbors(bk3.size) == {(0, 0), (3, 2), (2, 3)}

def test_one_player_blokus_mini_game() -> None:
    """For a 1-player Blokus mini game configuration, tests that the player 
    can place two or more pieces before retiring, verifying that the values 
    of game_over and curr_player are correct at each step. Verifies the values 
    of game_over, winners, and get_score(1)."""
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_piece = Piece(bk.shapes[ShapeKind.Z])
    z_piece.set_anchor((1, 1))

    assert bk.curr_player == 1
    assert bk.maybe_place(z_piece)
    assert bk.curr_player == 1
    assert not bk.game_over

    o_piece = Piece(bk.shapes[ShapeKind.LETTER_O])
    o_piece.set_anchor((3, 3))
    assert bk.maybe_place(o_piece)
    assert bk.curr_player == 1
    assert not bk.game_over

    bk.retire()

    assert bk.game_over
    assert bk.winners == [1]
    assert bk.get_score(1) == -80

def test_two_player_blokus_mini_game() -> None:
    """For a 2-player Blokus mini game configuration, tests that each player 
    can place two or more pieces before retiring, verifying that the values 
    of game_over and curr_player are correct at each step. Verifies the values 
    of game_over, winners, get_score(1), and get_score(2)"""
    bk = Blokus(2, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    c1_piece = Piece(bk.shapes[ShapeKind.C])
    c1_piece.set_anchor((0, 0))

    assert bk.curr_player == 1
    assert bk.maybe_place(c1_piece)
    assert bk.curr_player == 2
    assert not bk.game_over

    c2_piece = Piece(bk.shapes[ShapeKind.C])
    c2_piece.set_anchor((4, 4))
    c2_piece.rotate_right()
    c2_piece.rotate_right()

    assert bk.maybe_place(c2_piece)
    assert bk.curr_player == 1
    assert not bk.game_over 

    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((1, 2))
    assert bk.maybe_place(one_piece)
    assert bk.curr_player == 2
    assert not bk.game_over

    two_piece = Piece(bk.shapes[ShapeKind.TWO])
    two_piece.set_anchor((2, 3))
    two_piece.rotate_left()
    assert bk.maybe_place(two_piece)
    assert bk.curr_player == 1

    bk.retire()
    assert bk.curr_player == 2
    bk.retire()

    assert bk.game_over
    assert bk.winners == [2]
    assert bk.get_score(1) == -85
    assert bk.get_score(2) == -84
    
def test_exception_init() -> None:
    """Tests that four calls to the Blokus constructor each raise a ValueError,
      one for each of the four situations described in the docstring:
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players."""
    with pytest.raises(ValueError):
        bk = Blokus(0, 5, {(0, 0)})
    with pytest.raises(ValueError):
        bk = Blokus(5, 5, {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)})
    with pytest.raises(ValueError):
        bk = Blokus(1, 4, {(0, 0)})
    with pytest.raises(ValueError):
        bk = Blokus(1, 5, {(2, 6)})
    with pytest.raises(ValueError):
        bk = Blokus(2, 5, {(0, 0)})

def test_exception_place_already_played() -> None:
    """Tests that maybe_place raises a ValueError when trying to place an 
    already played piece."""
    bk = Blokus(1, 5, {(0, 0)})
    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((0, 0))
    assert bk.maybe_place(one_piece)

    another_one_piece = Piece(bk.shapes[ShapeKind.ONE])
    another_one_piece.set_anchor((4, 4))
    with pytest.raises(ValueError):
        bk.maybe_place(another_one_piece)
    
def test_exception_place_without_anchor() -> None:
    """Tests that maybe_place raises a ValueError when 
    trying to place a piece without an anchor."""
    bk = Blokus(1, 5, {(0, 0)})
    one_piece = Piece(bk.shapes[ShapeKind.ONE])

    with pytest.raises(ValueError):
        bk.maybe_place(one_piece)

def test_start_positions_1() -> None:
    """For a 1-player Blokus game configuration with one start position, tests
    that maybe_place will not place a piece that does not cover the start 
    position. Tests that maybe_place will place a 
    piece that does cover the start position, and that the player can place a
    second piece on the board.
    """
    bk = Blokus(1, 5, {(0, 0)})
    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((1, 1))
    assert not bk.maybe_place(one_piece)

    two_piece = Piece(bk.shapes[ShapeKind.TWO])
    two_piece.set_anchor((0, 0))
    assert bk.maybe_place(two_piece)

    three_piece = Piece(bk.shapes[ShapeKind.THREE])
    three_piece.set_anchor((1, 3))
    assert bk.maybe_place(three_piece)

def test_start_positions_2() -> None:
    """For a 2-player Blokus game configuration with two start positions, tests
    that Player 1 cannot place a piece that doesn't cover a start position,
    and that Player 2 cannot place a piece that doesn't cover a start position
    or that covers the occupied start position. Tests that Player 2 can then cover 
    the remaining start position. Tests that Player 1 and Player 2
    can then each play another piece. 
    """
    bk = Blokus(2, 10, {(0,0), (9, 9)})
    seven_piece = Piece(bk.shapes[ShapeKind.SEVEN])
    seven_piece.set_anchor((2, 2))
    assert not bk.maybe_place(seven_piece)

    seven_piece.set_anchor((1, 1))
    assert bk.maybe_place(seven_piece)

    a_piece = Piece(bk.shapes[ShapeKind.A])
    a_piece.set_anchor((7, 7))
    assert not bk.maybe_place(a_piece)
    a_piece.set_anchor((2, 0))
    assert not bk.maybe_place(a_piece)
    a_piece.set_anchor((9, 8))
    assert bk.maybe_place(a_piece)

    o_piece = Piece(bk.shapes[ShapeKind.LETTER_O])
    o_piece.set_anchor((3, 2))
    assert bk.maybe_place(o_piece)

    five_piece = Piece(bk.shapes[ShapeKind.FIVE])
    five_piece.set_anchor((5, 7))
    assert bk.maybe_place(five_piece)

def test_start_positions_3() -> None:
    """For a 2-player Blokus game configuration with four start positions, tests
    that Player 1 cannot place a piece that doesn't cover a start position,
    and that Player 2 cannot place a piece that doesn't cover a start position
    or that covers the occupied start position. Tests that Player 2 can then cover 
    the remaining start position. Tests that Player 1 and Player 2
    can then each play another piece. 
    """
    bk = Blokus(2, 10, {(0,0), (9, 9), (0, 9), (9, 0)})
    seven_piece = Piece(bk.shapes[ShapeKind.SEVEN])
    seven_piece.set_anchor((2, 2))
    assert not bk.maybe_place(seven_piece)

    seven_piece.set_anchor((1, 1))
    assert bk.maybe_place(seven_piece)

    a_piece = Piece(bk.shapes[ShapeKind.A])
    a_piece.set_anchor((7, 7))
    assert not bk.maybe_place(a_piece)
    a_piece.set_anchor((2, 0))
    assert not bk.maybe_place(a_piece)
    a_piece.set_anchor((9, 8))
    assert bk.maybe_place(a_piece)

    o_piece = Piece(bk.shapes[ShapeKind.LETTER_O])
    o_piece.set_anchor((3, 2))
    assert bk.maybe_place(o_piece)

    five_piece = Piece(bk.shapes[ShapeKind.FIVE])
    five_piece.set_anchor((5, 7))
    assert bk.maybe_place(five_piece)

def test_place_flipped_shape_1() -> None:
    """For a 1-player Blokus game configuration, tests that a flipped piece's 
    squares() are correct. After placing the piece, tests that grid stores 
    the correct values for every cell in the matrix."""
    bk = Blokus(1, 5, {(0, 0)})
    s_piece = Piece(bk.shapes[ShapeKind.S])
    s_piece.set_anchor((0, 1))
    s_piece.flip_horizontally()
    assert set(s_piece.squares()) == {(0, 0), (0, 1), (1, 1), (1, 2)}
    assert bk.maybe_place(s_piece)

    for square in s_piece.squares():
        r, c = square
        assert bk.grid[r][c][0] == bk.curr_player and bk.grid[r][c][1] == ShapeKind.S

def test_rotated_shape_1() -> None:
    """For a 1-player Blokus game configuration, tests that a right-rotated piece's 
    squares() are correct. After placing the piece, tests that grid stores 
    the correct values for every cell in the matrix."""
    bk = Blokus(1, 5, {(0, 0)})
    a_piece = Piece(bk.shapes[ShapeKind.A])
    a_piece.set_anchor((1, 0))
    a_piece.rotate_right()
    assert set(a_piece.squares()) == {(0, 0), (1, 0), (1, 1), (2, 0)}
    assert bk.maybe_place(a_piece)

    for square in a_piece.squares():
        r, c = square
        assert bk.grid[r][c][0] == bk.curr_player and bk.grid[r][c][1] == ShapeKind.A

def test_rotated_shape_2() -> None:
    """For a 1-player Blokus game configuration, tests that a left-rotated piece's 
    squares() are correct. After placing the piece, tests that grid stores 
    the correct values for every cell in the matrix."""
    bk = Blokus(1, 5, {(0, 0)})
    a_piece = Piece(bk.shapes[ShapeKind.A])
    a_piece.set_anchor((0, 1))
    a_piece.rotate_right()
    a_piece.rotate_right()
    assert set(a_piece.squares()) == {(0, 0), (0, 1), (0, 2), (1, 1)}
    assert bk.maybe_place(a_piece)

    for square in a_piece.squares():
        r, c = square
        assert bk.grid[r][c][0] == bk.curr_player and bk.grid[r][c][1] == ShapeKind.A

def test_flipped_and_rotated_shape_1() -> None:
    """For a 1-player Blokus game configuration, tests that flipped and 
    then right-rotated three times piece's squares() are correct. After placing the 
    piece, tests that grid stores the correct values for every cell in the matrix."""
    bk = Blokus(1, 5, {(1, 0)})
    s_piece = Piece(bk.shapes[ShapeKind.S])
    s_piece.set_anchor((1, 0))
    s_piece.flip_horizontally()
    s_piece.rotate_right()
    s_piece.rotate_right()
    s_piece.rotate_right()
    assert set(s_piece.squares()) == {(1, 0), (2, 0), (0, 1), (1, 1)}
    assert bk.maybe_place(s_piece)

    for square in s_piece.squares():
        r, c = square
        assert bk.grid[r][c][0] == bk.curr_player and bk.grid[r][c][1] == ShapeKind.S

def test_flipped_and_rotated_shape_2() -> None:
    """For a 1-player Blokus game configuration, tests that flipped twice and 
    then right-rotated four times piece's squares() are correct. After placing the 
    piece, tests that grid stores the correct values for every cell in the matrix."""
    bk = Blokus(1, 5, {(1, 1)})
    f_piece = Piece(bk.shapes[ShapeKind.F])
    f_piece.set_anchor((1, 1))
    f_piece.flip_horizontally()
    f_piece.flip_horizontally()
    f_piece.rotate_right()
    f_piece.rotate_right()
    f_piece.rotate_right()
    f_piece.rotate_right()
    assert set(f_piece.squares()) == {(1, 1), (1, 0), (2, 1), (0, 1), (0, 2)}
    assert bk.maybe_place(f_piece)

    for square in f_piece.squares():
        r, c = square
        assert bk.grid[r][c][0] == bk.curr_player and bk.grid[r][c][1] == ShapeKind.F

def test_prevent_own_edges_1() -> None:
    """For a 1-player Blokus game configuration, after placing a piece, 
    tests that the player cannot place another piece that shares an edge 
    with their first played piece."""
    bk = Blokus(1, 5, {(0, 0)})
    l_piece = Piece(bk.shapes[ShapeKind.L])
    l_piece.set_anchor((2, 0))
    assert bk.maybe_place(l_piece)

    three_piece = Piece(bk.shapes[ShapeKind.THREE])
    three_piece.set_anchor((0, 2))
    assert not bk.maybe_place(three_piece) 

def test_prevent_own_edges_2() -> None:
    """
    Tests that a player's piece cannot share an edge with their own pieces but
    can share an edge with other
    players' pieces."""
    bk = Blokus(2, 10, {(0, 0), (9, 9)})
    c_piece = Piece(bk.shapes[ShapeKind.C])
    c_piece.set_anchor((0, 0))
    assert bk.maybe_place(c_piece)

    four_piece = Piece(bk.shapes[ShapeKind.FOUR])
    four_piece.set_anchor((9, 7))
    assert bk.maybe_place(four_piece)

    seven_piece = Piece(bk.shapes[ShapeKind.SEVEN])
    seven_piece.set_anchor((2, 2))
    assert not bk.maybe_place(seven_piece)
    seven_piece.set_anchor((3, 2))
    assert bk.maybe_place(seven_piece)

    f_piece = Piece(bk.shapes[ShapeKind.F])
    f_piece.set_anchor((7, 6))
    assert not bk.maybe_place(f_piece)
    f_piece.set_anchor((7, 5))
    assert bk.maybe_place(f_piece)

    assert bk.curr_player == 1
    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((5, 3))
    assert bk.maybe_place(one_piece)

    a1_piece = Piece(bk.shapes[ShapeKind.A])
    a1_piece.set_anchor((4, 4))
    a1_piece.rotate_left()
    assert bk.maybe_place(a1_piece)

def test_require_own_corners_1() -> None:
    """
    Tests that a player cannot play pieces that share zero corners with their own
    pieces.
    """
    bk = Blokus(1, 5, {(0, 0)})
    l_piece = Piece(bk.shapes[ShapeKind.L])
    l_piece.set_anchor((2, 0))
    assert bk.maybe_place(l_piece)

    three_piece = Piece(bk.shapes[ShapeKind.THREE])
    three_piece.set_anchor((4, 4))
    assert not bk.maybe_place(three_piece) 

def test_require_own_corners_2() -> None:
    """
    Tests that a player cannot play pieces that share zero corners with their own
    pieces but can share zero corners with other players' pieces.
    """
    bk = Blokus(2, 10, {(0, 0), (9, 9)})
    c_piece = Piece(bk.shapes[ShapeKind.C])
    c_piece.set_anchor((0, 0))
    assert bk.maybe_place(c_piece)

    four_piece = Piece(bk.shapes[ShapeKind.FOUR])
    four_piece.set_anchor((9, 7))
    assert bk.maybe_place(four_piece)

    seven_piece = Piece(bk.shapes[ShapeKind.SEVEN])
    seven_piece.set_anchor((3, 3))
    assert not bk.maybe_place(seven_piece)
    seven_piece.set_anchor((3, 2))
    assert bk.maybe_place(seven_piece)

    f_piece = Piece(bk.shapes[ShapeKind.F])
    f_piece.set_anchor((6, 5))
    assert not bk.maybe_place(f_piece)
    f_piece.set_anchor((7, 5))
    assert bk.maybe_place(f_piece)

    three_piece = Piece(bk.shapes[ShapeKind.THREE])
    three_piece.set_anchor((1, 4))
    print(three_piece.intercardinal_neighbors(bk.size))
    
    assert bk.maybe_place(three_piece)

    two_piece = Piece(bk.shapes[ShapeKind.TWO])
    two_piece.set_anchor((6, 2))
    assert bk.maybe_place(two_piece)

def test_some_available_moves() -> None:
    """
    Test that create an instance of any Blokus game configuration. Verifies that 
    available_moves is non-empty. Plays a few pieces, and verify that the number 
    of available_moves for a player increases after their first move and then 
    decreases after subsequent moves.
    """
    bk = Blokus(1, 7, {(0, 0)})
    print(len(bk._shapes_left))
    left_1 = len(bk.available_moves())
    assert left_1 != 0
    p_piece = Piece(bk.shapes[ShapeKind.P])
    p_piece.set_anchor((1, 1))
    assert bk.maybe_place(p_piece)
    print(len(bk._shapes_left))
    left_2 = len(bk.available_moves())
    assert left_1 < left_2

    t_piece = Piece(bk.shapes[ShapeKind.T])
    t_piece.set_anchor((3, 3))
    assert bk.maybe_place(t_piece)
    print(len(bk._shapes_left))
    left_3 = len(bk.available_moves())
    assert left_2 > left_3

    two = Piece(bk.shapes[ShapeKind.TWO])
    two.set_anchor((5, 4))
    assert bk.maybe_place(two)
    left_4 = len(bk.available_moves())
    assert left_3 > left_4

def place_all(monimono: bool) -> Blokus:
    """
    A helper function that places all the pieces on the board, and either places
    the monimono as the last piece or not based on the input.
    Input:
        monimono [bool]: True if monimono is the last piece, False otherwise
    Returns [Blokus]: the updated state of the Blokus game
    """
    bk = Blokus(1, 20, {(0, 0)})
        
    l = Piece(bk.shapes[ShapeKind.L])
    l.set_anchor((0, 1))
    l.rotate_right()
    assert bk.maybe_place(l)

    v = Piece(bk.shapes[ShapeKind.V])
    v.set_anchor((2, 3))
    assert bk.maybe_place(v)

    x = Piece(bk.shapes[ShapeKind.X])
    x.set_anchor((5, 5))
    assert bk.maybe_place(x)

    t = Piece(bk.shapes[ShapeKind.T])
    t.set_anchor((2, 7))
    t.rotate_left()
    assert bk.maybe_place(t)

    if not monimono:
        one = Piece(bk.shapes[ShapeKind.ONE])
        one.set_anchor((3, 9))
        assert bk.maybe_place(one)

    five = Piece(bk.shapes[ShapeKind.FIVE])
    five.set_anchor((0, 9))
    five.rotate_left()
    assert bk.maybe_place(five)

    four = Piece(bk.shapes[ShapeKind.FOUR])
    four.set_anchor((1, 13))
    assert bk.maybe_place(four)

    three = Piece(bk.shapes[ShapeKind.THREE])
    three.set_anchor((0, 17))
    assert bk.maybe_place(three)

    y = Piece(bk.shapes[ShapeKind.Y])
    y.set_anchor((2, 18))
    y.flip_horizontally()
    y.rotate_right()
    assert bk.maybe_place(y)

    a = Piece(bk.shapes[ShapeKind.A])
    a.set_anchor((4, 16))
    a.rotate_right()
    a.rotate_right()
    assert bk.maybe_place(a)

    two = Piece(bk.shapes[ShapeKind.TWO])
    two.set_anchor((6, 17))
    assert bk.maybe_place(two)

    n = Piece(bk.shapes[ShapeKind.N])
    n.set_anchor((8, 15))
    assert bk.maybe_place(n)

    c = Piece(bk.shapes[ShapeKind.C])
    c.set_anchor((12, 14))
    c.rotate_right()
    c.rotate_right()
    assert bk.maybe_place(c)

    u = Piece(bk.shapes[ShapeKind.U])
    u.set_anchor((10, 12))
    u.rotate_left()
    assert bk.maybe_place(u)

    o = Piece(bk.shapes[ShapeKind.LETTER_O])
    o.set_anchor((12, 9))
    assert bk.maybe_place(o)

    s = Piece(bk.shapes[ShapeKind.S])
    s.set_anchor((13, 7))
    s.flip_horizontally()
    assert bk.maybe_place(s)

    seven = Piece(bk.shapes[ShapeKind.SEVEN])
    seven.set_anchor((5, 13))
    seven.flip_horizontally()
    seven.rotate_left()
    assert bk.maybe_place(seven)

    p = Piece(bk.shapes[ShapeKind.P])
    p.set_anchor((5, 1))
    assert bk.maybe_place(p)

    z = Piece(bk.shapes[ShapeKind.Z])
    z.set_anchor((7, 2))
    z.rotate_right()
    assert bk.maybe_place(z)

    f = Piece(bk.shapes[ShapeKind.F])
    f.set_anchor((10, 2))
    assert bk.maybe_place(f)

    w = Piece(bk.shapes[ShapeKind.W])
    w.set_anchor((15, 4))
    assert bk.maybe_place(w)

    if monimono:
        one = Piece(bk.shapes[ShapeKind.ONE])
        one.set_anchor((3, 9))
        assert bk.maybe_place(one)

    return bk

def test_no_available_moves() -> None:
    """
    Create an instance of any Blokus game configuration. Play pieces until there 
    are no more available moves, and verify that available_moves is empty.
    """
    bk = place_all(True)
    assert len(bk.available_moves()) == 0

def test_15_points() -> None:
    """
    Simulate a game where a player scores 15 points (plays all 21 of 
    their pieces). After all 21 pieces are played and the game is over, verify 
    the expected values for get_score(), game_over, winners, and remaining_shapes.
    """
    bk = place_all(False)
    assert bk.game_over
    assert bk.get_score(1) == 15
    assert bk.winners == [1]
    assert not bk.remaining_shapes(1)

def test_20_points() -> None:
    """
    Simulate a game where a player scores 15 points (plays all 21 of 
    their pieces and ONE is the last piece placed). After all 21 pieces are 
    played and the game is over, verify the expected values for get_score(), 
    game_over, winners, and remaining_shapes.
    """
    bk = place_all(True)
    print(bk.grid)
    assert bk.game_over
    assert bk.get_score(1) == 20
    assert bk.winners == [1]    
    assert not bk.remaining_shapes(1)
    


