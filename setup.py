# -*- coding:utf-8 -*-
import os
import setuptools

base_dir = os.path.dirname(__file__)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xini",
    version="0.1.0",
    author="Andrew Junzki",
    author_email="andrew.junzki@gmail.com",
    description="A setting manager based on extended INI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Junzki/xini",
    packages=setuptools.find_packages(exclude=('tests', )),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.6',
)
