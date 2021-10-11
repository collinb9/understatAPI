""" setup for understatAPI """
import os
import re
from setuptools import setup, find_packages


def read_version():
    """ read the current version from understatapi.__init__.py """
    with open(
        os.path.join(os.path.dirname(__file__), "understatapi", "__init__.py"),
        encoding="utf-8",
    ) as fpath:
        for line in fpath:
            match = re.search(
                r'^\s*__version__\s*=\s*([\'"])([^\'"]+)\1\s*$', line
            )
            if match:
                return match.group(2)
    raise RuntimeError("Unable to find version")


def long_description():
    """ Get description from readme """
    with open("README.md", "r", encoding="utf-8") as fpath:
        long_des = fpath.read()
    return long_des


setup(
    name="understatapi",
    version=read_version(),
    description="An API for scraping data from understat.com",
    packages=find_packages(exclude=("tests",)),
    long_description=long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/collinb9/understatAPI",
    author="collinb9",
    author_email="brendan.m.collins@outlook.com",
    license="MIT",
    install_requires=["requests>=2.0.0", "selenium>=3.141.0"],
    keywords=(
        "statistics xG expected goals fpl fantasy"
        "premier league understat football web scraping"
        "scraper"
    ),
    project_urls={
        "Source": "https://github.com/collinb9/understatAPI/",
    },
)
