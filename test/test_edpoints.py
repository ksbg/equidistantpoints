"""Tests the generation of points"""
from __future__ import division

import csv
import json
import os
from multiprocessing import freeze_support
from tempfile import mkstemp
from unittest import TestCase

from equidistantpoints import EquidistantPoints
from .helpers import calculate_max_nn_distance_percentage_deviation, subprocess_call

try:  # Python 2
    from Queue import Empty
except ImportError:  # Python 3
    from queue import Empty


class TestDistanceFluctuation(TestCase):
    def setUp(self):
        if os.name == 'nt':  # Windows fix
            freeze_support()

    def test_max_percentage_deviation_less_than_4_percent(self):
        for i in [3, 10, 100, 1000, 10000]:
            self.assertLessEqual(
                calculate_max_nn_distance_percentage_deviation(EquidistantPoints(i).geodetic), 0.04)

    def test_edpoints_npoints_less_than_3(self):
        for i in [-1, 0, 1, 2]:
            self.assertRaises(ValueError, EquidistantPoints, i)

    def test_edpoints_arguments_type(self):
        arguments = [['test', 1000.123, 10000.456],
                     [100, 'test', 10000.456],
                     [100, 1000.123, 'test']]
        for args in arguments:
            self.assertRaises(TypeError, EquidistantPoints, *args)


class TestPointGeneration(TestCase):
    @classmethod
    def setUpClass(cls):
        curdir = os.path.dirname(os.path.abspath(__file__))

        # Create temporary output files
        tmp_files = [path for _, path in (mkstemp() for _ in range(4))]
        cls.files = {
            'cartesian_out': tmp_files[0],
            'cartesian_expected': os.path.join(curdir, 'out', 'cartesian_1000.csv'),
            'ecef_out': tmp_files[1],
            'ecef_expected': os.path.join(curdir, 'out', 'ecef_1000.csv'),
            'geodetic_csv_out': tmp_files[2],
            'geodetic_csv_expected': os.path.join(curdir, 'out', 'geodetic_1000.csv'),
            'geodetic_json_out': tmp_files[3],
            'geodetic_json_expected': os.path.join(curdir, 'out', 'geodetic_1000.json'),
        }

        subprocess_call(['pip', 'install', '--upgrade', '--force-reinstall',
                         os.path.join(curdir, '..')])

    def __csv_compare(self, out_file, expected_file):
        with open(out_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            out_data = [row for row in reader]
        with open(expected_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            expected_data = [row for row in reader]

        for out, expected in zip(out_data, expected_data):
            for a, b in zip(out, expected):
                self.assertAlmostEqual(float(a), float(b))

    def test_cartesian_to_csv(self):
        subprocess_call(['edpoints', '1000', '-c', '-f',
                         self.files['cartesian_out']])
        self.__csv_compare(self.files['cartesian_out'], self.files['cartesian_expected'])

    def test_ecef_to_csv(self):
        subprocess_call(['edpoints', '1000', '-e', '-f',
                         self.files['ecef_out']])
        self.__csv_compare(self.files['ecef_out'], self.files['ecef_expected'])

    def test_geodetic_to_csv(self):
        subprocess_call(['edpoints', '1000', '-f',
                         self.files['geodetic_csv_out']])
        self.__csv_compare(self.files['geodetic_csv_out'], self.files['geodetic_csv_expected'])

    def test_geodetic_to_json(self):
        subprocess_call(['edpoints', '1000', '-g', '-f',
                         self.files['geodetic_json_out']])

        with open(self.files['geodetic_json_out'], 'r') as out_file:
            out_data = json.load(out_file)
        with open(self.files['geodetic_json_expected'], 'r') as out_file:
            expected_data = json.load(out_file)

        for out, expected in zip(out_data['coordinates'], expected_data['coordinates']):
            for a, b in zip(out, expected):
                self.assertAlmostEqual(float(a), float(b))

    @classmethod
    def tearDownClass(cls):
        for tmps in ('cartesian_out', 'ecef_out', 'geodetic_csv_out', 'geodetic_json_out'):
            os.remove(cls.files[tmps])
