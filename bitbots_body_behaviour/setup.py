# -*- coding:utf-8 -*-
from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
    packages=['bitbots_body_behaviour'],
    #scripts=['bin/myscript'],
    package_dir={'': 'src'}
)

setup(**d)
