# -*- coding: utf-8 -*-

import sys
import numpy as np


class Block(object):
    """
    An abstract class that represent a 2D tiling.
    """

    @classmethod
    def valid_block_string_length(cls):
        return len(cls.valid_letters)

    @classmethod
    def is_valid_block_string(cls, s):
        if len(s) != len(cls.valid_letters):
            return False
        for l, letters in zip(s, cls.valid_letters):
            if not l in letters:
                return False
        return True

    @classmethod
    def is_valid_start(cls, s):
        if len(s) > len(cls.valid_letters):
            return False
        for l, letters in zip(s, cls.valid_letters):
            if not l in letters:
                return False
        return True

    @classmethod
    def verify_block_string(cls, s):
        if len(s) > len(cls.valid_letters):
            raise ValueError(f'Too long block string "{s}".')
        for i, l in enumerate(s):
            if not l in cls.valid_letters[i]:
                raise ValueError(
                    f'Invalid letter "{l}" in the block string.')

    @classmethod
    def expand(cls, partial_string):
        """
        Return all the blocks whose code begin with the parameter
        'partial_string'.
        """
        if len(partial_string) > len(cls.valid_letters):
            raise ValueError(f'Too long partial string "{partial_string}".')
        elif len(partial_string) == len(cls.valid_letters):
            if cls.is_valid_block_string(partial_string):
                return [partial_string]
            else:
                raise ValueError(f'Invalid block string "{partial_string}".')
        else:
            cls.verify_block_string(partial_string)
            ret = []
            for l in cls.valid_letters[len(partial_string)]:
                ret = ret + cls.expand_(partial_string + l)
            return ret


    @classmethod
    def expand_(cls, partial_string):
        """
        Do not use this directly. Call expand() which will perform some
        initial checks.

        The 'partial_string' may be a proper block code or a shorter than a
        proper code. If it is shorter, is must be a start of a proper block
        code.
        """
        ret_list = []
        if cls.is_valid_block_string(partial_string):
            return [partial_string]
        else:
            b = partial_string
            for l in cls.valid_letters[len(partial_string)]:
                ret_list = ret_list + cls.expand(b + l)
        return ret_list

    def __init__(self, block_string):
        self.verify_block_string(block_string)

        ll = self.base
        bd = self.base_dims
        for i, l in enumerate(block_string):
            bd = bd / self.refinements[i]
            ll = ll + bd * self.offsets[i][self.valid_letters[i].index(l)]
        self.llcorner = ll
        self.dims = bd
        self.string = block_string

    def __str__(self):
        return (f'{self.string} llcorner: '
            f'{self.llcorner[0]:0.0f}, {self.llcorner[1]:0.0f} '
            f'[{self.dims[0]:0.0f} x {self.dims[1]:0.0f}]')

    def __repr__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other.string

    def __neq__(self, other):
        return self.string != other.string

    def bounds(self):
        return self.llcorner[0], \
            self.llcorner[1], \
            self.llcorner[0] + self.dims[0], \
            self.llcorner[1] + self.dims[1]

    def overlaps(self, xmin, ymin, xmax, ymax):
        ur = self.llcorner + self.dims # upper right corner
        if xmax < self.llcorner[0] or ur[0] < xmin or \
            ymax < self.llcorner[1] or ur[1] < ymin:
            return False
        return True

    def divide(self):
        if len(self.string) == len(self.valid_letters):
            return [self]
        else:
            s = self.string
            ret = []
            for l in self.valid_letters[len(s)]:
                ret.append(type(self)(s + l))
            return ret

    def neighbor_(self, dx, dy):
        level = len(self.string)
        cp = self.llcorner + 0.5 * self.dims
        lcp = cp + self.dims * np.array((dx, dy))
        return self.overlapping_blocks(lcp[0], lcp[1], lcp[0], lcp[1], level)

    def left_neighbor(self):
        """
        Return a list of blocks that have the same dimensions as this one
        and contain the point that is the center point of this block
        translated to the left by the width of this block.
        """
        return self.neighbor_(-1, 0)

    def right_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(1, 0)

    def top_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(0, 1)

    def bottom_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(0, -1)

    def top_left_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(-1, 1)

    def top_right_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(1, 1)

    def bottom_left_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(-1, -1)

    def bottom_right_neighbor(self):
        """
        Analogous to left_neighbor()
        """
        return self.neighbor_(1, -1)

    def neighbors(self):
        """
        Return all the neighbor blocks.
        """
        return self.top_left_neighbor() + self.top_neighbor() \
            + self.top_right_neighbor() + self.left_neighbor() \
            + self.right_neighbor() + self.bottom_left_neighbor() \
            + self.bottom_neighbor() + self.bottom_right_neighbor()

    @classmethod
    def overlapping_blocks(cls, xmin, ymin, xmax, ymax, level=0):
        """
        Return a list of blocks that overlap the given extent.

        The level parameter can be used to control the granularity of the
        blocks. Zero means that the smallest blocks are returned.
        """
        ret = [cls(l) for l in cls.valid_letters[0]]
        lvl = 0
        while True:
            lvl += 1
            done = True
            tmp = []
            for block in ret:
                if level == 0 or len(block.string) <= level:
                    if block.overlaps(xmin, ymin, xmax, ymax):
                        if lvl == level:
                            tmp.append(block)
                        else:
                            new_blocks = block.divide()
                            if len(new_blocks) > 1:
                                done = False
                                tmp = tmp + new_blocks
                            else:
                                tmp.append(block)
            ret = tmp
            tmp = []
            if done or lvl == level:
                return ret
