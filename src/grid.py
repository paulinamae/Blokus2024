from typing import Optional
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from blokus import Blokus
from textwrap import *

def grid_to_string(grid: Grid) -> str:
    dim = len(grid)
    final = "||" * (dim + 2)
    for row in grid:
        final += '\n' + "||"
        for cell in row:
            if cell:
                player = cell[0]
                kind = cell[1]
                if player == 1:
                    final += kind.value + (" ")
                else:
                    final += (" ") + kind.value
            else:
                final += "  "
        final += "||"
    final += "\n" + ("||" * (dim + 2))
    return final

def string_to_grid(s: str) -> Grid:
    new = s.splitlines()
    del new[0]
    size = int((len(new[0]) / 2 ) - 2)
    rowlen = len(new[1]) -1
    new_grid = [[None] * size for _ in range(size)] 
    for r, row in enumerate(new):
        for c, (char1, char2) in enumerate(zip(*[iter(row[2:rowlen])]*2)):
            if char1 == " " and char2 != " ":
                new_grid[r][c] = (2, ShapeKind(char2))
            if char1 != " " and char2 == " ":
                new_grid[r][c] = (1, ShapeKind(char1))
    return new_grid

def test_grid_1() -> None:
    bk = Blokus(2, 10, {(0, 0), (9, 9)})

    l = Piece(bk.shapes[ShapeKind.L])
    l.set_anchor((2, 0))
    assert bk.maybe_place(l)

    u = Piece(bk.shapes[ShapeKind.U])
    u.set_anchor((9, 8))
    assert bk.maybe_place(u)

    z = Piece(bk.shapes[ShapeKind.Z])
    z.set_anchor((5, 3))
    assert bk.maybe_place(z)

    w = Piece(bk.shapes[ShapeKind.W])
    w.set_anchor((6, 6))
    assert bk.maybe_place(w)
    
    grid = bk.grid
    s = """
        ||||||||||||||||||||||||
        ||L                   ||
        ||L                   ||
        ||L                   ||
        ||L L                 ||
        ||    Z Z             ||
        ||      Z        W    ||
        ||      Z Z    W W    ||
        ||           W W      ||
        ||               U   U||
        ||               U U U||
        ||||||||||||||||||||||||
        """
    
    assert dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_2() -> None:
    bk = Blokus(2, 5, {(0, 0), (4, 4)})
    grid = bk.grid
    s = """
        ||||||||||||||
        ||          ||
        ||          ||
        ||          ||
        ||          ||
        ||          ||
        ||||||||||||||
        """
    assert dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_3() -> None:
    bk = Blokus(2, 8, {(3, 3), (4, 4)})
    t = Piece(bk.shapes[ShapeKind.T])
    t.set_anchor((2, 3))
    assert bk.maybe_place(t)

    w = Piece(bk.shapes[ShapeKind.W])
    w.set_anchor((4, 5))
    w.rotate_right()
    w.rotate_right()
    assert bk.maybe_place(w)

    x = Piece(bk.shapes[ShapeKind.X])
    x.set_anchor((4, 1))
    assert bk.maybe_place(x)

    n = Piece(bk.shapes[ShapeKind.N])
    n.set_anchor((5, 6))
    assert bk.maybe_place(n)

    s = Piece(bk.shapes[ShapeKind.S])
    s.set_anchor((0, 6))
    s.flip_horizontally()
    assert bk.maybe_place(s)

    two = Piece(bk.shapes[ShapeKind.TWO])
    two.set_anchor((6, 2))
    assert bk.maybe_place(two)

    grid = bk.grid
    s = """
        ||||||||||||||||||||
        ||          S S   ||
        ||    T T T   S S ||
        ||      T         ||
        ||  X   T    W W  ||
        ||X X X    W W   N||
        ||  X      W   N N||
        ||     2 2     N  ||
        ||             N  ||
        ||||||||||||||||||||    
        """
    assert dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_4() -> None:
    bk = Blokus(2, 5, {(4, 0), (0, 4)})
    five_1 = Piece(bk.shapes[ShapeKind.FIVE])
    five_1.set_anchor((2, 0))
    assert bk.maybe_place((five_1))

    five_2 = Piece(bk.shapes[ShapeKind.FIVE])
    five_2.set_anchor((2, 4))
    assert bk.maybe_place((five_2))
    assert not bk.available_moves()

    grid = bk.grid
    s = """
        ||||||||||||||
        ||5        5||
        ||5        5||
        ||5        5||
        ||5        5||
        ||5        5||
        ||||||||||||||
        """
    assert dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_5() -> None:
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

    one = Piece(bk.shapes[ShapeKind.ONE])
    one.set_anchor((3, 9))
    assert bk.maybe_place(one)

    grid = bk.grid
    s = """
        ||||||||||||||||||||||||||||||||||||||||||||
        ||L L L L       5 5 5 5 5         3 3 3   ||
        ||L       V   T           4 4 4 4         ||
        ||        V   T T T               Y Y Y Y ||
        ||    V V V   T     1                 Y   ||
        ||P P       X             7     A A A     ||
        ||P P     X X X           7 7 7   A       ||
        ||P     Z   X                       2 2   ||
        ||  Z Z Z                         N       ||
        ||  Z                           N N       ||
        ||    F F               U U     N         ||
        ||  F F                   U     N         ||
        ||    F                 U U   C           ||
        ||                  O O     C C           ||
        ||            S S   O O                   ||
        ||          W   S S                       ||
        ||        W W                             ||
        ||      W W                               ||
        ||                                        ||
        ||                                        ||
        ||                                        ||
        ||||||||||||||||||||||||||||||||||||||||||||
        """
    assert dedent(s).strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))









