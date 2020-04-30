import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# list of (destination, source_file) tuples
DATA_FILES = [('~/.local/bin', ['m7i76e/mesaflash64', 'm7i76e/mesaflash32',])]
data_files = [(os.path.expanduser(dest), src_list) for dest, src_list in DATA_FILES]

setup(
    name="7i76e",
    version="0.0.5",
    author="John Thornton",
    author_email="<jt@gnipsel.com>",
    description="Mesa configuration tool for 7i76e",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jethornton/7i76e",
    download_url="https://github.com/jethornton/7i76e/tarball/master",
    python_requires='>=3',
    packages=find_packages(),
    data_files=data_files,
    include_package_data=True,
    entry_points={
        'gui_scripts': ['7i76e=m7i76e.m7i76e:main',],
    },
)

