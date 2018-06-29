"""The main module where all the magic happens."""
from __future__ import division

import csv
import json

from . import coord_utils


class EquidistantPoints(object):
    """Generates (almost) equally distributed point coordinates on the globe in cartesian format
       and converts them to both ECEF (earth-centered-earth-fixed) and geodetic
       (longitude/latitude) format."""
    def __init__(self, n_points, equatorial_radius=6378137.0, polar_radius=6356752.3):
        """
        Parameters
        ----------
        n_points : int
            Number of points to be generated
        equatorial_radius : float
            Earth's radius on the equator in meters (default taken from WGS-84 system)
        polar_radius : float
            Earth's polar radius in meters (default taken from WGS-84 system)
        """
        if n_points <= 2:
            raise ValueError('`n_points` must be larger than 2')

        rotation_axis = [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]  # Taken from Gade (2010)

        self.cartesian = coord_utils.generate_points(n_points=n_points)
        self.ecef = coord_utils.cartesian_to_ecef(coordinates=self.cartesian,
                                                  equatorial_radius=equatorial_radius,
                                                  polar_radius=polar_radius,
                                                  rotation_axis=rotation_axis)
        self.geodetic = coord_utils.ecef_to_geodetic(coordinates=self.ecef,
                                                     rotation_axis=rotation_axis)

    def __write_to_csv(self, file_path, coord_type, header=None):
        """
        Write coordinates to CSV

        Parameters
        ----------
        file_path : str
            Path to which the CSV should be written
        coord_type : str
            The coordinate type to be written ('geodetic' | 'cartesian' | 'ecef')
        header : list
            The header row to be written
        """
        if coord_type == 'geodetic':
            coordinates = self.geodetic
        elif coord_type == 'cartesian':
            coordinates = self.cartesian
        elif coord_type == 'ecef':
            coordinates = self.ecef
        else:
            raise ValueError('Argument `coord_type` must be one of: `geodetic`, `cartesian, `ecef`')

        with open(file_path, 'w') as target_file:
            writer = csv.writer(target_file)
            if header:
                writer.writerow(header)
            for coordinate in coordinates:
                writer.writerow(coordinate)

    def write_geodetic_to_csv(self, file_path, header=True):
        """
        Write geodetic coordinates to CSV

        Parameters
        ----------
        file_path : str
            Path to the output file
        header : bool
            Indicates if a header row shall be written
        """
        if header:
            header = ['longitude', 'latitude']

        self.__write_to_csv(file_path=file_path, coord_type='geodetic', header=header)

    def write_cartesian_to_csv(self, file_path, header=True):
        """
        Write cartesian coordinates to CSV

        Parameters
        ----------
        file_path : str
            Path to the output file
        header : bool
            Indicates if a header row shall be written
        """
        if header:
            header = ['x', 'y', 'z']

        self.__write_to_csv(file_path=file_path, coord_type='cartesian', header=header)

    def write_ecef_to_csv(self, file_path, header=True):
        """
        Write ECEF coordinates to CSV

        Parameters
        ----------
        file_path : str
            Path to the output file
        header : bool
            Indicates if a header row shall be written
        """
        if header:
            header = ['x', 'y', 'z']

        self.__write_to_csv(file_path=file_path, coord_type='ecef', header=header)

    def write_geodetic_to_geojson(self, file_path):
        """
        Write geodetic coordinates to GeoJSON

        Parameters
        ----------
        file_path : str
            Path to the output file
        """
        with open(file_path, 'w') as target_file:
            json.dump({'type': 'MultiPoint', 'coordinates': self.geodetic}, target_file)
