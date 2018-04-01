from __future__ import division
from math import sqrt, atan2, degrees


def cartesian_to_ecef(coordinates, equatorial_radius, polar_radius, rotation_axis):
    """
    Projects cartesian coordinates onto earth's ellipsoid. Results in ECEF coordinates (earth-centered-earth-fixed).
    
    Based on equation 23 in
        Gade (2010) A Non-Singular Horizontal Position Representation
    
    Args:
        coordinates (List[List[float]]): List of cartesian [x, y, z] coordinates
        equatorial_radius (float): Earth's radius on the equator in meters
        polar_radius (float): Earth's polar radius in meters
        rotation_axis (List[List[int]]): Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
                                         see Gade (2010) for a detailed explanation
    
    Returns:
        List[List[float]]: List of ECEF [x, y, z] coordinates
    """
    ecef_coordinates = []

    flattened = (equatorial_radius - polar_radius) / equatorial_radius
    e_squared = flattened * 2 - flattened ** 2
    for coord in coordinates:
        coord = list(map(lambda c: equatorial_radius * c, coord))
        coord = xyz_dot_matrix(coord, rotation_axis)
        rr_squared = coord[1] ** 2 + coord[2] ** 2
        rr = sqrt(rr_squared)
        p = rr_squared / equatorial_radius ** 2
        q = (1 - e_squared) / equatorial_radius ** 2 * coord[0] ** 2
        r = (p + q - e_squared ** 2) / 6
        s = e_squared ** 2 * p * q / (4 * r ** 3)
        t = (1 + s + sqrt(s * (2 + s))) ** 0.3333333333333333
        u = r * (1 + t + 1.0 / t)
        v = sqrt(u ** 2 + e_squared ** 2 * q)
        w = e_squared * (u + v - q) / (2 * v)
        k = sqrt(u + v + w ** 2) - w
        d = k * rr / (k + e_squared)
        tmp = 1 / sqrt(d ** 2 + coord[0] ** 2)
        x = tmp * coord[0]
        y = tmp * k / (k + e_squared) * coord[1]
        z = tmp * k / (k + e_squared) * coord[2]
        ra_rev = [[row[i] for row in rotation_axis] for i in range(len(rotation_axis[0]))]
        pt_dot = xyz_dot_matrix([x, y, z], ra_rev)
        pt_norm = sqrt(sum([a ** 2 for a in [x, y, z]]))
        unit_point = [p / pt_norm for p in pt_dot]
        ecef_coordinates.append(unit_point)

    return ecef_coordinates


def ecef_to_geodetic(coordinates, rotation_axis):
    """
    Converts ECEF [x, y, z] coordinates to geodetic [longitude, latitude] coordinates.
    
    Based on equation 5 and 6 in
        Gade (2010) A Non-Singular Horizontal Position Representation
    
    Args:
        coordinates (List[List[float]]): List of ECEF [x, y, z] coordinates
        rotation_axis (List[List[int]]): Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
                                         see Gade (2010) for a detailed explanation
    
    Returns:
        List[List[float]]: List of geodetic [longitude, latitude] coordinates
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
    
    Args:
        start (int): Starting value
        stop (int): End value
        n (int): Number of values
    
    Returns:
        List: Sequence of evenly spaced values
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
    
    Args:
        coordinate (List[float]): Coordinate to be multiplied with rotation axis
        rotation_axis (List[List[float]]): Rotation axis in format [[?, ?, ?], [?, ?, ?], [?, ?, ?]]
                                           see Gade (2010) for a detailed explanation
    
    Returns:
        List[List]: Matrix A * Matrix B
    """
    result = []

    for i in range(len(coordinate)):
        total = 0
        for j in range(len(rotation_axis[0])):
            total += coordinate[j] * rotation_axis[i][j]

        result.append(total)

    return result
