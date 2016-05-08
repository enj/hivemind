#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hivemind setup."""

from setuptools import setup

packages = [
    "hivemind",
    "hivemind.mpi",
    "hivemind.pipeline",
]

requires = ["networkx>=1.11", "mpi4py>=2.0.0"]

version = "0.1.0"

setup(
    name="hivemind",
    version=version,
    description="A generic system for running medical pipelines.",
    author="Monis Khan, Hussein Koprly, Sarah Baucom",
    author_email="{mmkhan2,hakoprly,srbaucom}@ncsu.edu",
    url="https://github.com/enj/hivemind",
    packages=packages,
    package_dir={"hivemind": "hivemind"},
    install_requires=requires,
    license="Apache 2.0",
    zip_safe=False,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: System :: Distributed Computing",
    ),
)
