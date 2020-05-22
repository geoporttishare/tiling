# -*- coding: utf-8 -*-

import sys
import numpy as np

from tiling.generic import Block


class TM35Block(Block):
    """
    A tiling that matches TM35 sheet line system used by the NLS.
    """

    valid_letters = (
        "KLMNPQRSTUVWX",
        "23456",
        "1234",
        "1234",
        "1234",
        "ABCDEFGH",
        "1234"
    )

    # The origin of the tiling.
    base = (-76000.0, 6570000.0)

    # The size of the first-level tiling.
    base_dims = np.array((5 * 192000, 13 * 96000))

    # How the tiles are divided in each level.
    refinements = np.array((
        (1, 13),
        (5, 1),
        (2, 2),
        (2, 2),
        (2, 2),
        (4, 2),
        (2, 2)
    ))

    # How the subtiles are located inside the parent tile.
    offsets = np.array((
        ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
         (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12)),
        ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)),
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 0), (0, 1), (1, 0), (1, 1)),
        ((0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)),
        ((0, 0), (0, 1), (1, 0), (1, 1))
    ))

