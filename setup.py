from setuptools import setup

setup(
    name='equidistantpoints',
    version='0.3',
    url='https://github.com/ksbg/equidistantpoints',
    author='Kevin Baumgarten',
    author_email='kevin@ksbg.io',
    description='Generates (almost) evenly distributed, equidistant points across a perfect sphere '
                'or the globe (in cartesian, ECEF and geodetic format)',
    packages=['equidistantpoints'],
    entry_points={
        'console_scripts': ['edpoints=equidistantpoints.command_line:cli_generate_points']
    },
    download_url='https://github.com/ksbg/equidistantpoints/archive/0.2.tar.gz',
    keywords=['mathematics', 'geography', 'coordinates', 'equidistant', 'sphere', 'globe', 'earth']
)
