#!/usr/bin/env python

import os
import setuptools
import mcddns.meta as meta

setuptools.setup(
    name=meta.NAME,
    version=meta.VERSION,
    author=meta.AUTHOR,
    author_email="mike@conigliaro.org",
    description=meta.DESCRIPTION,
    long_description=open(os.path.join(
        os.path.dirname(__file__),
        "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mconigliaro/mcddns",
    packages=setuptools.find_packages(),
    scripts=["bin/mcddns"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Systems Administration"
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3 >=1.12, <2.0",
        "requests >=2.23, <3.0"
    ],
)
