""" setup for understatAPI """
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="understatapi",
    version="0.4.0",
    description="An API for scraping data from understat.com",
    packages=find_packages(exclude=("tests",)),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/collinb9/understatAPI",
    author="collinb9",
    author_email="brendan.m.collins@outlook.com",
    license="MIT",
    install_requires=["pandas>=1.1.0", "requests>=2.0.0", "selenium>=3.141.0"],
    keywords=(
        "statistics xG expected goals fpl fantasy"
        "premier league understat football"
    ),
    project_urls={
        "Source": "https://github.com/collinb9/understatAPI/",
    },
)
