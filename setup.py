import os
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="c7i76e",
    version="0.1.5",
    author="John Thornton",
    author_email="<jt@gnipsel.com>",
    description="Mesa configuration tool for 7i76e",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jethornton/7i76e",
    download_url="https://github.com/jethornton/7i76e/tarball/master",
    python_requires='>=3',
    platforms=['Posix'],
    packages=['c7i76e'],
    include_package_data=True,
    entry_points={
        'gui_scripts': ['c7i76e=c7i76e.c7i76e:main',],
    },
    data_files = [
        ('share/applications/', ['7i76E Configurator.desktop'])
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: Qt",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)
