# setup.py
from setuptools import setup, find_packages

setup(
    name="CSCK541-EOM-Group-A",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add any project dependencies here
        # 'somepackage>=1.0.0',
    ],
    # other relevant metadata, like author, license, etc.
)
