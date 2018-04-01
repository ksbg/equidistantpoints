from __future__ import division

import csv
import json
from math import pi, sqrt, cos, sin

from . import math_utils


class EquidistantPoints:
    def __init__(self, n_points, equatorial_radius=6378137.0, polar_radius=6356752.3):
        """
        Generates (almost) equally distributed point coordinates on the globe in cartesian format and converts them
        to both ECEF (earth-centered-earth-fixed) and geodetic (longitude/latitude) format.
        
        Args:
            n_points (int): Number of points to be generated
            equatorial_radius (float): Earth's radius on the equator in meters (default taken from WGS-84 system)
            polar_radius (float): Earth's polar radius in meters (default taken from WGS-84 system)
        """
        if n_points <= 2:
            raise ValueError('`n_points` must be larger than 2')

        rotation_axis = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]  # Taken from Gade (2010)

        self.cartesian = self.__generate_points(n=n_points)
        self.ecef = math_utils.cartesian_to_ecef(coordinates=self.cartesian, equatorial_radius=equatorial_radius,
                                                 polar_radius=polar_radius, rotation_axis=rotation_axis)
        self.geodetic = math_utils.ecef_to_geodetic(coordinates=self.ecef, rotation_axis=rotation_axis)

    def __generate_points(self, n):
        """
        Generates a list of equidistant points on a perfect sphere in cartesian format
        
        Returns:
            List[List[float]]: List of cartesian [x, y, z] coordinates
        """
        golden_angle = pi * (3 - sqrt(5))
        theta = [golden_angle * i for i in range(0, n)]
        z_vals = math_utils.linspace(1 - 1.0 / n, 1.0 / n - 1, n)
        radius = [sqrt(1 - i * i) for i in z_vals]
        x_vals = [r * cos(t) for r, t in zip(radius, theta)]
        y_vals = [r * sin(t) for r, t in zip(radius, theta)]
        cartesian = list(zip(x_vals, y_vals, z_vals))

        return cartesian

    def __write_to_csv(self, file_path, coordinates, header):
        with open(file_path, 'wb') as target_file:
            writer = csv.writer(target_file)
            if header:
                writer.writerow(header)
            for coordinate in coordinates:
                writer.writerow(coordinate)

    def write_geodetic_to_csv(self, file_path, header=True):
        if header:
            header = ['longitude', 'latitude']

        self.__write_to_csv(file_path=file_path, coordinates=self.geodetic, header=header)

    def write_cartesian_to_csv(self, file_path, header=True):
        if header:
            header = ['x', 'y', 'z']

        self.__write_to_csv(file_path=file_path, coordinates=self.cartesian, header=header)

    def write_ecef_to_csv(self, file_path, header=True):
        if header:
            header = ['x', 'y', 'z']

        self.__write_to_csv(file_path=file_path, coordinates=self.ecef, header=header)

    def write_geodetic_to_geojson(self, file_path):
        with open(file_path, 'wb') as target_file:
            json.dump({'type': 'MultiPoint', 'coordinates': self.geodetic}, target_file)
