import sys
import os
from os.path import dirname, abspath, join, sep
tests_dir = dirname(dirname(abspath(__file__)))
assert os.path.exists(os.path.join(tests_dir, 'tiling'))
sys.path.insert(0, tests_dir)

import unittest

from tiling.tm35 import TM35Block


class TestTM35Block(unittest.TestCase):

    def test_expand_1(self):
        ret = TM35Block.expand('K3444B')
        self.assertEqual(len(ret), 4)
        self.assertTrue('K3444B1' in ret)
        self.assertTrue('K3444B2' in ret)
        self.assertTrue('K3444B3' in ret)
        self.assertTrue('K3444B4' in ret)

    def test_expand_2(self):
        ret = TM35Block.expand('K3')
        self.assertEqual(len(ret), 2048)

    def test_divide_1(self):
        ret = [a.string for a in TM35Block('K').divide()]
        self.assertEqual(len(ret), 5)
        self.assertTrue('K2' in ret)
        self.assertTrue('K3' in ret)
        self.assertTrue('K4' in ret)
        self.assertTrue('K5' in ret)
        self.assertTrue('K6' in ret)

    def test_divide_2(self):
        ret = [a.string for a in TM35Block('M234').divide()]
        self.assertEqual(len(ret), 4)
        self.assertTrue('M2341' in ret)
        self.assertTrue('M2342' in ret)
        self.assertTrue('M2343' in ret)
        self.assertTrue('M2344' in ret)

    def test_left_neighbour_1(self):
        ret = TM35Block('L4').left_neighbor()
        self.assertEqual(ret.string, 'L3')

    def test_left_neighbour_2(self):
        ret = TM35Block('N421').left_neighbor()
        self.assertEqual(ret.string, 'N343')

    def test_left_neighbour_3(self):
        ret = TM35Block('Q5222A2').left_neighbor()
        self.assertEqual(ret.string, 'Q4444G4')

    def test_top_neighbor_1(self):
        ret = TM35Block('L4').top_neighbor()
        self.assertEqual(ret.string, 'M4')

    def test_top_neighbor_2(self):
        ret = TM35Block('N421').top_neighbor()
        self.assertEqual(ret.string, 'N422')

    def test_top_neighbor_3(self):
        ret = TM35Block('Q5222A2').top_neighbor()
        self.assertEqual(ret.string, 'Q5222B1')

    def test_bottom_neighbor_1(self):
        ret = TM35Block('L4').bottom_neighbor()
        self.assertEqual(ret.string, 'K4')

    def test_bottom_neighbor_2(self):
        ret = TM35Block('N421').bottom_neighbor()
        self.assertEqual(ret.string, 'N412')

    def test_bottom_neighbor_3(self):
        ret = TM35Block('Q5222A2').bottom_neighbor()
        self.assertEqual(ret.string, 'Q5222A1')

    def test_top_left_neighbor_1(self):
        ret = TM35Block('L4').top_left_neighbor()
        self.assertEqual(ret.string, 'M3')

    def test_top_left_neighbor_2(self):
        ret = TM35Block('Q5222A2').top_left_neighbor()
        self.assertEqual(ret.string, 'Q4444H3')

    def test_top_right_neighbor_1(self):
        ret = TM35Block('L4').top_right_neighbor()
        self.assertEqual(ret.string, 'M5')

    def test_top_right_neighbor_2(self):
        ret = TM35Block('Q5222A2').top_right_neighbor()
        self.assertEqual(ret.string, 'Q5222B3')

    def test_bottom_left_neighbor_1(self):
        ret = TM35Block('L4').bottom_left_neighbor()
        self.assertEqual(ret.string, 'K3')

    def test_bottom_left_neighbor_2(self):
        ret = TM35Block('Q5222A2').bottom_left_neighbor()
        self.assertEqual(ret.string, 'Q4444G3')

    def test_bottom_right_neighbor_1(self):
        ret = TM35Block('L4').bottom_right_neighbor()
        self.assertEqual(ret.string, 'K5')

    def test_bottom_right_neighbor_2(self):
        ret = TM35Block('Q5222A2').bottom_right_neighbor()
        self.assertEqual(ret.string, 'Q5222A3')

    def test_overlapping_blocks_1(self):
        ret = TM35Block.overlapping_blocks(308657, 6762534, 308658, 6762535)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0].string, 'M4111A1')

    def test_overlapping_blocks_2(self):
        ret = TM35Block.overlapping_blocks(311145, 6764630, 327533, 6766638)
        self.assertEqual(len(ret), 12)
        codes = [a.string for a in ret]
        self.assertTrue('M4111A3' in codes)
        self.assertTrue('M4111A4' in codes)
        self.assertTrue('M4111C1' in codes)
        self.assertTrue('M4111C2' in codes)
        self.assertTrue('M4111C3' in codes)
        self.assertTrue('M4111C4' in codes)
        self.assertTrue('M4111E1' in codes)
        self.assertTrue('M4111E2' in codes)
        self.assertTrue('M4111E3' in codes)
        self.assertTrue('M4111E4' in codes)
        self.assertTrue('M4111G1' in codes)
        self.assertTrue('M4111G2' in codes)

    def test_overlapping_blocks_3(self):
        ret = TM35Block.overlapping_blocks(
            311145, 6764630, 327533, 6766638, level=6)
        self.assertEqual(len(ret), 4)
        codes = [a.string for a in ret]
        self.assertTrue('M4111A' in codes)
        self.assertTrue('M4111C' in codes)
        self.assertTrue('M4111E' in codes)
        self.assertTrue('M4111G' in codes)

    def test_constructor_01(self):
        ret = TM35Block('M')
        self.assertEqual(ret.llcorner[0], -76000)
        self.assertEqual(ret.llcorner[1], 6762000)
        self.assertEqual(ret.dims[0], 768000)
        self.assertEqual(ret.dims[1], 96000)

    def test_constructor_02(self):
        ret = TM35Block('K3')
        self.assertEqual(ret.llcorner[0], 116000)
        self.assertEqual(ret.llcorner[1], 6570000)
        self.assertEqual(ret.dims[0], 192000)
        self.assertEqual(ret.dims[1], 96000)

    def test_constructor_03(self):
        ret = TM35Block('K31')
        self.assertEqual(ret.llcorner[0], 116000)
        self.assertEqual(ret.llcorner[1], 6570000)
        self.assertEqual(ret.dims[0], 96000)
        self.assertEqual(ret.dims[1], 48000)

    def test_constructor_04(self):
        ret = TM35Block('K34')
        self.assertEqual(ret.llcorner[0], 212000)
        self.assertEqual(ret.llcorner[1], 6618000)
        self.assertEqual(ret.dims[0], 96000)
        self.assertEqual(ret.dims[1], 48000)

    def test_constructor_05(self):
        ret = TM35Block('K344')
        self.assertEqual(ret.llcorner[0], 260000)
        self.assertEqual(ret.llcorner[1], 6642000)
        self.assertEqual(ret.dims[0], 48000)
        self.assertEqual(ret.dims[1], 24000)

    def test_constructor_06(self):
        ret = TM35Block('K3444')
        self.assertEqual(ret.llcorner[0], 284000)
        self.assertEqual(ret.llcorner[1], 6654000)
        self.assertEqual(ret.dims[0], 24000)
        self.assertEqual(ret.dims[1], 12000)

    def test_constructor_07(self):
        ret = TM35Block('K3444H')
        self.assertEqual(ret.llcorner[0], 302000)
        self.assertEqual(ret.llcorner[1], 6660000)
        self.assertEqual(ret.dims[0], 6000)
        self.assertEqual(ret.dims[1], 6000)

    def test_constructor_08(self):
        ret = TM35Block('K3444H4')
        self.assertEqual(ret.llcorner[0], 305000)
        self.assertEqual(ret.llcorner[1], 6663000)
        self.assertEqual(ret.dims[0], 3000)
        self.assertEqual(ret.dims[1], 3000)

    def test_constructor_09(self):
        ret = TM35Block('M4')
        self.assertEqual(ret.llcorner[0], 308000)
        self.assertEqual(ret.llcorner[1], 6762000)
        self.assertEqual(ret.dims[0], 192000)
        self.assertEqual(ret.dims[1], 96000)

    def test_constructor_10(self):
        ret = TM35Block('M44')
        self.assertEqual(ret.llcorner[0], 404000)
        self.assertEqual(ret.llcorner[1], 6810000)
        self.assertEqual(ret.dims[0], 96000)
        self.assertEqual(ret.dims[1], 48000)

    def test_constructor_11(self):
        ret = TM35Block('M444')
        self.assertEqual(ret.llcorner[0], 452000)
        self.assertEqual(ret.llcorner[1], 6834000)
        self.assertEqual(ret.dims[0], 48000)
        self.assertEqual(ret.dims[1], 24000)

    def test_constructor_12(self):
        ret = TM35Block('M441')
        self.assertEqual(ret.llcorner[0], 404000)
        self.assertEqual(ret.llcorner[1], 6810000)
        self.assertEqual(ret.dims[0], 48000)
        self.assertEqual(ret.dims[1], 24000)

    def test_constructor_13(self):
        ret = TM35Block('M4414')
        self.assertEqual(ret.llcorner[0], 428000)
        self.assertEqual(ret.llcorner[1], 6822000)
        self.assertEqual(ret.dims[0], 24000)
        self.assertEqual(ret.dims[1], 12000)

    def test_constructor_14(self):
        ret = TM35Block('M4414H')
        self.assertEqual(ret.llcorner[0], 446000)
        self.assertEqual(ret.llcorner[1], 6828000)
        self.assertEqual(ret.dims[0], 6000)
        self.assertEqual(ret.dims[1], 6000)

    def test_constructor_15(self):
        ret = TM35Block('M4414H4')
        self.assertEqual(ret.llcorner[0], 449000)
        self.assertEqual(ret.llcorner[1], 6831000)
        self.assertEqual(ret.dims[0], 3000)
        self.assertEqual(ret.dims[1], 3000)

    def test_equality_1(self):
        r1 = TM35Block.overlapping_blocks(300001, 6990001, 301000, 6991000)
        r2 = TM35Block.overlapping_blocks(300001, 6990001, 301000, 6991000)
        self.assertEqual(len(r1), 1)
        self.assertEqual(r1[0], r2[0])

    def test_inequality_1(self):
        r1 = TM35Block.overlapping_blocks(300001, 6990001, 301000, 6991000)
        r2 = TM35Block.overlapping_blocks(303001, 6990001, 304000, 6991000)
        self.assertEqual(len(r1), 1)
        self.assertEqual(len(r2), 1)
        self.assertNotEqual(r1[0], r2[0])

    def test_no_overlapping_blocks(self):
        ret = TM35Block.overlapping_blocks(0, 0, 1, 1)
        self.assertEqual(len(ret), 0)

    def test_no_left_neighbor(self):
        ret = TM35Block('L2').left_neighbor()
        self.assertTrue(ret is None)

    def test_neighbors_missing(self):
        ret = TM35Block('L2').neighbors()
        labels = [b.string for b in ret]
        self.assertEqual(len(ret), 5)
        self.assertTrue('K2' in labels)
        self.assertTrue('K3' in labels)
        self.assertTrue('L3' in labels)
        self.assertTrue('M2' in labels)
        self.assertTrue('M3' in labels)


if __name__ == '__main__':
    unittest.main()
