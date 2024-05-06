import pytest
from typing import Optional

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from blokus import Blokus

def test_inheritance() -> None:
    """Test that Blokus inherits from BlokusBase"""
    assert issubclass(
        Blokus, BlokusBase
    ), "Blokus should inherit from BlokusBase"

def test_init_blokus_mini_1() -> None:
    blokus_mini = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    assert blokus_mini.num_players == 1
    assert blokus_mini.size == 5
    assert blokus_mini.curr_player == 1
    assert blokus_mini.start_positions == set((0,0), (0, 4), (4,0), (4, 4), (2, 2))
    assert blokus_mini.grid == [[None] * blokus_mini.size for _ in range(blokus_mini.size)]
    assert not blokus_mini.game_over

def test_init_blokus_mini_2() -> None:
    blokus_mini = Blokus(2, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    assert blokus_mini.num_players == 2
    assert blokus_mini.size == 5
    assert blokus_mini.curr_player == 1
    assert blokus_mini.start_positions == set((0,0), (0, 4), (4,0), (4, 4), (2, 2))
    assert blokus_mini.grid == [[None] * blokus_mini.size for _ in range(blokus_mini.size)]
    assert not blokus_mini.game_over

def test_init_blokus_mono() -> None:
    blokus_mono = Blokus(1, 11, {(5, 5)})

    assert blokus_mono.num_players == 1
    assert blokus_mono.size == 11
    assert blokus_mono.curr_player == 1
    assert blokus_mono.start_positions == set((5, 5))
    assert blokus_mono.grid == [[None] * blokus_mono.size for _ in range(blokus_mono.size)]
    assert not blokus_mono.game_over

def test_init_blokus_duo_2() -> None:
    blokus_duo = Blokus(2, 14, {(4, 4), (9, 9)})

    assert blokus_duo.num_players == 2
    assert blokus_duo.size == 14
    assert blokus_duo.curr_player == 1
    assert blokus_duo.start_positions == set((4, 4), (9, 9))
    assert blokus_duo.grid == [[None] * blokus_duo.size for _ in range(blokus_duo.size)]
    assert not blokus_duo.game_over

def test_shapes_loaded() -> None:
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
    assert shape.squares == [(0, 0), (0, 1)]

    shape = bk.shapes[ShapeKind.THREE]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (0, -1)]

    shape = bk.shapes[ShapeKind.C]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0)]

    shape = bk.shapes[ShapeKind.FOUR]
    assert shape.kind == ShapeKind.FOUR
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (0, -1), (0, 2)]

    shape = bk.shapes[ShapeKind.SEVEN]
    assert shape.kind == ShapeKind.SEVEN
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0)]

    shape = bk.shapes[ShapeKind.S]
    assert shape.kind == ShapeKind.S
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, -1), (1, 0)]

    shape = bk.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0), (1, 1)]

    shape = bk.shapes[ShapeKind.A]
    assert shape.kind == ShapeKind.A
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 0), (0, -1), (0, 1)]

    shape = bk.shapes[ShapeKind.F]
    assert shape.kind == ShapeKind.F
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, -1), (-1, 0), (-1, 1), (1, 0)]

    shape = bk.shapes[ShapeKind.FIVE]
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0)]

    shape = bk.shapes[ShapeKind.L]
    assert shape.kind == ShapeKind.L
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 0), (-2, 0), (1, 0), (1, 1)]

    shape = bk.shapes[ShapeKind.N]
    assert shape.kind == ShapeKind.N
    assert shape.origin == (1, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 1), (0, 1), (1, 0), (2, 0)]

    shape = bk.shapes[ShapeKind.P]
    assert shape.kind == ShapeKind.P
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, -1), (-1, -1), (-1, 0), (1, -1)]

    shape = bk.shapes[ShapeKind.T]
    assert shape.kind == ShapeKind.T
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)]

    shape = bk.shapes[ShapeKind.U]
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, -1), (-1, 1), (0, -1), (0, 1)]

    shape = bk.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]

    shape = bk.shapes[ShapeKind.W]
    assert shape.kind == ShapeKind.W
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 1), (0, 1), (1, -1), (1, 0)]

    shape = bk.shapes[ShapeKind.X]
    assert shape.kind == ShapeKind.X
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

    shape = bk.shapes[ShapeKind.Y]
    assert shape.kind == ShapeKind.Y
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, -1), (-1, 0), (1, 0), (2, 0)]

    shape = bk.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]

def test_some_flipped_shapes() -> None:
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.flip_horizontally()
    assert z_shape.squares == [(-1, 1), (-1, 0), (0, 0), (1, 0), (1, -1)]

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.flip_horizontally()
    assert f_shape.squares == [(0, 0), (0, 1), (-1, 0), (-1, -1), (1, 0)]

    W_shape = bk.shapes[ShapeKind.W]
    W_shape.flip_horizontally()
    assert W_shape.squares == [(0, 0), (0, -1), (-1, -1), (1, 0), (1, 1)]

def test_some_left_rotated_shapes() -> None:
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.rotate_left()
    assert z_shape.squares == [(0, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.rotate_left()
    assert f_shape.squares == [(0, 0), (0, 1), (0, -1), (-1, -1), (1, 0)]

    W_shape = bk.shapes[ShapeKind.W]
    W_shape.rotate_left()
    assert W_shape.squares == [(0, 0), (0, -1), (0, 1), (1, -1), (-1, 1)]

def test_some_right_rotated_shapes() -> None:
    bk = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    z_shape = bk.shapes[ShapeKind.Z]
    z_shape.rotate_right()
    assert z_shape.squares == set((0, 0), (0, 1), (0, -1), (1, -1), (-1, 1))

    f_shape = bk.shapes[ShapeKind.F]
    f_shape.rotate_right()
    assert f_shape.squares == set((0, 0), (0, 1), (0, -1), (-1, 0), (1, 1))

    W_shape = bk.shapes[ShapeKind.W]
    W_shape.rotate_right()
    assert W_shape.squares == set((0, 0), (0, -1), (1, 0), (-1, -1), (1, 1))

def test_some_cardinal_neighbors() -> None:
    bk1 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    f_piece = Piece(bk1.shapes[ShapeKind.F])
    f_piece.set_anchor((1, 1))
    assert f_piece.cardinal_neighbors() == set((0, 0), (0, 3), (1, 2), (2, 0), (2, 2), (3, 1))

    bk2 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    z_piece = Piece(bk2.shapes[ShapeKind.Z])
    z_piece.set_anchor((1, 1))
    assert f_piece.cardinal_neighbors() == set((1, 0), (2, 0), (0, 2), (1, 2), (2, 3), (3, 1), (3, 2))

    bk3 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    w_piece = Piece(bk3.shapes[ShapeKind.W])
    w_piece.set_anchor((1, 1))
    assert w_piece.cardinal_neighbors() == set((1, 0), (0, 1), (3, 0), (3, 1), (2, 2), (1, 3), (0, 3))

def test_some_intercardinal_neighbors() -> None:
    bk1 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    
    f_piece = Piece(bk1.shapes[ShapeKind.F])
    f_piece.set_anchor((1, 1))
    assert f_piece.cardinal_neighbors() == set((3, 0), (3, 2), (1, 3))

    bk2 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    z_piece = Piece(bk2.shapes[ShapeKind.Z])
    z_piece.set_anchor((1, 1))
    assert f_piece.cardinal_neighbors() == set((3, 0), (3, 3), (1, 3))

    bk3 = Blokus(1, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})
    w_piece = Piece(bk3.shapes[ShapeKind.W])
    w_piece.set_anchor((1, 1))
    assert w_piece.cardinal_neighbors() == set((0, 0), (3, 2), (2, 3))

def test_one_player_blokus_mini_game() -> None:
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
    bk = Blokus(2, 5, {(0,0), (0, 4), (4,0), (4, 4), (2, 2)})

    c1_piece = Piece(bk.shapes[ShapeKind.C])
    c1_piece.set_anchor((0, 0))

    assert bk.curr_player == 1
    assert bk.maybe_place(c1_piece)
    assert bk.curr_player == 2
    assert not bk.game_over

    c2_piece = Piece(bk.shapes[ShapeKind.C])
    c2_piece.rotate_right()
    c2_piece.rotate_right()
    c2_piece.set_anchor((4, 4))

    assert bk.maybe_place(c2_piece)
    assert bk.curr_player == 1
    assert not bk.game_over 

    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((1, 2))
    assert bk.maybe_place(one_piece)
    assert bk.curr_player == 2
    assert not bk.game_over

    two_piece = Piece(bk.shapes[ShapeKind.TWO])
    two_piece.rotate_left()
    two_piece.set_anchor((2, 3))
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
    with pytest.raises(ValueError):
        bk = Blokus(0, 5, {(0, 0)})
    with pytest.raises(ValueError):
        bk = Blokus(5, 5, {(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)})
    with pytest.raises(ValueError):
        bk = Blokus(1, 4, {(0, 0)})
    with pytest.raises(ValueError):
        bk = Blokus(1, 5, {(6, 6)})
    with pytest.raises(ValueError):
        bk = Blokus(2, 5, {(0, 0)})

def test_exception_place_already_played() -> None:
    bk = Blokus(1, 5, {(0, 0)})
    one_piece = Piece(bk.shapes[ShapeKind.ONE])
    one_piece.set_anchor((0, 0))
    assert bk.maybe_place(one_piece)

    another_one_piece = Piece(bk.shapes[ShapeKind.ONE])
    another_one_piece.set_anchor((4, 4))
    with pytest.raises(ValueError):
        bk.maybe_place(another_one_piece)
    
def test_exception_place_without_anchor() -> None:
    bk = Blokus(1, 5, {(0, 0)})
    one_piece = Piece(bk.shapes[ShapeKind.ONE])

    with pytest.raises(ValueError):
        bk.maybe_place(one_piece)

def test_start_positions_1() -> None:
    pass 


