"""Command-line usage of the package"""
from argparse import ArgumentParser

from . import EquidistantPoints


def parse_args():
    """Command-line arguments parsing"""
    parser = ArgumentParser()
    parser.add_argument(
        'n_points',
        help='Number of points to be generated',
        metavar='N',
        type=int
    )

    parser.add_argument(
        '-f', '--file-name',
        help='Path to a file for the result to be stored.',
        type=str
    )

    parser.add_argument(
        '-r', '--equatorial-radius',
        type=float,
        help='Specify a custom equatorial radius (default: WGS-84 standard)',
        default=6378137.0)
    parser.add_argument(
        '-p', '--polar-radius',
        type=float,
        help='Specify a custom polar radius (default: WGS-84 standard)',
        default=6356752.3)

    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        '-g', '--geojson',
        action='store_true',
        help='Indicates that the output should be stored in GeoJSON format (default: CSV)')
    type_group.add_argument(
        '-c', '--cartesian',
        action='store_true',
        help='Indicates that the coordinates to be stored should be in cartesian format '
             '(default: geodetic)',
    )
    type_group.add_argument(
        '-e', '--ecef',
        action='store_true',
        help='Indicates that the coordinates to be stored should be in ECEF format '
             '(default: geodetic)',
    )

    args = parser.parse_args().__dict__

    if args['geojson'] and not args['file_name']:
        parser.error('If `-g`/`--geojson` is given, `-f`/`--file-name` must also be specified.')

    return args


def cli_generate_points():
    """Command-line entry function"""
    args = parse_args()
    ed_points = EquidistantPoints(n_points=args['n_points'],
                                  equatorial_radius=args['equatorial_radius'],
                                  polar_radius=args['polar_radius'])

    if args['file_name']:
        if args['geojson']:
            ed_points.write_geodetic_to_geojson(file_path=args['file_name'])
        elif args['cartesian']:
            ed_points.write_cartesian_to_csv(file_path=args['file_name'])
        elif args['ecef']:
            ed_points.write_ecef_to_csv(file_path=args['file_name'])
        else:
            ed_points.write_geodetic_to_csv(file_path=args['file_name'])
    else:
        print(ed_points.cartesian if args['cartesian'] else ed_points.ecef
              if args['ecef'] else ed_points.geodetic)
