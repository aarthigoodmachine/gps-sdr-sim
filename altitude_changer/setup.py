
from distutils.core import setup

setup(
    name='altitude_changer',
    version='0.1dev',
    packages=["altitude_changer"],
    package_dir={"altitude_changer": "src"},
    long_description=open('README.md').read(),
    install_requires=[
        "requests",
        "urllib3==1.26.6",
        "numpy"
    ],
)