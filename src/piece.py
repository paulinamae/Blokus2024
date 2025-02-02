"""
Blokus shapes and pieces.

Modify only the methods marked as TODO.
"""
import copy
from typing import Optional

from shape_definitions import ShapeKind
import shape_definitions

# A point is represented by row and column numbers (r, c). The
# top-left corner of a grid is (0, 0). Note that rows/columns
# correspond to vertical/horizontal axes, respectively. So, we
# will typically index into a 2-dimensional grid using
# grid[r][c] (as opposed to grid[y][x]).
#
Point = tuple[int, int]


# We will typically unpack a Point as follows: (r, c) = point
# In other cases, the row and col functions may be helpful.
#
def row(point: Point) -> int:
    return point[0]


def col(point: Point) -> int:
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """

        lines = definition.splitlines()
        for line in lines:
            if "X" not in line and "O" not in line:
                lines.remove(line)

        spaces = []
        for line in lines:
            count = 0
            for char in line:
                if char != "X" and char != "O": # is a valid preceding space
                    count += 1
                else:
                    spaces.append(count)
                    break

        r_coord: int = -1
        c_coord: int = -1
        all_coords: list[Point] = list()
        for line in lines:
            newline = line.replace(" " * min(spaces),"")
            r_coord += 1
            for char in newline:
                c_coord += 1
                if char == "O" or char == "@":
                    o_coords: tuple[int,int] = (r_coord,c_coord)
                    all_coords.append((r_coord, c_coord))
                if char == "X":
                    all_coords.append((r_coord, c_coord))
            c_coord = -1

        if kind == ShapeKind.LETTER_O or kind == ShapeKind.ONE:
            o_coords = (0,0)
            transformed: bool = False
        elif kind == ShapeKind.X:
            o_coords = (1, 1)
            transformed = False
        else:
            transformed = True
        final: list[Point]= []
        for point in all_coords:
            row, col = o_coords
            a, b = point
            final.append((a - row, b - col))

        if kind == ShapeKind.V:
            final.remove((0, 0))

        return Shape(kind, o_coords, transformed, final)

    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        new_squares: list[Point] = []
        for square in self.squares:
            row, col = square 
            new_square = (row, -col)
            new_squares.append(new_square)

        self.squares = new_squares

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        new_squares: list[Point] = []
        for square in self.squares:
            x,y = square
            new_square: Point = (-y,x)
            new_squares.append(new_square)

        self.squares = new_squares

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        new_squares: list[Point] = []
        for square in self.squares:
            x,y = square
            new_square: Point = (y,-x)
            new_squares.append(new_square)
            
        self.squares = new_squares


class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If false, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.shape.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.shape.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()
            

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]

    def cardinal_neighbors(self, board_size: int) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        if not self.anchor:
            raise ValueError("Anchor point not set")
        
        result: set[Point] = set()

        for r, c in self.squares():
            if not (r - 1 < 0):
                north_neighbor: Point = (r - 1, c)
                if north_neighbor not in self.squares():
                    result.add(north_neighbor)
            
            if not (r + 1 >= board_size):
                south_neighbor: Point = (r + 1, c)
                if south_neighbor not in self.squares():
                    result.add(south_neighbor)
            
            if not (c + 1 >= board_size):
                east_neighbor: Point = (r, c + 1)
                if east_neighbor not in self.squares():
                    result.add(east_neighbor)
            
            if not (c - 1 < 0):
                west_neighbor: Point = (r, c - 1)
                if west_neighbor not in self.squares():
                    result.add(west_neighbor)
        
        return result

    def intercardinal_neighbors(self, board_size: int) -> set[Point]:
        """
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        if not self.anchor:
            raise ValueError("Anchor point not set")
            
        result: set[Point] = set()

        for r, c in self.squares():
            if not (r - 1 < 0) and not (c + 1 >= board_size):
                northeast_neighbor: Point = (r - 1, c + 1)
                result.add(northeast_neighbor)
            
            if not (r + 1 >= board_size) and not (c + 1 >= board_size):
                southeast_neighbor: Point = (r + 1, c + 1)
                result.add(southeast_neighbor)
            
            if not (r - 1 < 0) and not (c - 1 < 0):
                northwest_neighbor: Point = (r - 1, c - 1)
                result.add(northwest_neighbor)
            
            if not (r + 1 >= board_size) and not (c - 1 < 0):
                southwest_neighbor: Point = (r + 1, c - 1)
                result.add(southwest_neighbor)
        
        return result - self.cardinal_neighbors(board_size) - set(self.squares())
