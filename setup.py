try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "analysis",
    version = "0.1",
    author = "Christoph Sawade",
    description = ("Utility functions for iPython notebooks."),
    packages=['projects','tests'],
    install_requires=['nose']
)
