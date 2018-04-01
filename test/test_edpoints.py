from __future__ import division

import os
from math import radians, sin, cos, sqrt, atan2
from multiprocessing import Process, Manager, Queue, cpu_count, Lock, freeze_support
from unittest import TestCase

from edpoints import EquidistantPoints

try:  # Python 2
    from Queue import Empty
except ImportError:  # Python 3
    from queue import Empty


def get_nearest_neighbor_distance(point_queue, all_points, dists, lock):
    """Calculate nearest-neighbor great-circle distance of each point"""
    while True:
        try:
            point = point_queue.get_nowait()
            min_d = float('inf')
            for point2 in all_points:
                lon1, lat1 = [radians(p) for p in point]
                lon2, lat2 = [radians(p) for p in point2]
                sin_lat1, cos_lat1 = sin(lat1), cos(lat1)
                sin_lat2, cos_lat2 = sin(lat2), cos(lat2)
                delta_lng = lon2 - lon1
                cos_delta_lng, sin_delta_lng = cos(delta_lng), sin(delta_lng)
                d = 6372.795 * atan2(sqrt(
                    (cos_lat2 * sin_delta_lng) ** 2 + (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
                    sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)
                if 0 < d < min_d:
                    min_d = d

            with lock:
                dists.append(min_d)
        except Empty:
            break


def calculate_max_nn_distance_percentage_deviation(points):
    """Calculate the maximum percentage deviation from the mean nearest-neighbor great-circle distance (using
    multiprocessing)"""
    with Manager() as manager:
        distances = manager.list()
        queue = Queue()
        lock = Lock()
        for point in points:
            queue.put(point)

        procs = [Process(target=get_nearest_neighbor_distance, args=(queue, points, distances, lock))
                 for _ in range(cpu_count())]

        for p in procs:
            p.start()
        for p in procs:
            p.join()

        distances = list(distances)

    nnd_min, nnd_max, nnd_mean = min(distances), max(distances), sum(distances) / len(distances)
    max_dev = (nnd_mean - nnd_min) if (nnd_mean - nnd_min) < (nnd_max - nnd_mean) else (nnd_max - nnd_mean)
    perc_dev = max_dev / nnd_mean

    return perc_dev


class TestDistanceFluctuation(TestCase):
    def setUp(self):
        if os.name == 'nt':
            freeze_support()

    def test_max_percentage_deviation_less_than_4_percent(self):
        for i in [3, 10, 100, 1000, 10000]:
            self.assertLessEqual(calculate_max_nn_distance_percentage_deviation(EquidistantPoints(i).geodetic), 0.04)

    def test_edpoints_npoints_less_than_3(self):
        for i in [-1, 0, 1, 2]:
            self.assertRaises(ValueError, EquidistantPoints, i)

    def test_edpoints_arguments_type(self):
        arguments = [['test', 1000.123, 10000.456], [100, 'test', 10000.456], [100, 1000.123, 'test']]
        for args in arguments:
            self.assertRaises(TypeError, EquidistantPoints, *args)
