from setuptools import setup, find_packages

setup(
    name="interactive_subgraph_visualiser",
    version="1.0.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pytest',
        'pandas',
        'numpy',
        'pygame',
        'networkx',
        'scipy',
        'pygame_gui',
        'tk',
        'chardet'
    ],
    entry_points={
        'console_scripts': [
            'interactive_subgraph_visualiser=src.main:main',
        ],
    },
)
