""" Helper functions for formatting data """
import sys
from typing import List
import inspect
import re


def get_all_methods(cls: type) -> List[str]:
    """
    Get the names of all methods in a class, excluding
    methods decorated with ``@property``, ``@classmethod``, etc

    :param cls: The class to get the methods for
    :return: A list of the names of the methods
    """
    return [meth[0] for meth in inspect.getmembers(cls, inspect.isfunction)]


def get_public_methods(cls: type) -> List[str]:
    """
    Get the names of all public methods in a class

    :param cls: The class to get all public methods for
    :return: A list of the names of the public methods
    """
    methods = get_all_methods(cls)
    methods = [meth for meth in methods if not meth.startswith("_")]
    return methods


def find_endpoints(line: str) -> List[str]:
    """
    Find the name of a subclass of
    ``~understatapi.endpoints.base.BaseEndpoint`` in a string

    :param line: The string in which to search for the name of a
        ``~understatapi.endpoints.base.BaseEndpoint`` object
    """
    match = re.findall(r"\w+Endpoint", line)
    if match is None:
        return []  # pragma: no cover
    return match


def str_to_class(modulename: str, classname: str) -> type:
    """
    Get a class by using its name
    """
    return getattr(sys.modules[modulename], classname)
