#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

PACKAGE_VERSION = "1.0.1-dev2"
PACKAGE_NAME = "pytest-qatouch"
PACKAGE_AUTHOR = "Mohamed Raslan"
PACKAGE_AUTHOR_EMAIL = "MohamedRaslanG@gmail.com"
PACKAGE_REPO_URL = "https://github.com/MohamedRaslan/pytest-qatouch"

PACKAGE_DESCRIPTION = (
    "Pytest plugin for uploading test results to your QA Touch Testrun."
)


with open("README.md", "r", encoding="utf-8") as file:
    LONG_DESCRIPTION = file.read()

LONG_DESC_TYPE = "text/markdown"

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    url=PACKAGE_REPO_URL,
    description=PACKAGE_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    py_modules=["pytest_pyqatouch"],
    python_requires=">=3.5",
    install_requires=["pytest>=6.2.0", "requests>=2.25.1"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    project_urls={
        "Issue Tracker": PACKAGE_REPO_URL + "/issues",
    },
    keywords=[
        "qatouch",
        "pytest",
        "pytest-qatouch",
        "pytest-pyqatouch",
    ],
    license="MIT License",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Environment :: Plugins",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "pytest11": [
            "pyqatouch = pytest_qatouch.plugin",
        ],
    },
)
