# File: setup.py
# ---
# This script sets up the nz_test package, including dependencies and entry points.
# It uses setuptools to package the application, making it easy to install and distribute.
# The package includes a command-line interface for running tests, and it specifies dependencies
# such as PyYAML for reading YAML test definitions and Jinja2 for templating HTML reports.
# The setup script also defines metadata such as the package name, version, author, and
# a brief description of the package. It ensures compatibility with Python 3.7 and above
# and includes classifiers for categorizing the package in the Python Package Index (PyPI).
# This setup script is essential for packaging the nz_test framework, allowing users to install it
# easily and run tests defined in YAML files with modular executors for different command types.
from setuptools import setup, find_packages

setup(
    name="nz_test",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",  # for reading .yaml test definitions
        "jinja2",  # if you're using templating in HTML reports
    ],
    entry_points={
        "console_scripts": [
            "nztest=nz_test.main:main"
        ],
    },
    author="Your Name",
    description="Netezza test framework with YAML-defined tests and modular executors",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
