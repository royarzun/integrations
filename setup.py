from distutils.core import setup

import setuptools

setup(
    name="loyalty_integrations",
    version="0.4dev",
    packages=setuptools.find_packages(),
    license="",
    long_description=open("README.md").read(),
    install_requires=["Flask"],
)
