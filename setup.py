from setuptools import setup

setup(
    name='edpoints',
    version='0.0.1',
    url='https://github.com/ksbg/equidistant-points',
    author='Kevin Baumgarten',
    author_email='kevin@ksbg.io',
    description='Generates geographic coordinates on a perfect sphere or the globe with an almost equal distance '
                'between them (in cartesian, ECEF and geodetic format)',
    packages=['edpoints']
)
