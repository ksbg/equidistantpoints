"""Testing helpers"""
import os
import subprocess
from math import radians, sin, cos, sqrt, atan2
from multiprocessing import Process, Manager, Queue, cpu_count, Lock

try:  # Python 2
    from Queue import Empty
except ImportError:  # Python 3
    from queue import Empty


def __get_nearest_neighbor_distance(point_queue, all_points, dists, lock):
    """
    Calculate nearest-neighbor great-circle distance of each point. Used to test for maximum
    percentage deviation in nearest-neighbor distance.

    Parameters
    ----------
    point_queue : Queue
    all_points : list
        List of generated points
    dists : ListProxy
        Empty ListProxy (generate with Manager().list())
    lock : Lock
        Process lock
    """
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
                    (cos_lat2 * sin_delta_lng) ** 2 + (
                            cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
                    sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)
                if 0 < d < min_d:
                    min_d = d

            with lock:
                dists.append(min_d)
        except Empty:
            break


def calculate_max_nn_distance_percentage_deviation(points):
    """
    Calculate the maximum percentage deviation from the mean nearest-neighbor great-circle distance
    (using multiprocessing)

    Parameters
    ----------
    points : list
    """
    with Manager() as manager:
        distances = manager.list()
        queue = Queue()
        lock = Lock()
        for point in points:
            queue.put(point)

        procs = [
            Process(target=__get_nearest_neighbor_distance, args=(queue, points, distances, lock))
            for _ in range(cpu_count())
        ]

        for p in procs:
            p.start()
        for p in procs:
            p.join()

        distances = list(distances)

    nnd_min, nnd_max, nnd_mean = min(distances), max(distances), sum(distances) / len(distances)
    max_dev = (nnd_mean - nnd_min) if (nnd_mean - nnd_min) < (nnd_max - nnd_mean) else (
            nnd_max - nnd_mean)
    perc_dev = max_dev / nnd_mean

    return perc_dev


def subprocess_call(cmd):
    """
    Spawns a subprocess and executes command

    Parameters
    ----------
    cmd : list
        Command to be executed (see subprocess docs)
    """
    with open(os.devnull, 'wb') as devnull:
        subprocess.call(cmd, stdout=devnull, stderr=subprocess.STDOUT)
