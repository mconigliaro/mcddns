#!/usr/bin/env python

import os
import setuptools
import updatemyip.meta as meta

setuptools.setup(
    name=meta.NAME,
    version=meta.VERSION,
    author=meta.AUTHOR,
    author_email="mike@conigliaro.org",
    description="Industrial-strength dynamic DNS client",
    long_description=open(os.path.join(
        os.path.dirname(__file__),
        "README.md")).read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mconigliaro/updatemyip",
    packages=setuptools.find_packages(),
    scripts=["bin/updatemyip"],
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
    requires=["boto3 (<2.0, >=1.12)", "requests (< 3.0, >=2.23)"],
)
