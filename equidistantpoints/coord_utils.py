"""Various math helper functions"""
from __future__ import division
from math import sqrt, atan2, degrees, pi, cos, sin


def generate_points(n_points):
    """
    Generates a list of equidistant points on a perfect sphere in cartesian format

    Parameters
    ----------
    n_points : int
        Number of points to generate
    """
    golden_angle = pi * (3 - sqrt(5))
    theta = [golden_angle * i for i in range(0, n_points)]
    z_vals = linspace(1 - 1.0 / n_points, 1.0 / n_points - 1, n_points)
    radius = [sqrt(1 - i * i) for i in z_vals]
    x_vals = [r * cos(t) for r, t in zip(radius, theta)]
    y_vals = [r * sin(t) for r, t in zip(radius, theta)]
    cartesian = list(zip(x_vals, y_vals, z_vals))

    return cartesian


def cartesian_to_ecef(coordinates, equatorial_radius, polar_radius, rotation_axis):
    """
    Projects cartesian coordinates onto earth's ellipsoid. Results in ECEF coordinates
    (earth-centered-earth-fixed).

    Based on equation 23 in
        Gade (2010) A Non-Singular Horizontal Position Representation

    Parameters
    ----------
    coordinates : list
        List of cartesian [x, y, z] coordinates
    equatorial_radius : float
        Earth's radius on the equator in meters
    polar_radius : float
        Earth's polar radius in meters
    rotation_axis : list
        Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
        see Gade (2010) for a detailed explanation

    Returns
    -------
    list
        List of ECEF [x, y, z] coordinates
    """
    ecef_coordinates = []

    flattened = (equatorial_radius - polar_radius) / equatorial_radius
    e_squared = flattened * 2 - flattened ** 2
    for coord in coordinates:
        coord = [equatorial_radius * c for c in coord]
        coord = xyz_dot_matrix(coord, rotation_axis)
        rr_squared = coord[1] ** 2 + coord[2] ** 2
        rr = sqrt(rr_squared)

        p = rr_squared / equatorial_radius ** 2
        q = (1 - e_squared) / equatorial_radius ** 2 * coord[0] ** 2
        r = (p + q - e_squared ** 2) / 6
        s = e_squared ** 2 * p * q / (4 * r ** 3)
        t = (1 + s + sqrt(s * (2 + s))) ** (1/3)
        u = r * (1 + t + 1.0 / t)
        v = sqrt(u ** 2 + e_squared ** 2 * q)
        w = e_squared * (u + v - q) / (2 * v)
        k = sqrt(u + v + w ** 2) - w

        pre = 1 / sqrt((k * rr / (k + e_squared)) ** 2 + coord[0] ** 2)
        xyz = [pre * coord[0],
               pre * k / (k + e_squared) * coord[1],
               pre * k / (k + e_squared) * coord[2]]
        ra_rev = [[row[i] for row in rotation_axis] for i in range(len(rotation_axis[0]))]
        pt_dot = xyz_dot_matrix(xyz, ra_rev)
        pt_norm = sqrt(sum([a ** 2 for a in xyz]))
        unit_point = [p / pt_norm for p in pt_dot]
        ecef_coordinates.append(unit_point)

    return ecef_coordinates


def ecef_to_geodetic(coordinates, rotation_axis):
    """
    Converts ECEF [x, y, z] coordinates to geodetic [longitude, latitude] coordinates.

    Based on equation 5 and 6 in
        Gade (2010) A Non-Singular Horizontal Position Representation

    Parameters
    ----------
    coordinates : list
        List of ECEF [x, y, z] coordinates
    rotation_axis : list
        Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
        see Gade (2010) for a detailed explanation

    Returns
    -------
    list
        List of geodetic [longitude, latitude] coordinates
    """
    geodetic_coordinates = []

    for coord in coordinates:
        coord_dot = xyz_dot_matrix(coord, rotation_axis)
        lon_rad = atan2(coord_dot[1], -coord_dot[2])
        eq_comp = sqrt(coord_dot[1] ** 2 + coord_dot[2] ** 2)
        lat_rad = atan2(coord_dot[0], eq_comp)
        geodetic_coordinates.append([degrees(lon_rad), degrees(lat_rad)])

    return geodetic_coordinates


def linspace(start, stop, n):
    """
    Generates evenly spaced values over an interval

    Parameters
    ----------
    start : int
        Starting value
    stop : int
        End value
    n : int
        Number of values

    Returns
    -------
    list
        Sequence of evenly spaced values
    """
    if n < 0:
        raise ValueError('`n` must be a positive integer.')

    def __generate():
        if n == 1:
            yield stop
            return
        h = (stop - start) / (n - 1)
        for i in range(n):
            yield start + h * i

    return list(__generate())


def xyz_dot_matrix(coordinate, rotation_axis):
    """
    Calculates the dot matrix of a coordinate * rotation axis

    Parameters
    ----------
    coordinate : list
        Coordinate to be multiplied with rotation axis
    rotation_axis : list
        Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
        see Gade (2010) for a detailed explanation

    Returns
    -------
    list
        Matrix A * Matrix B
    """
    result = []

    for i in range(len(coordinate)):
        total = 0
        for j in range(len(rotation_axis[0])):
            total += coordinate[j] * rotation_axis[i][j]

        result.append(total)

    return result

