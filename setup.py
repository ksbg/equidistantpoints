from setuptools import setup

setup(
    name='equidistantpoints',
    version='0.4',
    url='https://github.com/ksbg/equidistantpoints',
    author='Kevin Baumgarten',
    author_email='kevin@ksbg.io',
    description='Generates (almost) evenly distributed, equidistant points across a perfect sphere '
                'or the globe (in cartesian, ECEF and geodetic format)',
    packages=['equidistantpoints'],
    entry_points={
        'console_scripts': ['edpoints=equidistantpoints.cli:cli_generate_points']
    },
    download_url='https://github.com/ksbg/equidistantpoints/archive/0.2.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['mathematics', 'geography', 'coordinates', 'equidistant', 'sphere', 'globe', 'earth'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4'
)
