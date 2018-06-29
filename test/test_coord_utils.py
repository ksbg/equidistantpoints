"""Tests the mathematical helper functions"""
from unittest import TestCase

from equidistantpoints import coord_utils

ra, er, pr = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]], 6378137.0, 6356752.3


class TestCoordUtils(TestCase):
    def test_dot_product_results(self):
        results = [
            [[4, 3, 2], [2, 3, -4]],
            [[-9.5, 22.23, 3.4], [3.4, 22.23, 9.5]],
            [[23, 44, 97], [97, 44, -23]],
            [[2, 4, 7], [7, 4, -2]]
        ]

        for res in results:
            self.assertEqual(coord_utils.xyz_dot_matrix(res[0], ra), res[1])

    def test_dot_invalid_dimensions(self):
        arguments = [
            [[1, 1, 1, 1], [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]],
            [[1, 1, 1], [[0, 0, 1], [-1, 0, 0]]]
        ]

        for args in arguments:
            self.assertRaises((TypeError, IndexError), coord_utils.xyz_dot_matrix, *args)

    def test_dot_arguments_type(self):
        arguments = [
            [[1, '1', 1], [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]],
            [[1, 1, 1], [[0, 0, 1], [0, 1, 0], [-1, 0, 'zero']]],
            ['test', [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]],
            [[1, 1, 1], 'test']
        ]

        for args in arguments:
            self.assertRaises(TypeError, coord_utils.xyz_dot_matrix, *args)

    def test_linspace_results(self):
        results = [
            [[10, 50, 6],
             [10.0, 18.0, 26.0, 34.0, 42.0, 50.0]],
            [[1, 2000, 6],
             [1.0, 400.8, 800.6, 1200.4, 1600.2, 2000.0]],
            [[414, 25348, 27],
             [414.0, 1373.0, 2332.0, 3291.0, 4250.0, 5209.0, 6168.0, 7127.0, 8086.0, 9045.0,
              10004.0, 10963.0, 11922.0, 12881.0, 13840.0, 14799.0, 15758.0, 16717.0, 17676.0,
              18635.0, 19594.0, 20553.0, 21512.0, 22471.0, 23430.0, 24389.0, 25348.0]],
            [[123445, 5123513, 8],
             [123445.0, 837740.4285714285, 1552035.857142857, 2266331.2857142854, 2980626.714285714,
              3694922.1428571427, 4409217.571428571, 5123513.0]],
            [[1, 99, 5],
             [1.0, 25.5, 50.0, 74.5, 99.0]]
        ]

        for res in results:
            self.assertEqual(coord_utils.linspace(*res[0]), res[1])

    def test_linspace_arguments_type(self):
        arguments = [[1, 1000, '4'], [1, '1000', 4], ['1', 1000, 4]]

        for args in arguments:
            self.assertRaises((TypeError, IndexError), coord_utils.linspace, *args)

    def test_linspace_n_not_positive(self):
        self.assertRaises(ValueError, coord_utils.linspace, 1, 1000, -4)

    def test_cartesian_to_ecef_results(self):
        results = [
            [[0.9732830948042264, -0.09485361020175874, -0.20910000000000006],
             [0.9729955014300911, -0.09482558210802891, -0.21044681792481235]],
            [[-0.44459823051156266, -0.027754700970959778, -0.8953],
             [-0.4422141872630115, -0.0276058735512257, -0.8964845388119017]],
            [[0.717728373321176, -0.15911496513445436, 0.6779],
             [0.7155117676469192, -0.1586235603806696, 0.6803539346920405]],
            [[0.5256372653699255, 0.7446729317320636, -0.4113],
             [0.5250373380026654, 0.7438230116429894, -0.41359777689613886]],
            [[0.40902883446967564, 0.8240811868817166, 0.3919],
             [0.40860490759589346, 0.82322709022188, 0.3941309267405542]]
        ]

        self.assertEqual(coord_utils.cartesian_to_ecef([r[0] for r in results], er, pr, ra),
                         [r[1] for r in results])

    def test_cartesian_to_ecef_argument_types(self):
        arguments = [
            ['test', er, pr, ra],
            [[1, 2, 3], er, pr, ra],
            [[[1, 2, 3], [4, 5, 6]], 'test', pr, ra],
            [[[1, 2, 3], [4, 5, 6]], er, 'test', ra],
            [[[1, 2, 3], [4, 5, 6]], er, pr, 'test']
        ]

        for args in arguments:
            self.assertRaises(TypeError, coord_utils.cartesian_to_ecef, *args)

    def test_cartesian_to_ecef_coordinate_invalid_dimensions(self):
        arguments = [
            [[[1, 2, 3, 4], [5, 6, 7, 8]], er, pr, ra],
            [[[1, 2], [5, 6]], er, pr, ra],
            [[[1, 2, 3], [4, 5, 6]], er, pr, [1, 2, 3]],
            [[[1, 2, 3], [4, 5, 6]], er, pr, [[1, 2, 3], [4, 5, 6]]],
            [[[1, 2, 3], [4, 5, 6]], er, pr, [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]]
        ]

        for args in arguments:
            self.assertRaises((IndexError, TypeError), coord_utils.cartesian_to_ecef, *args)

    def test_ecef_to_geodetic_results(self):
        results = [
            [[0.5205493942317323, 0.017223865552054747, -0.8536578158843399],
             [1.8951033504254897, -58.61177088931026]],
            [[0.9168057992817193, 0.3526783366348541, -0.18731021667778944],
             [21.04081672436105, -10.795852962628583]],
            [[0.3817193025236181, 0.9236918524460724, 0.03292014285548751],
             [67.54694598298178, 1.8865261005893832]],
            [[-0.6514787051302638, 0.7584761203710573, 0.017013864601088124],
             [130.6603059359551, 0.9748696715528735]],
            [[-0.6382320728849917, -0.6176503152726458, -0.45953009605958134],
             [-135.93889547442853, -27.35678961713994]]
        ]

        self.assertEqual(coord_utils.ecef_to_geodetic([r[0] for r in results], ra),
                         [r[1] for r in results])

    def test_ecef_to_geodetic_argument_types(self):
        arguments = [
            ['test', ra],
            [[1, 2, 3], ra],
            [[[1, 2, 3], [4, 5, 6]], 'test'],
            [[[1, 2, 3], [4, 5, 6]], 8]
        ]

        for args in arguments:
            self.assertRaises(TypeError, coord_utils.ecef_to_geodetic, *args)

    def test_ecef_to_geodetic_coordinate_invalid_dimensions(self):
        arguments = [
            [[[1, 2, 3, 4], [5, 6, 7, 8]], ra],
            [[[1, 2], [5, 6]], ra],
            [[[1, 2, 3], [4, 5, 6]], [1, 2, 3]],
            [[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]],
            [[[1, 2, 3], [4, 5, 6]], [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]]
        ]

        for args in arguments:
            self.assertRaises((IndexError, TypeError), coord_utils.ecef_to_geodetic, *args)
