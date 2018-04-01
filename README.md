## Description
This is a python module which generates (almost) evenly distributed, equidistant points across a perfect sphere or the globe.

While it is impossible to achieve a *truly* equidistant distribution of more than 5 points on a sphere, the implementation in this module
comes close (the maximum percentage deviation is always below 3.5%, and usually much less).

Other more accurate methods exist, but they are often highly inefficient (unlike the method used in this module). An example would be to continuously repel points from their
nearest neighbor until a threshold is reached.

#### Why?
I imagine there's a multitude of possible use-cases, but I initially wrote this module to feature engineer data for machine learning purposes.
More specifically, I wanted an even distribution of points across planet earth, so that I can assign global coordinates to their nearest neighbor among the
generated points.

## Install

Using pip:

    pip install edpoints

## Usage

Generate and store 10.000 equidistant points:

    from edpoints import EquidistantPoints

    points = EquidistantPoints(n_points=10000)

    # Access coordinates in cartesian format
    points.cartesian

    # Access coordinates in ECEF format
    points.ecef

    # Access coordinates in geodetic format
    points.geodetic

    # Write to file
    points.write_cartesian_to_csv('cartesian.csv', header=True)
    points.write_ecef_to_csv('ecef.csv', header=True)
    points.write_geodetic_to_csv('geodetic.csv', header=True)
    points.write_geodetic_to_geojson('geodetic.json')

Custom equatorial and polar radii can be supplied at the point of instantiation. The defaults are taken from the [WGS-84](https://en.wikipedia.org/wiki/World_Geodetic_System) standard.

#### Console usage
The module can also be used from console:

    usage: python -m edpoints [-h] [-f FILE_NAME] [-r EQUATORIAL_RADIUS]
                              [-p POLAR_RADIUS] [-g | -c | -e]
                              N

    positional arguments:
      N                     Number of points to be generated

    optional arguments:
      -h, --help            show help message
      -f FILE_NAME, --file-name FILE_NAME
                            Path to a file for the result to be stored.
      -r EQUATORIAL_RADIUS, --equatorial-radius EQUATORIAL_RADIUS
                            Specify a custom equatorial radius (default: WGS-84
                            standard)
      -p POLAR_RADIUS, --polar-radius POLAR_RADIUS
                            Specify a custom polar radius (default: WGS-84
                            standard)
      -g, --geojson         Indicates that the output should be stored in GeoJSON
                            format (default: CSV)
      -c, --cartesian       Indicates that the coordinates should be given
                            in cartesian format (default: geodetic)
      -e, --ecef            Indicates that the coordinates should be given
                            in ECEF format (default: geodetic)

Example: Generate and print 1000 points in geodetic format (longitude, latitude)

    python -m edpoints 1000

Example: Generate and print 1000 points in cartesian format

    python -m edpoints 1000 -c

Example: Generate and print 1000 points in ECEF format with custom radii, and write to file as csv

    python -m edpoints 1000 -e --equatorial-radius 999.999 --polar-radius 999.999 --file-name ecef.csv

Example: Generate 1000 points and write to file as geojson (only geodetic can be stored as geojson)

    python -m edpoints 1000 -g --file-name geodetic.json


## Running tests

Simply run ```python -m unittest discover -v``` in the project root.

## Theory
The following steps are taken during point generation:

1. *The desired number of points are evenly distributed on a perfect sphere, resulting in cartesian coordinates*

    This is an implementation of the method laid out in the paper *Fibonacci grids: A novel approach to global modelling* by [Swinbank & Pursor (2006)](#references). Simplified, it works by drawing
	[Golden Spirals](https://en.wikipedia.org/wiki/Golden_spiral) on perfect spheres and
	distributing the points on those, resulting in a pattern similar to what can be seen on a sun flower.

2.  *Cartesian coordinates are projected onto earth's ellipsoid, resulting in ECEF coordinates
(earth-centered-earth-fixed)*

    Based on equation 23 from *A Non-Singular Horizontal Position Representation* by [Gade (2010)](#references).

3. *ECEF coordinates are converted to geodetic format (longitude, latitude)*

	Based on equation 5 and 6 from [Gade (2010)](#references).

## References
Swinbank & Pursor (2006) *Fibonacci grids: A novel approach to global modelling*
http://onlinelibrary.wiley.com/doi/10.1256/qj.05.227/pdf

Gade (2010) *A Non-Singular Horizontal Position Representation*
http://www.navlab.net/Publications/A_Nonsingular_Horizontal_Position_Representation.pdf