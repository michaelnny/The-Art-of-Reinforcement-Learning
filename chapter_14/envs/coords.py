# Copyright (c) 2023 Michael Hu.
# This code is part of the book "The Art of Reinforcement Learning: Fundamentals, Mathematics, and Implementation with Python.".
# See the accompanying LICENSE file for details.


# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logic for dealing with coordinates.

This introduces some helpers and terminology that are used throughout Minigo.

Minigo Coordinate: This is a tuple of the form (row, column) that is indexed
    starting out at (0, 0) from the upper-left.
Flattened Coordinate: this is a number ranging from 0 - N^2 (so N^2+1
    possible values). The extra value N^2 is used to mark a 'pass' move.
SGF Coordinate: Coordinate used for SGF serialization format. Coordinates use
    two-letter pairs having the form (column, row) indexed from the upper-left
    where 0, 0 = 'aa'.
GTP Coordinate: Human-readable coordinate string indexed from bottom left, with
    the first character a capital letter for the column and the second a number
    from 1-19 for the row. Note that GTP chooses to skip the letter 'I' due to
    its similarity with 'l' (lowercase 'L').
PYGTP Coordinate: Tuple coordinate indexed starting at 1,1 from bottom-left
    in the format (column, row)

So, for a 19x19,

Coord Type      upper_left      upper_right     pass
-------------------------------------------------------
Minigo coord    (0, 0)          (0, 18)         None
flat            0               18              361
SGF             'aa'            'sa'            ''
GTP             'A19'           'T19'           'pass'
"""


# We provide more than 19 entries here in case of boards larger than 19 x 19.
_SGF_COLUMNS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_GTP_COLUMNS = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'


class CoordsConvertor:
    def __init__(self, board_size) -> None:
        self.board_size = board_size

    def from_flat(self, flat):
        """Converts from a flattened coordinate to a Minigo coordinate."""
        if flat == self.board_size * self.board_size:
            return None
        return divmod(flat, self.board_size)

    def to_flat(self, coord):
        """Converts from a Minigo coordinate to a flattened coordinate."""
        if coord is None:
            return self.board_size * self.board_size
        return self.board_size * coord[0] + coord[1]

    def from_sgf(self, sgfc):
        """Converts from an SGF coordinate to a Minigo coordinate."""
        if sgfc is None or sgfc == '' or (self.board_size <= 19 and sgfc == 'tt'):
            return None
        return _SGF_COLUMNS.index(sgfc[1]), _SGF_COLUMNS.index(sgfc[0])

    def to_sgf(self, coord):
        """Converts from a Minigo coordinate to an SGF coordinate."""
        if coord is None:
            return ''
        return _SGF_COLUMNS[coord[1]] + _SGF_COLUMNS[coord[0]]

    def from_gtp(self, gtpc):
        """Converts from a GTP coordinate to a Minigo coordinate."""
        gtpc = gtpc.upper()
        if gtpc == 'PASS':
            return None
        col = _GTP_COLUMNS.index(gtpc[0])
        row_from_bottom = int(gtpc[1:])
        return self.board_size - row_from_bottom, col

    def to_gtp(self, coord):
        """Converts from a Minigo coordinate to a GTP coordinate."""
        if coord is None:
            return 'pass'
        y, x = coord
        return '{}{}'.format(_GTP_COLUMNS[x], self.board_size - y)
