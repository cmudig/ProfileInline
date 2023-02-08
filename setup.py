#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages
from pathlib import Path

from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)

HERE = Path(__file__).parent.resolve()


# The name of the project
name = 'diginlineprofiler'

# Get the version
version = get_version(pjoin(name, '_version.py'))

with open((HERE / "requirements.txt")) as fp:
    install_requires = fp.read()

# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, 'nbextension', 'index.js'),
    pjoin(HERE, 'lib', 'index.js'),
]


package_data_spec = {
    name: [
        'nbextension/**js*',
        'labextension/**'
    ]
}


data_files_spec = [
    ('share/jupyter/nbextensions/diginlineprofiler',
     'diginlineprofiler/nbextension', '**'),
    ('share/jupyter/labextensions/diginlineprofiler',
     'diginlineprofiler/labextension', '**'),
    ('share/jupyter/labextensions/diginlineprofiler',
     '.', 'install.json'),
    ('etc/jupyter/nbconfig/notebook.d', '.',
     'diginlineprofiler.json'),
]


cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(HERE, build_cmd='build:prod'),
    ensure_targets(jstargets),
)


setup_args = dict(
    name=name,
    description='Inline data profiles',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_packages(),
    author='Will Epperson',
    author_email='willepp@cmu.edu',
    url='https://github.com/cmudig/ProfileInline',
    license='BSD',
    platforms="Linux, Mac OS X, Windows",
    keywords=['Jupyter', 'Widgets', 'IPython'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Jupyter',
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={
        'examples': [
            # Any requirements for the examples to run
        ],
        'docs': [
            'jupyter_sphinx',
            'nbsphinx',
            'nbsphinx-link',
            'pytest_check_links',
            'pypandoc',
            'recommonmark',
            'sphinx>=1.5',
            'sphinx_rtd_theme',
        ],
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
